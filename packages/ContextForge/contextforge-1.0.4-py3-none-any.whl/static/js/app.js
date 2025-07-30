// ContextForge Web Application JavaScript

class ContextForgeApp {
  constructor() {
    this.selectedFiles = new Set();
    this.fileTree = null;
    this.currentPath = null;
    this.columnsData = [];
    this.selectedColumn = 0;

    this.RECENT_FOLDERS_KEY = "contextforge-recent-folders";
    this.RECENT_FOLDERS_LIMIT = 7;
    this.SETTINGS_KEY = "contextforge-settings";

    this.settings = this.loadSettings();
    this.selectedModel = "gpt-4"; // Fixed model
    this.tokenEstimateCache = new Map();
    this.estimateDebounceTimer = null;
    this.useXmlFormatting = false; // Track XML formatting preference

    // File system monitoring
    this.eventSource = null;
    this.fileEventDebounceTimer = null;
    this.pendingFileEvents = new Set();
    this.treeState = new Map(); // Store expanded state of folders

    this.init();

    // Initialize DiffUI
    this.diffUI = new DiffUI(this);
  }

  init() {
    this.bindEvents();
    this.loadTheme();
    this.setupToasts();
    this.renderRecentFolderPills();
    this.updateCopyButtonsState();
    this.initFileSystemMonitoring();
  }

  // Save the current state of the file tree (expanded folders)
  saveTreeState() {
    this.treeState.clear();

    // Find all expanded folders
    const expandedFolders = document.querySelectorAll(".file-item.folder");
    expandedFolders.forEach((folder) => {
      const expandIcon = folder.querySelector(".expand-icon");
      if (expandIcon && expandIcon.classList.contains("expanded")) {
        const path = folder.dataset.path;
        this.treeState.set(path, true);
      }
    });
  }

  // Restore the tree state after a refresh
  restoreTreeState() {
    const folders = document.querySelectorAll(".file-item.folder");
    folders.forEach((folder) => {
      const path = folder.dataset.path;
      if (this.treeState.has(path) && this.treeState.get(path)) {
        const childrenContainer = folder.nextElementSibling;
        const expandIcon = folder.querySelector(".expand-icon");

        if (
          childrenContainer &&
          childrenContainer.classList.contains("children-container")
        ) {
          childrenContainer.style.display = "block";
          if (expandIcon) {
            expandIcon.classList.add("expanded");
            expandIcon.textContent = "▼";
          }
        }
      }
    });
  }

  // Initialize file system monitoring
  initFileSystemMonitoring() {
    // Don't start monitoring until we have a folder loaded
    if (!this.currentPath) return;

    this.startFileSystemMonitoring();
  }

  // Start monitoring file system changes
  startFileSystemMonitoring() {
    // Close existing connection if any
    this.stopFileSystemMonitoring();

    try {
      this.eventSource = new EventSource("/api/file-events");

      this.eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === "connected") {
          console.log("File system monitoring connected");
        } else if (data.type === "heartbeat") {
          // Ignore heartbeats
        } else {
          // Queue the file change event
          this.handleFileChangeEvent(data);
        }
      };

