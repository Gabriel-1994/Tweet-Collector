import pymysql
import api_url
from config import DB_password, DB
from datetime import date, datetime, timedelta

connection = pymysql.connect(    
    host="localhost",
    user="root",
    password=DB_password,
    db=DB,
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
) # connect to mysql

def insert_fullName (account):
    """ Get the id and the full name of the user and insert them in the DB """
    api = api_url.connect_to_tweepy()
    user = api.get_user(account)
    user_id = user.id
    name = user.name

    try:
         with connection.cursor() as cursor:
             query=""" INSERT INTO users (id, fullName,account)
             VALUES (%s,%s,%s)"""
             cursor.execute(query,(user_id, name, account, ))
             connection.commit()
    except:            
            return "ERROR connecting to DATABASE"

    #TODO: instead of always inserting, we should check first if the user is already there. 
    #TODO: so change the query to the same querey as below. 



def insert_followers(account):
    """ Get the foillowers and today's date of the user and insert them in the DB """
    api = api_url.connect_to_tweepy()
    user = api.get_user(account)
    followers = user.followers_count

    today = date.today()
    current_day = today.strftime("%Y-%m-%d")

    try:
         with connection.cursor() as cursor:            
            query = f"INSERT INTO followers (num_of_followers, day, account) select '{followers}','{current_day}', '{account}' " \
                    f"where  not exists (select account from followers where day = '{current_day}' and account = '{account}')" 
            cursor.execute(query)
            connection.commit()
    except pymysql.InternalError as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    except pymysql.IntegrityError as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


def get_data (from_date, to_date, user):
    """ Get the tweets, retweets, and likes of the user and insert them in the DB """    
    tweet_url = "https://api.twitter.com/2/tweets/search/recent?query=from:{}&start_time={}&end_time={}".format(user,from_date,to_date)
    response = api_url.get_response_from_url(tweet_url)
    api = api_url.connect_to_tweepy()
    tweets = response['meta'].get('result_count') # get the number of the tweets from the response of the twitter api
    retweet_count = 0
    fav_count = 0
    for i in response["data"]:                    # looping on all the tweets between the given dates
        status = api.get_status(i['id'])
        retweet_count += status.retweet_count     # getting the retweet count from tweepy
        fav_count += status.favorite_count        # getting the likes count from tweepy
    return tweets, retweet_count, fav_count


def get_mention (from_date, user):
    """ Get the the mentions of the user and insert them in the DB """    
    api = api_url.connect_to_tweepy()    
    account = api.get_user(user)    
    user_id = account.id    # get the twitter id of the user from tweepy (I could have also gotten it with an SQL query)
    mention_url = "https://api.twitter.com/2/users/{}/mentions?max_results=100&start_time={}".format(user_id,from_date)
    mentions = api_url.get_response_from_url(mention_url)
    mentions_count=0
    while (mentions['meta'].get('next_token') != None):
        next_page_url="https://api.twitter.com/2/users/{}/mentions?max_results=100&start_time={}&pagination_token={}".format(user_id,from_date,mentions['meta'].get('next_token'))
        # since we get a max of 100 per page, I used a while loop to go over all the pages and get the mentions count
        mentions = api_url.get_response_from_url(next_page_url)
        mentions_count+= mentions['meta'].get('result_count')
    return mentions_count


def get_num_of_days(from_date, to_date):    
    """ Get the amount of days between the two dates that the user inputed """    
    date_format = "%Y-%m-%d"
    first = datetime.strptime(from_date, date_format)
    last = datetime.strptime(to_date, date_format)
    difference = last - first
    return difference.days    
    

def add_day_to_str(from_date):
    """ add a day to the from_date that the user gave us. I use this function because I save each day along with its data in my data table """    
    from_date = from_date[0:10]    # removes the hours, minutes, and seconds
    date_format = "%Y-%m-%d"
    from_date = datetime.strptime(from_date, date_format)
    from_date += timedelta(days=1) # add one day
    return (str(from_date)[0:10])  # return it as a string
    

