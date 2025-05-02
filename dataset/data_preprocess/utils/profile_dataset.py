import os
import json

def profile_folder(folder, save=True):
    # Set your target folder
    TARGET_FOLDER = folder
    DISTINATION = os.path.join(folder, "profile.json")

    unique_el = {}
    total = 0
    unique = 0
    # Loop through all .zip files in the folder
    for filename in os.listdir(TARGET_FOLDER):
        if filename.endswith('.txt'):
            file_path = os.path.join(TARGET_FOLDER, filename)

            with open(file_path, 'rb') as infile:
                lines = infile.readlines()
                for line in lines:
                    l = str(line.decode("ascii")).strip("\n")
                    if l not in unique_el.keys():
                        unique_el[l] = 1
                        unique += 1
                    else:
                        unique_el[l] += 1
                    total += 1

    print(f"total: {total}\tunique: {unique}")      

    # Save the profile to a JSON file
    profile = {
        "total": total,
        "unique": unique,
    }
    if save:
        with open(DISTINATION, 'w') as outfile:
            json.dump(profile, outfile, indent=2)
        print(f"Profile saved to {DISTINATION}")
    return profile


def profile_folder_by_file(folder):
    # Set your target folder
    TARGET_FOLDER = folder
    DISTINATION = os.path.join(folder, "profile.json")


    profile = {}
    # Loop through all .zip files in the folder
    for filename in os.listdir(TARGET_FOLDER):
        if filename.endswith('.txt'):
            unique_el = {}
            total = 0
            unique = 0
            file_path = os.path.join(TARGET_FOLDER, filename)

            with open(file_path, 'rb') as infile:
                lines = infile.readlines()
                for line in lines:
                    l = str(line.decode("ascii")).strip("\n")
                    if l not in unique_el.keys():
                        unique_el[l] = 1
                        unique += 1
                    else:
                        unique_el[l] += 1
                    total += 1

            profile[filename] = {
                "total": total,
                "unique": unique,
            }
            print(f"{filename}: total: {total}\tunique: {unique}")

    profile["total"] = profile_folder(folder, save=False)
    


    with open(DISTINATION, 'w') as outfile:
        json.dump(profile, outfile, indent=2)
    print(f"Profile saved to {DISTINATION}")
    return profile