import os

from flask import Flask, request
from slackclient import SlackClient

client_id = os.environ['SLACK_CLIENT_ID']
client_secret = os.environ['SLACK_CLIENT_SECRET']
oauth_scope = 'channels:write channels:read'

app = Flask(__name__)


@app.route("/", methods=["GET"])
def pre_install():
    return f'<a href="https://slack.com/oauth/authorize?scope={oauth_scope}&client_id={client_id}">Get access token</a>'


@app.route("/finish_auth", methods=["GET", "POST"])
def post_install():
    auth_response = SlackClient("").api_call(
        "oauth.access",
        client_id=client_id,
        client_secret=client_secret,
        code=request.args['code']
    )
    tok = auth_response['access_token']
    app.logger.info(f'Access token: {tok}')
    return f'<code>{tok}</code>'
