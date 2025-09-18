#!/usr/bin/env python3
"""
setup script for barcarate
creates directory structure and sets up the project
"""

import os
import sys

def create_directories():
    """create necessary directories"""
    directories = [
        'frontend',
        'frontend/dist'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"created directory: {directory}")

def check_python_version():
    """ensure python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("error: python 3.8 or higher is required")
        sys.exit(1)
    print(f"python version: {sys.version}")

def main():
    """main setup function"""
    print("setting up barcarate project...")
    
    check_python_version()
    create_directories()
    
    print("\nsetup complete!")
    print("\nto run the project:")
    print("1. pip install -r requirements.txt")
    print("2. python app.py")
    print("3. open http://localhost:5000 in your browser")

if __name__ == '__main__':
    main()