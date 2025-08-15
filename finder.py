import os
import shutil
import pyperclip
from termcolor import colored

def copy_to_clipboard(text):
    """Copy the provided text to the clipboard."""
    pyperclip.copy(text)

def find_software_path(software_name):
    """Search for software path based on the user's command and copy it to clipboard."""
    
    # Replace spaces with hyphens in the software name from the command
    software_name = software_name.replace(' ', '-').lower()

    # Define common directories where programs might be installed (Windows example)
    common_paths = [
        os.environ.get("PROGRAMFILES", ""),          # C:\Program Files
        os.environ.get("PROGRAMFILES(X86)", ""),     # C:\Program Files (x86)
        os.environ.get("LOCALAPPDATA", ""),          # C:\Users\<User>\AppData\Local
        os.environ.get("APPDATA", ""),               # C:\Users\<User>\AppData\Roaming
        os.environ.get("WINDIR", ""),                # C:\Windows
    ]
    
    # Try finding the software using `shutil.which()` to check system PATH
    try:
        
        def write_to_config(key, value):
            import json
            config_file = 'config.json'
            
            try:
                # Load the current contents of config.json
                try:
                    with open(config_file, 'r') as file:
                        config_data = json.load(file)
                except FileNotFoundError:
                    config_data = {}  # If file doesn't exist, start with an empty dictionary
                
                # Update the dictionary with the new key-value pair
                config_data[key] = value
                
                # Write the updated data back to config.json
                with open(config_file, 'w') as file:
                    json.dump(config_data, file, indent=4)
                
                return f"Key '{key}' with value '{value}' added to config.json."

            except json.JSONDecodeError:
                return "Error reading or decoding config.json."
            except Exception as e:
                return f"An error occurred: {str(e)}"

        path = shutil.which(software_name)
        if path:
            copy_to_clipboard(path)
            return f"Software '{software_name}' found at: {path}"

        # If not found via `which`, manually search common installation paths
        for base_path in common_paths:
            if not base_path:
                continue
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if software_name.lower() in file.lower():
                        software_path = os.path.join(root, file)
                        copy_to_clipboard(software_path)
                        result = write_to_config(software_name, software_path)
                        return software_name , software_path

        return colored (f"Software '{software_name}' not found on this system." , "red")

    except Exception as e:
        return f"Error finding software: {str(e)}"


# Example usage:
while True:
    command = input (colored("\nEnter software (none to exit): " , "yellow"))
    if command == 'none':
        break
    result = find_software_path(command)
    print("Software" , end="")
    print ( colored(f"'{result[0]}'" , "blue"))
    print("Found at " , end="")
    print ( colored(f"{result[-1]}" , "green"))
