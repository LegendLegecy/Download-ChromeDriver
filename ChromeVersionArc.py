# GET CHROME VERSIION , WINDOW ARC LIKE 64 BIT AND DOWNLOAD CHROME DRIVER AND MOVE TO PARENT DIRECTORY.

import os
import requests
import zipfile
import shutil
import subprocess
import platform
import json

def get_chrome_version():
    try:
        # Command to get Chrome version
        result = subprocess.run(
            ['reg', 'query', r'HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon', '/v', 'version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "version" in line:
                    return line.split()[-1]
    except Exception as e:
        print(f"Error fetching Chrome version: {e}")
    return None

def is_64bit_windows():
    return platform.architecture()[0] == "64bit"

def save_to_database(data, file_path="DATABASE.JSON"):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving data to file: {e}")

def download_chromedriver(major_version, dest_dir):
    try:
        # Construct the new URL format
        arch = "win32" if not is_64bit_windows() else "win64"
        base_url = "https://storage.googleapis.com/chrome-for-testing-public"
        driver_url = f"{base_url}/{major_version}/{arch}/chromedriver-{arch}.zip"
        
        print(f"Downloading ChromeDriver from: {driver_url}")
        response = requests.get(driver_url, stream=True)
        
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            zip_path = os.path.join(dest_dir, "chromedriver.zip")
            with open(zip_path, "wb") as file:
                downloaded_size = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        progress = (downloaded_size / total_size) * 100
                        print(f"\rDownload progress: {progress:.2f}%", end="")
            print("\nDownload complete. Extracting...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(dest_dir)
            os.remove(zip_path)
            print("ChromeDriver is ready.")
        else:
            print(f"Failed to download ChromeDriver. HTTP Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error downloading ChromeDriver: {e}")

def move_chromedriver():
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Define the path to chromedriver.exe
    chromedriver_dir = next((os.path.join(current_dir, d) for d in os.listdir(current_dir) if "chromedriver" in d and os.path.isdir(os.path.join(current_dir, d))), None)
    if not chromedriver_dir:
        raise FileNotFoundError("No directory containing 'chromedriver' found in the current directory.")
    chromedriver_path = os.path.join(chromedriver_dir, "chromedriver.exe")
    
    # Define the destination path (parent directory)
    destination_path = os.path.join(current_dir, "chromedriver.exe")
    
    # Check if chromedriver.exe exists
    if os.path.exists(chromedriver_path):
        # Move chromedriver.exe to the parent directory
        shutil.move(chromedriver_path, destination_path)
        shutil.rmtree(chromedriver_path.split("\\")[-2])
        print(f"Moved chromedriver.exe to {destination_path}")
    else:
        print("chromedriver.exe not found in the chromedriver directory.")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chrome_version = get_chrome_version()
    windows_architecture = "64-bit" if is_64bit_windows() else "32-bit"
    if chrome_version:
        print(f"Detected Chrome version: {chrome_version}")
        print(f"Detected Windows architecture: {windows_architecture}")
        download_chromedriver(chrome_version, current_dir)
        move_chromedriver()
        save_to_database({"chrome_version": chrome_version, "windows_architecture": windows_architecture})
    else:
        print("Could not detect Chrome version. Please ensure Chrome is installed.")