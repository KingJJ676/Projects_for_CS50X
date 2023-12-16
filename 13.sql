SELECT DISTINCT(name) FROM people JOIN stars ON people.id = stars.person_id JOIN movies ON movies.id = stars.movie_id WHERE movie_id IN (SELECT movies.id FROM people, stars, movies WHERE stars.person_id = people.id AND movies.id = stars.movie_id AND name = 'Kevin Bacon' AND birth = '1958') AND name NOT IN (SELECT name FROM people WHERE name
 = 'Kevin Bacon' AND birth = '1958');