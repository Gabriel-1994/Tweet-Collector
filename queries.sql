create table users (
     -- this table is for all the users
     id varchar(255),                -- the id of the user on twitter 
     fullName varchar(255) not null, -- their full name   
     account varchar(255) not null,  -- their account
     primary key (account)    
);

create table followers (
     -- this table is specifically for the number of followers along with the date we saved that number
     id int auto_increment,           -- id that increments for the followers table
     num_of_followers int,            -- the number of followers
     day date,                        -- the date in which we saved the number of followers
     account varchar(255) not null,   -- the account which will be our foreign key
     primary key (id),              
     foreign key (account) references users(account)
);

create table twitter_data (
     -- this table is for twitter data
     id int auto_increment,  -- id that increments for the twitter_data table
     num_of_tweets int,      -- number of tweets
     retweets int,           -- muber of retweets
     favorites int,          -- muber of favorites/likes 
     mentions int,           -- muber of mentions
     day date,               -- the date of which we collected all the above data
     primary key (id),
     account varchar(255) not null,
     foreign key (account) references users(account)
)  
