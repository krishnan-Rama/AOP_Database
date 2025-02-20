import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

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
final_df = merged_df[['Entry', 'Human Target', 'Drug(s)', 'GeneID', 'Tissue', 'E_value', 'Isoform_Count', 'Gene_Count']]

# Set up argument parsing
parser = argparse.ArgumentParser(description="Search and display drug targets")
parser.add_argument("-drug", type=str, help="Filter results by drug name (case insensitive)", default=None)
args = parser.parse_args()

# Filter data if a drug name is provided
if args.drug:
    final_df = final_df[final_df['Drug(s)'].str.contains(args.drug, case=False, na=False)]

# Save the results to a CSV and TSV file
output_csv = "Mapped_Drug_Targets_in_Mamestra.csv"
output_tsv = "Mapped_Drug_Targets_in_Mamestra.tsv"
final_df.to_csv(output_csv, index=False)
final_df.to_csv(output_tsv, index=False, sep='\t')

# Display results in an elegant tabular format
print(tabulate(final_df, headers='keys', tablefmt='fancy_grid'))

# Optional: Create a summary report
#print(f"\nTotal matched drug targets: {len(final_df)}")
#print(f"Results saved to {output_csv} and {output_tsv}")

# Normalization of Gene Count and Isoform Count for relative expression analysis
final_df['Normalized_Gene_Count'] = final_df['Gene_Count'] / final_df['Gene_Count'].max()
final_df['Normalized_Isoform_Count'] = final_df['Isoform_Count'] / final_df['Isoform_Count'].max()

# Advanced Visualization - Boxplot for Gene Count across Tissues
plt.figure(figsize=(12, 6))
sns.boxplot(x='Tissue', y='Gene_Count', data=final_df)
plt.xticks(rotation=45, ha='right')
plt.xlabel("Tissue Type")
plt.ylabel("Gene Count")
plt.title("Gene Count Distribution Across Different Tissues")
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("Gene_Count_Tissue_Distribution.png", bbox_inches='tight')
print("Plot saved as 'Gene_Count_Tissue_Distribution.png'")

# Normalized expression plots
plt.figure(figsize=(12, 6))
sns.boxplot(x='Tissue', y='Normalized_Gene_Count', data=final_df)
plt.xticks(rotation=45, ha='right')
plt.xlabel("Tissue Type")
plt.ylabel("Normalized Gene Count")
plt.title("Normalized Gene Count Across Different Tissues")
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("Normalized_Gene_Count_Distribution.png", bbox_inches='tight')
print("Plot saved as 'Normalized_Gene_Count_Distribution.png'")

plt.figure(figsize=(12, 6))
sns.boxplot(x='Tissue', y='Normalized_Isoform_Count', data=final_df)
plt.xticks(rotation=45, ha='right')
plt.xlabel("Tissue Type")
plt.ylabel("Normalized Isoform Count")
plt.title("Normalized Isoform Count Across Different Tissues")
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("Normalized_Isoform_Count_Distribution.png", bbox_inches='tight')
print("Plot saved as 'Normalized_Isoform_Count_Distribution.png'")
