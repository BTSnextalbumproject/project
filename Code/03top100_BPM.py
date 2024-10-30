import pandas as pd

# File paths
file_bpm = './billboardTop100Totalduplicate_with_BPM.csv'
file_target = './billboardTop100Total.csv'

# Load the datasets
df_bpm = pd.read_csv(file_bpm)
df_target = pd.read_csv(file_target)

# Merging the BPM values from df_bpm into df_target based on matching 'Title' and 'Artist'
# We will do a left merge to add the 'BPM' column where 'Title' and 'Artist' match
df_merged = pd.merge(df_target, df_bpm[['Title', 'Artist', 'BPM']], on=['Title', 'Artist'], how='left')

# Save the result to a new CSV
output_file_path = './billboardTop100Total_with_BPM.csv'
df_merged.to_csv(output_file_path, index=False)

print("Merged file saved at:", output_file_path)

