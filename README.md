# Hacktoberfest Dashboard for the Bucharest Meetup

This is a simple dashboard that tracks the number of pull requests made during
a time frame by a set of GitHub users.

## Deployment

        pipenv install
        pipenv shell
        ./manage.py migrate
        ./magage.py collectstatic --no-input
        ./manage.py runserver

