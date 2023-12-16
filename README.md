# Movies (SQLITE3)
Week 7 is about learning SQL and implementing it with python.  
In this problem set, I dealt with several quesitons by selecting data from one or more tables in movies.db.  

## Tables in movies.db
The ```movies``` table has an ```id``` column that uniquely identifies each movie, as well as columns for the ```title``` of a movie and the ```year``` in which the movie was released.  

The ```people``` table also has an ```id``` column, and also has columns for each person’s ```name``` and ```birth``` year.

Movie ratings, meanwhile, are stored in the ```ratings``` table. The first column in the table is ```movie_id```: a foreign key that references the id of the movies table. The rest of the row contains data about the ```rating``` for each movie and the number of ```votes``` the movie has received on IMDb.

Finally, the ```stars``` and ```directors``` tables match people to the movies in which they acted or directed. (Only principal stars and directors are included.) Each table has just two columns: ```movie_id``` and ```person_id```, which reference a specific movie and person, respectively.
