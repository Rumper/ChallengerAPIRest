# ChallengerAPIRest

Creation of a simple api, to show knowledge in a Challenge. This project is done in Django.

## Installation

Necessary to have Python 3.5 or higher.

    $ git clone https://github.com/Rumper/ChallengerAPIRest.git

Create virtual machine.

(In case of not having it installed)

    $ sudo pip install virtualenv

Once obtained virtualenv.

    $ cd ChallengerAPIRest
    $ virtualenv Challenger
    $ source bin/activate

Install dependencies.

    (Challenger)$ pip install -r config/requeriments.txt

Create Database.

    (Challenger)$ python manage.py makemigrations
    (Challenger)$ python manage.py migrate

If you want to create superuser but it isn't necessary.

    (Challenger)$ python manage.py createsuperuser

It is ready for operation.

    (Challenger)$ python manage.py runserver

I recommend running the tests.

## Test

Apply the following command to execute the tests.

    (Challenger)$ python manage.py -test

If you want to see test with more details.

    (Challenger)$ python manage.py -test -v 2


## URLS ACTIVE

### /api/1.0/budgets/

METHOD POST

Create a new request in the system, if the email is not registered a new user is created,
your phone or address is updated.

#### Example


    {
      'title': 'Title of the budget request' (optional)),
      'description': 'Description of the budget request',
      'category: 'Category of the budget request '(optional),
      'email': 'User's email',
      'phone': 'User's phone',
      'address': 'User's address'
    }

METHOD GET

Request all system emails.

### /api/1.0/budgets/_email_/

METHOD GET

Request all the emails that are in the system with that user who has said _email_ last in the url.

### /api/1.0/budget/

METHOD POST

Update the title, description or category of the budget request identified by the uuid.

#### Example

    {
       'uuid': 'Budget request identifier',
       'title': 'Title of the budget request' (optional),
       'descripción': 'Description of the budget request' (optional),
       'category: 'Category of the budget request '(optional),
    }


### /api/1.0/budget/_uuid_/

METHOD PUT

Publish the budget request identified by _uuid_ passed in the url. If it is validated, otherwise it reports error.

METHOD DELETE

Discard the budget request identified by _uuid_ passed in the url. If it is validated, otherwise it reports error.

### /api/1.0/suggest_budget/_uuid_/

METHOD GET

Suggest a category or several for the budget request by the identifier _uuid_ passed in the url.

## License

This project is subject to the GPLv3 license see more in LINCENSE.
