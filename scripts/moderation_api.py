from openai import OpenAI
import os
import pandas as pd
from dotenv import load_dotenv


load_dotenv()
client = OpenAI()

def run_moderation(input_dir, output_dir):
    for subdir, dirs, filenames in os.walk(input_dir):
        if not dirs:
            # initialize an empty row
            csv_data = []
            for filename in filenames:
                if filename.endswith('.txt'):
                    file_path = os.path.join(subdir, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        text_content = file.read()
                    response = client.moderations.create(
                        model='omni-moderation-latest',
                        input=text_content
                    )

                    row = {
                        'filename' : filename[:-4],
                        'flagged' : response.results[0].flagged,
                        'harassment' : response.results[0].categories.harassment,
                        'harassment/threatening' : response.results[0].categories.harassment_threatening,
                        'hate' : response.results[0].categories.hate,
                        'hate/threatening' : response.results[0].categories.hate_threatening, 
                        'illicit' :response.results[0].categories.illicit,
                        'illicit/violent' : response.results[0].categories.illicit_violent,
                        'self-harm' : response.results[0].categories.self_harm, 
                        'self-harm/intent' : response.results[0].categories.self_harm_intent, 
                        'self-harm/instructions' : response.results[0].categories.self_harm_instructions,
                        'sexual' : response.results[0].categories.sexual, 
                        'violence' : response.results[0].categories.violence,
                        'violence/graphic' : response.results[0].categories.violence_graphic
                    }    
                    csv_data.append(row)
                    print(row)

                # Create a DataFrame and save it as a CSV file
                df = pd.DataFrame(csv_data)

                # Define the output path with the same directory structure in output_dir
                relative_path = os.path.relpath(subdir, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                output_file_path = os.path.join(output_subdir, 'moderation_results.csv')

                # Save the DataFrame to a .csv file
                df.to_csv(output_file_path, index=False, encoding='utf-8')


csv_file_name = 'data/try_moderation.csv'

input_dir = os.path.join(os.getcwd(), 'data', 'answers')
output_dir = os.path.join(os.getcwd(), 'data', 'results', 'moderation')

run_moderation(input_dir, output_dir)

# The following was the code was doing the annotations

# csv_file_name = 'data/try_moderation.csv'

# data_dir = os.path.join(os.getcwd(), 'data', 'annotations sample', 'selected answers')
# csv_data = []

# for filename in os.listdir(data_dir):
#     with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as file:
#         text_content = file.read()

#     response = client.moderations.create(
#         model='omni-moderation-latest',
#         input=text_content
#     )

#     row = {
#         'filename' : filename[:-4],
#         'flagged' : response.results[0].flagged,
#         'harassment' : response.results[0].categories.harassment,
#         'harassment/threatening' : response.results[0].categories.harassment_threatening,
#         'hate' : response.results[0].categories.hate,
#         'hate/threatening' : response.results[0].categories.hate_threatening, 
#         'illicit' :response.results[0].categories.illicit,
#         'illicit/violent' : response.results[0].categories.illicit_violent,
#         'self-harm' : response.results[0].categories.self_harm, 
#         'self-harm/intent' : response.results[0].categories.self_harm_intent, 
#         'self-harm/instructions' : response.results[0].categories.self_harm_instructions,
#         'sexual' : response.results[0].categories.sexual, 
#         'violence' : response.results[0].categories.violence,
#         'violence/graphic' : response.results[0].categories.violence_graphic
#     }    

#     csv_data.append(row)



# with open(csv_file_name, mode='w', newline='') as file:
#     # Get all fieldnames (keys) from the first row to be used as column headers
#     writer = csv.DictWriter(file, fieldnames=csv_data[0].keys())
    
#     # Write header
#     writer.writeheader()
    
#     # Write each row of data
#     for row in csv_data:
#         writer.writerow(row)




