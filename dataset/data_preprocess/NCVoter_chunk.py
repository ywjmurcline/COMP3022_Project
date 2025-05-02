import os
import shutil

# Set your target folder
FOLDER_FOLDER = '../cleaned/NCVoters'
DISTINATION = '../cleaned/NCVoters_chunk'

if os.path.isdir(DISTINATION):
    shutil.rmtree(DISTINATION)
    print(f"emptied {DISTINATION}")

os.makedirs(DISTINATION, exist_ok=True)


chunk_by = [
    [0, 20], 
    [0, 40], 
    [0, 60], 
    [0, 80], 
    [0, 100], 
    ]

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
for a, b in chunk_by:
    for i in range(a, b):
        file_path = os.path.join(FOLDER_FOLDER, f'ncvoter{i+1}.txt')
        output_file_path = os.path.join(DISTINATION, f"ncvoter_{a}_{b}.txt")
        if os.path.isfile(file_path):
            extract_third_elements(file_path, output_file_path)

with open(os.path.join(DISTINATION, "flag.txt"), 'a') as flagfile:
    flagfile.write("1")

print("DONE!")
        
