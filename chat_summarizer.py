import re
import string
import os
import nltk
from collections import Counter
from nltk.corpus import stopwords
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
# print(stop_words)
def clean_messages(text):
    
    text = text.lower()
    
    text = re.sub(f"[{string.punctuation}]", "", text)
    words = text.split()
    return [word for word in words if word not in stop_words]

def read_and_count_messages(file_path):
    user_messages = []
    ai_messages = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("User:"):
                
                user_messages.append(line[5:].strip())
            elif line.startswith("AI:"):
                
                ai_messages.append(line[3:].strip())

    total_messages = len(user_messages) + len(ai_messages)

    return user_messages, ai_messages, total_messages

def top_keywords_frequency(messages, top_n=5):
    all_words = []
    for message in messages:
        all_words.extend(clean_messages(message))
        
    most_common_words = Counter(all_words).most_common(top_n)
    return [word for word, _ in most_common_words]

def conversation_nature(keywords):
    if not keywords:
        return "The conversation topics are unclear."
    
    topics = ', '.join(keywords)
    return f"The conversation mainly revolves around: {topics}."

def summarize_chat(file_path):
    user_messages, ai_messages, total_messages = read_and_count_messages(file_path)
    stats = {
        "total_messages": total_messages,
        "user_messages_count": len(user_messages),
        "ai_messages_count": len(ai_messages)
    }

    keywords = top_keywords_frequency(user_messages + ai_messages)

    nature_summary = conversation_nature(keywords)

    summary = (
        f"Here's a quick overview of the chat:\n"
        f" Total messages exchanged: {stats['total_messages']}\n"
        f" Messages sent by you: {stats['user_messages_count']}\n"
        f" Messages sent by the AI: {stats['ai_messages_count']}\n"
        f" {nature_summary}\n"
        f" Top keywords used: {', '.join(keywords)}\n"
    )

    print(summary)

def summarize_multiple_chats(folder_path):
    print(f"Summarizing all chat logs in folder: {folder_path}\n")
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            print(f"Summary for '{filename}':")
            summarize_chat(os.path.join(folder_path, filename))
            print("-" * 50)


#summarize_chat("chat.txt")

summarize_multiple_chats(".")


