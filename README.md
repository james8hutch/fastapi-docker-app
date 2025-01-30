# fastapi-docker-app

A very basic POC involving creating some REST methods, that perform CRUD operations to a Postgres DB.
This runs in Docker, and the DB runs in a separate container.

To start this up run ./build.sh
To run the tests run ./cbuild_test.sh (The c is just to allow auto complete to work quicker)

The tests run against a sqllite DB. If I was doing this again, I would probably have a different PostGres instance running in a different Docker, but you live and learn.