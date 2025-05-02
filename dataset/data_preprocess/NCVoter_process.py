import os
import shutil
from utils.profile_dataset import profile_folder

# Set your target folder
FOLDER_FOLDER = '../raw/NCVoters'
DISTINATION = '../cleaned/NCVoters'

if os.path.isdir(DISTINATION):
    shutil.rmtree(DISTINATION)
    print(f"emptied {DISTINATION}")

os.makedirs(DISTINATION, exist_ok=True)

def extract_third_elements(file_path, output_path):
    print(f"processing: {file_path}")
    with open(file_path, 'rb') as infile:
        lines = infile.readlines()[1:]  # Skip the first line

    third_elements = []
    for line in lines:
        parts = line.strip().split()
        
        if len(parts) >= 3:
            part2 = parts[2].decode('ascii').strip('"')
            # print(type(part2))
            # input(part2)
            
            if part2 != 'HANOVER':
                third_elements.append(part2)  # Index 2 is the third element

    with open(output_path, 'a') as outfile:
        outfile.write('\n'.join(third_elements))


# Loop through all .zip files in the folder
for i in range(0, 100):
    file_path = os.path.join(FOLDER_FOLDER, f'ncvoter{i+1}/ncvoter{i+1}.txt')
    output_file_path = os.path.join(DISTINATION, f"ncvoter{i+1}.txt")
    if os.path.isfile(file_path):
        extract_third_elements(file_path, output_file_path)

# Profile the folder
profile_folder(DISTINATION)
print("Done profiling.")

# Create a flag file to indicate completion
with open(os.path.join(DISTINATION, "flag"), 'a') as flagfile:
    flagfile.write("1")

print("DONE!")
        
