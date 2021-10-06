Tweets Collector

Author: Gabriel Nalbandian
email: gabriel.nalbandian94@gmail.com

For this project, I created a tracker that
will use the twitter API and basically gather information on a
given user on a specific range of dates. I wrote this task in python 
along with SQL for the database. For the frontend part of the task, I 
used HTML and CSS with some Javascript. 

Files:
1. api_url.py : main purpose is to connect to the twitter APIs and
get back the data when we run a specific url.
2. config.py : file where I stored all the unnecessary/private data.
(such as pswd for the database or tokens for the twitter API)
3. db_funcs.py : where all the functions that extract/insert data
to the database
4. twitter_tracker.py : is where we have our class 
5. server.py : is our server. I used flask for this task. 
6. static folder contains all the CSS files
7. templates folder contains all the HTML files

How to run the program: run the server.py file