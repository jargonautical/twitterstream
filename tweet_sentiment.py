import sys
import json

# compute the sentiment of each tweet based on the sentiment scores of the terms in the tweet
# The sentiment of a tweet is equivalent to the sum of the sentiment scores for each term in the tweet.

# usage: $ python tweet_sentiment.py <sentiment file> <file containing tweets>

def hw():
    print 'Hello, world!'

def lines(fp):
    # str -> int
    # reads number of lines in input, prints number as a string
    linenum = len(fp.readlines())
    return linenum

def scoredict(sentfile):
    # file -> dict (str: int)
    # turns a tab-delimited file ($sentfile) into a dictionary
    
    scdict = {} # initialize an empty dictionary
    for line in sentfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scdict[term] = int(score)  # Convert the score to an integer.
    sentfile.close()
    return scdict

def twsentcalc(twlist):
    # list -> int
    # returns the cumulative sentiment value of a list of terms
    # each twlist is now a list containing all the words in a tweet,
    # so we need to compare it against the score in the AFINN dictionary ($scores)
    tsent = 0        # initial tweet sentiment = 0
    for word in twlist: # for every word in the tweet text compute its sentiment
        if word in scores:
            tsent += scores[word]
    # return tweet sentiment
    return tsent

def filescan(line):
    # file -> int
    # turns file into list of tweets and their sentiment
    # calls twsentcalc() on the way

    # parse using json.loads to reveal the dict
    opline = json.loads(line)
    if 'text' in opline:           # if there is no "text" key/value pair, move on to the next one)
        # break the tweet into a list of words and encode
        tl1 = opline['text'].split()
        ts = twsentcalc(tl1)
        return ts
    else:
        return 0

def main():
    # convert AFINN file to global dictionary $scores
    global scores
    sf = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = scoredict(sf) 
    for line in tweet_file:
        print filescan(line)
    tweet_file.close()
    

if __name__ == '__main__':
    main()
