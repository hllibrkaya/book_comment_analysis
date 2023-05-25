"""Two separate scorings were made, with or without word roots.
The reason for this is that the inflected language structure of
Turkish can change the positive/negative state of the meaning when it comes to the root of the word.
For example, "beğenmedim" has a negative meaning, while the root "beğenme" has a positive meaning.
Therefore, rooted comments sometimes give better results and sometimes worse results."""



import requests # to send http requests
from bs4 import BeautifulSoup # for extract site data
import pandas as pd #for create dataframe
from transformers import pipeline #for sentiment analysis
#import nltk #for installing the following stopwords and punkt packages
#these are required to be able to use the following two packages
from nltk.tokenize import word_tokenize #needed to split the sentence into tokens
from nltk.corpus import stopwords #for removing stopwords
import re #for manipulating texts
from TurkishStemmer import TurkishStemmer #for rooting words according to Turkish

#nltk.download('stopwords')
#nltk.download('punkt')

#required variables in loop created to get comments on first 50 pages
page_number = 1 
last_page = 50
#lists of book titles and comments
book_names=[]
comment_list=[]

#controlling comment lengths
def check_text_length(sentence):
    #while scoring, the text must be max 512 long.
    if len(sentence)<=512:
        return sentence
    else:
        sentence=sentence[:512]
        return sentence

#Scoring

#bert-based, Turkish-supporting model to analyze sentences
sentiment_analyzer = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")
  
def points(sentence):
    #checking the length of the comments and scoring in the result variable
    sentence=check_text_length(sentence)
    result = sentiment_analyzer(sentence)
    #this model scores as "1 star": 0.332235 when scoring
    #since the other score is not needed, only the label part consisting of stars is returned.
    return result[0]["label"] 

#removing special characters
punctuation ='''{!()-[];':'"\,<>./?@#$%^&*_~}''' #characters that won't make sense when scoring
def special_character_remover(comment):
    # deleting special characters
    return comment.translate(str.maketrans("","",punctuation)) 

#removing stopwords
def stopwords_remover(comment):
    
    stop_words = set(stopwords.words("turkish")) #for finding words that don't make sense in Turkish
    tokens = word_tokenize(comment)  # tokenize sentence into words
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words] #deleting stopwords
    filtered_comment = ' '.join(filtered_tokens)  # rejoining of sentence
    return filtered_comment

#removing emojis
def emoji_remover(comment):
    #commonly used emojis
    emoji = re.compile("["
                               u"\U0001F600-\U0001F64F"  
                               u"\U0001F300-\U0001F5FF"                                 
                               u"\U0001F680-\U0001F6FF"  
                               u"\U0001F1E0-\U0001F1FF"  
                               u"\U00002500-\U00002BEF"                                 
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    
    return emoji.sub(r"",comment) #returning text without emojis

# removing numbers
def remove_numbers(comment):
    cleaned_comment = re.sub(r'\d+', '', comment) #removing numbers, including numbers like 3,456
    return cleaned_comment

#finding roots of words
def find_stems(text):
    stemmer = TurkishStemmer() #creating a turkishstemmer object
    tokens = text.split() #split sentences into a list
    stems = [stemmer.stem(token) for token in tokens] #loop of rooting each word and putting it in the list
    stemmed_text = " ".join(stems) #rejoining  sentence by combining  roots
    return stemmed_text



while page_number <= last_page:
    #finding page url
    books_url = "https://www.idefix.com/kategori/Kitap/Edebiyat/grupno=00055?ShowNotForSale=True&Page="+ str(page_number) + ""
    #extracting page content
    books_request = requests.get(books_url)
    soup = BeautifulSoup(books_request.content, "lxml")
    
    #accessing all books on the page
    books = soup.find_all("div", {"class": "box-title"})
    
    
    #looping in books
    for soup in books:
        #getting book link
        book_link = "https://www.idefix.com/"+soup.a.get("href")
        #extracting book content
        book_request_inside=requests.get(book_link)
        soup2=BeautifulSoup(book_request_inside.content,"lxml")
        #getting the name of the book
        book_name=soup2.find("h3",{"style":"margin-bottom: 10px !important; margin-top: 0px;"}).text.replace('\n',"").strip(" ")
        #finding comments
        reviews=soup2.find_all("div",{"class":"comment"})
        #If a comment has been entered on the book, the following operations will be applied
        if len(reviews)!=0:
            #loop through comments
            for review in reviews:
                #extracting comment text
                comment=review.find(id="reviewBody").text
                
                #Normalizing comments
                clean_comment=comment.lower()
                clean_comment=emoji_remover(clean_comment) #removing some emojis
                clean_comment=special_character_remover(comment) # removing special characters
                clean_comment=remove_numbers(clean_comment) #removing numbers
                clean_comment= stopwords_remover(clean_comment) #removing stopwords
                
                point=points(clean_comment) #scoring
                #rooting and rescoring comments
                clean_comment2=find_stems(clean_comment) #rejoined sentence with roots
                point2=points(clean_comment2) #new score
                #combining all data of the comment into a list
                data=[book_name,comment,clean_comment,point,clean_comment2, point2]
                #list of comments
                comment_list.append(data)
                
                    
      
    page_number += 1

#creating a dataframe from the existing list, naming its columns and writing to excel file
comment_file=pd.DataFrame(comment_list) 
comment_file.columns=["Book Name", "Comment","Clean_Comment","Score","Rooted Comment","Rooted Comment Score"]
comment_file.to_excel("Idefix_Comments.xlsx", index=False)