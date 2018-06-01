# SlackGitBot 

**This is slackbot you will have:**

![](https://media.giphy.com/media/QKiWFh7KBfFMzVrt85/giphy.gif)

This is a  slackbot that responds to slash commands and uses Github APIs. It allows users on a channel to post messages to the channel.

**Features**:

1. Receive command: `/xyz here's a message for the channel sent from an anonymous team member`
2. Save the command data in the database (uses Hasura data APIs)
3. Provides the user to details by getting response using git apis
4. This Bot works on 6 slash commands which are deemed to be necessary for a better workflow in a community

This slack bot builds on top the following slack APIs:

1. [https://api.slack.com/custom-integrations/slash-commands](https://api.slack.com/custom-integrations/slash-commands)
2. [https://api.slack.com/interactive-messages](https://api.slack.com/interactive-messages)
3. [https://api.slack.com/methods/chat.postMessage](https://api.slack.com/methods/chat.postMessage)
4. [https://developer.github.com/v3/?](https://developer.github.com/v3/?)

### Codebase structure

All of the code is in one file that you can read at: `microservices/bot/app/src/server.py`

#### slash command callback request URL
 ```http
 POST /helpme
 Content-Type application/x-www-form-urlencoded

 command=/helpme
 text=Bot works on the ...
 ...
 ```

As taken from: [https://api.slack.com/custom-integrations/slash-commands](https://api.slack.com/custom-integrations/slash-commands)

### Deployment guide

Soon to be updated

## Note

If while sending slash commands through the bot you came across error something like this-
![](https://image.ibb.co/iffKDJ/error.png)

It might occur due to two possible reason- 

1.There might be a delay in the Api request. So try to execute the slash command, you will get the result.

2.This might happen if the cluster might be sleeping. Wake him up and execute your command. 
  	
Cluster uri- http://bot.boyishly25.hasura-app.io/

## Support

If you happen to get stuck anywhere, please feel free to mail me at chimpu755@gmail.com. Also, if you find an error or a bug, you can raise an issue [here](https://github.com/Satyabrat35/SlackGitBot).
