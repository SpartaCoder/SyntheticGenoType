"""
Synthetic Multi-Gene Family Genotype Dataset Generator

This script simulates genotypes for families with multiple genes and generates child genotypes based on Mendelian inheritance.
It produces a CSV file with the full dataset and visualizes the genotype distribution for one gene.

Libraries Used:
- random: For simulating genotype inheritance via random allele selection.
- pandas: For data manipulation and DataFrame operations.

Parameters and Variables:
- genes: List of gene names simulated in the dataset.
- genotypes: Possible genotypes per gene ('AA', 'Aa', 'aa').
- num_families: Number of families to simulate.
- children_per_family: Number of children per family.
"""

import random  # Used for random genotype and allele selection
import pandas as pd  # Used for DataFrame creation and CSV export

# ----- PARAMETERS -----
genes = ['Gene1', 'Gene2', 'Gene3']              # Genes to simulate
genotypes = ['AA', 'Aa', 'aa']                   # Possible genotypes for each gene
num_families = 100                               # Number of families to generate
children_per_family = 3                          # Number of children per family

# ----- GENOTYPE GENERATION FUNCTIONS -----
def generate_parent_genotypes():
    """Randomly assign a genotype for each gene to a parent."""
    return {gene: random.choice(genotypes) for gene in genes}

def get_alleles(genotype):
    """Split genotype string into its alleles (e.g. 'Aa' -> ['A', 'a'])."""
    return list(genotype)

def simulate_child_genotype(p1_geno, p2_geno):
    """
    Simulate child genotype by randomly inheriting one allele from each parent,
    then sorting alleles to standardize genotype notation.
    """
    allele1 = random.choice(get_alleles(p1_geno))
    allele2 = random.choice(get_alleles(p2_geno))
    return ''.join(sorted([allele1, allele2]))

def get_phenotype(genotype):
    """Return phenotype classification based on genotype ('Dominant' if contains 'A', else 'Recessive')."""
    return 'Dominant' if 'A' in genotype else 'Recessive'

# ----- GENERATE PARENT GENOTYPES -----
parent1_data = [generate_parent_genotypes() for _ in range(num_families)]
parent2_data = [generate_parent_genotypes() for _ in range(num_families)]

df_families = pd.DataFrame({
    'Family_ID': range(1, num_families + 1),
    'Parent1': parent1_data,
    'Parent2': parent2_data
})

# ----- SIMULATE CHILDREN GENOTYPES -----
children_records = []

for idx, row in df_families.iterrows():
    family_id = row['Family_ID']
    parent1 = row['Parent1']
    parent2 = row['Parent2']

    for child_num in range(1, children_per_family + 1):
        child_data = {'Family_ID': family_id, 'Child_ID': f'Child{child_num}'}

        for gene in genes:
            # Simulate child genotype for each gene
            child_geno = simulate_child_genotype(parent1[gene], parent2[gene])
            child_data[f'{gene}_Genotype'] = child_geno
            child_data[f'{gene}_Phenotype'] = get_phenotype(child_geno)

        children_records.append(child_data)

df_children = pd.DataFrame(children_records)

# ----- EXPAND PARENT GENOTYPE DATA -----
# Flatten parent genotype dictionaries into separate columns per gene
df_parents_expanded = pd.DataFrame({
    'Family_ID': df_families['Family_ID'],
    **{f'Parent1_{gene}': [p[gene] for p in parent1_data] for gene in genes},
    **{f'Parent2_{gene}': [p[gene] for p in parent2_data] for gene in genes}
})

# ----- MERGE CHILDREN AND PARENT DATA -----
df_full = pd.merge(df_children, df_parents_expanded, on='Family_ID')

# ----- SAVE AND VISUALIZE DATA -----
# Save full dataset to CSV
df_full.to_csv('multi_gene_family_genotypes.csv', index=False)

# Visualize distribution of Gene1 genotypes among children
df_full['Gene1_Genotype'].value_counts().plot(
    kind='bar',
    title='Gene1 Genotype Distribution (All Children)'
)
