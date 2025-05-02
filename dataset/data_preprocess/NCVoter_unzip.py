import zipfile
import os
import shutil

# Set your target folder
ZIP_FOLDER = '../download/NCVoters'
DISTINATION = '../raw/NCVoters'

os.makedirs(DISTINATION, exist_ok=True)

# Loop through all .zip files in the folder
for filename in os.listdir(ZIP_FOLDER):
    if filename.endswith('.zip'):
        zip_path = os.path.join(ZIP_FOLDER, filename)
        extract_folder = os.path.join(DISTINATION, filename.strip(".zip"))  # Unzip into a folder named after the zip

        print(f"Extracting {filename} to {extract_folder}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            os.makedirs(extract_folder, exist_ok=True)
            zip_ref.extractall(extract_folder)

print("All ZIP files extracted.")

if input("Remove download?") == "y":
    shutil.rmtree(ZIP_FOLDER)
    print("All zip file deleted.")

