import pickle
import sentence_cleaner
import numpy as np
from keras.preprocessing.sequence import pad_sequences

max_tokens = 509

def preprocess_tweets(tweets) :
    
    cleaned_tweets = []
    
    for tweet in tweets :
        cleaned_tweets.append( sentence_cleaner.tweet_cleaner( tweet ) )
        
    cleaned_tweets = np.array(cleaned_tweets)
    
    #Loading the tokenizer
    with open('tokenizer.pickle','rb') as handle :
        tokenizer = pickle.load(handle)
        
    cleaned_tweets_tokens = tokenizer.texts_to_sequences( cleaned_tweets )
    
    #Padding
    pad = 'pre'
    
    cleaned_tweets_pad = pad_sequences( cleaned_tweets_tokens , maxlen = max_tokens, 
                                         padding = pad , truncating = pad )
    
    return cleaned_tweets_pad