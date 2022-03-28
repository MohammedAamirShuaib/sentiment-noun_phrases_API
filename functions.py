import boto3
import nltk
import stanza
from textblob import TextBlob
import pandas as pd
import re
import json
from datetime import datetime
import time
nlp = stanza.Pipeline('en', use_gpu=True)

def get_asp(sentence):
    important = nlp(sentence)
    target = ''
    for sent in important.sentences:
        for wrd in sent.words:
            if wrd.deprel == 'nsubj' and wrd.pos == 'NOUN':
                target = wrd.text
    return target

def get_desp(sentence):
    important = nlp(sentence)
    descriptive_item = ''
    added_terms = ''
    for sent in important.sentences:
        for wrd in sent.words:
            if wrd.pos == 'ADV' and wrd.deprel == 'advmod':
                added_terms = wrd.text
            if wrd.pos == 'ADJ':
                descriptive_item = added_terms + ' ' + wrd.text
    return descriptive_item

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext

def get_batch_sentiment(sentence_list):
    sentiments_list=[]
    n = 25
    chunks_list = [sentence_list[i * n:(i + 1) * n] for i in range((len(sentence_list) + n - 1) // n )]
    for i in range(len(chunks_list)):
      batch_sentiment = json.dumps(comprehend.batch_detect_sentiment(TextList=chunks_list[i], LanguageCode='en'),sort_keys=True,indent=4)
      batch_sentiment = json.loads(batch_sentiment)
    
      for i in range(len(batch_sentiment['ResultList'])):
          sentiment = batch_sentiment['ResultList'][i]['Sentiment']
          sentiments_list.append(sentiment)
          
    return sentiments_list

def get_noun_phrases(sentence_list):
    noun_phrases_list = []
    for i in range(len(sentence_list)):
      # html cleaning
      sentence = str(sentence_list[i])
      sentence = cleanhtml(sentence)
      noun_phrases = TextBlob(sentence).noun_phrases
      noun_phrases = (','.join(map(str, noun_phrases)))
    
      if(len(noun_phrases) <= 1):  
          aspect = get_asp(sentence)
          descriptive_item = get_desp(sentence)
          aspect_descp = descriptive_item +' ' +aspect
          noun_phrases = aspect_descp
      else:
          noun_phrases = noun_phrases
      noun_phrases_list.append(noun_phrases)
    
    return noun_phrases_list