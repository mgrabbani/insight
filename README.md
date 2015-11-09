Solution to Insight Data Engineering - Coding Challenge
===========================================================
Below I detail the implementations of the two features. The scripts have also been heavily commented.

## Feature 1: Clean and extract text
Clean and extract text from raw tweets, each represented by JSON format. 

The solution code is the python script, tweets_cleaned.py. It takes location and name of input file containing the tweets and the locationa and name of the output file where the cleaned tweets are to be saved.

The script does the following -
1. Reads each line (tweet) which is in json format and converts the json into a python dict using python module json.
2. If the dict has a field called 'text'-
   * *Then the text is extracted.*
   * *The ascii escape characters are replaced by corresponding replace characters:* 
   
   escape_chars  = ["\'", '\"', '\n', '\t', '\r', '\v', '\a', '\b', '\f', '\/', '\\']
   
   replace_chars = ["'",  '"',  ' ',  ' ',  ' ',  ' ',  ' ',  ' ',  ' ',  '/',  '\\']
   * *The length of the text is saved in len_before*
   * *Each character, ch, in the text having ord(ch) < 128 are kept and other discarded*
   * *Again the length of the text is assigned to len_after*
   * *If the len_after is less than len_before, then a unicode counter is incremented*
   * *Leading and trailing spaces, if any, are also removed*
   * *'created_at' is extracted from the dict*
   * *text and time are saved*

### Notes
1. When the tweets.txt is read in python, I found that the read lines were already in unicode.
The python 'ch in text' (checking if certain character, ch, is in a string, text) does not catch '\/' and '\\', but the when the text (after cleaing other characters) is written to a file, '\/' and '\\' are written as simply '/' and '\'.
2. ord(ch) < 33 did not seem to affect the extracted test, but his could easily be acommodated in the code.

## Feature 2: Calculate the average degree
Calculate the average degree of a vertex in a Twitter hashtag graph

The solution is the python script average_degree.py. This again takes location and name of input tweets file and ouput file containing the running average degree.

First, it calls tweets_cleaned.py to get cleaned tweets saved in a temporay text file.

Some important variables and datastructures are:
* num_nodes: total number nodes in graph
* num_edges: sum of edges of all nodes
* avg_degree: ratio of num_edges to num_nodes
* start_time: initialized to time on 1/1/1970 as a reference but then updated to contain time of oldest tweet
* time_hashtags_list: each item in this list is a 2-tuple of (timestamp, [list of hashtags]). When the latest tweet time is beyond
60 seconds of the first item in this list, the list is scanned from the beggining and tweets that are older than 60 seconds are
removed from this list. The graph (described below) is also updated to reflect removal of nodes and edges.

* graph: is a python dictionary, with the keys being the hastags and the values for key are a **set** of the hashtags the 'key hashtag' is
connected to. In addition to update due to removal of tweets older than 60 seconds, if a a new tweet has two or more hashtags,
graph is updated. If a hashtag is an existing key of the graph dict, the other hastags in the same tweet are added to the set of values for this key.
If the hashtag is not in the keys of the graph, new key empty set for that key is created and and the connected hashtags are saved in the set.
The set length is tracked and num_edges is updated. 

Also node removal and addition triggeres update of num_nodes.
