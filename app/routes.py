from flask import render_template, flash, redirect, url_for, request, session, make_response, current_app
from app import app
from app.forms import SubmitNameForm
import requests
from time import sleep


IMDB_KEY = app.config['IMDB_KEY']
OMDB_KEY = app.config['OMDB_KEY']

@app.route('/awkward')
def awkward_greeting():
    return "I didn't think you were coming. This is awkward."

@app.route('/')
def index():
    user_address = get_remote_addr()
    app.logger.info('GUEST HAS ARRIVED! ' + user_address)
    return render_template('index.html', title='Away')


@app.route('/getactor', methods=['GET', 'POST'])
def get_actor():
    user_address = get_remote_addr()
    app.logger.info('GUEST READY TO PLAY! ' + user_address)
    form = SubmitNameForm()
    if form.validate_on_submit():
        user_address = get_remote_addr()
        app.logger.info(user_address + ' requested information on ' + form.actorname.data)
        results = search_imdb_with_name(form.actorname.data)
        return results
    return render_template('get_actor.html', title='Get Actor', form=form)
    
@app.route('/dashboard')
def dashboard():
    def generate():
        with open('logs/test-log-handle.log') as f:
            while True:
                yield f.read()
                sleep(1)

    return app.response_class(generate(), mimetype='text/plain')


def search_imdb_with_name(actor_name):
    app.logger.debug('search_imdb_with_name CALLED')
    # search takes in a name and from the response we extract actor_id
    imdb_url = "https://imdb8.p.rapidapi.com/auto-complete?q="
    api_url = imdb_url + actor_name
    headers = {"x-rapidapi-key": IMDB_KEY, "x-rapidapi-host": "imdb8.p.rapidapi.com"}
    response = requests.get(api_url, headers=headers)
    response = response.json()
    return response

def get_remote_addr():
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if address is None:  # pragma: no cover
        address = 'x.x.x.x'

    # DO NOT STORE A USERS COMPLETE IP ADDRESS
    address = address.split('.')
    address[2], address[3] = 'XX', 'XX'
    address = '.'.join(address)

    return address