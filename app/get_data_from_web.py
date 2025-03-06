import requests
from bs4 import BeautifulSoup
from googlesearch import search
import json

from transformers import AutoTokenizer, RobertaForQuestionAnswering
import torch

from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv()

# Access environment variables as if they came from the actual environment
API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

def get_url_from_web_for_keywords(keywords):
    """
    Searches the web for the given keywords and returns a list of URLs.

    Args:
        keywords (str): The keywords to search for.

    Returns:
        list: A list of URLs from the search results.
    """

    lst = []
    for j in search(keywords, tld="com", safe="on", num=10, stop=10, pause=2):
        lst.append(j)
    return lst

def get_data_from_web_for_url(url):
    """
    Fetches and extracts text data from a given URL.

    This function sends a GET request to the specified URL with a custom
    User-Agent header to mimic a browser request. It then parses the
    HTML response using BeautifulSoup and extracts all the text content
    from the page.

    Args:
        url (str): The URL from which to fetch and extract text data.

    Returns:
        str: A string containing the text content extracted from the URL.
    """

    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extracting the first search result snippet
    # answer = soup.find_all("p", limit=50)
    text = soup.get_text(strip=False, separator=' ')
    return text

def get_answer_from_model_for_data(run_mode, payload):
    """
    Send a payload to a pre-trained model on Hugging Face and retrieve an answer.

    This function sends a HTTP POST request with a JSON payload to a specified
    API endpoint. The endpoint is associated with a pre-trained model capable
    of answering questions based on the provided input data.

    Args:
        payload (dict): A dictionary containing the input data for the model.

    Returns:
        dict: A dictionary containing the model's response if successful.
        str: A JSON string with a dummy response if the request fails.
    
    To know more about this model: https://huggingface.co/deepset/roberta-base-squad2
    """

    if run_mode == 'R':
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()
        else:
            dumm_response = '{"score": 10, "start": 38, "end": 52, "answer": "dummy"}'
            dict_obj = json.loads(dumm_response)
            return dict_obj
    elif run_mode == 'L':
        tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
        model = RobertaForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")

        inputs = tokenizer(payload['inputs']['question'], payload['inputs']['context'], return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        answer_start_index = outputs.start_logits.argmax()
        answer_end_index = outputs.end_logits.argmax()

        predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
        response = {
            'answer': tokenizer.decode(predict_answer_tokens, skip_special_tokens=True),
            'score': outputs.start_logits[0, answer_start_index].item(),}
        return json.dumps(response)
    else:
        print("Invalid run mode. Please use 'R' or 'L'.")
        exit(1)

def main(run_mode, keywords, question):
    """
    Main function of the program.

    This function takes two parameters, keywords and question. It first uses the
    keywords to search for relevant URLs on the web. It then sends a request to
    each of the URLs and extracts the text content from the page. The text
    content is then sent to a pre-trained model on Hugging Face, which returns
    an answer based on the question and the text content. The answers are then
    saved in a raw_anwers.txt file. The answers are then processed to find the
    most common answer and saved in an ordered_anwers.txt file. Finally, the
    most common answer is saved in a final_anwer.txt file.

    Args:
        run_mode (str): run_mode tell program to use 'R': Remote model or 'L': Local model
        keywords (str): Keywords to search for on the web.
        question (str): Question to ask the model.

    Returns:
        str: The most common answer from the model.
    """

    result_urls = get_url_from_web_for_keywords(keywords)

    raw_anwers = {}
    for i in range(len(result_urls)):
        result_data =get_data_from_web_for_url(result_urls[i])
        payload = {
                "inputs": {
                "question": question,
                "context": result_data},
        }
        # add returned value from get_answer_from_model_for_data to raw_anwers dictionary
        raw_anwers[result_urls[i]] = get_answer_from_model_for_data(run_mode, payload)

    #Give me commands to save this raw_anwers in a txt file
    with open('raw_anwers.txt', 'w') as f:
        f.write(json.dumps(raw_anwers))
    f.close()

    ordered_anwers = {}
    for x in raw_anwers.values():
        worked_on_str = str(x['answer']).lower()
        if worked_on_str in ordered_anwers:
            ordered_anwers[worked_on_str] += 1
        else:
            ordered_anwers[worked_on_str] = 1

    with open('ordered_anwers.txt', 'w') as f:
        f.write(json.dumps(ordered_anwers))
    f.close()

    final_anwer = max(zip(ordered_anwers.values(), ordered_anwers.keys()))[1]  

    with open('final_anwer.txt', 'w') as f:
        f.write(final_anwer)
    f.close()

    return final_anwer


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gets data from web, sends it to the model and finally our model answers to question asked")

    # Define positional argument
    parser.add_argument("run_mode", type=str, help="run_mode tell program to use 'R': Remote model or 'L': Local model")
    parser.add_argument("keywords", type=str, help="Keywords to search in web")
    parser.add_argument("question", type=str, help="question to ask")

    # Parse arguments from command line
    args = parser.parse_args()
    main(run_mode=args.run_mode, keywords=args.keywords, question=args.question)
