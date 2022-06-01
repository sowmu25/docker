# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import streamlit as st
import streamlit as st
import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import re
from textblob import TextBlob
from nltk.corpus import stopwords
#from textblob import Word
from nltk.stem import WordNetLemmatizer

wordnet=WordNetLemmatizer()

st.write("Chrome Review Vs Rating")
#data_file = st.file_uploader("Upload CSV",type=["csv"])

#st.write(data_file.name)

#df = pd.read_csv(data_file.name)
#st.dataframe(df)

def clean_text(a):
    text=re.sub('[^A-za-z0-9]',' ',a)
    text=text.lower()
    text=text.split(' ')
    text = [wordnet.lemmatize(word) for word in text if word not in (stopwords.words('english'))]
    text = ' '.join(text)
    return text

data_file = st.file_uploader("Upload CSV",type=["csv"])
if data_file is not None:
    #file_details = {"filename":data_file.name, "filetype":data_file.type,"filesize":data_file.size}
    st.write(file_details)
    test = pd.read_csv(data_file,encoding="ISO-8859-1")
    chrome2=test.iloc[0:5000,[0,2,3]]

    
    chrome2['Text'].apply(clean_text)
    chrome2['senti_polar']=chrome2['Text'].apply(lambda x: TextBlob(x).sentiment.polarity )
    chrome2['sentiment'] = chrome2['senti_polar'].apply(lambda x : 'Positive' if x > 0 else ('Negative' if x<0 else 'Neutral'))
    chrome2['sentiment'] = chrome2['sentiment'].replace({'Negative': -1,'Positive': 1, 'Neutral': 0})


    filter=chrome2.loc[(chrome2.senti_polar>0) & (chrome2.Star<3)]
    new=test['ID'].isin(filter['ID'])
    st.write(test[new])
else:
    st.write("file not found")