      this.eventSource.onerror = (error) => {
        console.error("SSE connection error:", error);
        // Reconnect after a delay
        setTimeout(() => {
          if (this.currentPath) {
            this.startFileSystemMonitoring();
          }
        }, 5000);
      };
    } catch (error) {
      console.error("Error starting file system monitoring:", error);
    }
  }

  // Stop monitoring file system changes
  stopFileSystemMonitoring() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }

  // Handle file change events
  handleFileChangeEvent(event) {
    // Add to pending events
    this.pendingFileEvents.add(event.relative_path);

    // Clear existing debounce timer
    if (this.fileEventDebounceTimer) {
      clearTimeout(this.fileEventDebounceTimer);
    }

    // Debounce the refresh (wait 300ms after last event)
    this.fileEventDebounceTimer = setTimeout(() => {
      this.processPendingFileEvents();
    }, 300);
  }

  // Process all pending file events
  processPendingFileEvents() {
    if (this.pendingFileEvents.size === 0) return;

    console.log(`Processing ${this.pendingFileEvents.size} file change events`);

    // Save current tree state
    this.saveTreeState();

    // Save current selections
    const currentSelections = new Set(this.selectedFiles);

    // Reload the folder
    this.refreshFileTree().then(() => {
      // Restore selections
      this.selectedFiles = currentSelections;
      this.updateFileTreeCheckboxes();
      this.updateSelectionSummary();

      // Restore tree state
      this.restoreTreeState();

      // Clear pending events
      this.pendingFileEvents.clear();
    });
  }

  // Refresh just the file tree without showing toasts
  async refreshFileTree() {
    if (!this.currentPath) return;

    try {
      const response = await fetch("/api/browse", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          path: this.currentPath,
          settings: this.settings,
          show_ignored: this.settings.show_ignored || false,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to refresh folder");
      }

      this.fileTree = data.tree;
      this.fileStats = data.stats;

      this.renderFileTree();
      this.updateSelectionSummary();
    } catch (error) {
      console.error("Error refreshing file tree:", error);
    }
  }

  // Debounce utility function
  debounce(func, wait) {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }

  setupPathInputHandlers() {
    const pathInput = document.getElementById("browser-path-input");
    let previousPath = "";
    let lastBrowsedPath = "";

    // Store the initial path when the input gets focus
    pathInput.addEventListener("focus", (e) => {
      previousPath = e.target.value;
    });

    // Helper to normalize paths for comparison (remove trailing slashes)
    const normalizePath = (path) => {
      return path.replace(/\/+$/, "");
    };

    // Debounced browse function
    const debouncedBrowse = this.debounce(() => {
      const currentValue = pathInput.value;
      const path = currentValue.trim();

      // Only browse if the normalized path is different from last browsed path
      if (path && normalizePath(path) !== normalizePath(lastBrowsedPath)) {
        // Store the current cursor position and value
        const cursorPosition = pathInput.selectionStart;
        const originalValue = currentValue;

        this.browseFolderPath(path, true)
          .then(() => {
            // Successfully browsed
            lastBrowsedPath = path;
            previousPath = originalValue; // Store the exact value for ESC

            // Restore the original value with trailing slash if it had one
            if (originalValue.endsWith("/") && !pathInput.value.endsWith("/")) {
              pathInput.value = originalValue;
              // Restore cursor position
              pathInput.setSelectionRange(cursorPosition, cursorPosition);
            }
          })
          .catch(() => {
            // Browse failed, restore the original value
            pathInput.value = originalValue;
            pathInput.setSelectionRange(cursorPosition, cursorPosition);
          });
      }
    }, 500);

    // Input event to trigger debounced browse
    pathInput.addEventListener("input", (e) => {
      debouncedBrowse();
    });

    // Keydown event to handle ESC and Enter
    pathInput.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        e.preventDefault();
        e.stopPropagation(); // Prevent modal from closing
        pathInput.value = previousPath;
        pathInput.blur(); // Remove focus from input
      } else if (e.key === "Enter") {
        e.preventDefault();
        const currentValue = pathInput.value;
        const path = currentValue.trim();
        if (path) {
          // Instead of browsing, select the folder as workspace
          this.selectFolderFromColumn(path);
        }
      }
    });
  }

  bindEvents() {
    // Theme toggle
    document
      .getElementById("theme-toggle-btn")
      .addEventListener("click", () => {
        this.toggleTheme();
      });

    // File tree controls
    document.getElementById("select-all-btn").addEventListener("click", () => {
      this.selectAllFiles();
    });

    document.getElementById("select-none-btn").addEventListener("click", () => {
      this.selectNoFiles();
    });

    // Copy button - generate and copy prompt
    document.getElementById("copy-btn").addEventListener("click", () => {
      this.generateAndCopyPrompt(false);
    });

    // XML Copy button - generate and copy XML formatted prompt
    document.getElementById("xml-copy-btn").addEventListener("click", () => {
      this.generateAndCopyPrompt(true);
    });

    // Instructions change
    document.getElementById("instructions").addEventListener("input", () => {
      this.estimateTokens();
      this.updateCopyButtonsState();
    });

    // Model selector
    const modelSelector = document.getElementById("model-selector");
    if (modelSelector) {
      modelSelector.addEventListener("change", (e) => {
        this.selectedModel = e.target.value;
        localStorage.setItem(this.SELECTED_MODEL_KEY, this.selectedModel);
        this.tokenEstimateCache.clear(); // Clear cache when model changes
        this.estimateTokens();
      });
    }

    // Folder browser
    document
      .getElementById("browse-dialog-btn")
      .addEventListener("click", () => {
        this.openFolderBrowser();
      });

    // Settings button
    const settingsBtn = document.getElementById("settings-btn");
    if (settingsBtn) {
      settingsBtn.addEventListener("click", () => {
        console.log("Settings button clicked"); // Debug log
        this.openSettingsModal();
      });
    }

    // Modal controls
    document.getElementById("modal-close").addEventListener("click", () => {
      this.closeFolderBrowser();
    });

    // Quick access links
    document.querySelectorAll(".quick-link").forEach((link) => {
      link.addEventListener("click", (e) => {
        const path = e.currentTarget.dataset.path;
        document.getElementById("browser-path-input").value = path;
        this.browseFolderPath(path, true);

        // Update active state
        document.querySelectorAll(".sidebar-item").forEach((item) => {
          item.classList.remove("active");
        });
        e.currentTarget.classList.add("active");
      });
    });

    // Close modal on background click
    document
      .getElementById("folder-browser-modal")
      .addEventListener("click", (e) => {
        if (e.target.id === "folder-browser-modal") {
          this.closeFolderBrowser();
        }
      });

    // Keyboard navigation for modal
    document.addEventListener("keydown", (e) => {
      if (
        !document
          .getElementById("folder-browser-modal")
          .classList.contains("hidden")
      ) {
        this.handleKeyboardNavigation(e);
      }
    });

    // Path input handler with debounce and ESC support
    this.setupPathInputHandlers();
  }

  loadTheme() {
    const savedTheme = localStorage.getItem("contextforge-theme") || "dark";
    this.setTheme(savedTheme);
  }

  loadSettings() {
    const saved = localStorage.getItem(this.SETTINGS_KEY);
    if (saved) {
      return JSON.parse(saved);
    }
    return {
      use_gitignore: true,
      custom_ignore_patterns: [],
      whitelist_patterns: [],
      show_ignored: false,
    };
  }

  saveSettings() {
    localStorage.setItem(this.SETTINGS_KEY, JSON.stringify(this.settings));
  }

  setTheme(theme) {
    document.body.className = theme === "light" ? "light-theme" : "";
    localStorage.setItem("contextforge-theme", theme);
  }

  toggleTheme() {
    const currentTheme = document.body.classList.contains("light-theme")
      ? "light"
      : "dark";
    const newTheme = currentTheme === "light" ? "dark" : "light";
    this.setTheme(newTheme);
  }

  setupToasts() {
    // Error toast close
    document.getElementById("error-close").addEventListener("click", () => {
      this.hideToast("error");
    });

    // Success toast close
    document.getElementById("success-close").addEventListener("click", () => {
      this.hideToast("success");
    });

    // Auto-hide toasts
    setTimeout(() => {
      this.hideToast("error");
      this.hideToast("success");
    }, 5000);
  }

  async loadSupportedModels() {
    try {
      const response = await fetch("/api/models");
      const data = await response.json();

      const modelSelector = document.getElementById("model-selector");
      if (modelSelector && data.models) {
        modelSelector.innerHTML = data.models
          .map(
            (model) =>
              `<option value="${model}" ${
                model === this.selectedModel ? "selected" : ""
              }>${model}</option>`
          )
          .join("");
      }
    } catch (error) {
      console.error("Error loading models:", error);
    }
  }

  async estimateTokens(useDebounce = true) {
    if (this.selectedFiles.size === 0) {
      this.updateTokenDisplay(0, {});
      return;
    }

    // If debouncing is disabled, execute immediately
    if (!useDebounce) {
      await this.performTokenEstimation();
      return;
    }

    // Clear existing timer
    if (this.estimateDebounceTimer) {
      clearTimeout(this.estimateDebounceTimer);
    }

    // Debounce the estimation (1s for instruction typing)
    this.estimateDebounceTimer = setTimeout(() => {
      this.performTokenEstimation();
    }, 1000); // 1s debounce as requested
  }

  async performTokenEstimation() {
    const instructions = document.getElementById("instructions").value.trim();
    const format = "xml"; // Hardcoded to XML

    // Create cache key
    const cacheKey = `${Array.from(this.selectedFiles)
      .sort()
      .join("|")}|${instructions}|${format}|${this.selectedModel}|${
      this.useXmlFormatting
    }`;

    // Check cache
    if (this.tokenEstimateCache.has(cacheKey)) {
      const cached = this.tokenEstimateCache.get(cacheKey);
      this.updateTokenDisplay(cached.total_tokens, cached.file_estimates);
      return;
    }

    try {
      const response = await fetch("/api/estimate-tokens", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          files: Array.from(this.selectedFiles),
          instructions: instructions,
          format: format,
          model: this.selectedModel,
          use_xml_formatting: this.useXmlFormatting,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Cache the result
        this.tokenEstimateCache.set(cacheKey, data);

        // Update display
        this.updateTokenDisplay(data.total_tokens, data.file_estimates);
      }
    } catch (error) {
      console.error("Error estimating tokens:", error);
      // Fall back to rough estimate
      const roughEstimate = this.selectedFiles.size * 500;
      this.updateTokenDisplay(roughEstimate, {});
    }
  }

  updateTokenDisplay(totalTokens, fileEstimates = {}) {
    const tokenElement = document.getElementById("token-estimate");
    if (tokenElement) {
      tokenElement.textContent = totalTokens.toLocaleString();

      // Add color coding based on token count
      tokenElement.classList.remove("token-warning", "token-danger");
      if (totalTokens > 100000) {
        tokenElement.classList.add("token-danger");
        tokenElement.title = "Very high token count - may exceed model limits";
      } else if (totalTokens > 50000) {
        tokenElement.classList.add("token-warning");
        tokenElement.title =
          "High token count - consider reducing file selection";
      } else {
        tokenElement.title = `Estimated ${totalTokens.toLocaleString()} tokens for ${
          this.selectedModel
        }`;
      }
    }

    // Store file estimates for potential use in UI
    this.fileTokenEstimates = fileEstimates;
  }

  showToast(type, message) {
    const toast = document.getElementById(`${type}-toast`);
    const messageEl = document.getElementById(`${type}-message`);

    messageEl.textContent = message;
    toast.classList.remove("hidden");

    // Auto-hide after 5 seconds
    setTimeout(() => {
      this.hideToast(type);
    }, 5000);
  }

  hideToast(type) {
    const toast = document.getElementById(`${type}-toast`);
    toast.classList.add("hidden");
  }

  showLoading() {
    // Always create a new column for the loading state
    const container = document.getElementById("columns-browser");

    // Create a new column with loading state
    const loadingColumn = document.createElement("div");
    loadingColumn.className = "column-view loading";
    container.appendChild(loadingColumn);

    // Ensure the new column is visible by scrolling
    setTimeout(() => {
      container.scrollLeft = container.scrollWidth;
    }, 10);
  }

  hideLoading() {
    // Remove all columns that only have the loading state (empty loading columns)
    const loadingColumns = document.querySelectorAll(".column-view.loading");
    loadingColumns.forEach((col) => {
      // Only remove if it's an empty loading column (no content)
      if (col.children.length === 0) {
        col.remove();
      } else {
        // Otherwise just remove the loading class
        col.classList.remove("loading");
      }
    });
  }

  // --- Recent Folders Methods ---
  getRecentFolders() {
    const folders = localStorage.getItem(this.RECENT_FOLDERS_KEY);
    if (!folders) return [];

    const parsed = JSON.parse(folders);
    // Handle legacy format (array of strings) and new format (array of objects)
    if (parsed.length > 0 && typeof parsed[0] === "string") {
      // Convert legacy format to new format
      return parsed.map((path) => ({ path, instructions: "" }));
    }
    return parsed;
  }
  setRecentFolders(folders) {
    localStorage.setItem(this.RECENT_FOLDERS_KEY, JSON.stringify(folders));
  }
  addRecentFolder(path) {
    if (!path) return;
    let folders = this.getRecentFolders();

    // Get current instructions
    const instructions = document.getElementById("instructions").value || "";

    // Remove if already exists
    folders = folders.filter((f) => f.path !== path);

    // Add new entry with path and instructions
    folders.unshift({ path, instructions });

    if (folders.length > this.RECENT_FOLDERS_LIMIT) {
      folders = folders.slice(0, this.RECENT_FOLDERS_LIMIT);
    }

    this.setRecentFolders(folders);
    this.renderRecentFolders();
    this.renderRecentFolderPills(); // Also update pills in main view
  }
  renderRecentFolders() {
    const recentContainer = document.getElementById("recent-folders");
    const recentSection = document.getElementById("recent-section");
    if (!recentContainer) return;

    const folders = this.getRecentFolders();
    if (folders.length === 0) {
      recentSection.style.display = "none";
      return;
    }

    recentSection.style.display = "block";

    // Extract just the folder name from the path for display
    const getFolderName = (path) => {
      const parts = path.split("/");
      return parts[parts.length - 1] || parts[parts.length - 2] || path;
    };

    recentContainer.innerHTML = folders
      .map((folder) => {
        const path = folder.path || folder; // Handle both old and new format
        const instructions = folder.instructions || "";
        return `
            <button class="sidebar-item recent-folder-btn" data-path="${path}" data-instructions="${encodeURIComponent(
          instructions
        )}" title="${path}">
                <span class="sidebar-item-icon">📁</span>
                <span>${getFolderName(path)}</span>
            </button>
        `;
      })
      .join("");

    recentContainer.querySelectorAll(".recent-folder-btn").forEach((btn) => {
      btn.addEventListener("click", async (e) => {
        e.preventDefault();
        const path = e.currentTarget.dataset.path;
        const encodedInstructions = e.currentTarget.dataset.instructions;
        const instructions = encodedInstructions
          ? decodeURIComponent(encodedInstructions)
          : "";

        // Update active state
        document.querySelectorAll(".sidebar-item").forEach((item) => {
          item.classList.remove("active");
        });
        e.currentTarget.classList.add("active");

        // Try to load the folder directly
        try {
          const response = await fetch("/api/browse", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ path: path }),
          });

          const data = await response.json();

          if (response.ok) {
            // Folder exists, select it directly
            this.closeFolderBrowser();
            this.loadFolder(path, instructions);
          } else {
            // Folder doesn't exist, show error
            this.showToast("error", `Folder not found: ${path}`);
            // Remove from recent folders
            let folders = this.getRecentFolders();
            folders = folders.filter((f) => f.path !== path);
            this.setRecentFolders(folders);
            this.renderRecentFolders();
            this.renderRecentFolderPills();
          }
        } catch (error) {
          this.showToast("error", `Error accessing folder: ${error.message}`);
        }
      });
    });
  }

  async loadFolder(folderPath, restoreInstructions = null) {
    if (!folderPath) {
      this.showToast("error", "Please select a folder");
      return;
    }

    try {
      const response = await fetch("/api/browse", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          path: folderPath,
          settings: this.settings,
          show_ignored: this.settings.show_ignored || false,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to browse folder");
      }

      this.fileTree = data.tree;
      this.currentPath = data.path;
      this.fileStats = data.stats;
      this.selectedFiles.clear();

      this.renderFileTree();
      this.updateFolderDisplay();
      this.updateSelectionSummary();

      // Restore instructions if provided
      if (restoreInstructions !== null) {
        document.getElementById("instructions").value = restoreInstructions;
      }

      const statsMessage = data.stats
        ? `Folder loaded (${data.stats.total_files} files, ${data.stats.ignored_files} ignored)`
        : "Folder loaded successfully";
      this.showToast("success", statsMessage);

      // Add to recent folders
      this.addRecentFolder(data.path);

      // Start file system monitoring
      this.startFileSystemMonitoring();
    } catch (error) {
      console.error("Error loading folder:", error);
      this.showToast("error", error.message);
    }
  }

  renderRecentFolderPills() {
    const container = document.getElementById("file-tree");
    const folders = this.getRecentFolders();

    if (!this.fileTree && folders.length > 0) {
      // Extract just the folder name from the path for display
      const getFolderName = (path) => {
        const parts = path.split("/");
        return parts[parts.length - 1] || parts[parts.length - 2] || path;
      };

      const pillsHtml = folders
        .map((folder, index) => {
          const path = folder.path || folder;
          const instructions = folder.instructions || "";
          return `
                    <button class="recent-pill" data-path="${path}" data-instructions="${encodeURIComponent(
            instructions
          )}" title="${path}">
                        📁 ${getFolderName(path)}
                    </button>
                `;
        })
        .join("");

      container.innerHTML = `
                <div class="empty-state">
                    <p>👆 Click "Browse" to select a folder</p>
                    <div class="recent-pills-container">
                        <p class="recent-pills-label">Recent workspaces:</p>
                        <div class="recent-pills">
                            ${pillsHtml}
                        </div>
                    </div>
                </div>
            `;

      // Add click handlers to pills
      container.querySelectorAll(".recent-pill").forEach((pill) => {
        pill.addEventListener("click", async (e) => {
          e.preventDefault();
          const path = e.currentTarget.dataset.path;
          const encodedInstructions = e.currentTarget.dataset.instructions;
          const instructions = encodedInstructions
            ? decodeURIComponent(encodedInstructions)
            : "";

          try {
            const response = await fetch("/api/browse", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ path: path }),
            });

            const data = await response.json();

            if (response.ok) {
              this.loadFolder(path, instructions);
            } else {
              this.showToast("error", `Folder not found: ${path}`);
              // Remove from recent folders
              let folders = this.getRecentFolders();
              folders = folders.filter((f) => f.path !== path);
              this.setRecentFolders(folders);
              this.renderRecentFolderPills();
            }
          } catch (error) {
            this.showToast("error", `Error accessing folder: ${error.message}`);
          }
        });
      });
    }
  }

  renderFileTree() {
    const container = document.getElementById("file-tree");

    if (!this.fileTree || !this.fileTree.name) {
      this.renderRecentFolderPills();
      return;
    }

    container.innerHTML = "";
    this.renderTreeNode(container, this.fileTree, 0);

    // Auto-expand the top-level folder's children
    // Find the first .children-container after the root .file-item
    const rootItem = container.querySelector(".file-item.folder");
    if (rootItem) {
      const childrenContainer = rootItem.nextElementSibling;
      if (
        childrenContainer &&
        childrenContainer.classList.contains("children-container")
      ) {
        childrenContainer.style.display = "block";
        // Also update the expand icon if present
        const expandIcon = rootItem.querySelector(".expand-icon");
        if (expandIcon) {
          expandIcon.classList.add("expanded");
          expandIcon.textContent = "▼";
        }
      }
    }
  }

  renderTreeNode(container, node, depth) {
    const item = document.createElement("div");
    item.className = `file-item ${
      node.is_dir ? "folder" : "file"
    } indent-${Math.min(depth, 4)}`;
    if (node.ignored) {
      item.classList.add("ignored");
    }
    item.dataset.path = node.path;
    item.dataset.isDir = node.is_dir;

    let expandIcon = "";
    if (node.is_dir && node.children.length > 0) {
      expandIcon = '<span class="expand-icon">▶</span>';
    }

    // Calculate checkbox state for folders
    let checkboxState = "unchecked";
    if (node.is_dir) {
      const childStates = this.getFolderSelectionState(node);
      if (childStates.all) {
        checkboxState = "checked";
      } else if (childStates.some) {
        checkboxState = "indeterminate";
      }
    } else {
      checkboxState = this.selectedFiles.has(node.path)
        ? "checked"
        : "unchecked";
    }

    const checkboxHtml = `
            <div class="checkbox-wrapper">
                <input type="checkbox" class="checkbox"
                    ${checkboxState === "checked" ? "checked" : ""}
                    ${checkboxState === "indeterminate" ? "indeterminate" : ""}>
                <div class="checkbox-visual">
                    <span class="checkbox-icon check">✓</span>
                    <span class="checkbox-icon minus">−</span>
                </div>
            </div>
        `;

    item.innerHTML = `
            ${expandIcon}
            <div class="item-content">
                <span class="icon">${node.icon}</span>
                <span class="name">${node.name}</span>
            </div>
            ${checkboxHtml}
        `;

    // Add click handlers
    const expandIconEl = item.querySelector(".expand-icon");
    if (expandIconEl) {
      expandIconEl.addEventListener("click", (e) => {
        e.stopPropagation();
        this.toggleFolder(item, node);
      });
    }

    const checkbox_el = item.querySelector(".checkbox");
    const checkboxWrapper = item.querySelector(".checkbox-wrapper");

    // Handle checkbox clicks
    checkboxWrapper.addEventListener("click", (e) => {
      e.stopPropagation();
      if (node.is_dir) {
        this.toggleFolderSelection(node, checkbox_el);
      } else {
        const newState = !checkbox_el.checked;
        checkbox_el.checked = newState;
        this.toggleFileSelection(node.path, newState);
      }
    });

    // Fix: Also handle direct clicks on the checkbox for files
    if (!node.is_dir) {
      checkbox_el.addEventListener("click", (e) => {
        e.stopPropagation();
        const newState = !this.selectedFiles.has(node.path);
        checkbox_el.checked = newState;
        this.toggleFileSelection(node.path, newState);
      });
    }

    // Handle folder row clicks
    if (node.is_dir) {
      item.addEventListener("click", (e) => {
        if (
          e.target.closest(".checkbox-wrapper") ||
          e.target.closest(".expand-icon")
        )
          return;

        if (node.children.length > 0) {
          this.toggleFolder(item, node);
        }
      });
    } else {
      // Handle file row clicks
      item.addEventListener("click", (e) => {
        if (e.target.closest(".checkbox-wrapper")) return;

        const isCurrentlySelected = this.selectedFiles.has(node.path);
        checkbox_el.checked = !isCurrentlySelected;
        this.toggleFileSelection(node.path, !isCurrentlySelected);
      });
    }

    container.appendChild(item);

    // Add children container
    if (node.is_dir && node.children.length > 0) {
      const childrenContainer = document.createElement("div");
      childrenContainer.className = "children-container";
      childrenContainer.style.display = "none";

      node.children.forEach((child) => {
        this.renderTreeNode(childrenContainer, child, depth + 1);
      });

      container.appendChild(childrenContainer);
    }
  }

  toggleFolder(item, node) {
    const expandIcon = item.querySelector(".expand-icon");
    const childrenContainer = item.nextElementSibling;

    if (
      childrenContainer &&
      childrenContainer.classList.contains("children-container")
    ) {
      const isExpanded = childrenContainer.style.display !== "none";

      if (isExpanded) {
        childrenContainer.style.display = "none";
        expandIcon.classList.remove("expanded");
        expandIcon.textContent = "▶";
      } else {
        childrenContainer.style.display = "block";
        expandIcon.classList.add("expanded");
        expandIcon.textContent = "▼";
      }
    }
  }

  toggleFileSelection(path, selected) {
    if (selected) {
      this.selectedFiles.add(path);
    } else {
      this.selectedFiles.delete(path);
    }

    this.updateSelectionSummary();
    this.updateParentCheckboxes();
    this.updateCopyButtonsState();
  }

  getFolderSelectionState(folder) {
    let selectedCount = 0;
    let totalCount = 0;

    const countFiles = (node) => {
      if (!node.is_dir) {
        totalCount++;
        if (this.selectedFiles.has(node.path)) {
          selectedCount++;
        }
      }

      if (node.children) {
        node.children.forEach((child) => countFiles(child));
      }
    };

    countFiles(folder);

    return {
      all: totalCount > 0 && selectedCount === totalCount,
      some: selectedCount > 0,
      none: selectedCount === 0,
    };
  }

  toggleFolderSelection(folder, checkbox) {
    const state = this.getFolderSelectionState(folder);

    // If indeterminate or some selected, unselect all
    // Otherwise, select all
    const shouldSelect = state.none;

    const toggleAllFiles = (node) => {
      if (!node.is_dir) {
        if (shouldSelect) {
          this.selectedFiles.add(node.path);
        } else {
          this.selectedFiles.delete(node.path);
        }
      }

      if (node.children) {
        node.children.forEach((child) => toggleAllFiles(child));
      }
    };

    toggleAllFiles(folder);

    // Update UI
    this.updateFileTreeCheckboxes();
    this.updateSelectionSummary();
    this.updateCopyButtonsState();
  }

  updateParentCheckboxes() {
    // This will be called when individual files are toggled
    // It will trigger a re-render of checkboxes to update parent states
    setTimeout(() => {
      this.updateFileTreeCheckboxes();
    }, 10);
  }

  selectAllFiles() {
    if (!this.fileTree) return;

    this.selectedFiles.clear();
    this.collectAllFiles(this.fileTree);
    this.updateFileTreeCheckboxes();
    this.updateSelectionSummary();
    this.updateCopyButtonsState();
  }

  selectNoFiles() {
    this.selectedFiles.clear();
    this.updateFileTreeCheckboxes();
    this.updateSelectionSummary();
    this.updateCopyButtonsState();
  }

  collectAllFiles(node) {
    if (!node.is_dir) {
      this.selectedFiles.add(node.path);
    }

    if (node.children) {
      node.children.forEach((child) => {
        this.collectAllFiles(child);
      });
    }
  }

  updateFileTreeCheckboxes() {
    const fileItems = document.querySelectorAll(".file-item");
    fileItems.forEach((item) => {
      const checkbox = item.querySelector(".checkbox");
      if (!checkbox) return;

      const path = item.dataset.path;
      const isDir = item.dataset.isDir === "true";

      if (isDir) {
        // Find the node in the tree
        const node = this.findNodeByPath(this.fileTree, path);
        if (node) {
          const state = this.getFolderSelectionState(node);
          checkbox.indeterminate = false;

          if (state.all) {
            checkbox.checked = true;
          } else if (state.some) {
            checkbox.checked = false;
            checkbox.indeterminate = true;
          } else {
            checkbox.checked = false;
          }
        }
      } else {
        checkbox.checked = this.selectedFiles.has(path);
      }
    });
  }

  findNodeByPath(node, targetPath) {
    if (node.path === targetPath) {
      return node;
    }

    if (node.children) {
      for (const child of node.children) {
        const found = this.findNodeByPath(child, targetPath);
        if (found) return found;
      }
    }

    return null;
  }

  updateSelectionSummary() {
    const fileCount = this.selectedFiles.size;
    document.getElementById("selected-count").textContent = fileCount;
    this.updateCopyButtonsState();
  }

  updateFolderDisplay() {
    const folderDisplay = document.getElementById("current-folder-display");
    if (this.currentPath) {
      const pathParts = this.currentPath.split("/");
      const folderName = pathParts[pathParts.length - 1] || this.currentPath;
      folderDisplay.textContent = `📁 ${folderName}`;
      folderDisplay.title = this.currentPath;
    } else {
      folderDisplay.textContent = "No folder selected";
      folderDisplay.title = "";
    }
  }

  async generateAndCopyPrompt(useXml = false) {
    if (this.selectedFiles.size === 0) {
      this.showToast("error", "No files selected");
      return;
    }

    const instructions = document.getElementById("instructions").value.trim();

    // Show loading state on buttons
    const copyBtn = document.getElementById(
      useXml ? "xml-copy-btn" : "copy-btn"
    );
    const originalText = copyBtn.textContent;
    copyBtn.textContent = "Generating...";
    copyBtn.disabled = true;

    try {
      const response = await fetch("/api/generate-prompt", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          files: Array.from(this.selectedFiles),
          instructions: instructions,
          use_xml_formatting: useXml,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to generate prompt");
      }

      // Update the token display with the accurate count from the actual prompt
      this.updateTokenDisplay(data.token_count, data.file_token_counts || {});

      // Copy to clipboard
      try {
        await navigator.clipboard.writeText(data.prompt);
        this.showToast("success", "Copied to clipboard!");
      } catch (clipboardError) {
        console.error("Error copying to clipboard:", clipboardError);
        // Fallback for older browsers
        this.fallbackCopyToClipboard(data.prompt);
      }
    } catch (error) {
      console.error("Error generating prompt:", error);
      this.showToast("error", error.message);
    } finally {
      // Restore button state
      copyBtn.textContent = originalText;
      copyBtn.disabled = this.selectedFiles.size === 0;
    }
  }

  updateCopyButtonsState() {
    const hasFiles = this.selectedFiles.size > 0;
    document.getElementById("copy-btn").disabled = !hasFiles;
    document.getElementById("xml-copy-btn").disabled = !hasFiles;
  }

  fallbackCopyToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      document.execCommand("copy");
      this.showToast("success", "Copied to clipboard!");
    } catch (error) {
      console.error("Fallback copy failed:", error);
      this.showToast("error", "Failed to copy to clipboard");
    }

    document.body.removeChild(textArea);
  }

  // Folder Browser Methods
  openFolderBrowser() {
    const modal = document.getElementById("folder-browser-modal");
    modal.classList.remove("hidden");

    // Reset columns data
    this.columnsData = [];
    this.selectedColumn = 0;

    // Render recent folders
    this.renderRecentFolders();

    // Start with current path or home
    const startPath = this.currentPath || "~";
    this.browseFolderPath(startPath, true);
  }

  closeFolderBrowser() {
    const modal = document.getElementById("folder-browser-modal");
    modal.classList.add("hidden");

    // Remove keyboard event listeners
    this.columnsData = [];
    this.selectedColumn = 0;
  }

  // Settings Modal Methods
  openSettingsModal() {
    const modal = document.getElementById("settings-modal");
    modal.classList.remove("hidden");

    // Populate current settings
    this.populateSettingsModal();

    // Bind settings modal events
    this.bindSettingsEvents();

    // Update stats if we have a current folder
    if (this.currentPath && this.fileStats) {
      this.updateIgnoreStats();
    }
  }

  closeSettingsModal() {
    const modal = document.getElementById("settings-modal");
    modal.classList.add("hidden");

    // Unbind temporary event listeners
    this.unbindSettingsEvents();
  }

  populateSettingsModal() {
    // Populate gitignore checkbox
    document.getElementById("use-gitignore").checked =
      this.settings.use_gitignore;

    // Populate show ignored files checkbox
    document.getElementById("show-ignored-files").checked =
      this.settings.show_ignored || false;

    // Populate custom ignore patterns
    this.renderPatternList(
      "ignore-patterns-list",
      this.settings.custom_ignore_patterns || []
    );

    // Populate whitelist patterns
    this.renderPatternList(
      "whitelist-patterns-list",
      this.settings.whitelist_patterns || []
    );

    // Show default patterns
    this.renderDefaultPatterns();
  }

  renderPatternList(containerId, patterns) {
    const container = document.getElementById(containerId);

    if (patterns.length === 0) {
      container.innerHTML =
        '<div class="pattern-item empty-state">No patterns added</div>';
      return;
    }

    container.innerHTML = patterns
      .map(
        (pattern, index) => `
            <div class="pattern-item">
                <code>${this.escapeHtml(pattern)}</code>
                <button class="pattern-remove" data-pattern="${this.escapeHtml(
                  pattern
                )}" data-type="${containerId}">
                    ×
                </button>
            </div>
        `
      )
      .join("");
  }

  renderDefaultPatterns() {
    const container = document.getElementById("default-patterns-list");
    const defaultPatterns = [
      ".git",
      "__pycache__",
      "node_modules",
      ".idea",
      ".vscode",
      "venv",
      ".env",
      ".DS_Store",
      "dist",
      "build",
      "*.egg-info",
      ".pytest_cache",
      ".coverage",
      "coverage",
      ".nyc_output",
    ];

    container.innerHTML = defaultPatterns
      .map((pattern) => `<span class="default-pattern-chip">${pattern}</span>`)
      .join("");
  }

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  bindSettingsEvents() {
    // Close button
    this.settingsCloseHandler = () => this.closeSettingsModal();
    document
      .getElementById("settings-modal-close")
      .addEventListener("click", this.settingsCloseHandler);

    // Cancel button
    this.settingsCancelHandler = () => this.closeSettingsModal();
    document
      .getElementById("settings-cancel")
      .addEventListener("click", this.settingsCancelHandler);

    // Save button
    this.settingsSaveHandler = () => this.saveSettingsModal();
    document
      .getElementById("settings-save")
      .addEventListener("click", this.settingsSaveHandler);

    // Add ignore pattern
    this.addIgnoreHandler = () => this.addPattern("ignore");
    document
      .getElementById("add-ignore-pattern")
      .addEventListener("click", this.addIgnoreHandler);

    // Add whitelist pattern
    this.addWhitelistHandler = () => this.addPattern("whitelist");
    document
      .getElementById("add-whitelist-pattern")
      .addEventListener("click", this.addWhitelistHandler);

    // Enter key handlers for pattern inputs
    this.ignoreEnterHandler = (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        this.addPattern("ignore");
      }
    };
    document
      .getElementById("new-ignore-pattern")
      .addEventListener("keydown", this.ignoreEnterHandler);

    this.whitelistEnterHandler = (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        this.addPattern("whitelist");
      }
    };
    document
      .getElementById("new-whitelist-pattern")
      .addEventListener("keydown", this.whitelistEnterHandler);

    // Pattern remove buttons (delegated)
    this.patternRemoveHandler = (e) => {
      if (e.target.classList.contains("pattern-remove")) {
        const pattern = e.target.dataset.pattern;
        const type = e.target.dataset.type;
        this.removePattern(pattern, type);
      }
    };
    document
      .getElementById("settings-modal")
      .addEventListener("click", this.patternRemoveHandler);

    // Background click to close
    this.modalBackgroundHandler = (e) => {
      if (e.target.id === "settings-modal") {
        this.closeSettingsModal();
      }
    };
    document
      .getElementById("settings-modal")
      .addEventListener("click", this.modalBackgroundHandler);
  }

  unbindSettingsEvents() {
    // Remove all event listeners
    document
      .getElementById("settings-modal-close")
      .removeEventListener("click", this.settingsCloseHandler);
    document
      .getElementById("settings-cancel")
      .removeEventListener("click", this.settingsCancelHandler);
    document
      .getElementById("settings-save")
      .removeEventListener("click", this.settingsSaveHandler);
    document
      .getElementById("add-ignore-pattern")
      .removeEventListener("click", this.addIgnoreHandler);
    document
      .getElementById("add-whitelist-pattern")
      .removeEventListener("click", this.addWhitelistHandler);
    document
      .getElementById("new-ignore-pattern")
      .removeEventListener("keydown", this.ignoreEnterHandler);
    document
      .getElementById("new-whitelist-pattern")
      .removeEventListener("keydown", this.whitelistEnterHandler);
    document
      .getElementById("settings-modal")
      .removeEventListener("click", this.patternRemoveHandler);
    document
      .getElementById("settings-modal")
      .removeEventListener("click", this.modalBackgroundHandler);
  }

  addPattern(type) {
    const inputId =
      type === "ignore" ? "new-ignore-pattern" : "new-whitelist-pattern";
    const input = document.getElementById(inputId);
    const pattern = input.value.trim();

    if (!pattern) {
      this.showToast("error", "Please enter a pattern");
      return;
    }

    const arrayName =
      type === "ignore" ? "custom_ignore_patterns" : "whitelist_patterns";

    // Check if pattern already exists
    if (
      this.settings[arrayName] &&
      this.settings[arrayName].includes(pattern)
    ) {
      this.showToast("error", "Pattern already exists");
      return;
    }

    // Add pattern
    if (!this.settings[arrayName]) {
      this.settings[arrayName] = [];
    }
    this.settings[arrayName].push(pattern);

    // Clear input
    input.value = "";

    // Re-render list
    const listId =
      type === "ignore" ? "ignore-patterns-list" : "whitelist-patterns-list";
    this.renderPatternList(listId, this.settings[arrayName]);

    // Update stats
    this.updateIgnoreStats();
  }

  removePattern(pattern, listId) {
    const arrayName = listId.includes("ignore")
      ? "custom_ignore_patterns"
      : "whitelist_patterns";

    if (this.settings[arrayName]) {
      this.settings[arrayName] = this.settings[arrayName].filter(
        (p) => p !== pattern
      );
      this.renderPatternList(listId, this.settings[arrayName]);
      this.updateIgnoreStats();
    }
  }

  async saveSettingsModal() {
    // Update settings from UI
    this.settings.use_gitignore =
      document.getElementById("use-gitignore").checked;
    this.settings.show_ignored =
      document.getElementById("show-ignored-files").checked;

    // Save to localStorage
    this.saveSettings();

    // Send to backend
    try {
      const response = await fetch("/api/settings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ settings: this.settings }),
      });

      if (!response.ok) {
        throw new Error("Failed to save settings");
      }

      this.showToast("success", "Settings saved successfully");
      this.closeSettingsModal();

      // Reload current folder with new settings if one is loaded
      if (this.currentPath) {
        this.loadFolder(this.currentPath);
      }
    } catch (error) {
      this.showToast("error", "Error saving settings: " + error.message);
    }
  }

  updateIgnoreStats() {
    const statsEl = document.getElementById("ignore-stats");
    if (this.fileStats) {
      statsEl.textContent = `Files: ${this.fileStats.total_files} total, ${this.fileStats.ignored_files} ignored`;
    } else {
      statsEl.textContent = "No folder loaded";
    }
  }

  async browseFolderPath(path, clearColumns = false) {
    this.showLoading();

    try {
      const response = await fetch("/api/browse", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          path: path,
          settings: this.settings,
          show_ignored: false,
          max_depth: 1,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to browse folder");
      }

      if (clearColumns) {
        this.columnsData = [
          {
            path: data.path,
            tree: data.tree,
            selectedIndex: 0,
          },
        ];
        this.selectedColumn = 0;
      } else {
        // Add new column
        const currentColumnIndex = this.columnsData.findIndex(
          (col) => col.path === path
        );
        if (currentColumnIndex !== -1) {
          // Truncate columns after the current one
          this.columnsData = this.columnsData.slice(0, currentColumnIndex + 1);
          this.selectedColumn = currentColumnIndex;
        } else {
          // This is a child navigation
          this.columnsData = this.columnsData.slice(0, this.selectedColumn + 1);
          this.columnsData.push({
            path: data.path,
            tree: data.tree,
            selectedIndex: -1, // Don't select any item by default
          });
          // Don't change selectedColumn - keep it on the parent folder
        }
      }

      this.renderColumnsView();
      this.updateBrowserPath();

      // Check if the selected item is a folder and load its contents
      const currentColumn = this.columnsData[this.selectedColumn];
      if (currentColumn && currentColumn.tree && currentColumn.tree.children) {
        const items = currentColumn.tree.children.sort((a, b) => {
          if (a.is_dir === b.is_dir) {
            return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
          }
          return a.is_dir ? -1 : 1;
        });

        // Get the selected item (not just the first)
        const selectedIndex = currentColumn.selectedIndex || 0;
        const selectedItem = items[selectedIndex];
        if (selectedItem && selectedItem.is_dir) {
          // Load the contents of the selected folder
          this.previewFolderContents(selectedItem.path);
        }
      }
    } catch (error) {
      console.error("Error browsing folder:", error);
      this.showToast("error", error.message);
      throw error; // Re-throw to handle in promise chain
    } finally {
      this.hideLoading();
    }
  }

  async previewFolderContents(path) {
    this.showLoading();

    try {
      const response = await fetch("/api/browse", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          path: path,
          max_depth: 1,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to browse folder");
      }

      // Truncate columns after current one and add preview
      this.columnsData = this.columnsData.slice(0, this.selectedColumn + 1);
      this.columnsData.push({
        path: data.path,
        tree: data.tree,
        selectedIndex: -1, // Don't select anything in preview
      });

      // Don't change selectedColumn - stay on current column
      this.renderColumnsView();
    } catch (error) {
      console.error("Error previewing folder:", error);
      this.showToast("error", error.message);
    } finally {
      this.hideLoading();
    }
  }

  renderColumnsView() {
    const container = document.getElementById("columns-browser");
    container.innerHTML = "";

    this.columnsData.forEach((columnData, columnIndex) => {
      const column = document.createElement("div");
      column.className = "column-view";
      column.dataset.columnIndex = columnIndex;

      if (!columnData.tree || !columnData.tree.children) {
        column.innerHTML = '<div class="empty-state"><p>Empty folder</p></div>';
        container.appendChild(column);
        return;
      }

      // Sort items: folders first, then files
      const items = columnData.tree.children.sort((a, b) => {
        if (a.is_dir === b.is_dir) {
          return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
        }
        return a.is_dir ? -1 : 1;
      });

      items.forEach((item, itemIndex) => {
        const itemEl = document.createElement("div");
        itemEl.className = "column-item";
        if (item.is_dir) {
          itemEl.classList.add("has-children");
        }

        // Apply selected class to the currently selected item in the active column
        if (
          columnIndex === this.selectedColumn &&
          itemIndex === columnData.selectedIndex
        ) {
          itemEl.classList.add("selected");
        }

        // Apply parent-selected class for previous columns' selected items
        if (
          columnIndex < this.selectedColumn &&
          itemIndex === columnData.selectedIndex
        ) {
          itemEl.classList.add("parent-selected");
        }

        itemEl.dataset.path = item.path;
        itemEl.dataset.isDir = item.is_dir;
        itemEl.dataset.itemIndex = itemIndex;

        itemEl.innerHTML = `
                    <span class="item-icon">${item.icon}</span>
                    <span class="item-name">${item.name}</span>
                `;

        let clickTimer = null;
        let clickCount = 0;

        itemEl.addEventListener("click", (e) => {
          e.preventDefault();
          e.stopPropagation();

          clickCount++;

          if (clickCount === 1) {
            clickTimer = setTimeout(() => {
              // Single click
              this.handleColumnItemClick(columnIndex, itemIndex, item);
              clickCount = 0;
            }, 250);
          } else if (clickCount === 2) {
            // Double click
            clearTimeout(clickTimer);
            clickCount = 0;

            if (item.is_dir) {
              // Double-click on folder selects it
              this.selectFolderFromColumn(item.path);
            } else {
              // Double-click on file selects parent folder
              this.selectFolderFromColumn(this.columnsData[columnIndex].path);
            }
          }
        });

        column.appendChild(itemEl);
      });

      container.appendChild(column);
    });

    // Scroll to show the latest column
    setTimeout(() => {
      container.scrollLeft = container.scrollWidth;
    }, 10);
  }

  handleColumnItemClick(columnIndex, itemIndex, item) {
    // Update the selected item in the clicked column
    this.columnsData[columnIndex].selectedIndex = itemIndex;

    // Only update selectedColumn if clicking in a different column
    if (this.selectedColumn !== columnIndex) {
      this.selectedColumn = columnIndex;
    }

    if (item.is_dir) {
      // Truncate any columns after this one before loading new content
      this.columnsData = this.columnsData.slice(0, columnIndex + 1);
      // Load the folder contents in the next column
      this.browseFolderPath(item.path);
    } else {
      // For files, update selectedColumn and truncate
      this.selectedColumn = columnIndex;
      this.columnsData = this.columnsData.slice(0, columnIndex + 1);
      this.renderColumnsView();
    }
  }

  handleKeyboardNavigation(e) {
    const currentColumn = this.columnsData[this.selectedColumn];
    if (!currentColumn || !currentColumn.tree || !currentColumn.tree.children)
      return;

    const items = currentColumn.tree.children.sort((a, b) => {
      if (a.is_dir === b.is_dir) {
        return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
      }
      return a.is_dir ? -1 : 1;
    });

    const currentIndex = currentColumn.selectedIndex;

    switch (e.key) {
      case "ArrowUp":
        e.preventDefault();
        if (currentIndex > 0) {
          // Clear any columns after the current one immediately
          this.columnsData = this.columnsData.slice(0, this.selectedColumn + 1);
          this.renderColumnsView();

          // Show loading animation
          this.showLoading();

          // Update selection index
          currentColumn.selectedIndex = currentIndex - 1;
          const newSelectedItem = items[currentColumn.selectedIndex];

          // Re-render to show new selection
          this.renderColumnsView();

          // If it's a directory, preview its contents
          if (newSelectedItem && newSelectedItem.is_dir) {
            // Small delay for visual feedback
            setTimeout(() => {
              this.previewFolderContents(newSelectedItem.path);
            }, 100);
          } else {
            // For files, just hide loading
            setTimeout(() => {
              this.hideLoading();
            }, 100);
          }
        }
        break;

      case "ArrowDown":
        e.preventDefault();
        if (currentIndex < items.length - 1) {
          // Clear any columns after the current one immediately
          this.columnsData = this.columnsData.slice(0, this.selectedColumn + 1);
          this.renderColumnsView();

          // Show loading animation
          this.showLoading();

          // Update selection index
          currentColumn.selectedIndex = currentIndex + 1;
          const newSelectedItem = items[currentColumn.selectedIndex];

          // Re-render to show new selection
          this.renderColumnsView();

          // If it's a directory, preview its contents
          if (newSelectedItem && newSelectedItem.is_dir) {
            // Small delay for visual feedback
            setTimeout(() => {
              this.previewFolderContents(newSelectedItem.path);
            }, 100);
          } else {
            // For files, just hide loading
            setTimeout(() => {
              this.hideLoading();
            }, 100);
          }
        }
        break;

      case "ArrowRight":
        e.preventDefault();
        // Move to next column if it exists
        if (this.selectedColumn < this.columnsData.length - 1) {
          this.selectedColumn++;
          // Ensure the first item is selected in the new column
          if (this.columnsData[this.selectedColumn].selectedIndex === -1) {
            this.columnsData[this.selectedColumn].selectedIndex = 0;
          }
          this.renderColumnsView();

          // Check if the newly selected item is a folder and load its contents
          const newColumn = this.columnsData[this.selectedColumn];
          if (newColumn && newColumn.tree && newColumn.tree.children) {
            const newItems = newColumn.tree.children.sort((a, b) => {
              if (a.is_dir === b.is_dir) {
                return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
              }
              return a.is_dir ? -1 : 1;
            });

            const selectedItem = newItems[newColumn.selectedIndex];
            if (selectedItem && selectedItem.is_dir) {
              // Load the contents of the selected folder
              this.previewFolderContents(selectedItem.path);
            }
          }
        } else {
          // If we're on a directory in the last column, open it
          const selectedItem = items[currentIndex];
          if (selectedItem && selectedItem.is_dir) {
            this.browseFolderPath(selectedItem.path);
          }
        }
        break;

      case "ArrowLeft":
        e.preventDefault();
        if (this.selectedColumn > 0) {
          this.selectedColumn--;
          // Don't truncate columns, just move focus back
          this.renderColumnsView();
        }
        break;

      case "Enter":
        e.preventDefault();
        const enterItem = items[currentIndex];
        if (enterItem) {
          if (enterItem.is_dir) {
            this.selectFolderFromColumn(enterItem.path);
          } else {
            // Select parent folder for files
            this.selectFolderFromColumn(currentColumn.path);
          }
        }
        break;

      case "Escape":
        // Only close modal if path input is not focused
        if (
          document.activeElement !==
          document.getElementById("browser-path-input")
        ) {
          e.preventDefault();
          this.closeFolderBrowser();
        }
        break;
    }
  }

  selectFolderFromColumn(path) {
    // Load the selected folder
    this.closeFolderBrowser();
    this.loadFolder(path);
  }

  updateBrowserPath() {
    const pathInput = document.getElementById("browser-path-input");
    if (this.columnsData.length > 0) {
      const currentPath = this.columnsData[this.selectedColumn].path;

      // Only update the input value if it's not currently focused
      // This prevents overwriting the user's typing
      if (document.activeElement !== pathInput) {
        pathInput.value = currentPath;
      }
    } else {
      if (document.activeElement !== pathInput) {
        pathInput.value = "";
      }
    }
  }
}

