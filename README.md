# Movies (SQLITE3)
Week 7 is about learning SQL and implementing it with python.  
In this problem set, I dealt with 13 quesitons(stated below) by selecting data from one or more tables in movies.db.  

## Tables in movies.db
The ```movies``` table has an ```id``` column that uniquely identifies each movie, as well as columns for the ```title``` of a movie and the ```year``` in which the movie was released.  

The ```people``` table also has an ```id``` column, and also has columns for each person’s ```name``` and ```birth``` year.

Movie ratings, meanwhile, are stored in the ```ratings``` table. The first column in the table is ```movie_id```: a foreign key that references the id of the movies table. The rest of the row contains data about the ```rating``` for each movie and the number of ```votes``` the movie has received on IMDb.

Finally, the ```stars``` and ```directors``` tables match people to the movies in which they acted or directed. (Only principal stars and directors are included.) Each table has just two columns: ```movie_id``` and ```person_id```, which reference a specific movie and person, respectively.

## 13 questions to deal with
In ```1.sql```, write a SQL query to list the titles of all movies released in 2008.  
In ```2.sql```, write a SQL query to determine the birth year of Emma Stone.  
In ```3.sql```, write a SQL query to list the titles of all movies with a release date on or after 2018, in alphabetical order.  
In ```4.sql```, write a SQL query to determine the number of movies with an IMDb rating of 10.0.  
In ```5.sql```, write a SQL query to list the titles and release years of all Harry Potter movies, in chronological order.  
In ```6.sql```, write a SQL query to determine the average rating of all movies released in 2012.  
In ```7.sql```, write a SQL query to list all movies released in 2010 and their ratings, in descending order by rating. For movies with the same rating, order them alphabetically by title.  
In ```8.sql```, write a SQL query to list the names of all people who starred in Toy Story.  
In ```9.sql```, write a SQL query to list the names of all people who starred in a movie released in 2004, ordered by birth year.  
In ```10.sql```, write a SQL query to list the names of all people who have directed a movie that received a rating of at least 9.0.  
In ```11.sql```, write a SQL query to list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated.  
In ```12.sql```, write a SQL query to list the titles of all movies in which both Bradley Cooper and Jennifer Lawrence starred.  
In ```13.sql```, write a SQL query to list the names of all people who starred in a movie in which Kevin Bacon also starred.
