from src import app
from flask import jsonify, request
import requests
import json
import os

slackToken = os.environ['SLACK_TOKEN']
botAccessToken = os.environ['BOT_ACCESS_TOKEN']
hasuraDataUrl = "http://data.hasura/v1/query"
chatUrl = "https://slack.com/api/chat.postMessage"

##################### APIs ######################

@app.route('/', methods=['GET'])
def test():
    return "Slackbot is running."

@app.route('/echo', methods=['POST'])
def event():
    data = request.form.to_dict()
    print(data)
    print("SlackToken: " + slackToken)
    receivedToken = data["token"]
    print("ReceivedToken: " + receivedToken)
    if (receivedToken==slackToken):
        receivedMessage= data["text"]
        id = storeMsgToDB(receivedMessage)
        sendConfirmation(id, receivedMessage, data["response_url"])
        return "Waiting for confirmation"
    else:
        return "Invalid Token"


@app.route('/repo', methods=['POST'])
def repos():
    data = request.form.to_dict()
    print(data)
    print("SlackToken: " + slackToken)
    receivedToken = data["token"]
    print("ReceivedToken: " + receivedToken)
    if (receivedToken==slackToken):
        receivedMessage= data["text"]
        return getRepo(receivedMessage)
    else:
        return "Invalid Token"


@app.route('/issue', methods=['POST'])
def issues():
    data = request.form.to_dict()
    print(data)
    print("SlackToken: " + slackToken)
    receivedToken = data["token"]
    print("ReceivedToken: " + receivedToken)
    if (receivedToken==slackToken):
        receivedMessage= data["text"]
        return getIssue(receivedMessage)
    else:
        return "Invalid Token"


@app.route('/branch', methods=['POST'])
def branches():
    data = request.form.to_dict()
    print(data)
    print("SlackToken: " + slackToken)
    receivedToken = data["token"]
    print("ReceivedToken: " + receivedToken)
    if (receivedToken==slackToken):
        receivedMessage= data["text"]
        return getBranch(receivedMessage)
    else:
        return "Invalid Token"


@app.route('/helpme', methods=['POST'])
def helps():
    data = request.form.to_dict()
    print(data)
    print("SlackToken: " + slackToken)
    receivedToken = data["token"]
    print("ReceivedToken: " + receivedToken)
    if (receivedToken==slackToken):
        receivedMessage= data["text"]
        return getHelp(receivedMessage)
    else:
        return "Invalid Token"


@app.route('/member', methods=['POST'])
def members():
    data = request.form.to_dict()
    print(data)
    print("SlackToken: " + slackToken)
    receivedToken = data["token"]
    print("ReceivedToken: " + receivedToken)
    if (receivedToken==slackToken):
        receivedMessage= data["text"]
        return getMember(receivedMessage)
    else:
        return "Invalid Token"



@app.route('/confirm', methods=['POST'])
def confirm():
    req = request.form.to_dict()
    data = json.loads(req["payload"])
    print (data)
    receivedToken = data["token"]
    channel = data["channel"]["id"]
    if (receivedToken == slackToken):
        if (data["actions"][0]["value"] == "yes"):
            message = fetchFromDBAndSend(data["callback_id"], channel)
            return ("Message Sent: " + str(message))
        else:
            return "Ok. Not sending. :confused:"


##################### Utility functions ######################



def getRepo(text):
    slashparts = text.split('/')
    url = 'https://api.github.com/repos/'+ slashparts[0] + '/' + slashparts[1]
    req = requests.get(url)
    resp = req.json()
    finalstr = ""
    if 'message' not in resp:
        resplist = [resp['language'],str(resp['forks']),str(resp['open_issues']),resp['html_url']]
        strlist = ["Majority of the repo is written in ","No of Forks made ","No of open issues for this repo is ","Check here: "]
        for i in range(0,4):
            strlist[i] = strlist[i] + resplist[i]
        for j in range(0,3):
            finalstr = finalstr + strlist[j] + '\n'
        finalstr = finalstr + strlist[3]
        return finalstr
    else:
        finalstr = "We could not find the result" + '\n' + "Make sure you entered the correct details"
        return finalstr



def getIssue(text):
    slashparts = text.split('/')
    url = 'https://api.github.com/repos/'+ slashparts[0] + '/' + slashparts[1] + '/issues/' + slashparts[2]
    r = requests.get(url)
    resp = r.json()
    finalstr = ""
    if 'message' not in resp:
        resplist = [resp['title'],resp['user']['login'],resp['state'],resp['html_url']]
        strlist = ["Issue title: ","Issue was opened by ","The issue is ","Check here: "]
        for i in range(0,4):
            strlist[i] = strlist[i] + resplist[i]
        for j in range(0,3):
            finalstr = finalstr + strlist[j] + '\n'
        finalstr = finalstr + strlist[3]
        return finalstr
    else:
        finalstr = "We could not find the result" + '\n' + "Make sure that the particular issue exists"
        return finalstr

    