def insert_data_to_DB(from_date, to_date, user):
    """ 
    The ideal way to store the data with a given date range is to take day by day.
    In this function, I split the range of the dates to one day at a time and insert the data accordingly.
    """
    num_of_days = get_num_of_days(from_date, to_date) # get the difference of the two dates
    to_date = from_date  # since we will add one day to the from_date and start looping on the num_of_days, we change the to_date to from_date
    while num_of_days >= 0:
        from_date += "T00:00:00Z" # from the beginning of the day
        to_date += "T23:59:59Z"   # until the end of the day

        tweets, retweets, likes = get_data(from_date, to_date, user) # get the data for that day
        mentions = get_mention(from_date, user)                      # get the data for that day

        try: # insert the data for that day
             with connection.cursor() as cursor:
                 query=""" INSERT INTO twitter_data (num_of_tweets, retweets ,favorites,mentions,account,day)
                 VALUES (%s,%s,%s,%s,%s,%s)"""
                 cursor.execute(query,(tweets,retweets,likes,mentions,user,from_date[0:10] ))
                 connection.commit()
        except:            
            return "ERROR connecting to DATABASE"

        num_of_days -= 1 
        from_date = add_day_to_str(from_date) # add a day to our from_date
        to_date = from_date                   # change to_date again


def get_num_followers_today(user, day):  # TODO: name sould be get_num_followers on a specific day  
    """ Get the number of followers from our DB """
    try:
         with connection.cursor() as cursor:
             query=""" SELECT num_of_followers FROM followers WHERE account = %s and day = %s"""
             cursor.execute(query,(user, day ))
             connection.commit()
             result=cursor.fetchone()             
    except:
        result = "ERROR connecting to DATABASE"
    if result == None:
        return 0
    else: 
        return (result.get("num_of_followers"))


def view_data(from_date, to_date, user):
    """ Get all the data from our DB and put them in a list """
    return_list = []
    #----------------------------fullname-------------------------------
    try:
         with connection.cursor() as cursor:
             query=""" SELECT fullName FROM users WHERE account = %s"""
             cursor.execute(query,(user, ))
             connection.commit()
             result=cursor.fetchone()             
    except:
        result = "ERROR connecting to DATABASE"

    fullname = result.get("fullName")    
    return_list.append(fullname)

    #----------------------------followers-------------------------------
    try:
         with connection.cursor() as cursor:
             query=""" SELECT num_of_followers FROM followers WHERE account = %s"""
             cursor.execute(query,(user, ))
             connection.commit()
             result=cursor.fetchone()             
    except:
        result = "ERROR connecting to DATABASE"

    followers = result.get("num_of_followers")
    return_list.append(followers)

    #------------------------all the remaining data-------------------------------
    try:
         with connection.cursor() as cursor:
             query=""" SELECT SUM(num_of_tweets) , SUM(retweets), SUM(favorites), SUM(mentions) FROM twitter_data WHERE account = %s and day between %s and %s"""
             cursor.execute(query,(user, from_date,to_date ))
             connection.commit()
             result=cursor.fetchall()             
    except:
        result = "ERROR connecting to DATABASE"
        
    data_list = result

    tweets = data_list[0]["SUM(num_of_tweets)"]
    return_list.append(tweets)

    retweets = data_list[0]["SUM(retweets)"]
    return_list.append(retweets)

    favorites = data_list[0]["SUM(favorites)"]
    return_list.append(favorites)

    mentions = data_list[0]["SUM(mentions)"]
    return_list.append(mentions)

    # code below is to check and see if we have the followers count of yesterday
    today = date.today()
    yesterday = datetime.now() - timedelta(1)

    yesterday = datetime.strftime(yesterday, '%Y-%m-%d')
    followers_today = get_num_followers_today(user, today)
    followers_yesterday = get_num_followers_today(user, yesterday)

    if followers_yesterday == 0:
        return_list.append("Come back tomorrow to check for the growth!")
    else:        
        return_list.append(followers_today - followers_yesterday)

    return return_list
        
def fetch_all_users():
    """ get all users from our DB """
    try:
         with connection.cursor() as cursor:
             query=""" SELECT account FROM users"""
             cursor.execute(query,( ))
             connection.commit()
             result=cursor.fetchall()             
    except:
        result = "ERROR connecting to DATABASE"
    result_list = []
    for i in result:
        result_list.append(i.get("account"))
    return result_list       
