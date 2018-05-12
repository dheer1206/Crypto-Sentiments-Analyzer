# -*- coding: utf-8 -*-
#Necessary Imports
import re
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer
import lxml


"""
We will follow the following order for cleaning tweets :

1. Souping (Converting to lxml)
2. BOM (Byte Order Marks) removing 
3. Url address(‘http:’pattern) and twitter ID removing
4. Url address(‘www.'pattern) removing
5. Converting to lower-case
6. Negation handling
7. Removing numbers and special characters
8. Tokenizing and joining

"""

### ----------------------------------------------------------
### Making necessary cleaning patterns and negation dictionary
### ----------------------------------------------------------

tok = WordPunctTokenizer()

pat1 = r'@[A-Za-z0-9_]+' #Removing texts starting with '@'
pat2 = r'https?://[^ ]+' #Removing https urls
combined_pat = r'|'.join((pat1, pat2)) #Combining both patterns

www_pat = r'www.[^ ]+' #Removing links starting with 'www' and containing any character

#Dictionary for negative words , so that when we remove special chars other than alphabets and digits,
#we do not remove the apostrophe
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}

neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')


### ----------------------------------------------------------
### Defining The CleanTweet Function
### ----------------------------------------------------------


#Function for cleaning tweets
def tweet_cleaner(tweet):
    
    #1. Souping (Converting to lxml)
    soup = BeautifulSoup(tweet, 'lxml')
    souped = soup.get_text()
    
    #2. Removing byte order marks (BOM's)
    try:
        bom_removed = souped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        bom_removed = souped
    
    #3. Removing '@' and 'https'
    stripped = re.sub(combined_pat, '', bom_removed)
    
    #4. Removing 'www'
    stripped = re.sub(www_pat, '', stripped)
    
    #5. Converting to lower case
    lower_case = stripped.lower()
    
    #6. Replacing negative words from negative dictionary
    neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case)
    
    #7. Removing unnecessary Characters
    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)
    
    #8. Taking out Words from the text
    words = [x for x  in tok.tokenize(letters_only) if len(x) > 1]
    
    #9. Joining words and returning the cleaned tweet
    return (" ".join(words)).strip()


    