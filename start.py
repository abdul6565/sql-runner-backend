#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    # Set port from environment or default to 8000
    port = os.environ.get('PORT', '8000')
    
    # Start the FastAPI server
    cmd = [
        sys.executable, '-m', 'uvicorn', 
        'main:app', 
        '--host', '0.0.0.0', 
        '--port', port
    ]
    
    subprocess.run(cmd)

if __name__ == '__main__':
    main()