def getHelp(text):
    str1 = "The Bot works on the following Slash commands: \n"
    sl_str = ["/repo <org_name>/<repo_name> \n","/issue <org_name>/<repo_name>/<issue_no> \n","/branch <org_name>/<repo_name>/<branch_name> \n","/member <org_name>"]
    for i in range(0,4):
        str1 = str1 + sl_str[i]
    return str1


def getBranch(text):
    slashparts = text.split('/')
    url = 'https://api.github.com/repos/'+ slashparts[0] + '/' + slashparts[1] + '/branches/' + slashparts[2]
    r = requests.get(url)
    resp = r.json()
    finalstr = ""
    if 'message' not in resp:
        resplist = [resp['commit']['author']['login'],resp['commit']['commit']['message'],resp['commit']['html_url']]
        strlist = ["Author of this branch: ","Message: ","Check here: "]
        for i in range(0,3):
            strlist[i] = strlist[i] + resplist[i]
        for j in range(0,2):
            finalstr = finalstr + strlist[j] + '\n'
        finalstr = finalstr + strlist[2]
        return finalstr
    else:
        finalstr = "We could not find the result" + '\n' + "Are u sure about the typo :confused:??"
        return finalstr


def getMember(text):
    url = 'https://api.github.com/orgs/'+text+'/public_members'
    r = requests.get(url)
    resp = r.json()
    finalstr = ""
    fstr = ""
    if 'message' not in resp:
        i = len(resp)
        for j in range(0,i):
            fstr = fstr + resp[j]['login'] + " "
        finalstr = "Your organisation has " + fstr + "as their public members"
        return finalstr
    else:
        finalstr = "We could not find the result" + '\n' + "Make sure that the particular organisation exists :confused:"
        return finalstr



def sendConfirmation(id, message, responseUrl):
    payload = {
        "text": "Are you sure you want to send a message?",
        "attachments": [
            {
                "text": '"'+message+'"',
                "fallback": "You are indecisive",
                "callback_id": id,
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "yes",
                        "text": "Yep",
                        "type": "button",
                        "value": "yes"
                    },
                    {
                        "name": "no",
                        "text": "Nope",
                        "type": "button",
                        "value": "no"
                    }
                ]
            }
        ]
    }
    headers = {
        'content-type': "application/json",
    }

    response = requests.request("POST", responseUrl, data=json.dumps(payload), headers=headers)
    print(response.text)

def storeMsgToDB(text):
    """
        This function stores 'text' in the database, and
        takes note of the auto-generated unique id for the message.

        The table it stores it in is:
        +-------------------------+----------------+
        | id (auto-increment int) | message (text) |
        +-------------------------+----------------+

        Instead of contacting the postgres database directly 
        this function uses the Hasura Data APIs.

        Try out the data APIs by running this from your terminal:
        $ hasura api-console

        Use the query builder and the API explorer to try out the
        data APIs.
    """
    requestPayload = {
        "type": "insert",
        "args": {
            "table": "slack_messages",
            "objects": [
                {
                    "message": text,
                }
            ],
            "returning": [
                "id"
            ]
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "X-Hasura-User-Id": "1",
        "X-Hasura-Role": "admin"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", hasuraDataUrl, data=json.dumps(requestPayload), headers=headers)
    respObj = resp.json()
    print(respObj)
    id = respObj["returning"][0]["id"]
    return id

def fetchFromDBAndSend(id, channel):
    """
        This function fetches the stored message from the database.

        The table it fetches from is:
        +-------------------------+----------------+
        | id (auto-increment int) | message (text) |
        +-------------------------+----------------+

        Instead of contacting the postgres database directly
        this function uses the Hasura Data APIs.

        Try out the data APIs by running this from your terminal:
        $ hasura api-console

        Use the query builder and the API explorer to try out the
        data APIs.
    """
    requestPayload = {
        "type": "select",
        "args": {
            "table": "slack_messages",
            "columns": [
                "message",
            ],
            "where": {
                "id": {
                    "$eq": id
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "X-Hasura-User-Id": "1",
        "X-Hasura-Role": "admin"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", hasuraDataUrl, data=json.dumps(requestPayload), headers=headers)
    respObj = resp.json()
    print(respObj)
    message = respObj[0]["message"]
    return sendSlackMessage(message, channel)

def sendSlackMessage(message, channel):
    payload = {
        "token": botAccessToken,
        "text": message,
        "channel": channel
    }
    headers = {
        'content-type': "application/json",
        'Authorization': 'Bearer '+botAccessToken
    }

    response = requests.request("POST", chatUrl, data=json.dumps(payload), headers=headers)
    print(response.json())
    return message
