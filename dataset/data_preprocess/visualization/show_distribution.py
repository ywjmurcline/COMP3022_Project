import json
import os
from collections import Counter
import matplotlib.pyplot as plt
import sys




def process_json_directory(directory_path, dataset_name):

    # Initialize an empty list to collect all data
    all_data = []
    
    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            
            try:
                # Read the JSON file
                with open(file_path, 'r') as file:
                    data = json.load(file)
                
                # Extract values from keys starting with "data_"
                for key, value in data.items():
                    if key.startswith("data_"):
                        # Handle both single values and lists
                        if isinstance(value, list):
                            all_data.extend(value)
                        else:
                            all_data.append(value)
            
            except (json.JSONDecodeError, PermissionError) as e:
                print(f"Error processing {filename}: {e}")
                continue

    # Open and read the JSON file
    with open(profile_json, 'r') as file:
        data = json.load(file)

    total_lines = data["total"]["total"]

    
    # Calculate frequency if we found any data
    if all_data:
        frequency = Counter(all_data)
        
        # Sort by frequency (descending) for better visualization
        sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        labels, values = zip(*sorted_freq)
        
        # Create the bar chart
        plt.figure(figsize=(12, 6))
        bars = plt.bar(labels, values)
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            # plt.text(bar.get_x() + bar.get_width()/2., height,
            #         f'{height}',
            #         ha='center', va='bottom')
        
        plt.xlabel('Items')
        plt.ylabel('Frequency')
        plt.title(f'Frequency of Items from {dataset_name}')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
        # Also print the frequency table
        print("\nFrequency Table:")
        print("----------------")
        for item, count in sorted_freq:
            print(f"{item}: {count}")
    else:
        print("No data found in any JSON files from keys starting with 'data_'")



if len(sys.argv) < 3:
    print("Usage: python script_a.py <argument>")
    sys.exit(1)

directory_path = sys.argv[1]
dataset_name = sys.argv[2]
print(f"Received argument: {directory_path} {dataset_name}")



process_json_directory(directory_path, dataset_name)