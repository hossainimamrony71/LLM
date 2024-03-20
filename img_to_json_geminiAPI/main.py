import os
import json
import textwrap
from IPython.display import Markdown
import google.generativeai as genai
import json_repair

# Function to convert text data into JSON question-answer pairs
def text_to_json(folder_path, output_file, model, max_length=2000):
    """
    Convert text data into JSON question-answer pairs and save to a file.

    Args:
    folder_path (str): Path to the folder containing text files.
    output_file (str): Path to the output JSON file.
    model (GenerativeModel): Generative AI model instance.
    max_length (int): Maximum length of text to process in a single request.

    Returns:
    None
    """
    json_data = []
    counter = 1
    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        # Check if it's a text file
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read().replace("﻿________________",'').replace("\n",' ').replace("[]",' ').replace("www.bdniyog.com",'')
                    # Split text into chunks if its length exceeds max_length
                    chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]
                    for chunk in chunks:

                        # Process the chunk
                        response = model.generate_content(
                            f'''**Input:** "{chunk}"

                                        **Task:** Convert the provided data into a JSON object with question-answer pairs. Values should always be in Bangla. If there are multiple-choice questions (MCQs), ensure to take the value as the answer, not the number corresponding to the choice.

                                        **Important:** 
                                        - Each item in the JSON must have keys "question" and "answer".
                                        -The question and answer should be as detailed as possible.
                                        - Ensure no text is lost from the context during the conversion, don't miss any data, clean text.
                                        -Ensure to give valid json data.
                                        - Avoid adding any top-level structure in the JSON data.
                                        '''
                                         )
                        response_data = response.text.strip().replace('`json', '').replace("`",'').replace("JSON",'').replace("**",'').strip()
                        if response_data[0] != '[':
                            response_data = f"[{response_data}]"
                        try:
                            json_data_set = json.loads(response_data) 
                            json_data.extend(json_data_set)

                        except json.JSONDecodeError as e:
                            json_data_set = json_repair.loads(response_data)
                            json_data.extend(json_data_set)
                            

                        print(f"done - {counter}")
                        counter+=1

            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
    
    # Save JSON data to output file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)
        print(f"JSON data saved to {output_file}")

# Initialize Generative Model
GOOGLE_API_KEY = "AIzaSyD_Yfzye8xf7SHsh_wUOo1p5ELOQ_5BSG8"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# Example usage:
folder_path = "content"
output_file = "agradut_bangla.json"
text_to_json(folder_path, output_file, model)
