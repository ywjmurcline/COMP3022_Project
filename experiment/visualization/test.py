import matplotlib.pyplot as plt
import seaborn as sns

# Example mock result for demonstration
# Replace this with your actual processed dictionary from extract_estimated_cardinalities
example_data = {
    "4": [1.15, 1.20, 1.18],
    "8": [2.10, 2.05, 2.15],
    "16": [4.00, 3.95, 4.10],
}

# Simulated ground truth function (replace this with your actual function)
def get_ground_truth(data_path):
    # Example mock ground truth, adjust logic as needed
    return 4.0

# Plotting function
def plot_cardinality_boxplot(data_dict, ground_truth_value):
    # Prepare data for plotting
    data_for_plot = []
    for m_value, estimates in data_dict.items():
        for est in estimates:
            data_for_plot.append({'m': m_value, 'Estimated Cardinality': est})

    df_plot = sns.load_dataset("tips")  # workaround to ensure seaborn is initialized properly
    df_plot = df_plot.iloc[0:0]  # clear it
    import pandas as pd
    df_plot = pd.DataFrame(data_for_plot)

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_plot, x='m', y='Estimated Cardinality', palette="Set2")
    plt.axhline(ground_truth_value, color='red', linestyle='--', label=f'Ground Truth: {ground_truth_value}')
    plt.title("Estimated Cardinality by m")
    plt.xlabel("m")
    plt.ylabel("Estimated Cardinality")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# Example usage with mock data and a fixed ground truth
plot_cardinality_boxplot(example_data, ground_truth_value=4.0)