// Initialize the app when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new ContextForgeApp();
});

// Add some utility functions
window.ContextForgeUtils = {
  formatFileSize(bytes) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  },

  getFileExtension(filename) {
    return filename.split(".").pop().toLowerCase();
  },

  isTextFile(filename) {
    const textExtensions = [
      "txt",
      "md",
      "py",
      "js",
      "jsx",
      "ts",
      "tsx",
      "html",
      "css",
      "json",
      "xml",
      "yaml",
      "yml",
      "toml",
      "ini",
      "cfg",
      "conf",
      "log",
      "sh",
      "bat",
      "ps1",
      "sql",
      "php",
      "rb",
      "go",
      "rs",
      "cpp",
      "c",
      "h",
      "hpp",
      "java",
      "cs",
      "swift",
      "kt",
      "scala",
      "clj",
      "hs",
      "elm",
      "vue",
      "svelte",
      "dart",
    ];

    const ext = this.getFileExtension(filename);
    return textExtensions.includes(ext);
  },
};

// Diff Processor UI
class DiffUI {
  constructor(app) {
    this.app = app;
    this.xmlContent = "";
    this.parsedChanges = [];
    this.fileGroups = new Map(); // Group changes by file
    this.previews = [];
    this.fullContents = new Map(); // Store full file contents
    this.currentFile = null;
    this.individualChangeStates = new Map(); // Track individual change states
    this.bindEvents();
  }

