import subprocess
import re

# Strict regex patterns
time_pattern = re.compile(r'^FM addBatch time: ([0-9]+\.[0-9]+) seconds$')
cardinality_pattern = re.compile(r'^Estimated cardinality: ([0-9]+\.[0-9]+)$')
memory_pattern = re.compile(r'^Memory usage: ([0-9]+\.[0-9]+) MB$')

executables = [
    "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/algorithms/executable/fm", 
    # "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/algorithms/executable/fm_para", 
    "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/algorithms/executable/PCSA", 
    "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/algorithms/executable/AMS", 
    # "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/algorithms/executable/AMS_para", 
    "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/algorithms/executable/hyperloglog"]

# Define your parameter sets here: (number, string)
parameter_sets = [
    (64, "1359916", "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/cleaned/NCVoters/ncvoter_1_20.txt"),
    (64, "3065243", "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/cleaned/NCVoters/ncvoter_1_40.txt"),
    (64, "5487661", "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/cleaned/NCVoters/ncvoter_1_60.txt"),
    (64, "6737002", "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/cleaned/NCVoters/ncvoter_1_80.txt"),
    (64, "8569683", "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/cleaned/NCVoters/ncvoter_all.txt"),
]

results = {}

for num, tag, text in parameter_sets:
    print(tag)

    param_key = f"{num}-{tag}"
    results[param_key] = {}
    
    for exe in executables:
        print(exe.split("/")[-1])
        try:
            # Run the executable with parameters
            completed = subprocess.run(
                [exe, str(num), text],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = completed.stdout.strip().splitlines()
            
            # Initialize parsed values
            time_val = cardinality_val = memory_val = None
            
            # Parse output strictly line by line
            for line in output:
                if time_match := time_pattern.match(line):
                    time_val = float(time_match.group(1))
                elif card_match := cardinality_pattern.match(line):
                    cardinality_val = float(card_match.group(1))
                elif mem_match := memory_pattern.match(line):
                    memory_val = float(mem_match.group(1))
            
            if None in (time_val, cardinality_val, memory_val):
                raise ValueError(f"Missing output in {exe} for parameters {num}, {text}")

            exe_name = exe.lstrip('./')
            results[param_key][exe_name] = {
                "FM addBatch time": time_val,
                "Estimated cardinality": cardinality_val,
                "Memory usage": memory_val
            }

        except subprocess.CalledProcessError as e:
            print(f"Error running {exe} with parameters {num}, {text}: {e}")
        except Exception as e:
            print(f"Parsing error for {exe} with parameters {num}, {text}: {e}")

# You can print or save the results
import json
with open('time.json', 'w') as f:
    json.dump(results, f, indent=2)
