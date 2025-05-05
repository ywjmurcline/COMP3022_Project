import os
import json

def get_ground_truth(path):
    basename = os.path.basename(path)
    dirname = os.path.dirname(path)
    profile_path = os.path.join(dirname, "profile.json")
    if os.path.isfile(profile_path):
        with open(profile_path, 'r') as file:
            profile = json.load(file)
            return profile[basename]["unique"]
        
def get_size(path):
    basename = os.path.basename(path)
    dirname = os.path.dirname(path)
    profile_path = os.path.join(dirname, "profile.json")
    if os.path.isfile(profile_path):
        with open(profile_path, 'r') as file:
            profile = json.load(file)
            return profile[basename]["total"]

def get_entropy(path):
    basename = os.path.basename(path)
    dirname = os.path.dirname(path)
    entropy_path = os.path.join(dirname, "entropy.json")
    if os.path.isfile(entropy_path):
        with open(entropy_path, 'r') as file:
            profile = json.load(file)
            return profile[basename]
        
import numpy as np

def mean_error_std(truth, estimate):
    """
    Parameters:
        truth (float): The true value.
        estimate (list of float): List of estimated values.

    Returns:
        error (float): Absolute error between mean(estimate) and truth.
        std (float): Standard deviation within the estimate list.
    """
    estimate = np.array(estimate)
    mean = estimate.mean()
    error = mean - truth
    std = estimate.std(ddof=1)  # Sample standard deviation
    return mean.item(), error.item(), std.item()


