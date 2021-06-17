# flask-postgres-CRUD

# About
  A basic CRUD application built in flask using postgres as database

# Taks list
- [x] Config files
- [x] Database class/access
- [x] CRUD routes
- [x] Basic frontend files to view application
- [x] Dockerfile
- [x] Initial docker-compose - It is working
- [ ] PyTest - In development
- [ ] CRUD revision - better management
- [ ] Advanced frontend
  - [ ] Bootstrap - CSS framework
  - [ ] JS - framework is being chosen
- [ ] Dockerfile/dockercompose adjusts - It will be necessary because futures features
- [ ] Free hosting on [herokuapp.com/](herokuapp.com/) - Whatever I hosting before done

# How to test now
## Make the following steps to debug this application inside a [docker container](https://docs.docker.com/get-started/)
  ``` 

  [example@example]$ git clone https://github.com/PabloEmidio/flask-postgres-CRUD.git

  [example@example]$ cd flask-postgres-CRUD

  [example@example flask-postgres-CRUD]$ docker-compose build

  [example@example flask-postgres-CRUD]$ docker-compose up -d

  [example@example flask-postgres-CRUD]$ URL="http://127.0.0.1:8088/"; xdg-open $URL || sensible-browser $URL || x-www-browser $URL || gnome-open $URL

  ```

