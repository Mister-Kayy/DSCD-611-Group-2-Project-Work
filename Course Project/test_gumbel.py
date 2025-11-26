import pandas as pd
import numpy as np
from scipy.stats import gumbel_r

# Load data
rainfall_data = pd.read_csv('gha-rainfall-subnat-full.csv')
pcode = pd.read_excel('PCODE_GHA.xlsx')
merged_df = pd.merge(rainfall_data, pcode[['PCODE', 'Name', 'Municipality']], left_on='PCODE', right_on='PCODE', how='left')
rain_acc = merged_df[merged_df['Municipality'] == 'Greater Accra']
rain_acc['date'] = pd.to_datetime(rain_acc['date'])

# Extract year from date
rain_acc['year'] = rain_acc['date'].dt.year

# Extract annual maxima: group by PCODE and year, take max rfh
annual_max = rain_acc.groupby(['PCODE', 'year'])['rfh'].max().reset_index()

# Function to calculate return period thresholds using Gumbel distribution
def calculate_return_period_thresholds(rainfall_series, periods=[2, 5, 10]):
    # Fit Gumbel distribution to the rainfall data (now annual maxima)
    params = gumbel_r.fit(rainfall_series.dropna())
    thresholds = {}
    for period in periods:
        # Return level for given return period
        # For Gumbel, return level R_T = u + a * ln(-ln(1-1/T))
        u, a = params
        thresholds[period] = u + a * np.log(-np.log(1 - 1/period))
    return thresholds

# Calculate return period thresholds for each PCODE using annual maxima
thresholds_df = annual_max.groupby('PCODE')['rfh'].apply(calculate_return_period_thresholds).reset_index()

# Expand the 'rfh' column (which contains dicts) into separate columns
expanded_thresholds = thresholds_df['rfh'].apply(pd.Series)
expanded_thresholds.columns = ['return_2yr', 'return_5yr', 'return_10yr']

# Join back with PCODE
thresholds_df = thresholds_df[['PCODE']].join(expanded_thresholds)

# Merge thresholds back to rain_acc dataframe
rain_acc = rain_acc.merge(thresholds_df, on='PCODE', how='left')

# Print the result
print(thresholds_df[['PCODE', 'return_5yr']])
