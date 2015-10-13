# reddit's words of wisdom
Using Markov chains to generate sage advice from reddit comments. 
(Major work in progress)

retrieve_text.py takes command line arguments for the subreddit and the number of pages to get text from. (For example, if you wanted 3 pages from /r/AskReddit, you'd run it with "python retrieve_text.py AskReddit 3")

markov.py takes one command line argument for the subreddit (i.e., "python markov.py AskReddit"). If there's a file with filtered text data in the directory, it reads the data in from the file with the correct name. If not, markov.py will read the text generated from retrieve_text.py and then write the files for later use.
