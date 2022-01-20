import os
import openai
import argparse
import regex as re

MAX_INPUT_LENGTH =32 

def main():
    #Get userinput from the command line 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input","-i",type=str,required=True)
    args=parser.parse_args()
    user_input = args.input
    print(f"User Input : ", user_input)

    if validate_length(user_input):
        branding_result = generate_branding_snippet(user_input)
        keywords_result = generate_keywords(user_input)
    else:
        raise ValueError(
            f"Input length is too long.Must be under {MAX_INPUT_LENGTH}. Submittied input is : {user_input}"
            )

def validate_length(prompt: str) -> bool:
    return len(prompt) <= 12

def generate_branding_snippet(prompt: str)-> str:
    #Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")

    enriched_prompt =f"Generate upbeat branding snippet for {prompt}:"
    print(enriched_prompt)

    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3", prompt=enriched_prompt, max_tokens=32)

    #Extract output text.
    branding_text: str = response["choices"][0]["text"]
    #strip whitespace
    branding_text = branding_text.strip()

    #Add ... to truncate statements
    last_char = branding_text[-1]
    if last_char not in {".","!","?"}:
        branding_text += "..."
    print(f"Snippet: {branding_text}")
    return branding_text

def generate_keywords(prompt: str)-> str:
    #Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")

    enriched_prompt =f"Generate related branding keywords for {prompt}:"
    print(enriched_prompt)

    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3", prompt=enriched_prompt, max_tokens=32)

    #Extract output text.
    keyword_text: str = response["choices"][0]["text"]
    #strip whitespace
    keyword_text = keyword_text.strip()
    keyword_arr= re.split(",|\n|;|-",keyword_text)
    keyword_arr = [k.lower().strip() for k in keyword_arr]
    keyword_arr = [k for k in keyword_arr if len(k) >0]
    print(f"Keywords: {keyword_arr}")
    return keyword_arr

if __name__=="__main__":
    main()
