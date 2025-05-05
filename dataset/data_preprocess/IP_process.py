import os
import shutil
from utils.profile_dataset import profile_folder_by_file
import glob
import random

random.seed(42)  # Any fixed number
# print(random.randint(1, 100))
# print(random.random())


# Set your target folder
FOLDER_FOLDER = '../download/IPs'
DISTINATION = '../cleaned/IPs'

if os.path.isdir(DISTINATION):
    shutil.rmtree(DISTINATION)
    print(f"emptied {DISTINATION}")

os.makedirs(DISTINATION, exist_ok=True)

def extract_IP_addresses_1(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    ip1 = parts[1]
                    if ip1.count('.') == 3 and all(part.isdigit() for part in ip1.split('.')):
                        # Write the second and third elements to the output file
                        output_file.write(f"{ip1}\n")
                    ip2 = parts[3]
                    # Check if the third element is an IP address
                    if ip2.count('.') == 3 and all(part.isdigit() for part in ip2.split('.')):
                        # Write the second and third elements to the output file
                        output_file.write(f"{ip2}\n")


def extract_third_elements_2(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 1:
                    ip1 = parts[0]
                    if ip1.count('.') == 3 and all(part.isdigit() for part in ip1.split('.')):
                        # Write the second and third elements to the output file
                        output_file.write(f"{ip1}\n")
                    ip2 = parts[1]
                    # Check if the third element is an IP address
                    if ip2.count('.') == 3 and all(part.isdigit() for part in ip2.split('.')):
                        # Write the second and third elements to the output file
                        output_file.write(f"{ip2}\n")


input_files = glob.glob(os.path.join(FOLDER_FOLDER, '*.csv'))

# Loop through all .zip files in the folder
for input_file in input_files:
    # Get the base name of the file (without the directory path)
    base_name = os.path.basename(input_file)

    print(f"Processing {base_name}...")
    
    # Create the output file path
    output_file_path = os.path.join(DISTINATION, base_name.replace('.csv', '.txt'))

    if base_name == "Dataset-Unicauca-Version2-87Atts.csv":
        # Extract the third elements from the input file and write to the output file
        extract_IP_addresses_1(input_file, output_file_path)
    else:
        # Extract the third elements from the input file and write to the output file
        extract_third_elements_2(input_file, output_file_path)


# Profile the folder
print("Profiling the folder...")
profile_folder_by_file(DISTINATION)
print("Done profiling.")

# Create a flag file to indicate completion
with open(os.path.join(DISTINATION, "flag"), 'a') as flagfile:
    flagfile.write("1")

print("DONE!")
        
