# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 14:04:55 2017

@author: Vincent.EC.Lo
"""

#%%


import nltk
import numpy as np
import pandas as pd
import re
import numpy as np
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer




remove_words = ['hi','ok','etc','yes',"against","no"
                ,"its","were","once","about","after"
                ,"yourself","her","too","into","http",
                "us","thank","versus","com","would",
                "thanks","thing","cc","lot","bit","year",
                "even","though","way","day","time"]



def reg_exp(text):
        #### Regular expression
    text = re.sub(r"(http\S+|www\S+|WWW\S+)","", text)
    text = re.sub(r'\[/QUOTE\]'," ",text)
    text = re.sub("(-- hide signature --)(.*)$",'',text)
    text = re.sub('<[^>]*>','',text)
    text = re.sub('[\W]+', ' ',text.lower())
    
    return text
    
    

    
 
def unigram_cleaned_string(text):
        
        
        #### lemmatizer
    lemmatizer = WordNetLemmatizer()
        
        #### stopwords
    stops = set(stopwords.words('english'))
        
        #### Regular expression    
    text_clean = reg_exp(text)
    
    word_list = nltk.word_tokenize(text_clean)

            ### clean before stemmer
    unigrams =  [lemmatizer.lemmatize(w) for w in word_list if w not in stops
                 and w not in remove_words and not w.isdigit()]
        ### clean after stemmer
    unigrams =  [u for u in unigrams if u not in stops
                 and u not in remove_words and len(u)>=2 and len(u)<=20 
                 and not u.isdigit()]
   
    unigram_string = ' '.join(unigrams) 

    return unigram_string

    
#%%
df = pd.read_csv("D://Project2017/word correlation/social_listening_monitor.csv",encoding = 'utf-8')

df.head()
df = df.dropna()

df = df.iloc[0:1000]

df = df[['content']]


#%%

### df subset use & for bitwise 


def pairwise_correlation(word1,word2):
    
    
    def n10(word1,word2):
        return len(df[(df['words'].str.contains(word1)) & (~df['words'].str.contains(word2))])

    def n11(word1,word2):
        return len(df[(df['words'].str.contains(word1)) & (df['words'].str.contains(word2))])    

    def n01(word1,word2):
        return len(df[(~df['words'].str.contains(word1)) & (df['words'].str.contains(word2))])
    
    def n00(word1,word2):
        return len(df[(~df['words'].str.contains(word1)) & (~df['words'].str.contains(word2))])

    
    n1_dot = n10(word1,word2)+n11(word1,word2)    ## n1.
    n0_dot = n01(word1,word2)+n00(word1,word2)    ## n0.
    n_dot0 = n10(word1,word2)+n00(word1,word2)    ## n.0
    n_dot1 = n11(word1,word2)+n01(word1,word2)    ## n.1
    
    phi = (n11(word1,word2)*n00(word1,word2)-n10(word1,word2)*n01(word1,word2))/np.sqrt(n1_dot*n0_dot*n_dot0*n_dot1)
    

    
    return phi
#%%
df['words'] = df['content'].apply(unigram_cleaned_string)

#%%

### Extract 


#%%
word1  = 'great'
word2  = 'sw2700'

pairwise_correlation(word1,word2)
#%%

### df_wordstring must be pandas dataframe with string column

def word_frequency(df_wordstring,remove_list):
    all_words = []
  
    for l in df_wordstring:
        all_words = all_words+nltk.word_tokenize(l)


    all_words = [word for word in all_words if word not in remove_list]
    freqwords = nltk.FreqDist(all_words)
    
    return freqwords.most_common()
    
#%%

word_counts = dict(word_frequency(df["words"],remove_words))
### remove frequency lower than 3  

#%%

df_wordstring = df["words"] 

all_words = []
tokenized_word = nltk.word_tokenize(l)
tokenized_word
#%%

all_words = all_words+tokenized_word 
all_words
#%%















#%%