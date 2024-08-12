# python3
# Please install OpenAI SDK first：`pip3 install openai`
from openai import OpenAI

client = OpenAI(api_key="sk-c7e36dd880fe47e1afb1a43de39b718b", base_url="https://api.deepseek.com")

while(1) :
    question = input("请输入对话：")
    if question == 'exit':
        break

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": question},
        ],
        stream=False
    )
    
    print("")
    
    print("回复：")
    
    print("")

    print(response.choices[0].message.content)
    
    print("--------------------------------------------------")
    print("")    
    