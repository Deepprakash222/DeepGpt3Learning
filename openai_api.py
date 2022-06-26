import openai
import sys
import os
import re
from typing import List, Text, Dict, Tuple
import openai
from getpass import getpass
from pprint import pprint

import nltk
nltk.download('punkt')
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm import tqdm

#api = getpass('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')
#os.environ['OPENAI_API_KEY'] = api

history_chat = ["King is an intelligent assistant author of horror, supernatural fiction, suspense, crime, science-fiction, and fantasy novels inspired by Stephen King. It has great ideas for articles, blogs, and movie creation. It is helping to provide article titles, sub-headers for the article's title, and also great, flourishing, expensive vocabulary within paragraphs. If the user said no to something, King will offer to help the user.\n\nKing: Hello there, you have with you, King! an Artificial Intelligent Assistant for helping you create beautiful, inspired, horror, supernatural fiction, suspense, crime, science-fiction, fantasy articles, and novels. Please tell me if you have an idea for a title for what you want to write about.\n"]
ARTICLE = []


#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key ='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'

def chatbot(user_insertion: Text):
  global history_chat
  history_chat.append(f"You: {user_insertion}\nKing:")
  response = openai.Completion.create(
    model="text-davinci-002",
    prompt="".join(history_chat),
    temperature=0.85,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  response = re.sub(r"(^\n\n)(\S.+)", r"\2", response.choices[0].text)
  history_chat.append(f"{response}\n")
  
  return response


def paragraph_generator(list_of_sub_headers: List):
  list_of_paragraphs = []
  list_of_sub_headers = list(filter(None, list_of_sub_headers[-1].strip(' ').split('\n')))

  prompt = ["Expand this sub-headers in to a detailed professional , witty and clever explanation paragraph."]

  for index, sub_header in enumerate(tqdm(list_of_sub_headers, desc="Generating paragraphs")):
    if index != 0:
      prompt.append(f"\n\n{sub_header}\n")
    else:
      prompt.append(f"\n{sub_header}\n\n")

    response = openai.Completion.create(
      model="text-davinci-002",
      prompt="".join(prompt),
      temperature=0.7,
      max_tokens=200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    list_of_paragraphs.append(
        sentence_tokenization(
            re.sub(r"("+sub_header+")", "", response.choices[0].text.replace(sub_header, ""),
                   re.IGNORECASE)
        )
    )

  return "\n\n".join("".join([header, paragraph])
                 for header, paragraph in  list(zip(list_of_sub_headers,
                                                    list_of_paragraphs)))


def sentence_tokenization(text: Text) -> List[Text]:
  text = re.sub(r"(^\n)(\n)(\w)", r"\2\3", text)
  tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
  str_tokenized_text = " ".join([sentence for sentence in tokenizer.tokenize(text) if sentence[-1] in [".", "!", "?"]])
  str_tokenized_text = str_tokenized_text.replace(r'\s ', ' ')
  str_tokenized_text= str_tokenized_text.replace(r'(^\s)|(\s$)', '')
  return str_tokenized_text
