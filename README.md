This version of this project is currently online at
http://ec2-3-16-29-150.us-east-2.compute.amazonaws.com

# The challenge

1. We want you to create a search engine that can do the following:
* Search within the database with a text query
* Display the players that match the search criteria ( the “searchable”
attributes are: name, club & nationality)
* The displayed attributes for a search result are the following:
  * name
  * age
  * Nationality
  * Club
  * photo (should display it)
  * Overall (score)
  * Value

2. The second feature is a team builder:
* You should create a textfield in the web app where I can input a specific
budget (e.g: $200,000,000) \
  * Once the budget defined, the tool shows me a list of 11 players
that constitute the best team I can have for this specific
budget . Best player is defined from their overall score. (You
can also decide to use other attributes to define the best player if
you wish).

# Installation
Python 3.7.2

1. Clone repository
``` bash
$ git clone https://github.com/wpbdry/phiture-challenge-backend.git
$ cd path/to/new/git/directory
```
2. Checkout into `host-frontend-with-flask` branch
``` bash
$ git checkout origin/host-frontend-with-flask
```
3. Install python dependencies
```bash
$ pip install requirements.txt
```
4. Setup database password \
Create `secret.py` and add the following line
```python
elephantsql_dbpassword = "secret"
```
5. You probably need to change the port that this app serves on \
Edit the following line in `config.py`
```python
flask_port = 80
```

# Run the application
```bash
$ python3 app.py
```