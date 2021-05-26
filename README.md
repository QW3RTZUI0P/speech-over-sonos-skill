Abandoned project. Contact me or file an issue if you're still interested.
# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/comments.svg" card_color="#222222" width="50" height="50" style="vertical-align:bottom"/> Speech Over Sonos
Lets mycroft speak over your own sonos system! no other speakers necessary

## About
This skill takes mycroft's answers, converts them using the user's tts engine to speech and plays them over the user's sonos speakers. currently a separate server (https://github.com/jishi/node-sonos-http-api) and basic linux command line knowledge are required to set up and utilise this skill.

## Installation
To use this skill you have to have an instance of this Node JS Sonos Server up and running: https://github.com/jishi/node-sonos-http-api. I hope to develop a solution that doesn't require this server anymore in the future, but currently this skill depends on it. The server can be run on the same device as Mycroft runs on or any other device, but please be sure to give it a static ip address. Enter this ip address into the corresponding text field on home.mycroft.ai.
This skill depends on the "placement" value you gave your Mycroft device on home.mycroft.ai. Please be sure you name this value **exactly** like the Sonos speaker that you want Mycroft to utilize.

## Credits
QW3RTZUI0P
https://github.com/jishi/node-sonos-http-api
https://github.com/SoCo/SoCo 

## Category
**Configuration**

## Tags
#Sonos
#Home

