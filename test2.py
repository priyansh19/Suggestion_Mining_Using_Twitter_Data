from tkinter import *
from PIL import ImageTk, Image
import os
import tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt

class SentimentAnalysis:
    def __init__(self):
        self.tweets = []
        self.tweetText = []
    def DownloadData(self):
        consumerKey = 'w4JcsEOK6XFg14wtJGXXVHVYD'
        consumerSecret = 'FdSxxaqQgqB1dvcEucADIqD1kwEHZf8izfeoBmRvWCEFxSOWoD'
        accessToken = '994417184322433025-2xVI05eTyTHkxWaPn3qpjophxPZvsQt'
        accessTokenSecret = 'R7hHaHnvMlK6GOXvLviyyZm0bBiNS0yrNbXWeglPXGGxH'
        
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
        searchTerm = e1.get()
        NoOfTerms = int(e2.get())
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)
        polarity = 0
        positive = 0
        stronglypositive = 0
        negative = 0
        stronglynegative = 0
        neutral = 0
        csvFile = open('results123.csv', 'w')
        csvWriter = csv.writer(csvFile)
        for tweet in self.tweets:
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity  
            if (analysis.sentiment.polarity == 0):  
                neutral += 1
            elif (analysis.sentiment.polarity > 0.0 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                stronglypositive += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= 0.00):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                stronglynegative += 1
        csvWriter.writerow(self.tweetText)
        csvFile.close()
        positive = self.percentage(positive, NoOfTerms)
        stronglypositive = self.percentage(stronglypositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        stronglynegative = self.percentage(stronglynegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)
        polarity = polarity / NoOfTerms
        global res
        if (polarity == 0):
            res = "Neutral"
        elif (polarity > 0 and polarity <= 0.6):
            res = "Positive"
        elif (polarity > 0.6 and polarity <= 1):
            res = "Strongly Positive"
        elif (polarity > -0.6 and polarity <= 0):
            res = "Negative"
        elif (polarity > -1 and polarity <= -0.6):
            res = "Strongly Negative"
            
        self.plotPieChart(positive, stronglypositive, negative, stronglynegative, neutral, searchTerm, NoOfTerms)
        root = Tk()  
        label = Label(root,text = "general result")
        label.grid(row = 0,column = 0)
        label1 = Label(root, text = res)
        label1.grid(row = 0,column = 3)
        label2 = Label(root,text = "percentages : ")
        label2.grid(row = 1,column= 2)
        label3 = Label(root,text = "extremely positive : ")
        label3.grid(row = 2, column = 0)
        label4 = Label(root,text = stronglypositive )
        label4.grid(row = 2, column = 3)
        label5 = Label(root,text = "positive : ")
        label5.grid(row = 3, column = 0)
        label6 = Label(root,text = positive)
        label6.grid(row = 3, column = 3)
        label7 = Label(root,text = "neutral : ")
        label7.grid(row = 4, column = 0)
        label8 = Label(root,text = neutral)
        label8.grid(row = 4, column = 3)
        label9 = Label(root,text = "negative : ")
        label9.grid(row = 5, column = 0)
        label10 = Label(root,text = negative)
        label10.grid(row = 5, column = 3)
        label11 = Label(root,text = "extremely negative : ")
        label11.grid(row = 6,column = 0)
        label12 = Label(root,text = stronglynegative)
        label12.grid(row = 6, column = 3)
        button = Button(root,text = "close",command = root.destroy)
        button.grid(row = 7)
    
    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())  
    
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, stronglypositive, negative, stronglynegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]','Strongly Positive [' + str(stronglypositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Strongly Negative [' + str(stronglynegative) + '%]']
        sizes = [positive, stronglypositive, neutral, negative, stronglynegative]
        colors = ['yellowgreen','darkgreen', 'gold', 'red','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('graph.jpeg')

        
if __name__== "__main__":
    sa=SentimentAnalysis()
    master = Tk()
    Label(master,text='keyword').grid(row = 0)
    Label(master,text='no of tweets').grid(row = 1)
    e1 = Entry(master)
    e2 = Entry(master)
    e1.grid(row = 0,column=1)
    e2.grid(row = 1,column=1)
    but = Button(master,text = "show general result",width = 50 ,command = sa.DownloadData)
    but.grid(row = 2,column = 0)
    button = Button(master, text = 'exit', width = 50, command = master.destroy)
    button.grid(row = 2,column = 1)
    mainloop()