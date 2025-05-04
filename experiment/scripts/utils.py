import re

def parse_output_std(output):
    # Strict regex patterns
    time_pattern = re.compile(r'^FM addBatch time: ([0-9]+\.[0-9]+) seconds$')
    cardinality_pattern = re.compile(r'^Estimated cardinality: ([0-9]+\.[0-9]+)$')
    memory_pattern = re.compile(r'^Memory usage: ([0-9]+\.[0-9]+) MB$')
    thread_use = re.compile(r'^Number of threads used: ([0-9]+)$')

    time_val, cardinality_val, memory_val, thread_val = None, None, None, None
    # Parse output strictly line by line
    for line in output:
        # print(line)
        if time_match := time_pattern.match(line):
            time_val = float(time_match.group(1))
        elif card_match := cardinality_pattern.match(line):
            cardinality_val = float(card_match.group(1))
        elif mem_match := memory_pattern.match(line):
            memory_val = float(mem_match.group(1))
        elif thread_match := thread_use.match(line):
            thread_val = int(thread_match.group(1))

    return (time_val, cardinality_val, memory_val, thread_val)


def parse_output_bucket(output):
    # Strict regex patterns
    time_pattern = re.compile(r'^FM addBatch time: ([0-9]+\.[0-9]+) seconds$')
    cardinality_pattern = re.compile(r'^Estimated cardinality: ([0-9]+\.[0-9]+)$')
    memory_pattern = re.compile(r'^Memory usage: ([0-9]+\.[0-9]+) MB$')
    thread_use = re.compile(r'^Number of threads used: ([0-9]+)$')
    bucket_pattern = re.compile(r'^Bucket counts: (.+)', re.MULTILINE)

    time_val, cardinality_val, memory_val, thread_val, bucket_counts= None, None, None, None, None
    # Parse output strictly line by line
    for line in output:
        if time_match := time_pattern.match(line):
            time_val = float(time_match.group(1))
        elif card_match := cardinality_pattern.match(line):
            cardinality_val = float(card_match.group(1))
        elif mem_match := memory_pattern.match(line):
            memory_val = float(mem_match.group(1))
        elif thread_match := thread_use.match(line):
            thread_val = int(thread_match.group(1))
        elif bucket_match := bucket_pattern.search(line):
            # print(f"Bucket match: {bucket_match.group(1)}")
            # Extract bucket counts
            bucket_counts = list(map(int, bucket_match.group(1).split()))


    return (time_val, cardinality_val, memory_val, thread_val, bucket_counts)


# import numpy as np

# def compute_error_stats(ground_truth, estimations):
#     errors = np.array(estimations) - ground_truth
#     avg_error = np.mean(errors)
#     std_dev = np.std(errors)
#     return avg_error, std_dev

# def compute_entropy(ground_truth_file, estimations_file_name, estimations):
#     with open(ground_truth_file, 'r') as file:
#         ground_truth = file.read().splitlines()
#     with open(estimations_file, 'r') as file:
#         estimations = file.read().splitlines()

#     # Convert to numpy arrays for easier manipulation
#     ground_truth = np.array(ground_truth, dtype=float)
#     estimations = np.array(estimations, dtype=float)

#     # Compute entropy
#     total = len(estimations)
#     counts = np.bincount(estimations.astype(int))
#     entropy = -np.sum((counts / total) * np.log2(counts / total + 1e-10))  # Adding a small value to avoid log(0)

#     return entropy


