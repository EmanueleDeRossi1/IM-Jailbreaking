import os
import random
import shutil
import re
import csv
from collections import defaultdict


def get_all_txt_files(directory):
    all_txt_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                # Add the full path of each .txt file to the list
                full_path = os.path.join(root, file)
                all_txt_files.append(full_path)
    
    return all_txt_files

# select a single random file from each category and each propmt
# which results in 13 x 7 = 91
def select_from_categories_prompts(all_files, seed=None):
    prompt_list = ["Abyss", "AIM", "BH", "Code Red", "Cody", "Mad Void", "OPPO"]
    # processed list contains instead of filepaths lists of strings divided by /
    processed_list = []
    random_answers = []

    if seed is not None:
        random.seed(seed)
    for path in all_files:
        path = path.replace('\\', '/')
        components = path.split('/')
        processed_list.append(components)
    
    cat_prompt_dict = defaultdict(lambda: defaultdict(list))

    for answer in processed_list:
        category = answer[3]
        prompt = answer[5]

        cat_prompt_dict[category][prompt].append(answer)
    
    # select a random answer from each category and from each prompt

    for category in cat_prompt_dict:
        for prompt in cat_prompt_dict[category]:
            random_answer = random.choice(cat_prompt_dict[category][prompt])
            random_answer_path = '/'.join(str(dir) for dir in random_answer)
            random_answers.append(random_answer_path)
    return random_answers

def count_patterns(file_list):
    # Dictionary to hold the count of each pattern
    pattern_count = defaultdict(int)

    # Regex to extract patterns like "0 - Original", "2 - Without Specific Instructions.txt"
    pattern_regex = re.compile(r'\d+ - .+\.txt')

    # Loop through each file path
    for file_path in file_list:
        # Extract the pattern using regex
        match = pattern_regex.search(file_path)
        if match:
            pattern = match.group()  # Get the matched pattern
            pattern_count[pattern] += 1  # Increment the count for that pattern

    return pattern_count


def select_random_files(all_files, num_files=100, seed=None):
    if seed is not None:
        random.seed(seed)
    return random.sample(all_files, num_files)

def rename_and_copy_files(selected_files, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    for file in selected_files:
        # Split the path into parts by both "/" and "\" 
        path_parts = file.replace("\\", "/").split("/")
        
        # Extract the 3rd, 4th, and 6th parts
        new_name = f"{path_parts[3]} - {path_parts[4]} - {path_parts[6]}"

        dest_path = os.path.join(destination_dir, new_name)
        # copy files
        shutil.copy(file, dest_path)

def create_file_annotation(random_answers_dir, output_csv):
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Loop through the files in the directory
        for filename in os.listdir(random_answers_dir):
            # Check if the file ends with .txt
            if filename.endswith('.txt'):
                # Remove the .txt extension
                file_name_without_extension = os.path.splitext(filename)[0]
                # Write the filename (without extension) as a row in the CSV
                writer.writerow([file_name_without_extension])
        

if __name__ == "__main__":
    current_directory = os.getcwd() 
    # Select the directory from which to extract the files
    # In this case, I took the answers from the seed 10
    directory = os.path.join("data/answers")
    destination_dir = "data/answer_classification"
    num_files = 50
    random_seed = 40
    
    # Collect all file paths
    all_txt_files = get_all_txt_files(directory)
    print(len(all_txt_files))

    random_answer_paths = select_from_categories_prompts(all_txt_files, seed=21)
    print(random_answer_paths)

    print(len(random_answer_paths))

    print(count_patterns(random_answer_paths))


    rename_and_copy_files(random_answer_paths, "data/answer_classification")
    create_file_annotation("data/answer_classification1", "data/annotations.csv")
    # Select random .txt files
    # selected_files = select_random_files(all_txt_files, num_files, seed=random_seed)

    # Rename and copy the selected files to the destination directory
    # rename_and_copy_files(selected_files, destination_dir)

    #for file in selected_files:
    #    print(file)
