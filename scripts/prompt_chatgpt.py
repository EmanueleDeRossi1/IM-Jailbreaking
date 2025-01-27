import os
import openai
import csv
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")




def read_prompts(folder_path):
    """
    Reads all .txt files in a folder and returns a list of prompts.
    :param folder_path: Path to the folder containing .txt files with prompts.
    :return: List of prompts.
    """
    prompts = {}
    for prompt_category in os.listdir(folder_path):
        prompt_folder = os.path.join(prompts_folder_path, prompt_category)
        prompts[prompt_category] = {}
        for filename in os.listdir(prompt_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(prompt_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    prompts[prompt_category][filename] = file.read()
    return prompts

def read_questions(question_file):
    """
    Reads the .csv file containing the malicious questions and returns a list of questions
    
    :param file_path: Path to .csv file
    :return: List of questions (category id, category, question id, question).
    """
    questions = []
    with open(question_file, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            questions.append(row)
    return questions

def get_response(prompt, question, seed):
    """
    Gets a response from the Chatgpt API for the given prompt + question and save it in a .txt file.
    
    :param prompt: The prompt to send to the API.
    :param question_file: The question to send to the API.
    :param seed: 
    :return: The response from the API.
    """
    
    
         
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.7,  # Controls randomness
        top_p=0.9,        # Controls diversity
        frequency_penalty=0,  # Controls repetition
        presence_penalty=0,    # Controls new topic introduction
        seed=seed
    )
    
    return response.choices[0].message.content

def prompt_and_save_answers(seed, questions, prompts, answers_folder_path):
    """
    Generate and save answers for each question and prompt combination.
    :param seed: List of seeds.
    :param questions: List of questions.
    :param prompts: Dictionary of prompts.
    :param answers_folder_path: Main path to save the answers.
    """
    for seed in seeds:
        seed_path = os.path.join(answers_folder_path, str(seed))
        for question in questions:
            question_category_folder_name = question[0] + " - " + question[1]
            question_category_path = os.path.join(seed_path, question_category_folder_name)
            question_folder_name = question[2] + " - " + question[3].replace("?", "").replace('"', '')
            question_path = os.path.join(question_category_path, question_folder_name)
            for prompt in prompts.keys():
                prompt_path = os.path.join(question_path, prompt)
                for prompt_variation, prompt_text in prompts[prompt].items():
                    answer = get_response(prompt_text, question[3], seed)
                    if not os.path.exists(prompt_path):
                        os.makedirs(prompt_path)
                    with open(os.path.join(prompt_path, prompt_variation), "w", encoding="utf-8") as file:
                        file.write(answer)
                            

                        


if __name__ == "__main__":
    # set up file paths
    current_dir = os.path.dirname(__file__)
    question_file = os.path.join(current_dir, "..", "data", "forbidden_question_set.csv")     
    prompts_folder_path = os.path.join(current_dir, "..", "data","prompts") 
    answers_folder_path = os.path.join(current_dir, "..", "data","answers") 
    
    # Load seeds, questions and prompts
    seeds = [5, 10, 313, 200, 1000]
    questions = read_questions(question_file)
    prompts = read_prompts(prompts_folder_path)
    
    # prompt and save answers
    #prompt_and_save_answers(seeds, questions, prompts, answers_folder_path)

    
    # 5 seeds * 139 questions * 7 prompts * 8 prompts variations = 38 920 requests
            
