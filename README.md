# challenge-eng-base

This starter kit supports `React` for the frontend and `Python`for the backend.

First, clone the project from Github through: https://github.com/SiddharthMehtaRajendra/MovieSearch.git

IMPORTANT: Make the memory available to your Docker as 4 GB since Elastic Search most likely will require some memory.

Follow the below steps after that,

To get the project up and running:
1. Install Docker https://docs.docker.com/engine/installation/
2. In a terminal, go to the directory `challenge-eng-base-master`
3. For a backend project
    a. `docker-compose up backend`
    b. Test that it's running http://localhost:8080/test
4. For a fullstack project
    a. `docker-compose up backend site`
    b. Test that backend s running http://localhost:8080/test
    c. Test that frontend/site is running http://localhost:8090/test
    d. Test Elastic Search is running using http://localhost:8090/test-es
       The hostname/port may be different for the frontend depending on your
       OS/docker setup. See the log messages from service startup.  
5. First, start by loading the data into MySQL by making an empty (no parameters) POST request to localhost:8080/load-data. This will also index the data in Elastic Search. You may have to wait for around 15-20 minutes for everything to finish loading.
6. After Step 5 finishes successfully, to view the home page of the application, open http://localhost:8090/. On page load, the top 10 most popular titles will be displayed.
7. Feel free to try out searching movie titles using movie title, year or genres or view titles by their average rating.
8. Enjoy the experience of quick searching using elastic search!

To restart the project:

    docker-compose down
    docker-compose up backend or docker-compose up backend site

Starting the backend service automatically starts the mariadb database service
as a dependency.

To see schema changes in the db, remove the old db volume by adding `-v` when
stopping:

    docker-compose down -v

If you run into issues connecting to the db on startup, try restarting (without
the `-v` flag).

To execute the data load cli command:

    docker-compose exec backend flask load-movielens


Code changes should trigger live reload of the docker services in the docker
containers by way of the volume binds specified in the compose file.
