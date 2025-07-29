import matplotlib.pyplot as plt

def plot_rankings(result_df, id_col='ID'):
    """
    Plot a horizontal bar chart of TOPSIS rankings.
    """
    plt.figure(figsize=(10, 6))
    sorted_df = result_df.sort_values(by='Rank')
    plt.barh(sorted_df[id_col], sorted_df['Topsis Score'], color='skyblue')
    plt.xlabel('TOPSIS Score')
    plt.ylabel(id_col)
    plt.title('TOPSIS Rankings')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
