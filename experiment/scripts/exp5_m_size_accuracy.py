import subprocess
from utils import parse_output_std, parse_output_bucket
import os
import shutil

# You can print or save the results
import json

current_dir = os.path.dirname(__file__)

DISTINATION = os.path.join(current_dir, "../result/exp5_m_size_accuracy")

os.makedirs(DISTINATION, exist_ok=True)

parameter_sets = [
    (4, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_1.txt")),
    (4, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_2.txt")),
    (4, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_3.txt")),
    (4, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_4.txt")),
    (4, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_5.txt")),
    (4, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_6.txt")),
    (4, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_7.txt")),
    (8, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_1.txt")),
    (8, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_2.txt")),
    (8, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_3.txt")),
    (8, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_4.txt")),
    (8, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_5.txt")),
    (8, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_6.txt")),
    (8, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_7.txt")),
    (16, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_1.txt")),
    (16, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_2.txt")),
    (16, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_3.txt")),
    (16, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_4.txt")),
    (16, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_5.txt")),
    (16, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_6.txt")),
    (16, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_7.txt")),
    (32, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_1.txt")),
    (32, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_2.txt")),
    (32, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_3.txt")),
    (32, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_4.txt")),
    (32, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_5.txt")),
    (32, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_6.txt")),
    (32, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_7.txt")),
    (64, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_1.txt")),
    (64, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_2.txt")),
    (64, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_3.txt")),
    (64, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_4.txt")),
    (64, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_5.txt")),
    (64, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_6.txt")),
    (64, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_7.txt")),
    (128, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_1.txt")),
    (128, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_2.txt")),
    (128, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_3.txt")),
    (128, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_4.txt")),
    (128, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_5.txt")),
    (128, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_6.txt")),
    (128, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_7.txt")),
    (256, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_1.txt")),
    (256, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_2.txt")),
    (256, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_3.txt")),
    (256, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_4.txt")),
    (256, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_5.txt")),
    (256, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_6.txt")),
    (256, "cpp_hash", os.path.join(current_dir, "../../dataset/cleaned/IPs_chunk/IPs_chunk_7.txt")),
]




def algorithm(algo_name):

    RESULT_PATH = os.path.join(DISTINATION, f"result_{algo_name}.json")

    if os.path.isfile(RESULT_PATH):
        if input("result exist, re-run will cover the previous result. Still run? (y/n) ").lower() == "y":
            os.remove(RESULT_PATH)
            print(f"emptied {RESULT_PATH}")
        else:
            exit(0)

    executables = [
        os.path.join(current_dir, f"../../algorithms/executable/{algo_name}"),
    ]


    results = {}

    REPEAT = 20


    for num, hash, text in parameter_sets:
        print("procesing: ", text)
        datapath = os.path.abspath(text)

        for i in range(REPEAT):
            print("repeat: ", i)
            seed = str(i)
            for exe in executables:
                exe_name = exe.split("/")[-1]
                print(f"running algorithm: {exe_name}")

                try:
                    # Run the executable with parameters
                    # print(exe, str(num), "cpp_hash", str(para), "1337", text)
                    completed = subprocess.run(
                        [exe, str(num), hash, seed, text],
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

                    if num not in results:
                        results[num] = {}
                    if datapath not in results[num]:
                        results[num][datapath] = {}

                    results[num][datapath][i] = {
                        "exe_name": exe_name,
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

                
                

    with open(RESULT_PATH, 'w') as f:
        json.dump(results, f, indent=2)

algorithm("hyperloglog")
algorithm("PCSA_O1")