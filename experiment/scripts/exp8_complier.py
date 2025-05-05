import subprocess
from utils import parse_output_std
import os
import shutil


current_dir = os.path.dirname(__file__)


DISTINATION = os.path.join(current_dir, "../result/exp8_complier")

os.makedirs(DISTINATION, exist_ok=True)

RESULT_PATH = os.path.join(DISTINATION, "result.json")

if os.path.isfile(RESULT_PATH):
    if input("result exist, re-run will cover the previous result. Still run? (y/n) ").lower() == "y":
        os.remove(RESULT_PATH)
        print(f"emptied {RESULT_PATH}")
    else:
        exit(0)

executables = [
    os.path.join(current_dir, "../../algorithms/executable/loglog"),
    os.path.join(current_dir, "../../algorithms/executable/loglog_O1"),
    os.path.join(current_dir, "../../algorithms/executable/loglog_O2"),
    os.path.join(current_dir, "../../algorithms/executable/loglog_O3"),
    os.path.join(current_dir, "../../algorithms/executable/PCSA_O0"),
    os.path.join(current_dir, "../../algorithms/executable/PCSA_O1"),
    os.path.join(current_dir, "../../algorithms/executable/PCSA_O2"),
    os.path.join(current_dir, "../../algorithms/executable/PCSA_O3"),
    os.path.join(current_dir, "../../algorithms/executable/hyperloglog_O0"),
    os.path.join(current_dir, "../../algorithms/executable/hyperloglog_O1"),
    os.path.join(current_dir, "../../algorithms/executable/hyperloglog_O2"),
    os.path.join(current_dir, "../../algorithms/executable/hyperloglog_O3"),
]


parameter_sets = [
    (64, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_100.txt")),
    # (64, "3065243", os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_40.txt")),
    # (64, "5487661", os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    # (64, "6737002", os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_80.txt")),
    # (64, "8569683", os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_100.txt")),
]

results = {}

for num, text in parameter_sets:
    print("procesing: ", text)
    

    for exe in executables:
        exe_name = exe.split("/")[-1]
        if "_" in exe_name:
            algorithm, opt_level = exe_name.split("_")
        else:
            algorithm = exe_name
            opt_level = "O0"
        print(f"running algorithm: {algorithm} {opt_level}")
        try:
            # Run the executable with parameters
            # print(exe, str(num), "cpp_hash", "1337", text) 
            completed = subprocess.run(
                [exe, str(num), "cpp_hash", "1337", text],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = completed.stdout.strip().splitlines()

            # print(output)
            
            # Initialize parsed values
            time_val, cardinality_val, memory_val, thread_val = parse_output_std(output)
            
            if None in (time_val, cardinality_val, memory_val):
                raise ValueError(f"Missing output in {exe} for parameters {num}, {text}")

            if algorithm not in results:
                results[algorithm] = {}
            
            results[algorithm][opt_level] = {
                "FM addBatch time": time_val,
                "Estimated cardinality": cardinality_val,
                "Memory usage": memory_val,
                "Threads used": thread_val
            }
            # print(results)

        except subprocess.CalledProcessError as e:
            print(f"Error running {exe} with parameters {num}, {text}: {e}")
        except Exception as e:
            print(f"Parsing error for {exe} with parameters {num}, {text}: {e}")

# You can print or save the results
import json
with open(RESULT_PATH, 'w') as f:
    json.dump(results, f, indent=2)