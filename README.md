# Christian Guard Assistant
#### Video Demo:  https://youtu.be/MyuovxNGw0Y
#### Description:
##### History
The game Christian Guard is played with secret roles determining which team you are on and if you are the Christian Guard
(the double agent) or not. Previously to assign these secret roles, one person would sit out for a round in order to assign the roles.
The other complication with game creation was deciding how many players should be on each team and what the Winning Number is.
##### Overview
This web app facilitates the in-person game Christian Guard by keeping a list of the players and their secret roles. It allows
users to enter their room with a Room Name and Room Code, in which they can add, delete, and clear players from a visible list.
When 10 players are in the room, the user can Create Roles. This function totals the number of players, does a few calculations
determining how many players should be on each team, how many Christian Guards there should be, and what the Winning Number is.
Then, a list of roles is created, shuffled, and a role is assigned to each player. The list of players is displayed in a Bootstrap
Accordion, which allows each player to tap their name to see their role, then tap their name again to hide.
The Winning Number is shown at the top for every player to see! If a player is deleted from the list, the Winning Number is updated.
##### Files
###### app.py
This is my Flask application that handles the backend of the webpage. It begins with some app configuration and functions created to
use the database. We then see the functions that handle joining and leaving a room. Following is the home function which is consistently
redirected to. This function displays the updated player list in an accordion view. Next we have the functions for deleting and clearing
the full player list and creating roles for the players! Finally the last function displays the Info page.
###### helpers.py
This Python file is imported into app.py to abstract a couple of larger functions. It holds create_roles() which does the calculations
for team creation and creates the list of roles, one of which will be assigned to each player. It also holds check_name() which
just makes sure when a player enters a name, the field isn't empty and the name contains no numbers.
###### layout.html
This HTML file is the backbone for the other HTML files. It contains the Navbar.
###### info.html
This file is the webpage that simply explains how to use this app and how to play the game.
###### join_room.html
This file is the webpage that you are automatically directed to upon entering the site. Here you can enter your Room Name and Code to
enter a game room and play.
###### index.html
This file is the webpage you enter after joining a room, and where everything happens. On this page you can add, delete, and clear players.
You can also create and check players roles to play the game. Finally, you can Leave Room from this page. Which clears your session and brings
you back to Join Room.
###### styles.css
This file holds a few special stylings for a few objects across my webpages.
###### venv Folder
This folder contains everything required to run the virtual environment and deploy this app to Heroku.
###### Procfile
This file is for the serving the app using Gunicorn.
###### requirements.txt
This file is for Gunicorn and Heroku.
###### rooms.db
This is my database that has two tables. "rooms" which holds the Room Names and Codes for joining a room. "CCBC" this is the only room avaiable
right now. This table holds the names and roles of players in the room: CCBC.
###### TODO.txt
This file contains my plans for Phase 2!
##### Design Choices
###### Secret Role View
One of my biggest decisions in design choice was how each player would safely and conviently see their secret role. I originally had each player on
a Bootstrap Card and when they tapped their name, JS would switch their name with their role and vice versa. I switched away from this because it didn't
feel obvious enough, and it is harder to tell that your role is still shown. With an accordion view. It is clear that an accordion fold is open and needs
to be closed before the device is passed along to the next player.
###### Master vs Player View
This choice ties in directly to the Secret Role View choice above. The player list is currently shown in what I describe as Master view. This view shows
and controls all players on the player list. As outlined in my Phase 2 of my TODO file, the Player view would have each player logging into the room, and
also inputting their name at the join room stage. When they enter the room, they would only be shown their role. I ulimately decided on the Master view
because of my time constraint to finish this project. But I've already had a group use the app with Master View only and it worked perfectly!
