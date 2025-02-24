import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import networkx as nx
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Load the CSV files
drug_targets_file = "Drug_targets_tool.csv"
mamestra_file = "Mamestra_b_160124_combined_final.csv"

# Read CSV files
drug_targets_df = pd.read_csv(drug_targets_file)
mamestra_df = pd.read_csv(mamestra_file)

# Extract relevant information from the first column of drug_targets_df
drug_targets_df[['Entry', 'Human Target']] = drug_targets_df.iloc[:, 0].str.split('|', expand=True)

# Merge on the Entry column to find matches
merged_df = drug_targets_df.merge(mamestra_df, left_on='Entry', right_on='Entry', how='inner')

# Select relevant columns for visualization
final_df = merged_df[['Entry', 'Human Target', 'Drug(s)', 'GeneID', 'Tissue', 'E_value', 'Isoform_Count', 'Gene_Count', 'Gene.Ontology..GO.']]

# Rank sensitivity based on Gene_Count (lower count -> more sensitive)
final_df['Sensitivity_Rank'] = final_df['Gene_Count'].rank(method='dense', ascending=True)

# Set up argument parsing
parser = argparse.ArgumentParser(description="Search and display drug targets with multiple analysis options")
parser.add_argument("-drug", type=str, help="Filter results by drug name (case insensitive)", default=None)
parser.add_argument("-tissue", type=str, help="Filter results by tissue type", default=None)
parser.add_argument("-network", action="store_true", help="Construct drug-target interaction network and visualize metrics")
parser.add_argument("-rank", action="store_true", help="Rank most sensitive drug targets")
args = parser.parse_args()

# Apply filtering based on user input
if args.drug:
    final_df = final_df[final_df['Drug(s)'].str.contains(args.drug, case=False, na=False)]
if args.tissue:
    final_df = final_df[final_df['Tissue'].str.contains(args.tissue, case=False, na=False)]

# Save the results to a CSV and TSV file
output_csv = "Mapped_Drug_Targets_in_Mamestra.csv"
output_tsv = "Mapped_Drug_Targets_in_Mamestra.tsv"
final_df.to_csv(output_csv, index=False)
final_df.to_csv(output_tsv, index=False, sep='\t')

# Rank most sensitive drug targets if requested
if args.rank:
    print("\nRanking most sensitive drug targets...")
    ranked_df = final_df.sort_values(by='Sensitivity_Rank')
    ranked_df.to_csv("Ranked_Sensitive_Drug_Targets.csv", index=False)
    print("Ranked sensitive drug targets saved to 'Ranked_Sensitive_Drug_Targets.csv'")
    print(tabulate(ranked_df, headers='keys', tablefmt='fancy_grid'))

# Display results in an elegant tabular format
print(tabulate(final_df, headers='keys', tablefmt='fancy_grid'))

# Optional: Create a summary report
print(f"\nTotal matched drug targets: {len(final_df)}")
print(f"Results saved to {output_csv} and {output_tsv}")

# === Tissue Distribution Boxplot ===
plt.figure(figsize=(12, 6))
sns.boxplot(data=final_df, x='Tissue', y='Gene_Count')
plt.xticks(rotation=30)
plt.title("Gene Count Distribution Across Different Tissues")
plt.xlabel("Tissue Type")
plt.ylabel("Gene Count")
plt.savefig("Gene_Count_Tissue_Distribution.png", bbox_inches='tight')
print("Tissue distribution plot saved as 'Gene_Count_Tissue_Distribution.png'")

# === NETWORK ANALYSIS AND VISUALIZATION ===
if args.network:
    print("\nConstructing Drug-Target Interaction Network...")

    G = nx.Graph()
    primary_targets = set()
    drug_nodes = set()

    # Create nodes and edges
    for _, row in final_df.iterrows():
        drugs = row['Drug(s)'].split(', ')
        target = row['Entry']
        primary_targets.add(target)

        for drug in drugs:
            G.add_edge(drug, target, type='drug-target')  # Direct drug-target connection
            drug_nodes.add(drug)  # Store drug nodes separately

    # Add target-to-target interactions
    for target1 in primary_targets:
        for target2 in primary_targets:
            if target1 != target2:  # Avoid self-loops
                G.add_edge(target1, target2, type='target-target')  # Target-to-target interaction

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)

    # Assign colors
    node_colors = ['red' if node in drug_nodes else 'green' for node in G.nodes()]
    edge_styles = ['solid' if G[u][v]['type'] == 'drug-target' else 'dashed' for u, v in G.edges()]

    # Draw edges with different styles
    for edge, style in zip(G.edges(), edge_styles):
        nx.draw_networkx_edges(G, pos, edgelist=[edge], style=style, edge_color='black')

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700, edgecolors='black')

    # Draw labels with increased font size
    # Increase padding for better spacing
    plt.margins(0.2)  # Adds extra space around the plot to avoid cutoff

    # Adjust label positions dynamically
    label_pos = {node: (x, y + 0.05) for node, (x, y) in pos.items()}  # Moves labels slightly up
    nx.draw_networkx_labels(G, label_pos, font_size=10, font_weight='bold', verticalalignment='bottom')


    # Create custom legend
    from matplotlib.patches import Patch
    legend_handles = [
        Patch(color='red', label='Drug'),
        Patch(color='green', label='Target'),
        Patch(color='black', linestyle='solid', label='Drug-Target Interaction'),
        Patch(color='black', linestyle='dashed', label='Target-Target Interaction')
    ]
    plt.legend(handles=legend_handles, loc='upper right', fontsize=10, frameon=True)

        # Dynamically update title with queried drug name
    queried_drug = args.drug if args.drug else "All Drugs"
    plt.title(f"Drug-Target Interaction Network ({queried_drug})", fontsize=14, fontweight='bold')

#plt.title("Drug-Target Interaction Network", fontsize=14, fontweight='bold')
    plt.savefig("Drug_Target_Network.png", bbox_inches='tight')
    print("Network plot saved as 'Drug_Target_Network.png'")

