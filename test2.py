# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 07:32:52 2019

@author: Priyansh
"""

import tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
class SentimentAnalysis:
    def __init__(self):
        self.tweets = []
        self.tweetText = []
    def DownloadData(self):
        consumerKey = 'uKVWaoSBGM4injls6rcPhizvZ'
        consumerSecret = 'AOvPPDih7TaQgZLe7V2Wt3xGZE2r8jLzE3EfQI1wuJtOLKlBDt'
        accessToken = '994417184322433025-fTX9RbOBlgYQVHt1AFX8w22e2bdWahY'
        accessTokenSecret = 'DCsrfwrssN24z8mwioZ1OTMtRqY47mERf09f4hGaAjeL6'
        
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
        searchTerm = input("Enter Keyword/Tag to search about: ")
        NoOfTerms = int(input("Enter how many tweets to search: "))
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)
        csvFile = open('result123.csv', 'a')
        csvWriter = csv.writer(csvFile)
        polarity = 0
        positive = 0
        stronglypositive = 0
        negative = 0
        stronglynegative = 0
        neutral = 0
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
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")
        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.6 and polarity <= 0):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")
            
        self.plotPieChart(positive, stronglypositive, negative, stronglynegative, neutral, searchTerm, NoOfTerms)
    
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
        plt.show()
        
if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()        