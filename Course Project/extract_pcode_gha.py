import pandas as pd

# Load the pcode data
pcode_df = pd.read_csv('Course Project/global_pcodes.csv')

# Extract all values where Location == 'GHA'
pcode_gha = pcode_df[pcode_df['Location'] == 'GHA']

# Optionally extract PCODE column values
pcode_gha_values = pcode_gha['PCODE'].tolist()

print(pcode_gha_values)
