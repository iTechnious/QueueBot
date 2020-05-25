# Queue

### A Discord bot that allows you to create an automated voice support channel and more.
---
## Introduction
#### The basic idea behind this bot is to bring those teamspeak-like support queue channels to Discord.  This is how it works: A user joins a specific voice channel on your Discord. This channel will act as a kind of "queue" channel. As soon as the user has joined the channel, all supporters will get a message. After a supporter reacted to that message, the user will be moved to the  voice channel of the supporter.

![No image available](https://itechnious.com/files/queue-bot/open-ticket.png)
#### After a supporter has claimed the ticket by reacting to the message:
![No image available](https://itechnious.com/files/queue-bot/close-ticket.png)
---
## Installation guide

1. Clone the repo: ```git clone https://github.com/AuxiliumCDNG/QueueBot```

2. Rename the file 'sample_config.py' in the 'statics/' folder to 'config.py'

3. Open the config file, paste your Discord bot token and fill in your MySQL data

4. Invite your bot user to your Discord server

5. Start the bot:

	- Linux/macOS:

	```python3 main.py```

	- Windows:

	```python main.py```

---

## Features/Commands (& how to use them)

> The default prefix is '!'. The prefix must always be in front of the command so that the bot knows that this message is addressed to him. Example: !test

#### Testing

-  ```test```: The bot should react to your message and send a message to the channel, if you have configured everything properly.

#### Configuration

> Every configuration command starts with "config". Example: !config prefix -

-  ```config ...```

	-  ```prefix <new-prefix>``` Changes the prefix. Example: !config prefix -

	-  ```queue <channel-id>``` Changes the queue voice channel into which users can join. Supporters will then get an automated message by the bot. Example: !config queue 584823253378400256

	-  ```text <channel-id>``` Defines the channel into which the bot sends the notifications for the supporters. Example: !config text 713385799105773598

	-  ```role <role-id>``` Changes the role that is permitted to claim tickets. In most cases that is the supporter or the moderator role.

	-  ```video <youtube-url>``` The bot will join the queue channel automatically as soon as a user joins. While the user is waiting for a supporter, the bot will play the sound of that YT-Video.