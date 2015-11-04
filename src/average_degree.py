import os, re, datetime
from sys import argv
import tweets_cleaned


def myfun2(infile, outfile):
    
    # Date time format for reading in timestamp
    tformat = "%a %b %d %H:%M:%S +0000 %Y"
    
    # tweet time window is 60 seconds
    tweet_window = 60
    
    num_nodes = 0      # total number nodes in graph
    num_edges = 0      # sum of edges of all nodes
    avg_degree = 0.00  # ratio of num_edges to num_nodes
    
    # No tweet exists at this point, so time is set to the 'beginning'
    start_time = datetime.datetime(1970, 1, 1, 0, 0, 0)
    
    # This maintains a list of (timestamp, [hashtags]) tuple
    time_hashtags_list = []
    
    # This is the hash graph
    graph = {}
    
    # Open the cleaned tweet file
    with open(infile, 'r') as fr, open(outfile, 'w') as fw:
        # New tweet (or, line) arrives!
        for line in fr:
            if "(timestamp: " in line:
                # Split tweet into message and timestamp
                message, timestamp = line.lower().split("(timestamp: ")
                
                # Clean up timestamp
                timestamp = timestamp.replace(")", '').replace("\n", '')
                
                # Convert timestamp string to datetime time
                try:
                    new_time = datetime.datetime.strptime(timestamp, tformat)
                except ValueError:
                    break
                
                ## Things to do if new_time is larger than start_time by tweet_window seconds
                if (new_time - start_time).seconds > tweet_window:
                    for time_hashtags in time_hashtags_list:
                        # Extract tweet time and hashtags
                        item_time, hashtags = time_hashtags
                        
                        # If tweet time is out of tweet window
                        if (new_time - item_time).seconds > tweet_window:
                            # Remove this entry from list
                            time_hashtags_list.remove(time_hashtags)
                            # More updates are needed due to removal of the entry
                            # For each hashtag in hashtags
                            for hashtag in hashtags:
                                # If this hastag node is in graph
                                if hashtag in graph:
                                    # Save initial number of edges
                                    len_before = len(graph[hashtag])
                                    # Again for each hashtag in hashtags
                                    for item in hashtags:
                                        # Remove edges to other nodes
                                        if item != hashtag:
                                            graph[hashtag].difference_update([item])
                                    # Find updated number of edges
                                    len_after = len(graph[hashtag])
                                    # Update num_edges
                                    num_edges = num_edges + (len_after - len_before)
                                    
                                    # If all edges have been removed
                                    if len_after == 0:
                                        # Remove this node
                                        del graph[hashtag]
                                        # Decrement num_nodes
                                        num_nodes = num_nodes - 1
                                        break # maybe break is not needed
                        else:
                            # Reset beginning of tweet window
                            start_time = item_time
                            break
                
                # Extract new_hashtags, if any, from message
                new_hashtags  = set(re.findall(r"#(\w+)", message))
                
                ## Things to do if more than one new_hashtags are found in tweet
                if len(new_hashtags) >= 2:
                    # Add this tweet info to time_hashtags_list
                    time_hashtags_list.append((new_time, new_hashtags))
                    # For each hashtag in new_hashtags
                    for hashtag in new_hashtags:
                        # If this node does not exist
                        if not hashtag in graph:
                            # Add this node to the graph
                            graph[hashtag] = set()
                            # Increment num_nodes
                            num_nodes = num_nodes + 1
                        # Save initial number of edges
                        len_before = len(graph[hashtag])
                        # Again for each hashtag in new_hashtags
                        for item in new_hashtags:
                            # Add edges to other nodes
                            if item != hashtag:
                                graph[hashtag].update([item])
                        # Find updated number of edges
                        len_after = len(graph[hashtag])
                        # Update num_edges
                        num_edges = num_edges + (len_after - len_before)
                
                # Finally calculate average degree, make sure some nodes exist
                if num_nodes > 0:
                    avg_degree = float(num_edges) / num_nodes
                fw.write('{0:.2f}'.format(avg_degree) + '\n')


if __name__ == "__main__":
    
    infile  = argv[1]              # input file
    outfile = argv[2]              # output file
    
    # generate name for a temp file
    tempfile = outfile.split('/')
    tempfile[-1] = 'temp.txt'
    tempfile = '/'.join(tempfile)
    
    # get cleaned tweets
    tweets_cleaned.myfun1(infile, tempfile)
    
    # calculate average degree
    myfun2(tempfile, outfile)
    
    # remove the temporary file
    if os.path.isfile(tempfile):
        os.remove(tempfile)