  bindEvents() {
    // Preview button in main UI
    const previewBtn = document.getElementById("preview-changes-btn");
    if (previewBtn) {
      previewBtn.addEventListener("click", () => this.previewFromMain());
    }

    // Modal close button
    document
      .getElementById("diff-modal-close")
      .addEventListener("click", () => this.close());

    // Cancel button
    document
      .getElementById("diff-cancel-btn")
      .addEventListener("click", () => this.close());

    // Apply buttons
    document
      .getElementById("diff-apply-all-btn")
      .addEventListener("click", () => this.applyAll());
    document
      .getElementById("diff-apply-selected-btn")
      .addEventListener("click", () => this.applySelected());

    // Close on background click
    document.getElementById("diff-modal").addEventListener("click", (e) => {
      if (e.target.id === "diff-modal") {
        this.close();
      }
    });
  }

  previewFromMain() {
    this.xmlContent = document.getElementById("xml-input").value.trim();
    if (!this.xmlContent) {
      this.app.showToast("error", "Please paste XML content in the input area");
      return;
    }

    this.open();

    // Clear any stale state before parsing
    this.fileGroups.clear();

    this.parseXML();
  }

  open() {
    document.getElementById("diff-modal").classList.remove("hidden");
  }

  close() {
    document.getElementById("diff-modal").classList.add("hidden");
  }

