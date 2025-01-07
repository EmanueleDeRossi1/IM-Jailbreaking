import csv
import re
import os
import pandas as pd

def extract_and_save_scores(strongreject_folder, filename, output_csv='scores.csv'):

    with open(os.path.join(strongreject_folder, filename), 'r', encoding='utf-8') as file:
        strongreject_response = file.read()

    # Define a pattern to extract the score labels (e.g., 1.a, 1.b, etc.) and corresponding scores
    pattern = r'(\d+\.[b])\s(\d+)'
    
    # Find all matches in the text
    matches = re.findall(pattern, strongreject_response)
    print(matches)

    # If fewer than 3 matches are found, pad the list with empty values to avoid errors
    while len(matches) < 3:
        matches.append(('', ''))

    # Prepare a DataFrame row with the format: filename, matches[0], matches[1], matches[2]
    row_data = {
        'filename': filename[:-4],
        'match_1': matches[0][1] if matches else '',
        'match_2': matches[1][1] if len(matches) > 1 else '',
        'match_3': matches[2][1] if len(matches) > 2 else ''
    }

    # Create a DataFrame
    df = pd.DataFrame([row_data])

    # Save the DataFrame to a CSV file
    df.to_csv(output_csv, mode='a', header=not os.path.exists(output_csv), index=False)
    
    print(f"Data saved to {output_csv}")

    return df


data_dir = os.path.join(os.getcwd(), 'data')

# # CHANGE BELOW AFTER
strongreject_dir = os.path.join(data_dir, 'annotations sample', 'strongreject with GPT lower')


# # loop through the files in the select answer directory
for filename in os.listdir(strongreject_dir):
    extract_and_save_scores(strongreject_dir, filename, output_csv=os.path.join(data_dir, 'annotations sample', 'strongreject_lower.csv'))
