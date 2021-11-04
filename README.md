# KU Polls
[![Django CI](https://github.com/tboonma/ku-polls/actions/workflows/django.yml/badge.svg?branch=master)](https://github.com/tboonma/ku-polls/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/tboonma/ku-polls/branch/main/graph/badge.svg?token=2MWQ6V5ND5)](https://codecov.io/gh/tboonma/ku-polls)    
Web application for conducting online polls and surveys in [Kasetsart University](https://www.ku.ac.th/).

## Project Documents
[Vision Statement](../../wiki/Vision%20Statement)    
[Requirements](../../wiki/Requirements)    
[Iteration 1 Plan](../../wiki/Iteration%201%20Plan)   
[Iteration 2 Plan](../../wiki/Iteration%202%20Plan)   
[Iteration 3 Plan](../../wiki/Iteration%203%20Plan)

## Getting Started
### Requirements
|Name  | Recommended version(s)|   
|------|-----------------------|
|Python | 3.7 or higher |
|Django | 2.2 or higher |

### Install Packages
1. Clone this project repository to your machine.

    ```
    git clone https://github.com/tboonma/ku-polls.git
    ```
2. Get into the directory of this repository.

    ```
    cd ku-polls
    ```
3. Create a virtual environment.

    ```
    python -m venv venv
    ```
4. Activate the virtual environment.

    - for Mac OS / Linux.   
    ```
    source venv/bin/activate
    ```
    - for Windows.   
    ```
    venv\Scripts\activate
    ```
5. Install all required packages.

    ```
    pip install -r requirements.txt
    ```
6. Create `.env` file in `mysite/` and write down:

    ```
    DEBUG=True
    SECRET_KEY=Your-Secret-Key
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```
9. Run this command to migrate the database.

    ```
    python manage.py migrate --run-syncdb
    ```
10. Initialize data
    ```
    python3 manage.py loaddata users polls
    ```
12. Start running the server by this command.
    ```
    python manage.py runserver
    ```

## Running KU Polls
Users provided by the initial data (users.json):

| Username  | Password    |
|-----------|-------------|
| demo1     | Vote4me!    |
| demo2     | Vote4me2    |
