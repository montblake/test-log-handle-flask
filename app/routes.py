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
    app.logger.warning('GUEST HAS ARRIVED!!!')
    app.logger.info("Request coming from this address: " + request.remote_addr)
    app.logger.info(request.headers['Cookie'])
    session['arrived'] = True
    print(session)
    return render_template('index.html', title='Away')

@app.route('/getactor', methods=['GET', 'POST'])
def get_actor():
    app.logger.warning('GUEST READY TO PLAY!!!')
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if address is None:  # pragma: no cover
        address = 'x.x.x.x'
    address = address.encode('utf-8').split(b',')[0].strip()
    app.logger.warning("START ADDRESS")
    app.logger.warning(address)
    app.logger.warning("START ADDRESS")
    app.logger.info("Request coming from this address: " + request.remote_addr)
    app.logger.info(request.headers['Cookie'])
    # cookie_data = request.headers['Cookie'].split(';')
    # print('cookie_data: ', cookie_data)
    # if len(cookie_data) >= 2:
    #     app.logger.info(cookie_data[2].strip())
    form = SubmitNameForm()
    if form.validate_on_submit():
        app.logger.warning('Info requested for {}'.format(form.actorname.data))
        app.logger.info("Request coming from this address: " + request.remote_addr)
        app.logger.info(request.headers['Cookie'])
        results = search_imdb_with_name(form.actorname.data)
        # flash('Info requested by: {}'.format(
        #     HOW DO I GET THIS DATA HERE
        # ))
        
        
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
    app.logger.info('info requested on actor ' + actor_name)
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
    address = address.encode('utf-8').split(b',')[0].strip()
    return address