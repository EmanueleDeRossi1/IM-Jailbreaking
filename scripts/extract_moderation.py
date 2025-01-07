# extract moderation

import os
import re
import pandas as pd

def extract_scores(moderation_path, output_csv):

    for root, dirs, files in os.walk(moderation_path):    

        for filename in files:
            file_path = os.path.join(root, filename)     
    
            path_split = re.split(r'[\\/]', file_path)
            seed = path_split[-5]
            cont_policy_id = path_split[-4]
            question_id = path_split[-3]
            prompt = path_split[-2]

            # Read the small CSV file
            df = pd.read_csv(file_path)
            
            # Split 'filename' column into 'variation_category' and 'variation'
            df[['variation_category', 'variation']] = df['filename'].str.extract(r' - (\d) - (.+)')
            
            # Drop the original 'filename' column if it’s no longer needed
            df = df.drop(columns=['filename'])
            
            # Add new columns to the DataFrame
            df['seed'] = seed
            df['content_policy_id'] = cont_policy_id
            df['q_id'] = question_id
            df['prompt'] = prompt
            
            # Append the modified DataFrame to the output CSV file
            with open(output_csv, 'a') as f:
                df.to_csv(f, header=f.tell() == 0, index=False)


    print("Saved .csv file to ", output_csv)


moderation_path = 'data/results/moderation'
output_csv = 'data/results/moderation_all_results_new.csv'

extract_scores(moderation_path, output_csv)


