import re

def parse_output_std(output):
    # Strict regex patterns
    time_pattern = re.compile(r'^FM addBatch time: ([0-9]+\.[0-9]+) seconds$')
    cardinality_pattern = re.compile(r'^Estimated cardinality: ([0-9]+\.[0-9]+)$')
    memory_pattern = re.compile(r'^Memory usage: ([0-9]+\.[0-9]+) MB$')
    thread_use = re.compile(r'^Number of threads used: ([0-9]+)$')

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

    return (time_val, cardinality_val, memory_val, thread_val)