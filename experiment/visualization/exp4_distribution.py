import matplotlib.pyplot as plt
import json
import os
from utils import get_ground_truth, get_size, mean_error_std, get_entropy
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

EXP_NAME = "exp4_distribution"

current_dir = os.path.dirname(__file__)


JSON_PATH = os.path.join(current_dir, f"../result/{EXP_NAME}/result.json")
FIGURE_PATH1 = os.path.join(current_dir, f"../result/{EXP_NAME}/{EXP_NAME}_4.png")
FIGURE_PATH2 = os.path.join(current_dir, f"../result/{EXP_NAME}/{EXP_NAME}_256.png")

def plot_entropy_estimations(data, ground_truths, figure_path):
    """
    Plots box plots of estimation values for each entropy level.
    
    Parameters:
    - data: dict where data[entropy][m] = list of estimations (m is ignored)
    - ground_truths: dict mapping entropy (float) to its ground truth value
    """
    # Reformat data into a flat list for plotting
    plot_data = []
    for entropy, est_list in data.items():
        for est in est_list:
            plot_data.append({'entropy': round(entropy, 2), 'estimation': est})

    # Convert to DataFrame
    
    df = pd.DataFrame(plot_data)

    # Create the box plot
    plt.figure(figsize=(5, 5))
    sns.boxplot(x='entropy', y='estimation', data=df, palette="Set2")

    # Plot ground truth lines
    for entropy, gt in ground_truths.items():
        plt.axhline(y=gt, linestyle='--', color='black', linewidth=1, alpha=0.3)
        # plt.text(x=list(data.keys()).index(entropy), y=gt +5, s=f'GT={gt:.1f}', 
        #          color='black', ha='center', va='bottom', fontsize=12)
        break

    plt.title('Estimation Distribution by Entropy Level')
    plt.xlabel('Entropy')
    plt.ylabel('Estimated Cardinality')
    plt.tight_layout()
    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.show()




with open(JSON_PATH , 'r') as file:
    results = json.load(file)


ground_truths = {}

for key, value in results.items():
    if key == "4":
        data = {}
        for datapath, trials in value.items():
            # print(datapath)
            truth = get_ground_truth(datapath)
            entropy = get_entropy(datapath)
            data[entropy] = []
            ground_truths[entropy] = truth
            for trial_num, trail_result in trials.items():
                data[entropy].append(trail_result["Estimated cardinality"])

        print(data)

        plot_entropy_estimations(data, ground_truths, FIGURE_PATH1)

    elif key == "256":
        data = {}
        for datapath, trials in value.items():
            # print(datapath)
            truth = get_ground_truth(datapath)
            entropy = get_entropy(datapath)
            data[entropy] = []
            ground_truths[entropy] = truth
            for trial_num, trail_result in trials.items():
                data[entropy].append(trail_result["Estimated cardinality"])

        print(data)

        plot_entropy_estimations(data, ground_truths, FIGURE_PATH2)
