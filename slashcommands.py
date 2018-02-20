from flask import Flask, request, jsonify, abort
import urllib.request, json
from slackclient import SlackClient
import os

'''
Built by Lincoln Roth
Project started on February 18, 2018
'''
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Welcome to hackerbot! I run the slash commands'

##Grabs json hosted on github pages, and just puts it into a readable string
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

    return 'To submit your hack go to our devpost page, <http://go.hackPHS.tech/submit>'

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

    #Grabs json hosted on github pages, and just puts it into a readable string
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

@app.route('/mentor', methods=['POST'])
def mentor():
    token = request.form.get('token', None)  # TODO: validate the token
    command = request.form.get('command', None)
    text = request.form.get('text', None)
    user_id = request.form.get('user_id', None)

    if not token:
        abort(400)

    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))#needs slack bot token generated for your bot
    hackerbot_id = slack_client.api_call("auth.test")["user_id"]
    slack_client.api_call(
        "chat.postMessage",
        channel='G97J8D6GM',
        text="<@{}>".format(user_id) + " needs help with \"" + text + "\""
    )


    return 'Sent your message, ' + text + ', to the mentors'

@app.route('/say', methods=['POST'])
def say():
        token = request.form.get('token', None)  # TODO: validate the token
        command = request.form.get('command', None)
        text = request.form.get('text', None)
        channel = request.form.get('channel_id', None)
        user_id = request.form.get('user_id', None)

        if not token:
            abort(400)
        with urllib.request.urlopen("https://hackprincetonhs.github.io/hackPHS-2018/admins.json") as url:
            data = json.loads(url.read().decode())
            organizers = "Organizers: \n"
            isAdmin = False
            for i in data["admins"]:
                if i['id'] == user_id:
                    isAdmin = True
                    break
            if isAdmin:
                slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))#needs slack bot token generated for your bot
                hackerbot_id = slack_client.api_call("auth.test")["user_id"]
                slack_client.api_call(
                    "chat.postMessage",
                    channel=channel,
                    text=text
                )
                return 'done'
            else:
                return 'Sorry 😞, only admins can have hackerbot talk for them'
