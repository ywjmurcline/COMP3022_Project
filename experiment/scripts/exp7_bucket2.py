import subprocess
from utils import parse_output_std, parse_output_bucket
import os
import shutil


current_dir = os.path.dirname(__file__)


DISTINATION = os.path.join(current_dir, "../result/exp7_bucket")

os.makedirs(DISTINATION, exist_ok=True)

RESULT_PATH = os.path.join(DISTINATION, "result_mix.json")

if os.path.isfile(RESULT_PATH):
    if input("result exist, re-run will cover the previous result. Still run? (y/n) ").lower() == "y":
        os.remove(RESULT_PATH)
        print(f"emptied {RESULT_PATH}")
    else:
        exit(0)

executables = [
    os.path.join(current_dir, "../../algorithms/executable/PCSA_mixhash"),
    os.path.join(current_dir, "../../algorithms/executable/hyperloglog_mixhash")
]


parameter_sets = [
    (64, "fnv1a", "murmurhash2", os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, "fnv1a", "linearhash", os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, "fnv1a", "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, "murmurhash2", "fnv1a", os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, "linearhash", "fnv1a", os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
    (64, "cpp_hash", "fnv1a", os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")),
]


results = {}

REPEAT = 10


for num, hash1, hash2, text in parameter_sets:
    print("procesing: ", text)

    for i in range(REPEAT):
        print("repeat: ", i)
        seed = str(i)
        hash_key = f"{hash1}_{hash2}"
        for exe in executables:
            exe_name = exe.split("/")[-1]
            print(f"running algorithm: {exe_name}")

            try:
                # Run the executable with parameters
                # print(exe, str(num), "cpp_hash", str(para), "1337", text)
                completed = subprocess.run(
                    [exe, str(num), hash1, hash2, seed, text],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                output = completed.stdout.strip().splitlines()

                # print(output)
                
                # Initialize parsed values
                time_val, cardinality_val, memory_val, thread_val, bucket_count = parse_output_bucket(output)
                
                if None in (time_val, cardinality_val, memory_val):
                    raise ValueError(f"Missing output in {exe} for parameters {num}, {text}")

                if exe_name not in results:
                    results[exe_name] = {}
                if hash_key not in results[exe_name]:
                    results[exe_name][hash_key] = {}

                results[exe_name][hash_key][i] = {
                    "FM addBatch time": time_val,
                    "Estimated cardinality": cardinality_val,
                    "Memory usage": memory_val,
                    "Threads used": thread_val,
                    "Bucket counts": bucket_count,
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