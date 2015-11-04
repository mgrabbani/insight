import json
from sys import argv

def myfun1(infile, outfile):
    
    # Escape characters and their replacements:
    escape_chars  = ["\'", '\"', '\n', '\t', '\r', '\v', '\a', '\b', '\f', '\/', '\\']
    replace_chars = ["'",  '"',  ' ',  ' ',  ' ',  ' ',  ' ',  ' ',  ' ',  '/',  '\\']
    # 'ch in text', where ch is an item from the list escape_chars, check does not
    # find '\/' and '\\' in any tweet text. However, cleaned tweets do not contain them
    # Also I oculd not represent backspace as '\'
    
    # For each tweet, <text> and <time> are replaced by appropriate strings
    output_format = "<text> (timestamp: <time>)"
    
    # This keeps track of number of tweets containing unicodes
    num_unicode = 0
    
    # Open input file as fr and output file as fw
    with open(infile, 'r') as fr, open(outfile, 'w') as fw:
        # For each line (i.e. each tweet)
        for line in fr:
            # Convert from JSON to python dict
            # ***Assumes field values are read as unicode***
            try:
                tweet = json.loads(line)
            except ValueError:
                break
            
            # Check that 'text' field exists
            if 'text' in tweet:
                # Extract value of 'text' field
                text = tweet['text']
                
                # Replace escape characters
                for ii, ch in enumerate(escape_chars):
                    text = text.replace(ch, replace_chars[ii])
                
                # Remove non-ascii unicode characters (those with ord(c) > 127
                len_before = len(text)
                text = ''.join(c for c in text if ord(c) < 128)
                len_after = len(text)
                if len_after < len_before: # True if unicode characters were removed
                    num_unicode = num_unicode + 1 # So increment the counter
                    
                # Also remove leading and trailing spaces
                text = text.strip()  # This may not be a requirement?
                
                # Extract creation time
                c_time = tweet['created_at']
                
                # Write the extracted text and time to the output file in proper format
                fw.write(output_format.replace('<text>', text).replace('<time>', c_time) + '\n')
        
        # Write number of unicode tweets
        fw.write("\n" +str(num_unicode) + " tweets contained unicode.")


if __name__ == "__main__":
    
    infile  = argv[1]              # input file
    outfile = argv[2]              # output file
    
    # get cleaned tweets
    myfun1(infile, outfile)