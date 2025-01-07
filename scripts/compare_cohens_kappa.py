import pandas as pd
from sklearn.metrics import cohen_kappa_score


def openai_kappa_scores(openai_df):

    kappa_scores = {}

    openai_columns = [col for col in openai_df.columns if 'ann' not in col and 'filename' not in col]
    annotator_columns = [col for col in openai_df.columns if 'ann' in col]

    # Ensure matching columns
    for openai_col in openai_columns:
        # Find the corresponding annotator column
        corresponding_ann_col = f"ann. {openai_col}"
        if corresponding_ann_col in annotator_columns:
            # Calculate Cohen's Kappa for binary labels
            kappa = cohen_kappa_score(openai_df[openai_col], openai_df[corresponding_ann_col])
            kappa_scores[openai_col] = kappa
        else:
            print(f"Warning: No matching annotation column found for {openai_col}")

    return kappa_scores

def strongreject_kappa_scores(strongreject_df):

    kappa_scores = {}

    # Drop columns with 'diff.' in the name
    strongreject_df = strongreject_df.drop(columns=[col for col in strongreject_df.columns if 'diff.' in col])
    # Print len of the df
    print(len(strongreject_df))

    strongreject_columns = [col for col in strongreject_df.columns if 'annotations' not in col and 'filename' not in col]
    annotator_columns = [col for col in strongreject_df.columns if 'annotations' in col]

    # Ensure matching columns
    for strongreject_col in strongreject_columns:
        # Find the corresponding annotator column
        corresponding_ann_col = f"{strongreject_col} annotations"
        if corresponding_ann_col in annotator_columns:
            if strongreject_col == '1. refusal':
                # Calculate Cohen's Kappa for binary labels
                kappa_refusal = cohen_kappa_score(strongreject_df[strongreject_col], strongreject_df[corresponding_ann_col])
                kappa_scores[strongreject_col] = kappa_refusal
                print(f"binary: {strongreject_col} -> {kappa_refusal}")
            else:
                # Drop rows that have 1s in refusal of strongreject or annotator (total score with refusal=1 will always be 0)
                strongreject_df = strongreject_df[~((strongreject_df['1. refusal'] == 1) | (strongreject_df['1. refusal annotations'] == 1))]
                print(len(strongreject_df))
                # Calculate Cohen's Kappa for ordinal labels(1-5)
                kappa_weighted = cohen_kappa_score(strongreject_df[strongreject_col], strongreject_df[corresponding_ann_col], weights='linear')
                kappa_scores[strongreject_col] = kappa_weighted
                print(f"ordinal: {strongreject_col} -> {kappa_weighted}")

        else:
            print(f"Warning: No matching annotation column found for {strongreject_col}")

    return kappa_scores



file_path_openai = r'C:\Users\emanu\Documents\GitHub\IM-Jailbreaking\data\annotations\comparison_openai_annotations.csv'
openai_annotations = pd.read_csv(file_path_openai)
# Replace NaN with 0 and 'X' with 1
openai_annotations = openai_annotations.fillna(0).replace('X', 1)

file_path_strongreject = r'C:\Users\emanu\Documents\GitHub\IM-Jailbreaking\data\annotations\comparison_strongreject_annotations.csv'
strongreject_annotations = pd.read_csv(file_path_strongreject)

print(openai_kappa_scores(openai_annotations))
print(strongreject_kappa_scores(strongreject_annotations))