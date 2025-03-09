#!/usr/bin/env python3
"""
YouTube Optimizer Setup Script
This script creates the necessary file structure and configuration
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def main():
    # Define API key inside the function to avoid the UnboundLocalError
    YOUTUBE_API_KEY = "YOUR_API_KEY_HERE"
    
    print("=" * 70)
    print("YouTube Content Optimizer Setup")
    print("=" * 70)
    print("\nThis setup script will prepare your environment for the YouTube Optimizer.")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("\nError: Python 3.6 or higher is required.")
        print(f"Current version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        input("\nPress Enter to exit...")
        return
    
    print(f"\nPython version {python_version.major}.{python_version.minor}.{python_version.micro} detected. ✓")
    
    # Install required packages
    print("\nInstalling required packages...")
    required_packages = ["requests", "numpy"]
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        for package in required_packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"\nError installing packages: {str(e)}")
        print("\nPlease manually install these packages:")
        print("pip install requests numpy")
    
    # Create directory structure
    print("\nCreating directory structure...")
    directories = ["data", "output"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' created. ✓")
    
    # Create empty competitor database
    print("\nInitializing competitor database...")
    competitor_db = {
        "productivity": [],
        "health_fitness": [],
        "ai_tech": []
    }
    
    with open("competitor_database.json", "w") as f:
        json.dump(competitor_db, f, indent=2)
    
    print("Competitor database initialized. ✓")
    
    # Update API key in main script
    print("\nConfiguring API key...")
    if YOUTUBE_API_KEY == "YOUR_API_KEY_HERE":
        # Default key is being used, ask user if they want to change
        print("\nYou're currently using the default API key.")
        change_key = input("Do you want to use a different YouTube API key? (y/n): ").lower() == 'y'
        
        if change_key:
            new_key = input("Enter your YouTube API key: ").strip()
            if new_key:
                YOUTUBE_API_KEY = new_key
                update_api_key_in_files(new_key)
    else:
        # Update the key in the files
        update_api_key_in_files(YOUTUBE_API_KEY)
    
    print("API key configured. ✓")
    
    # Final steps
    print("\nSetup complete! ✓")
    print("\nTo start using the YouTube Optimizer, run:")
    print("python api-youtube-optimizer.py")
    
    input("\nPress Enter to exit...")

def update_api_key_in_files(api_key):
    """Update the API key in all necessary files"""
    try:
        # Update in api-youtube-optimizer.py
        optimizer_file = "api-youtube-optimizer.py"
        if os.path.exists(optimizer_file):
            with open(optimizer_file, "r") as f:
                content = f.read()
            
            # Replace the API key
            content = content.replace('YOUTUBE_API_KEY = "YOUR_API_KEY_HERE"', f'YOUTUBE_API_KEY = "{api_key}"')
            content = content.replace('YOUTUBE_API_KEY = "YOUR_API_KEY_HERE"', f'YOUTUBE_API_KEY = "{api_key}"')
            
            with open(optimizer_file, "w") as f:
                f.write(content)
            
            print(f"API key updated in {optimizer_file}. ✓")
        
        # No need to update this file as API key is now local to function
            
    except Exception as e:
        print(f"Error updating API key in files: {str(e)}")
        print("Please manually update the API key in the files.")

if __name__ == "__main__":
    main()