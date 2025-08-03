#!/usr/bin/env python3
"""
Project renaming utility
"""

import os
import sys
import shutil


def rename_project(new_name):
    """Rename the project directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    new_path = os.path.join(parent_dir, new_name)
    
    if os.path.exists(new_path):
        print(f"Error: Directory '{new_name}' already exists!")
        return False
    
    try:
        # Get the current directory name
        current_name = os.path.basename(current_dir)
        
        print(f"Renaming project from '{current_name}' to '{new_name}'...")
        
        # Rename the directory
        shutil.move(current_dir, new_path)
        
        print(f"✓ Project successfully renamed to '{new_name}'")
        print(f"✓ New location: {new_path}")
        
        return True
        
    except Exception as e:
        print(f"Error renaming project: {e}")
        return False


if __name__ == "__main__":
    print("AI Network Simulator - Project Renamer")
    print("=" * 40)
    print("\nSuggested names:")
    print("1. cyberwatch-ai")
    print("2. netguard-ml")
    print("3. packet-sentinel")
    print("4. neural-netops")
    print("5. threatwave-sim")
    print("6. aidefender-net")
    print("7. quantum-soc")
    print("8. packet-prophet")
    print("9. netbrain-sim")
    print("10. cyber-cortex")
    print("\nOr enter your own name (lowercase with dashes)")
    
    choice = input("\nEnter number (1-10) or custom name: ").strip()
    
    name_map = {
        "1": "cyberwatch-ai",
        "2": "netguard-ml",
        "3": "packet-sentinel",
        "4": "neural-netops",
        "5": "threatwave-sim",
        "6": "aidefender-net",
        "7": "quantum-soc",
        "8": "packet-prophet",
        "9": "netbrain-sim",
        "10": "cyber-cortex"
    }
    
    if choice in name_map:
        new_name = name_map[choice]
    else:
        new_name = choice.lower().replace(" ", "-")
    
    if new_name and new_name != "ai-network-simulator":
        confirm = input(f"\nRename to '{new_name}'? (y/n): ").lower()
        if confirm == 'y':
            rename_project(new_name)
        else:
            print("Rename cancelled.")
    else:
        print("Invalid name or same as current name.")