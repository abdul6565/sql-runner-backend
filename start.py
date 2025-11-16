#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    # Set port from environment or default to 8000
    port_str = os.environ.get('PORT', '8000')

    # Convert port to integer to validate it
    try:
        port = int(port_str)
    except ValueError:
        print(f"Error: Invalid PORT value '{port_str}', using default 8000")
        port = 8000

    # Start the FastAPI server
    cmd = [
        sys.executable, '-m', 'uvicorn',
        'app:app',
        '--host', '0.0.0.0',
        '--port', str(port)
    ]

    print(f"Starting server on port {port}")
    subprocess.run(cmd)

if __name__ == '__main__':
    main()
