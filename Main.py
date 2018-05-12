
# coding: utf-8

# In[2]:


import numpy as np

from keras.models import load_model

from tweepy.streaming import StreamListener
from tweepy import Stream

import tweets_preprocessor, sentence_cleaner, twitter

import datetime

import matplotlib.pyplot as plt
import matplotlib.animation as animation
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


#get_ipython().run_cell_magic('time', '', 'model = load_model("model_new.h5")')


# In[4]:

model = load_model("model_new.h5")

temp_counter = 0 



# In[6]:


def tweets_processor_and_graph_plotter( tweet ) :
    
    global temp_counter, start_time , current_index , window , sentiment_list
    global mean_list , index_list
    global line1
    
    tweet_list = [ tweet.text ]
    
    tweet_list_pad = tweets_preprocessor.preprocess_tweets( tweet_list )
    
    prediction = model.predict( tweet_list_pad )
    
    tweet_time = tweet.created_at
    
    duration = ( tweet_time - start_time ).seconds
    
    if ( int( duration / window ) != current_index ) :
        
        assert( current_index < int( duration / window ) )
        
        current_index = int( duration / window )
        
        mean_sentiment = np.mean( np.array( sentiment_list ) )
        
        #print ("inside " + str(mean_sentiment) + " " + str(current_index) )
        
        mean_list.append( mean_sentiment )
        index_list.append( current_index )
        
        #ani = animation.FuncAnimation( fig , animate , interval = 1000 )
        line1.set_ydata( mean_list )
        line1.set_xdata( index_list )
        plt.draw()
        
       
        
    else :
        sentiment_list.append( prediction[0] )
        temp_counter += 1 
        if (temp_counter % 10 == 0) :
            with open( 'debug.txt' , 'a' ) as debugger :
                line = "Done " + str(temp_counter) + " tweets in " + str(duration) + " seconds.\n"
                debugger.write( line )
    


# In[7]:


class TwitterListener(StreamListener) :
    
    #Basic Listener that just prints tweets to stdout and also saves them to file
    
    def __init( self) :
        pass
    
    def on_status( self , data ) :
        
        try : 
            tweets_processor_and_graph_plotter(data)
        
        except BaseException as e :
            print ("Error on Data : ", str(e))
        
        return True 
    
    def on_error( self , status ) :
        
        #Returning False on_data method if rate limit occurs
        if (status == 420) :
            return False
        if (status == 429) :
            print ("Rate Limit Exceeded")
        
        print (status)


# In[8]:


class TwitterStreamer() :
    
    #Class for streaming and processing live tweets
    
    def __init__(self) :
        self.twitter_authenticator = twitter.TwitterAuthenticator() 
    
    def stream_tweets( self , hash_tags_list ) :
        
        listener = TwitterListener( )
        
        auth = self.twitter_authenticator.authenticate_twitter_app()
        
        stream = Stream( auth , listener ) 
        
        #Filtering tweets according to out hash tags list
        stream.filter( track = hash_tags_list , languages=["en"]  )
        


# In[ ]:


hash_tags_list = ['bitcoin','btc']

#Initial Variables
start_time = datetime.datetime.utcnow()
current_index = 0
window = 30
sentiment_list = []

mean_list = []
index_list = []

line1, = plt.plot([], []) 


twitter_streamer = TwitterStreamer() 

twitter_streamer.stream_tweets( hash_tags_list )


