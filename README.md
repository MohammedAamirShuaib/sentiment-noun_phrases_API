# Sentiment and Noun Phrases API

Required libraries for testing - json, requests.

Input should be a list of sentences
Define the list of sentences as sentence_list

### Get the Sentiment of the sentence : 
##### requests.post('http://ec2-54-164-248-248.compute-1.amazonaws.com:8000/sentiment/', data=json.dumps({"input":sentence_list})).json()
### Get Noun Phrases in the sentence : 
##### requests.post('http://ec2-54-164-248-248.compute-1.amazonaws.com:8000/noun_phrases/', data=json.dumps({"input":sentence_list})).json()

