# Step 1 Import libraries
import random
import pandas as pd

# Step 2 define parameters
# Define genes and genotypes
genes = ['Gene1', 'Gene2', 'Gene3']
genotypes = ['AA', 'Aa', 'aa']
num_families = 100
children_per_family = 3  # You can change this to any number

# Step 3 Genotypes
def generate_parent_genotypes():
    return {gene: random.choice(genotypes) for gene in genes}

# Create parent genotype dictionaries
parent1_data = [generate_parent_genotypes() for _ in range(num_families)]
parent2_data = [generate_parent_genotypes() for _ in range(num_families)]

# Combine into a DataFrame
df_families = pd.DataFrame({
    'Family_ID': range(1, num_families + 1),
    'Parent1': parent1_data,
    'Parent2': parent2_data
})

# Step 4 Children Genotypes
def get_alleles(genotype):
    return list(genotype)

def simulate_child_genotype(p1_geno, p2_geno):
    allele1 = random.choice(get_alleles(p1_geno))
    allele2 = random.choice(get_alleles(p2_geno))
    return ''.join(sorted([allele1, allele2]))

def get_phenotype(genotype):
    return 'Dominant' if 'A' in genotype else 'Recessive'

# Create a list to hold all children
children_records = []

for idx, row in df_families.iterrows():
    family_id = row['Family_ID']
    parent1 = row['Parent1']
    parent2 = row['Parent2']
    
    for child_num in range(1, children_per_family + 1):
        child_data = {'Family_ID': family_id, 'Child_ID': f'Child{child_num}'}
        
        for gene in genes:
            child_geno = simulate_child_genotype(parent1[gene], parent2[gene])
            child_data[f'{gene}_Genotype'] = child_geno
            child_data[f'{gene}_Phenotype'] = get_phenotype(child_geno)
        
        children_records.append(child_data)

# Convert to DataFrame
df_children = pd.DataFrame(children_records)
df_children.head()

# Step 5 Merge children and Parent data sets
# Expand parent genotypes
df_parents_expanded = pd.DataFrame({
    'Family_ID': df_families['Family_ID'],
    **{f'Parent1_{gene}': [p[gene] for p in parent1_data] for gene in genes},
    **{f'Parent2_{gene}': [p[gene] for p in parent2_data] for gene in genes}
})

# Merge with children
df_full = pd.merge(df_children, df_parents_expanded, on='Family_ID')
df_full.head()

# Step 6 Save and visualize the data sets
# Save to CSV
df_full.to_csv('multi_gene_family_genotypes.csv', index=False)

# Example visualization: Gene1 genotype distribution across all children
df_full['Gene1_Genotype'].value_counts().plot(kind='bar', title='Gene1 Genotype Distribution (All Children)')
