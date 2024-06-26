# -*- coding: utf-8 -*-
"""MedicalBot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13MZ-7KidzVV9Ptk3KwBMZepDFndMvg-0
"""

!pip install openai==1.13.3

# Add Azure OpenAI package
from openai import AzureOpenAI
import requests

#Set the API Keys, Endpoint and Model for Image Deployment
azure_image_oai_endpoint ="https://eyuser26.openai.azure.com/"
azure_image_oai_key ="98138d9733f746a6aa3652f29c183d0d"
azure_image_oai_deployment ="Dalle3"

#Set the API Keys, Endpoint and Model for Text Deployment
azure_text_oai_endpoint ="https://eyuser19.openai.azure.com/"
azure_text_oai_key ="f8a4b97dd6fb4630b143f94acce8e34a"
azure_text_oai_deployment ="GaneshTestDeployment"

# Initialize the Azure OpenAI client
azure_image_endpoint = azure_image_oai_endpoint
api_image_key=azure_image_oai_key
azure_text_endpoint = azure_text_oai_endpoint
api_text_key=azure_text_oai_key
api_version="2024-02-15-preview"

client = AzureOpenAI(
          azure_endpoint = azure_text_oai_endpoint,
          api_key=azure_text_oai_key,
          api_version="2024-02-15-preview"
        )

url = "{}openai/deployments/dalle3/images/generations?api-version={}".format(azure_image_oai_endpoint, api_version)
headers= { "api-key": azure_image_oai_key, "Content-Type": "application/json" }

async def main():
    messages = [{"role": "system", "content": "You are chatting with a Medical Assistant. I can provide information on medical topics and answer health-related questions. Please remember that I'm not a substitute for professional medical advice. If you have a medical emergency, please call emergency services immediately."}]
    try:
        while True:
            # Get input from the user to select Chat or Image Bot
            print("Please enter from the below options to interact with Chat Bot or Image Bot:")
            print("1. For Medical Chat Bot Assisstance")
            print("2. For Medical Image Bot Assisstance")
            option = input("\nEnter your option to choose Medical Bot Assisstance.")

            user_text = input("Enter your message:")

            if(option == '1'):
              messages.append({"role": "user", "content": user_text})
              print("Please wait while we find the best response...")

              # Call the Azure OpenAI model
              response = client.chat.completions.create(
                model = azure_text_oai_deployment,
                messages = messages,
                temperature = 0.2,
                max_tokens = 100
              )
              bot_response = response.choices[0].message.content
              print("Bot Response: \n" + bot_response + "\n")

              # Add generated text to messages array
              messages.append({"role": "system", "content": bot_response})

            else :
              body = { "prompt": user_text, "n": 1, "size": "1024x1024" }
              response = requests.post(url, headers=headers, json=body)
              print(response.text)

              # Get the revised prompt and image URL from the response
              revised_prompt = response.json()['data'][0]['revised_prompt']
              image_url = response.json()['data'][0]['url']
              save_path = 'image_name.jpg'

              print("Please wait while we are generating the image...")

              # Download the image and save it to the specified path
              response = requests.get(image_url)
              if response.status_code == 200:
                with open(save_path, 'wb') as f:
                  f.write(response.content)
                print(f"Image saved to {save_path}")
              else:
                print("Failed to download the image")

            # Pause the app to allow the user to enter the system prompt
            text = input("Enter Exit to Exit, anything else to continue ")

            if text.lower() == 'exit':
                print('Exiting program...')
                break

    except Exception as ex:
      print(ex)

await main()

