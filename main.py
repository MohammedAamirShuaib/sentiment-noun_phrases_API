import boto3
import nltk
import stanza
from textblob import TextBlob
import pandas as pd
import re
import json
from datetime import datetime
import time
from functions import *
from fastapi import BackgroundTasks, FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel
from typing import List

comprehend = boto3.client(service_name='comprehend',
                          region_name='us-east-1',
                          aws_access_key_id='AKIAWFPZMNZHUGEYWIIS',
                          aws_secret_access_key='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')

class SentimentBaseModel(BaseModel):
    input: str

class ListSentimentBaseModel(BaseModel):
    input: List[str]

app = FastAPI()

@app.post("/")
async def get_sentiment_noun(sentence:SentimentBaseModel):
    sentence = sentence.input
    sentence = cleanhtml(sentence)
    
    sentiment = json.dumps(comprehend.detect_sentiment(Text=sentence, LanguageCode='en'),
                           sort_keys=True,
                           indent=4)
    sentiment = json.loads(sentiment)['Sentiment']
    noun_phrases = TextBlob(sentence).noun_phrases
    noun_phrases = (','.join(map(str, noun_phrases)))
    
    if(len(noun_phrases) <= 1):  
        aspect = get_asp(sentence)
        descriptive_item = get_desp(sentence)
        aspect_descp = descriptive_item +' ' +aspect
        noun_phrases = aspect_descp
    else:
        noun_phrases = noun_phrases

    output = {'sentence': sentence,'sentiment': sentiment, 'noun_phrases': noun_phrases}    

    return output


@app.post('/batch/')
async def get_batch_sentiment(sentence_list:ListSentimentBaseModel):    
    sentence_list = sentence_list.input
    batch_sentiment = json.dumps(comprehend.batch_detect_sentiment(TextList=sentence_list, LanguageCode='en'),
                           sort_keys=True,
                           indent=4)
    batch_sentiment = json.loads(batch_sentiment)
    
    sentiments_list=[]
    for i in range(len(batch_sentiment['ResultList'])):
        sentiment = batch_sentiment['ResultList'][i]['Sentiment']
        sentiments_list.append(sentiment)

    return sentiments_list