#!/usr/bin/env python3
"""
Simple script to run the RepoPPrompt web version
"""

import argparse
import os
import sys
from pathlib import Path

# Add current directory to path to import app
sys.path.insert(0, str(Path(__file__).parent))

from app import app

def main():
    """Main entry point for ContextForge."""
    parser = argparse.ArgumentParser(description='ContextForge - AI-friendly code prompt generator')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Port to listen on (default: 5000)')
    parser.add_argument('--dev', action='store_true', help='Run in development mode with Flask dev server')
    
    args = parser.parse_args()
    
    print(f"🚀 Starting ContextForge on http://{args.host}:{args.port}")
    print(f"🔑 To access over SSH, use: ssh -L {args.port}:localhost:{args.port} your-server")
    print()
    
    try:
        if args.dev:
            print("⚠️  Running in development mode")
            app.run(debug=True, host=args.host, port=args.port)
        else:
            # Use waitress for production
            from waitress import serve
            print("✨ Running with Waitress WSGI server")
            serve(
                app,
                host=args.host,
                port=args.port,
                threads=6,
                cleanup_interval=30,
                url_prefix="/"
            )
    except KeyboardInterrupt:
        print("\n👋 Shutting down ContextForge...")

if __name__ == '__main__':
    main() 