  async parseXML() {
    if (!this.xmlContent) {
      this.xmlContent = document.getElementById("xml-input").value.trim();
    }

    if (!this.xmlContent) {
      this.app.showToast("error", "No XML content to parse");
      return;
    }

    try {
      const response = await fetch("/api/diff/parse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          xml: this.xmlContent,
          project_root: this.app.currentPath  // Add the current selected folder path
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to parse XML");
      }

      this.parsedChanges = data.changes;
      this.previews = data.previews;

      // Initialize individual change states based on the now-validated changes from backend
      this.individualChangeStates.clear();
      this.parsedChanges.forEach((change, idx) => {
        if (change.action === "modify" && change.individual_applied) {
          const key = `${change.relative_path}`;
          this.individualChangeStates.set(key, change.individual_applied);
        }
        // Also update the 'isApplied' status based on backend data
        change.isApplied =
          change.applied ||
          (this.previews[idx] && this.previews[idx].trim() === "");
      });

      // Group changes by file
      this.groupChangesByFile();

      // Check which changes are applied
      await this.checkAppliedStatus();

      // Fetch full file contents for all files
      await this.fetchFullContents();

      this.renderFileGroups();
      this.updateSummary();

      // Show preview section
      document
        .getElementById("diff-preview-section")
        .classList.remove("hidden");

      // Update button labels since we simplified the logic
      document.getElementById("diff-apply-all-btn").textContent =
        "Apply All Pending";
      document.getElementById("diff-apply-selected-btn").textContent =
        "Apply All Pending";

      // Show first file preview if available
      const firstFile = Array.from(this.fileGroups.keys())[0];
      if (firstFile) {
        this.showFilePreview(firstFile);
      }
    } catch (error) {
      console.error("Error parsing XML:", error);
      this.app.showToast("error", `Parse error: ${error.message}`);
    }
  }

