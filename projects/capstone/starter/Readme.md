# Casting Agency 

### About the app:
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.
This a simple CRUD app with python flask, angular, and postgres

### instructions:
#### Testing:
navigate to the backend directory and run `pip install -r ./requirements.txt` 
after installing the dependencies run `python test_app.py`
all the test cases are in one file for the purpose of simplification 
#### Running the app:
You can start by manually installing dependencies or by using docker.
##### Installing Using Docker:
**Requirements:** *Docker*  
All you need is to navigate to the project directory and `run docker-compose up` and that's it  
it might take some time to start.
You can access the api through `http://localhost:5000` 
and the frontend app using `http://localhost:4200`

#### Manual installation:
**Requirements:** *python, postgres, nodejs*  
1. Database setup:
    1. you must have `postgreSQL` installed in local machine.
    2. create a database with the name `casting` can be configured see the backend installation.
    3. the database should be accessible on port **`5432`** the default postgreSQL port, it should be accessible by user `postgres` and password `postgres`, user and password can be configured see backend installation.  
2. Backend setup:
    1. you must have `python >= 3.7` installed on the local machine.
    2. navigate to the backend directory and run `pip install -r ./requirements.txt` to install project dependencies.
    3. a `.env` file is present for default configuration for the environment variables, the following can be changed:
        1. `FLASK_APP=app.py`.
        2. `POSTGRES_USER` the postgres user defined in database setup section default is `postgres`.
        3. `POSTGRES_PASSWORD` the postgres password defined in database setup section default is `postgres`.
        4. `POSTGRES_DB` the postgres database name defined in database setup section default is `casting`.
    4. the database is updated and seeded on startup.
    5. run the command `flask run` to start the api app server.
3. frontend setup:
    1. you must have `nodejs` installed in the local machine.
    2. you must have `@angular/cli` installed or run the command `npm i @angular/cli@10.0.8`
    3. run the command `npm install` to install project dependencies
    4. run the command `npm start` to start the angular server and navigate to `http://localhost:4200` to view and interact with the app, the app assumes the backend api to be running on port `5000` ie `http://localhost:5000` so make sure that is the case.  
    

## Backend API Reference:
The api has 3 main endpoints movies, artists and roles.
all api endpoints return a main object for the response which look something like this:   
>{  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "success": true,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "message": "request completed successfully",  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "data": could contain object, array of objects, or null,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "status_code": 200  
>}

in case of errors the object looks like this:  
>{  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "success": false,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "message": error description,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "status_code": 404, 400, 500, ...    
>}  

###### Api success response data:
the data property of the success response can be array of objects or a single object containing the data to the requested end point:
1. the movie object:
> {  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'id': movie id,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'name': movie name,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'release_date': movie release date with no time,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'cast': list roles related to the movie,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'description': movie description,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'image': movie poster image  
>}
2. the artist object:
>{  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'id': artist id,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'name': artist name,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'age': artist age,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'gender': artist gender 'Male' or 'Female",  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'movies': list of roles related to this artist,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'description': artist description 'About',  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 'image': artist image  
>}
3. the role object:
>{  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "id": role id,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "artist_id": role related artist id,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "artist": role related artist name,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "movie_id": role related movie id,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "movie": role relate movie name,  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "character": role artist character name  
>}

##### api endpoints:
all end points start with the main endpoint  prefix eg. **GET** `movies/:id`, **POST** `artists/`, **DELETE** `roles/:id`.  
the `:` indicates a variable to be passed to the endpoint.
all **POST** and **DELETE** endpoints require Authorization, which is available using the frontend app with permitted users.  
all **POST** and **DELETE** endpoints returns status code 403 if the user making the request is not permitted.  
all **POST** endpoints require data in the request body.  
all endpoints returns status_code 500 in case of any server error.
1. movies endpoints:
    1. **GET** methods:
        1. **GET** `/movies/` get movies list returns:
            1. status code 404 if no movies found.
            2. a list of all movies as movie objects.
        2. **GET** `/movies/:id` get movie by id returns:
            1. status code 404 if the movie with the id supplied not found.
            2. the requested movie object.
        3. **GET** `movies/names` get movies names list returns:
            1. status code 404 if no movies found.
            2. list of objects with all movies names and ids { 'id': movie id, 'name': movie name }.
    2. **DELETE** methods:
        1. **DELETE** `/movies/:id` delete a movie by id returns:
            1. status code 404 if the movie with supplied id is not found.
            2. status code 200 if the movie deleted successfully.
    3. **POST** methods:
        1. **POST** `/movies/` add a new movie returns:
            1. status code 400 if body is empty.
            1. status code 400 if body is not valid.
            2. the inserted movie object id success.
        2. **POST** `/movies/:id` modify an existing movie returns:
            1. status code 400 if body is empty.
            1. status code 404 if movie is not found.
            1. status code 400 if body is not valid.
            2. the inserted movie object id success.
2. artists endpoints:
    1. **GET** methods:
        1. **GET** `/artists/` get artists list returns:
            1. status code 404 if no artists found.
            2. a list of all artists as artist objects.
        2. **GET** `/artists/:id` get artist by id returns:
            1. status code 404 if the artist with the id supplied not found.
            2. the requested artist object.
        3. **GET** `artists/names` get artists names list returns:
            1. status code 404 if no artists found.
            2. list of objects with all artists names and ids { 'id': artist id, 'name': artist name }.
    2. **DELETE** methods:
        1. **DELETE** `/artists/:id` delete a artist by id returns:
            1. status code 404 if the artist with supplied id is not found.
            2. status code 200 if the artist deleted successfully.
    3. **POST** methods:
        1. **POST** `/artists/` add a new artist returns:
            1. status code 400 if body is empty.
            1. status code 400 if body is not valid.
            2. the inserted artist object id success.
        2. **POST** `/artists/:id` modify an existing artist returns:
            1. status code 400 if body is empty.
            1. status code 404 if artist is not found.
            1. status code 400 if body is not valid.
            2. the inserted artist object id success.
3. roles endpoints:
    1. **GET** methods:
        1. **GET** `/roles/` get roles list returns:
            1. status code 404 if no roles found.
            2. a list of all roles as role objects.
        2. **GET** `/roles/:id` get role by id returns:
            1. status code 404 if the role with the id supplied not found.
            2. the requested role object.
    2. **DELETE** methods:
        1. **DELETE** `/roles/:id` delete a role by id returns:
            1. status code 404 if the role with supplied id is not found.
            2. status code 200 if the role deleted successfully.
    3. **POST** methods:
        1. **POST** `/roles/` add a new role returns:
            1. status code 400 if body is empty.
            1. status code 400 if body is not valid.
            2. the inserted role object id success.
## permissions:
##### Roles
the app has three roles
1. Assistant.
2. Director.
3. Producer.
##### assigned permissions
1. Assistant: the default role can access any and read any data but cannot delete, insert or update .
2. Director: same permission as the *Assistant* but can modify, add and delete new artists and roles.
3. Producer: same permissions as the *Director* but can modify, add and delete movies.