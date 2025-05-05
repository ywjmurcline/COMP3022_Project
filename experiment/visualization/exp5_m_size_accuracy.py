import matplotlib.pyplot as plt
import json
import os
from utils import get_ground_truth, get_size, mean_error_std
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


EXP_NAME = "exp5_m_size_accuracy"

current_dir = os.path.dirname(__file__)



def plot_error_std_heatmap(data, FIGURE_PATH):
    """
    Parameters:
        data (dict of dicts): data[m][size] = [error, std]
    """
    # Get sorted unique keys
    m_values = sorted(data.keys())
    size_values = sorted({size for m in data for size in data[m]})

    # Create matrices
    abs_error_matrix = np.zeros((len(m_values), len(size_values)))
    label_matrix = [['' for _ in size_values] for _ in m_values]

    for i, m in enumerate(m_values):
        for j, size in enumerate(size_values):
            if size in data[m]:
                error, std = data[m][size]
                abs_error_matrix[i][j] = abs(error)
                label_matrix[i][j] = f"{error:.2f}\n±{std:.2f}"
            else:
                abs_error_matrix[i][j] = np.nan
                label_matrix[i][j] = ""

    # Plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(abs_error_matrix, annot=label_matrix, fmt='', cmap="GnBu", cbar_kws={'label': 'Absolute Error'}, linewidths=.5, linecolor='white', square=True)

    plt.xticks(ticks=np.arange(len(size_values)) + 0.5, labels=size_values)
    plt.yticks(ticks=np.arange(len(m_values)) + 0.5, labels=m_values, rotation=0)
    plt.xlabel("Size")
    plt.ylabel("m")
    plt.title("Heatmap of Error ± Std (Bluer = Larger Abs Error)")
    plt.tight_layout()
    plt.savefig(FIGURE_PATH, dpi=300, bbox_inches='tight')
    plt.show()




def show_algo(algorithm_name):

    JSON_PATH = os.path.join(current_dir, f"../result/{EXP_NAME}/result_{algorithm_name}.json")
    FIGURE_PATH = os.path.join(current_dir, f"../result/{EXP_NAME}/{EXP_NAME}_{algorithm_name}.png")

    with open(JSON_PATH , 'r') as file:
        results = json.load(file)

    data = {}

    for m, value in results.items():
        data[int(m)] = {}
        for data_path, sub_value in value.items():
            truth = get_ground_truth(data_path)
            size = get_size(data_path)
            estimate = []
            last = None
            for trial, sub_value2 in sub_value.items():
                estimate.append(sub_value2["Estimated cardinality"])
            mean, error, std = mean_error_std(truth, estimate)

            data[int(m)][size] = [error, std]

    print(data)

    # Call the function to plot
    plot_error_std_heatmap(data, FIGURE_PATH)


# show_algo("hyperloglog")
show_algo("PCSA_O1")