#!/usr/bin/python
#-----------------------------------------------------------------------
# twitter-search
#  - performs a basic keyword search for tweets containing the keywords
#-----------------------------------------------------------------------
# compute the sentiment of each tweet based on the sentiment scores of the terms in the tweet
# The sentiment of a tweet is equivalent to the sum of the sentiment scores for each term in the tweet.
# usage: $ python tweet_sentiment.py <sentiment file> <file containing tweets>
#-----------------------------------------------------------------------

from twitter import *
import csv
import json
import sys

#-----------------------------------------------------------------------
# load our API credentials 
#-----------------------------------------------------------------------
config = {}
execfile("config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
		        auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

#-----------------------------------------------------------------------
# Loop through each of the results, and write its contents to file
#-----------------------------------------------------------------------

def scoredict(sentfile):
    sentfile = sys.argv[1]
    sf = open(sentfile, 'rb')
    # file -> dict (str: int)
    # turns a tab-delimited file ($sentfile) into a dictionary
    scdict = {} # initialize an empty dictionary
    for line in sf:
        term, score  = line.split("\t")  # The file is tab-delimited
        scdict[score] = int(score)  # Convert the score to an integer.
    sf.close()
    return scdict

def main():
    
    sentfile = sys.argv[1]
    sf = open(sentfile)
    keyword = raw_input("> Keyword ...? ")
    query = twitter.search.tweets(q=keyword, lang='en', count=1000)
    scores = scoredict(sf)
    filenametab = "tweetstream-"+keyword+".tsv"
    targettab = open(filenametab, 'wb')
    #read a line
    for line in query["statuses"]:
        #set initial tweet sentiment = 0
        tsent = 0  
        #get the text
        if "text" in line:
            # break the tweet into a list of words and encode
            twlist = line["text"].split()
            twlist=json.dumps(twlist)
            #get a score for each word
            for word in twlist: # for every word in the tweet text compute its sentiment
                if word in scores:
                    tsent += scores[word]
                    # return tweet sentiment
            myline = '@%s \t %s \t %s \t "%s" \t %s \t %s \n' % (line["user"]["name"], line["retweeted"], line["is_quote_status"], line["text"], keyword, tsent)
            #target.write("@%s" % line["user"]["name"])
            #target.write("\t"+"%r"+"\t"+" %s" % (line["retweeted"], line["text"]))
            #target.write("\t"+keyword+"\n"
            targettab.write(myline.encode("utf-8"))
            print (myline.encode("utf-8"))
            print ("twlist",twlist)
            print ("tsent", tsent)
        
if __name__ == '__main__':
    main()