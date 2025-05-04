import subprocess
from utils import parse_output_std
import os
import shutil


current_dir = os.path.dirname(__file__)


DISTINATION = os.path.join(current_dir, "../result/exp9_para")

os.makedirs(DISTINATION, exist_ok=True)

RESULT_PATH = os.path.join(DISTINATION, "result.json")

if os.path.isfile(RESULT_PATH):
    if input("result exist, re-run will cover the previous result. Still run? (y/n) ").lower() == "y":
        os.remove(RESULT_PATH)
        print(f"emptied {RESULT_PATH}")
    else:
        exit(0)

executables = [
    os.path.join(current_dir, "../../algorithms/executable/AMS_para"),
    os.path.join(current_dir, "../../algorithms/executable/FM_para"),
]


parameter_sets = [
    (64, 1, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 2, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 3, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 4, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 5, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 6, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 7, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 8, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 9, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 10, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 11, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 12, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 13, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, 14, os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),

]

results = {}



for num, para, text in parameter_sets:
    print("procesing: ", text)

    for exe in executables:
        exe_name = exe.split("/")[-1]
        algorithm, opt_level = exe_name.split("_")
        print(f"running algorithm: {exe_name}")
        try:
            # Run the executable with parameters
            # print(exe, str(num), "cpp_hash", str(para), "1337", text)
            completed = subprocess.run(
                [exe, str(num), "cpp_hash", str(para), "1337", text],
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
            
            results[algorithm][para] = {
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