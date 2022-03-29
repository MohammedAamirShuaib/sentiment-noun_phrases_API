# Sentiment and Noun Phrases API

required libraries for testing - json, requests.

Input should be a list of sentences
define the list of sentences as sentence_list

get the Sentiment of the sentence : requests.post('http://ec2-54-164-248-248.compute-1.amazonaws.com:8000/sentiment/', data=json.dumps({"input":sentence_list})).json()
get Noun Phrases in the sentence : requests.post('http://ec2-54-164-248-248.compute-1.amazonaws.com:8000/noun_phrases/', data=json.dumps({"input":sentence_list})).json()

