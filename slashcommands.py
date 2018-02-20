# import your app object
from flask import Flask, request, jsonify, abort
import urllib.request, json

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Welcome to hackerbot! I run the slash commands'

@app.route('/schedule', methods=['POST'])
def schedule():
    """Parse the command parameters, validate them, and respond.
    Note: This URL must support HTTPS and serve a valid SSL certificate.
    """
    # Parse the parameters you need
    token = request.form.get('token', None)  # TODO: validate the token
    command = request.form.get('command', None)
    text = request.form.get('text', None)
    # Validate the request parameters
    if not token:  # or some other failure condition
        abort(400)

    with urllib.request.urlopen("https://hackprincetonhs.github.io/hackPHS-2018/events.json") as url:
        data = json.loads(url.read().decode())
        schedule = "Schedule: \n"
        for i in data["events"]:
            schedule += i["name"]
            schedule += ": "
            schedule += i["time"]
            schedule += "\n"
        print(schedule)
        return schedule

@app.route('/submit', methods=['POST'])
def submit():
    """Parse the command parameters, validate them, and respond.
    Note: This URL must support HTTPS and serve a valid SSL certificate.
    """
    # Parse the parameters you need
    token = request.form.get('token', None)  # TODO: validate the token
    command = request.form.get('command', None)
    text = request.form.get('text', None)
    # Validate the request parameters
    if not token:  # or some other failure condition
        abort(400)

    return 'To submit your hack go to our devpost page, go.hackPHS.tech/submit'

@app.route('/organizers', methods=['POST'])
def organizers():
    """Parse the command parameters, validate them, and respond.
    Note: This URL must support HTTPS and serve a valid SSL certificate.
    """
    # Parse the parameters you need
    token = request.form.get('token', None)  # TODO: validate the token
    command = request.form.get('command', None)
    text = request.form.get('text', None)
    # Validate the request parameters
    if not token:  # or some other failure condition
        abort(400)

    with urllib.request.urlopen("https://hackprincetonhs.github.io/hackPHS-2018/admins.json") as url:
        data = json.loads(url.read().decode())
        organizers = "Organizers: \n"
        for i in data["admins"]:
            organizers += i["name"]
            organizers += ": "
            organizers += i["title"]
            organizers += "\n"
        print(organizers)
        return organizers
