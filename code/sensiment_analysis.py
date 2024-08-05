from transformers import pipeline

# 使用Hugging Face的情感分析pipeline
classifier = pipeline('sentiment-analysis')

def get_sentiment(text):
    result = classifier(text)
    return result[0]['label']

# 示例
text = "I am very happy with the results."
sentiment = get_sentiment(text)
print(f"Sentiment: {sentiment}")