  groupChangesByFile() {
    this.fileGroups.clear();

    this.parsedChanges.forEach((change, idx) => {
      const filePath = change.relative_path || change.path;

      if (!this.fileGroups.has(filePath)) {
        this.fileGroups.set(filePath, {
          path: filePath,
          changes: [],
          indexes: [],
          changeCount: 0, // Track total change count
        });
      }

      const group = this.fileGroups.get(filePath);
      group.changes.push(change);
      group.indexes.push(idx);

      // Calculate the actual number of changes based on action type
      if (change.action === "modify" && change.changes) {
        // For modify, count the number of search/replace pairs
        group.changeCount += change.changes.length;
      } else if (
        (change.action === "create" || change.action === "rewrite") &&
        change.contents
      ) {
        // For create/rewrite, count the number of content blocks
        group.changeCount += change.contents.length || 1;
      } else {
        // For other actions (delete, rename), count as 1
        group.changeCount += 1;
      }
    });
  }

  async checkAppliedStatus() {
    try {
      // Collect all changes to check
      const changes = [];

      for (const [filePath, group] of this.fileGroups) {
        if (group.changes.length > 0) {
          changes.push(group.changes[0]);
        }
      }

      const response = await fetch("/api/diff/check-applied", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ changes, project_root: this.app.currentPath }),
      });

      const data = await response.json();

      if (data.success) {
        // Update the applied status directly in our file groups
        for (const [filePath, group] of this.fileGroups) {
          if (group.changes.length > 0) {
            const change = group.changes[0];
            const relativePath = change.relative_path || change.path;

            // Update the applied status from backend response
            if (data.results.hasOwnProperty(relativePath)) {
              change.applied = data.results[relativePath];
            }
          }
        }
      }
    } catch (error) {
      console.error("Error checking applied status:", error);
    }
  }

  async toggleIndividualChange(
    filePath,
    changeIndex,
    searchText,
    replaceText,
    apply
  ) {
    try {
      const response = await fetch("/api/diff/toggle-change", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          file_path: filePath,
          change_index: changeIndex,
          search: searchText,
          replace: replaceText,
          apply: apply,
          project_root: this.app.currentPath,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to toggle individual change");
      }

      // Update the individual change state
      const key = `${filePath}`;
      if (!this.individualChangeStates.has(key)) {
        this.individualChangeStates.set(key, []);
      }
      const states = this.individualChangeStates.get(key);
      if (states.length > changeIndex) {
        states[changeIndex] = apply;
      }

      // Show success message
      const action = apply ? "Applied" : "Reverted";
      this.app.showToast("success", `${action} change ${changeIndex + 1}`);

      // Refresh the current view
      if (this.currentFile === filePath) {
        this.showFilePreview(filePath);
      }

      // Update summary
      this.updateSummary();

      return true;
    } catch (error) {
      const action = apply ? "apply" : "revert";
      this.app.showToast(
        "error",
        `Failed to ${action} change: ${error.message}`
      );
      return false;
    }
  }

  async toggleFileChange(filePath, apply) {
    const group = this.fileGroups.get(filePath);
    if (!group || group.changes.length === 0) return;

    const change = group.changes[0];

    // Additional validation for modify actions
    if (
      change.action === "modify" &&
      (!change.changes || change.changes.length === 0)
    ) {
      this.app.showToast("error", "No valid changes to apply for this file");
      return;
    }

    console.log("Sending toggle request with change data:", change);

    try {
      const response = await fetch("/api/diff/toggle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          change: change,
          apply: apply,
          project_root: this.app.currentPath,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to toggle change");
      }

      // Update the applied status from the backend response
      change.applied = apply;

      // Show success message
      const action = apply ? "Applied" : "Reverted";
      this.app.showToast(
        "success",
        `${action} changes to ${data.path || filePath}`
      );

      // Refresh file tree if needed
      if (this.app.currentPath) {
        setTimeout(() => {
          this.app.loadFolder(this.app.currentPath);
        }, 500);
      }

      return true;
    } catch (error) {
      // Provide more context in error messages
      const action = apply ? "apply" : "revert";
      this.app.showToast(
        "error",
        `Failed to ${action} changes: ${error.message}`
      );
      return false;
    }
  }

  async fetchFullContents() {
    for (const [filePath, group] of this.fileGroups) {
      // Only fetch for existing files (not create actions)
      const hasExistingFile = group.changes.some((c) => c.action !== "create");

      if (hasExistingFile) {
        try {
          const response = await fetch("/api/file-content", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ path: group.changes[0].path }),
          });

          if (response.ok) {
            const data = await response.json();
            this.fullContents.set(filePath, data.content);
          }
        } catch (error) {
          console.error(`Error fetching content for ${filePath}:`, error);
        }
      }
    }
  }

  renderFileGroups() {
    const container = document.getElementById("file-groups-list");
    container.innerHTML = "";

    for (const [filePath, group] of this.fileGroups) {
      const fileGroup = document.createElement("div");
      fileGroup.className = "file-group";
      fileGroup.dataset.path = filePath;

      // Check if this file has valid changes
      const hasValidChanges = group.changeCount > 0;

      if (!hasValidChanges) {
        fileGroup.classList.add("no-changes");
        fileGroup.style.opacity = "0.5";
        fileGroup.style.pointerEvents = "none";
      }

      const header = document.createElement("div");
      header.className = "file-group-header";

      // Check if this file is already applied
      const isApplied = group.changes[0].applied;

      if (isApplied) {
        header.classList.add("applied");
        header.style.backgroundColor = "rgba(52, 199, 89, 0.1)";
        header.style.borderColor = "rgba(52, 199, 89, 0.3)";
      }

      // Create content container for path and count
      const contentContainer = document.createElement("div");
      contentContainer.className = "file-group-content";
      contentContainer.style.display = "flex";
      contentContainer.style.flexDirection = "column";
      contentContainer.style.flex = "1";
      contentContainer.style.minWidth = "0"; // Allow text truncation

      const pathSpan = document.createElement("span");
      pathSpan.className = "file-group-path";
      pathSpan.textContent = filePath;
      pathSpan.title = filePath;
      pathSpan.style.fontSize = "0.9rem";
      pathSpan.style.fontWeight = "500";
      pathSpan.style.overflow = "hidden";
      pathSpan.style.textOverflow = "ellipsis";
      pathSpan.style.whiteSpace = "nowrap";

      const countSpan = document.createElement("span");
      countSpan.className = "file-group-count";

      if (!hasValidChanges) {
        countSpan.textContent = "0 changes (all invalid)";
        countSpan.style.color = "var(--error-color, #ff6b6b)";
      } else {
        const changeCount = group.changeCount || group.changes.length;

        // Calculate applied changes for this file
        let appliedInFile = 0;
        if (group.changes[0].action === "modify") {
          const individualStates =
            this.individualChangeStates.get(filePath) || [];
          appliedInFile = individualStates.filter((state) => state).length;
        } else if (group.changes[0].applied) {
          appliedInFile = changeCount;
        }

        const progressText =
          appliedInFile > 0
            ? `${appliedInFile}/${changeCount} changes applied`
            : `${changeCount} change${changeCount > 1 ? "s" : ""}`;

        countSpan.textContent = progressText;
      }

      countSpan.style.fontSize = "0.75rem";
      countSpan.style.marginTop = "2px";

      contentContainer.appendChild(pathSpan);
      contentContainer.appendChild(countSpan);

      const checkboxWrapper = document.createElement("div");
      const checkbox = document.createElement("input");
      const checkboxVisual = document.createElement("div");

      if (hasValidChanges) {
        // Create checkbox wrapper
        checkboxWrapper.className = "checkbox-wrapper";
        checkboxWrapper.style.marginRight = "8px";

        checkbox.type = "checkbox";
        checkbox.className = "checkbox";
        checkbox.checked = isApplied;

        checkboxVisual.className = "checkbox-visual";
        checkboxVisual.innerHTML = `
                    <span class="checkbox-icon check">✓</span>
                    <span class="checkbox-icon minus">−</span>
                `;

        checkboxWrapper.appendChild(checkbox);
        checkboxWrapper.appendChild(checkboxVisual);

        // Handle checkbox toggle with live apply/revert
        checkboxWrapper.onclick = async (e) => {
          e.stopPropagation();

          // this is correct because the checkbox is already changed before the event is triggered
          const newState = checkbox.checked;

          // Disable checkbox during operation
          checkbox.disabled = true;
          checkboxVisual.style.opacity = "0.5";

          // Apply or revert based on new state
          const success = await this.toggleFileChange(filePath, newState);

          if (success) {
            // Update visual state with green color effect
            header.classList.toggle("applied", newState);
            if (newState) {
              header.style.backgroundColor = "rgba(52, 199, 89, 0.1)";
              header.style.borderColor = "rgba(52, 199, 89, 0.3)";
            } else {
              header.style.backgroundColor = "";
              header.style.borderColor = "";
            }
          } else {
            // Revert checkbox state on failure
            checkbox.checked = !newState;
          }

          checkbox.disabled = false;
          checkboxVisual.style.opacity = "1";
          this.updateSummary();
        };

        header.appendChild(checkboxWrapper);
      }
      header.appendChild(contentContainer);

      // Only add click handler if there are valid changes
      if (hasValidChanges) {
        header.onclick = async (e) => {
          // Don't trigger if clicking directly on checkbox wrapper
          if (e.target.closest(".checkbox-wrapper")) {
            return;
          }

          // Toggle the checkbox state
          const newState = !checkbox.checked;
          checkbox.checked = newState;

          // Disable checkbox during operation
          checkbox.disabled = true;
          checkboxVisual.style.opacity = "0.5";

          // Apply or revert based on new state
          const success = await this.toggleFileChange(filePath, newState);

          if (success) {
            // Update visual state with green color effect
            header.classList.toggle("applied", newState);
            if (newState) {
              header.style.backgroundColor = "rgba(52, 199, 89, 0.1)";
              header.style.borderColor = "rgba(52, 199, 89, 0.3)";
            } else {
              header.style.backgroundColor = "";
              header.style.borderColor = "";
            }
          } else {
            // Revert checkbox state on failure
            checkbox.checked = !newState;
          }

          checkbox.disabled = false;
          checkboxVisual.style.opacity = "1";
          this.updateSummary();
        };
      }

      // Add change details
      const changesDiv = document.createElement("div");
      changesDiv.className = "file-group-changes";

      let changeIndex = 0;
      group.changes.forEach((change) => {
        if (change.action === "modify" && change.changes) {
          // For modify actions, show each search/replace as a separate change
          change.changes.forEach(() => {
            changeIndex++;
            const changeItem = document.createElement("div");
            changeItem.className = "change-item";

            const actionSpan = document.createElement("span");
            actionSpan.className = `change-action ${change.action.toLowerCase()}`;
            actionSpan.textContent = change.action;

            const descSpan = document.createElement("span");
            descSpan.textContent = `Change ${changeIndex}`;

            changeItem.appendChild(actionSpan);
            changeItem.appendChild(descSpan);
            changesDiv.appendChild(changeItem);
          });
        } else if (
          (change.action === "create" || change.action === "rewrite") &&
          change.contents &&
          change.contents.length > 0
        ) {
          // For create/rewrite with multiple content blocks
          change.contents.forEach(() => {
            changeIndex++;
            const changeItem = document.createElement("div");
            changeItem.className = "change-item";

            const actionSpan = document.createElement("span");
            actionSpan.className = `change-action ${change.action.toLowerCase()}`;
            actionSpan.textContent = change.action;

            const descSpan = document.createElement("span");
            descSpan.textContent = `Change ${changeIndex}`;

            changeItem.appendChild(actionSpan);
            changeItem.appendChild(descSpan);
            changesDiv.appendChild(changeItem);
          });
        } else {
          // Default: single change
          changeIndex++;
          const changeItem = document.createElement("div");
          changeItem.className = "change-item";

          const actionSpan = document.createElement("span");
          actionSpan.className = `change-action ${change.action.toLowerCase()}`;
          actionSpan.textContent = change.action;

          const descSpan = document.createElement("span");
          descSpan.textContent = `Change ${changeIndex}`;

          changeItem.appendChild(actionSpan);
          changeItem.appendChild(descSpan);
          changesDiv.appendChild(changeItem);
        }
      });

      fileGroup.appendChild(header);
      fileGroup.appendChild(changesDiv);
      container.appendChild(fileGroup);
    }
  }

  checkHashMismatch(filePath) {
    const group = this.fileGroups.get(filePath);
    if (!group) return false;

    const change = group.changes[0];
    const stateKey = this.getStateKey(filePath, change.xml_hash);
    const savedState = this.appliedState[stateKey];

    if (!savedState || !savedState.applied) return false;

    // Check if there's a different version already applied
    for (const key in this.appliedState) {
      const [statePath] = key.split("|");
      if (
        statePath === filePath &&
        key !== stateKey &&
        this.appliedState[key].applied
      ) {
        return true;
      }
    }

    return false;
  }

  renderFileList() {
    const list = document.getElementById("file-change-list");
    list.innerHTML = this.parsedChanges
      .map((change, idx) => {
        const actionClass = change.action.toLowerCase();
        const checked = this.selectedIndexes.has(idx) ? "checked" : "";
        const selected = idx === this.currentPreviewIndex ? "selected" : "";

        return `
                <li class="change-item ${selected}" data-idx="${idx}">
                    <input type="checkbox" ${checked} data-idx="${idx}" />
                    <span class="change-action ${actionClass}">${change.action}</span>
                    <span class="change-path" title="${change.relative_path}">${change.relative_path}</span>
                </li>
            `;
      })
      .join("");

    // Add event listeners
    list.querySelectorAll(".change-item").forEach((item) => {
      const idx = parseInt(item.dataset.idx);

      // Click on item to show preview
      item.addEventListener("click", (e) => {
        if (e.target.type !== "checkbox") {
          this.showPreview(idx);
        }
      });

      // Checkbox change
      const checkbox = item.querySelector('input[type="checkbox"]');
      checkbox.addEventListener("change", (e) => {
        if (e.target.checked) {
          this.selectedIndexes.add(idx);
        } else {
          this.selectedIndexes.delete(idx);
        }
        this.updateSummary();
      });
    });
  }

  showFilePreview(filePath) {
    this.currentFile = filePath;
    const group = this.fileGroups.get(filePath);

    if (!group) return;

    // Update title with applied status
    const titleElement = document.getElementById("code-viewer-title");

    // Check if this change is already applied
    const isApplied =
      group.changes[0].applied ||
      (this.previews[group.indexes[0]] &&
        this.previews[group.indexes[0]].trim() === "");

    if (isApplied) {
      titleElement.innerHTML = `
                <span>${filePath}</span>
                <span class="applied-badge" style="
                    margin-left: 12px;
                    padding: 4px 8px;
                    background: rgba(52, 199, 89, 0.2);
                    color: #34c759;
                    border-radius: 4px;
                    font-size: 0.8em;
                    font-weight: 500;
                ">✅ Applied</span>
            `;
    } else {
      titleElement.textContent = filePath;
    }

    // Render file tabs
    this.renderFileTabs();

    // Show unified diff view
    this.showUnifiedDiffView(filePath);
  }

  renderFileTabs() {
    const tabsContainer = document.getElementById("file-tabs");
    tabsContainer.innerHTML = "";

    for (const [filePath, group] of this.fileGroups) {
      const tab = document.createElement("div");
      tab.className = "file-tab";
      if (filePath === this.currentFile) {
        tab.classList.add("active");
      }

      // Get the primary action (first change action)
      const action = group.changes[0].action;
      const actionSpan = document.createElement("span");
      actionSpan.className = `file-tab-action ${action.toLowerCase()}`;
      actionSpan.textContent = action;

      const nameSpan = document.createElement("span");
      nameSpan.textContent = filePath.split("/").pop();
      nameSpan.title = filePath;

      tab.appendChild(actionSpan);
      tab.appendChild(nameSpan);

      tab.onclick = () => this.showFilePreview(filePath);

      tabsContainer.appendChild(tab);
    }
  }

  showUnifiedDiffView(filePath) {
    const viewer = document.getElementById("code-viewer");
    const group = this.fileGroups.get(filePath);

    if (!group) return;

    // Clear viewer
    viewer.innerHTML = "";

    // Get change info for rendering
    const change = group.changes[0];

    let lines = [];
    let lineStates = []; // Track state of each line: 'normal', 'added', 'removed'
    let changeIndexMap = []; // Maps line indices to change indices

    // Handle different action types
    if (group.changes[0].action === "create") {
      // For create, all lines are new
      const content = group.changes[0].content || "";
      lines = content.split("\n");
      lineStates = new Array(lines.length).fill("added");
    } else if (group.changes[0].action === "rewrite") {
      // For rewrite, show old content as removed and new as added
      if (this.fullContents.has(filePath)) {
        const oldContent = this.fullContents.get(filePath);
        const oldLines = oldContent.split("\n");
        const newContent = group.changes[0].content || "";
        const newLines = newContent.split("\n");

        // Add old lines as removed
        lines.push(...oldLines);
        lineStates.push(...new Array(oldLines.length).fill("removed"));

        // Add new lines as added
        lines.push(...newLines);
        lineStates.push(...new Array(newLines.length).fill("added"));
      } else {
        // No old content, treat as create
        const content = group.changes[0].content || "";
        lines = content.split("\n");
        lineStates = new Array(lines.length).fill("added");
      }
    } else if (group.changes[0].action === "modify") {
      // For modify, apply changes and track which lines changed
      if (this.fullContents.has(filePath)) {
        let content = this.fullContents.get(filePath);
        lines = content.split("\n");
        lineStates = new Array(lines.length).fill("normal");

        const changeMap = {}; // Map line indices to change indices
        let currentChangeIndex = 0;

        // Get individual applied states
        const key = `${filePath}`;
        const individualStates = this.individualChangeStates.get(key) || [];

        // Track line changes
        for (const change of group.changes) {
          for (const [search, replace] of change.changes) {
            const searchLines = search.split("\n");
            const replaceLines = replace.split("\n");

            // Find where the change occurs in the content
            const contentStr = lines.join("\n");
            const searchIndex = contentStr.indexOf(search);

            if (searchIndex !== -1) {
              // Calculate line numbers
              const beforeSearch = contentStr.substring(0, searchIndex);
              const startLine = beforeSearch.split("\n").length - 1;
              const endLine = startLine + searchLines.length;

              // Map this change to its starting line
              changeMap[startLine] = currentChangeIndex;

              // Check if this individual change is applied
              const isChangeApplied =
                individualStates[currentChangeIndex] || false;

              // Mark old lines as removed (even if applied, we want to show the diff)
              for (let i = startLine; i < endLine; i++) {
                if (i < lines.length) {
                  lineStates[i] = isChangeApplied
                    ? "applied-removed"
                    : "removed";
                }
              }

              // Insert new lines as added
              const newLines = [];
              const newStates = [];

              for (let i = 0; i < lines.length; i++) {
                if (i === startLine) {
                  // First, add the OLD lines marked as removed
                  for (
                    let j = startLine;
                    j < endLine && j < lines.length;
                    j++
                  ) {
                    newLines.push(lines[j]);
                    newStates.push("removed");
                  }

                  // Then add the NEW lines marked as added
                  newLines.push(...replaceLines);
                  newStates.push(
                    ...new Array(replaceLines.length).fill("added")
                  );

                  // Skip to the end of the replaced section
                  i = endLine - 1;
                } else if (i >= startLine && i < endLine) {
                  // Skip these lines as they've already been processed
                  continue;
                } else {
                  newLines.push(lines[i]);
                  newStates.push(lineStates[i]);
                }
              }

              lines = newLines;
              lineStates = newStates;
            }

            currentChangeIndex++;
          }
        }

        // Create change data object
        const changeData = {
          filePath: filePath,
          changeMap: changeMap,
          changes: change.changes,
          appliedStates: individualStates,
        };

        // Render the lines with change data
        this.renderUnifiedDiffLines(viewer, lines, lineStates, changeData);
        return;
      }
    } else if (group.changes[0].action === "delete") {
      lines = ["[File will be deleted]"];
      lineStates = ["removed"];
    } else {
      lines = ["[Unable to load file content]"];
      lineStates = ["normal"];
    }

    // Render the lines with proper diff styling
    this.renderUnifiedDiffLines(viewer, lines, lineStates);
  }

  renderUnifiedDiffLines(viewer, lines, lineStates, changeData = null) {
    viewer.innerHTML = "";

    // Create a container div instead of just a table
    const container = document.createElement("div");
    container.className = "code-viewer-wrapper";

    // Track which changes we've already rendered buttons for
    const renderedChanges = new Set();

    // Group consecutive lines by their change index
    const lineGroups = [];
    let currentGroup = null;

    lines.forEach((line, index) => {
      const state = lineStates[index] || "normal";
      const changeIndex =
        changeData && changeData.changeMap && changeData.changeMap[index];

      // Check if we need to start a new group
      if (changeIndex !== undefined && !renderedChanges.has(changeIndex)) {
        // Start a new change group
        currentGroup = {
          changeIndex: changeIndex,
          startIndex: index,
          lines: [],
        };
        lineGroups.push(currentGroup);
        renderedChanges.add(changeIndex);
      }

      // Add line to current group or create a normal group
      if (currentGroup && (state === "removed" || state === "added")) {
        currentGroup.lines.push({ line, index, state });
      } else {
        // Create a normal lines group
        if (!currentGroup || currentGroup.changeIndex !== undefined) {
          currentGroup = {
            changeIndex: undefined,
            lines: [],
          };
          lineGroups.push(currentGroup);
        }
        currentGroup.lines.push({ line, index, state });
      }
    });

    // Render each group
    lineGroups.forEach((group) => {
      if (group.changeIndex !== undefined && changeData) {
        // This is a change group - render with action bar
        const changeSection = document.createElement("div");
        changeSection.className = "change-section";

        // Create action bar
        const actionBar = document.createElement("div");
        actionBar.className = "change-action-bar";

        const label = document.createElement("span");
        label.className = "change-action-bar-label";
        label.textContent = `Change ${group.changeIndex + 1}`;
        actionBar.appendChild(label);

        // Add apply/revert button
        const isApplied =
          changeData.appliedStates &&
          changeData.appliedStates[group.changeIndex];

        const button = document.createElement("button");
        button.className = `change-action-btn ${isApplied ? "undo" : "apply"}`;
        button.textContent = isApplied ? "Revert" : "Apply";
        button.dataset.changeIndex = group.changeIndex;

        button.onclick = async () => {
          button.disabled = true;

          // Validate that the change exists before accessing it
          if (!changeData.changes || !changeData.changes[group.changeIndex]) {
            console.error(
              "Invalid change index:",
              group.changeIndex,
              "for changes:",
              changeData.changes
            );
            button.disabled = false;
            return;
          }

          const [searchText, replaceText] =
            changeData.changes[group.changeIndex];
          if (!searchText || !replaceText) {
            console.error("Invalid change data at index:", group.changeIndex);
            button.disabled = false;
            return;
          }

          const success = await this.toggleIndividualChange(
            changeData.filePath,
            group.changeIndex,
            searchText,
            replaceText,
            !isApplied
          );

          if (success) {
            // Refresh the view to show updated state
            await this.app.refreshFileTree();
            this.showFilePreview(changeData.filePath);
          }

          button.disabled = false;
        };

        actionBar.appendChild(button);
        changeSection.appendChild(actionBar);

        // Create table for this change's lines
        const table = document.createElement("table");
        table.className = "code-viewer-table";

        group.lines.forEach(({ line, index, state }) => {
          const lineRow = document.createElement("tr");
          lineRow.className = "code-line";

          if (state === "added") {
            lineRow.classList.add("added");
          } else if (state === "removed") {
            lineRow.classList.add("removed");
          } else if (state === "context") {
            lineRow.classList.add("context");
          }

          // Add line number cell
          const lineNumberCell = document.createElement("td");
          lineNumberCell.className = "line-number";
          lineNumberCell.textContent = (index + 1).toString();

          // Add line content cell
          const lineContentCell = document.createElement("td");
          lineContentCell.className = "line-content";
          lineContentCell.textContent = line;

          lineRow.appendChild(lineNumberCell);
          lineRow.appendChild(lineContentCell);
          table.appendChild(lineRow);
        });

        changeSection.appendChild(table);
        container.appendChild(changeSection);
      } else {
        // Normal lines group - render without action bar
        const table = document.createElement("table");
        table.className = "code-viewer-table";

        group.lines.forEach(({ line, index, state }) => {
          const lineRow = document.createElement("tr");
          lineRow.className = "code-line";

          if (state === "added") {
            lineRow.classList.add("added");
          } else if (state === "removed") {
            lineRow.classList.add("removed");
          } else if (state === "context") {
            lineRow.classList.add("context");
          }

          // Add line number cell
          const lineNumberCell = document.createElement("td");
          lineNumberCell.className = "line-number";
          lineNumberCell.textContent = (index + 1).toString();

          // Add line content cell
          const lineContentCell = document.createElement("td");
          lineContentCell.className = "line-content";
          lineContentCell.textContent = line;

          lineRow.appendChild(lineNumberCell);
          lineRow.appendChild(lineContentCell);
          table.appendChild(lineRow);
        });

        container.appendChild(table);
      }
    });

    viewer.appendChild(container);
  }

  showDiffView(filePath) {
    const viewer = document.getElementById("code-viewer");
    const group = this.fileGroups.get(filePath);

    if (!group) return;

    // Combine all diffs for this file
    let combinedDiff = "";
    group.indexes.forEach((idx, i) => {
      if (i > 0) combinedDiff += "\n\n--- Change " + (i + 1) + " ---\n\n";
      combinedDiff += this.previews[idx];
    });

    // Format diff with syntax highlighting
    viewer.innerHTML = this.formatDiff(combinedDiff);
  }

  setViewMode(mode) {
    this.viewMode = mode;

    // Update button states
    document
      .getElementById("toggle-diff-view")
      .classList.toggle("btn-primary", mode === "diff");
    document
      .getElementById("toggle-full-view")
      .classList.toggle("btn-primary", mode === "full");

    // Re-render current file
    if (this.currentFile) {
      if (mode === "full") {
        this.showFullCode(this.currentFile);
      } else {
        this.showDiffView(this.currentFile);
      }
    }
  }

  formatDiff(diff) {
    // Simple diff syntax highlighting
    return diff
      .split("\n")
      .map((line) => {
        if (line.startsWith("+++") || line.startsWith("---")) {
          return `<span class="diff-header">${this.escapeHtml(line)}</span>`;
        } else if (line.startsWith("+")) {
          return `<span class="diff-added">${this.escapeHtml(line)}</span>`;
        } else if (line.startsWith("-")) {
          return `<span class="diff-removed">${this.escapeHtml(line)}</span>`;
        } else {
          return this.escapeHtml(line);
        }
      })
      .join("\n");
  }

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  updateSummary() {
    const totalFiles = this.fileGroups.size;
    let appliedCount = 0;
    let pendingCount = 0;
    let visibleCount = 0;
    let totalChanges = 0;
    let appliedChanges = 0;

    for (const [filePath, group] of this.fileGroups) {
      visibleCount++;

      if (group.changes[0].action === "modify") {
        // Count individual changes for modify actions
        const individualStates =
          this.individualChangeStates.get(filePath) || [];
        const changeCount = group.changes[0].changes.length;
        totalChanges += changeCount;

        const appliedInFile = individualStates.filter((state) => state).length;
        appliedChanges += appliedInFile;

        if (appliedInFile === changeCount) {
          appliedCount++;
        } else if (appliedInFile > 0) {
          // Partially applied
        } else {
          pendingCount++;
        }
      } else {
        // For non-modify actions, count as single change
        totalChanges++;
        if (group.changes[0].applied) {
          appliedCount++;
          appliedChanges++;
        } else {
          pendingCount++;
        }
      }
    }

    // Disable Apply buttons if no pending changes
    const hasPending = pendingCount > 0;
    document.getElementById("diff-apply-all-btn").disabled = !hasPending;
    document.getElementById("diff-apply-selected-btn").disabled = !hasPending;

    const text =
      visibleCount === 0
        ? "No changes to apply"
        : `${appliedChanges}/${totalChanges} changes applied across ${visibleCount} files`;
    document.getElementById("diff-summary-text").textContent = text;
  }

  async applyAll() {
    const allIndexes = [];
    for (const group of this.fileGroups.values()) {
      allIndexes.push(...group.indexes);
    }
    await this.apply(allIndexes);
  }

  async applySelected() {
    // Note: With individual toggles, this bulk operation is less useful
    // For now, just apply all pending changes
    const pendingIndexes = [];
    for (const [filePath, group] of this.fileGroups) {
      if (!group.changes[0].applied) {
        pendingIndexes.push(...group.indexes);
      }
    }
    await this.apply(pendingIndexes);
  }

  async apply(indexes) {
    if (indexes.length === 0) {
      this.app.showToast("error", "No files selected");
      return;
    }

    const selectedChanges = indexes.map((i) => this.parsedChanges[i]);

    try {
      const response = await fetch("/api/diff/apply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          selected_changes: selectedChanges,
          project_root: this.app.currentPath,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to apply changes");
      }

      const { summary } = data;
      if (summary.failed > 0) {
        this.app.showToast(
          "warning",
          `Applied ${summary.succeeded} changes, ${summary.failed} failed`
        );
      } else {
        this.app.showToast(
          "success",
          `Successfully applied ${summary.succeeded} changes!`
        );
      }

      // Refresh file tree if folder is loaded
      if (this.app.currentPath) {
        this.app.loadFolder(this.app.currentPath);
      }

      // Close modal on success
      if (summary.failed === 0) {
        setTimeout(() => this.close(), 1500);
      }
    } catch (error) {
      this.app.showToast("error", `Apply error: ${error.message}`);
    }
  }
}
