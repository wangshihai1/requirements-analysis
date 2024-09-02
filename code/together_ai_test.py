import os
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

models = ['meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo', 'google/gemma-2-27b-it', 'allenai/OLMo-7B-Instruct', 'Austism/chronos-hermes-13b', 'deepseek-ai/deepseek-coder-33b-instruct', 'openchat/openchat-3.5-1210']

question = ''
with open('../question_in_English.txt','r',encoding='utf-8') as f:
    for line in f:
        question = question + line

sentence = "The product interface should be fast for 90% of the time. "

stream = client.chat.completions.create(
  model="openchat/openchat-3.5-1210",
  messages=[{"role": "user", 
             "content": question + '\n' + sentence
            }],
  stream=True,
)
for chunk in stream:
  print(chunk.choices[0].delta.content or "", end="", flush=True)