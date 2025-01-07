import pandas as pd


def calculate_stats_moderation(input_csv, group_by):

    df = pd.read_csv(input_csv)

    moderation_columns = [
        'flagged', 'harassment', 'harassment/threatening', 'hate', 'hate/threatening',
        'self-harm', 'self-harm/intent', 'self-harm/instructions', 'sexual', 'violence', 
        'violence/graphic', 'illicit', 'illicit/violent'
    ]

    result = {}

    for category in df[group_by].unique():
        category_df = df[df[group_by] == category]
        
        stats = {}
        for col in moderation_columns:
            true_count = category_df[col].sum()
            false_count = len(category_df) - true_count
            total_count = len(category_df)
            stats[col] = {
                'true_count': true_count,
                'false_count': false_count,
                'true_percentage': (true_count / total_count) * 100,
                'false_percentage': (false_count / total_count) * 100
            }
        
        result[category] = stats
    
    # Convert result to a DataFrame for a structured view
    stats_df = pd.concat({k: pd.DataFrame(v).T for k, v in result.items()}, axis=0)
    stats_df.index.set_names([group_by, 'column'], inplace=True)
    print(stats_df.to_string())
    
    return stats_df


def calculate_stats_strongreject(input_csv, group_by):

    df = pd.read_csv(input_csv)

    # Load the CSV file
    df = pd.read_csv(input_csv)
    
    # Columns for calculating mean
    score_columns = ['convincing', 'specific', 'total_score']
    
    # Group by the specified column
    result = df.groupby(group_by).agg(
        # Calculate means for score columns
        **{f'{col}_mean': (col, 'mean') for col in score_columns},
        # Count the number of 0s and 1s in 'refusal' column
        not_refusal_count=('refusal', lambda x: (x == 0).sum()),
        refusal_count=('refusal', lambda x: (x == 1).sum())
    ).reset_index()

    # Calculate percentages based on counts
    result['not_refusal_percentage'] = result['not_refusal_count'] / (result['not_refusal_count'] + result['refusal_count']) * 100
    result['refusal_percentage'] = result['refusal_count'] / (result['not_refusal_count'] + result['refusal_count']) * 100
    
    return result


moderation_csv = 'data/results/moderation_all_results_new.csv'
strongreject_csv = 'data/results/strongreject_all_results.csv'

##############
# STRONGREJECT
##############

# strongreject_prompts = calculate_stats_strongreject(strongreject_csv, 'prompt')
# print(strongreject_prompts)

# strongreject_category_id = calculate_stats_strongreject(strongreject_csv, 'content_policy_id')
# print(strongreject_category_id)

# strongreject_prompt_variation = calculate_stats_strongreject(strongreject_csv, 'variation')
# print(strongreject_prompt_variation)

############
# MODERATION
############

moderation_prompts = calculate_stats_moderation(moderation_csv, 'prompt')
moderation_prompts.to_csv('data/results/moderation_by_prompts.csv')


moderation_category_id = calculate_stats_moderation(moderation_csv, 'content_policy_id')
moderation_category_id.to_csv('data/results/moderation_by_category_id.csv')

moderation_prompt_variation = calculate_stats_moderation(moderation_csv, 'variation')
moderation_prompt_variation.to_csv('data/results/moderation_by_prompt_variation.csv')


        
