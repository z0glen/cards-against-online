#!/bin/bash
docker build -t registry.heroku.com/still-fortress-86423/web .
docker push registry.heroku.com/still-fortress-86423/web
heroku container:release --app still-fortress-86423 web