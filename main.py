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

@app.post('/batch_sentiment_25/')
async def get_batch_sentiment(sentence_list:ListSentimentBaseModel):

@app.post('/noun_phrases/')
