# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:24:03 2024

@author: emanu
"""

from extract_information_from_answers import read_txt_files

# Define the root directory
root_dir = r"C:\Users\emanu\Desktop\IM"

replies = read_txt_files(root_dir)
# Convert the flattened dictionary to a list of lists
table_data = []
for key, value in replies.items():
    category, question, option, prompt = key.split(' - ')
    prompt_type = option + " - " + prompt 
    replied = value[0]
    warning_in_prompt = value[1]
    warning_on_reply = value[2]
    word_count = value[3]
    table_data.append([category, prompt_type, question, replied, warning_in_prompt, warning_on_reply, word_count])

import matplotlib.pyplot as plt


# Initialize counters
replied_counts = {'Abyss': 0}
warning_prompt_counts = {'Abyss': 0}
warning_reply_counts = {'Abyss': 0}

# Count the occurrences
for entry in table_data:
    method = entry[0]
    replied = entry[3]
    warning_prompt = entry[4]
    warning_reply = entry[5]
    
    if replied == 'No':
        replied_counts[method] = replied_counts.get(method, 0) + 1
    if warning_prompt == 'Yes':
        warning_prompt_counts[method] = warning_prompt_counts.get(method, 0) + 1
    if warning_reply == 'Yes':
        warning_reply_counts[method] = warning_reply_counts.get(method, 0) + 1

# Plotting
methods = list(replied_counts.keys())
replied_values = list(replied_counts.values())
warning_prompt_values = list(warning_prompt_counts.values())
warning_reply_values = list(warning_reply_counts.values())

bar_width = 0.25
index = range(len(methods))

plt.bar(index, replied_values, bar_width, label='Did Not Reply')
plt.bar([i + bar_width for i in index], warning_prompt_values, bar_width, label='Warning in Prompt')
plt.bar([i + 2 * bar_width for i in index], warning_reply_values, bar_width, label='Warning in Reply')

plt.xlabel('Method')
plt.ylabel('Count')
plt.title('Model reaction by method')
plt.xticks([i + bar_width for i in index], methods)
plt.legend()
plt.tight_layout()
plt.savefig(r"C:\Users\emanu\Desktop\IM\reply rate plots\by_methods.png")
plt.show()
