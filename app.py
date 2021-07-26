from sqlite3.dbapi2 import connect
from flask import Flask, render_template, request, g, session
import sqlite3
from flask.helpers import url_for
from helpers import get_roles, check_name
from werkzeug.utils import redirect
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "poiujkfepqocjnwoicz"  # This is required by session
app.permanent_session_lifetime = timedelta(hours=5)

# Functions to prepare and utilize the database
def connect_db():
    sql = sqlite3.connect('./rooms.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite3_db'):
        g.sqlite3_db.close()

# These values are prepared for gameplay
winning_number = 0
statement = "Add at least 10 players and then click Create Roles!"  # The statement is updated frequently


@app.route("/join_room", methods=["GET", "POST"]) # If the user is not in session, they will be redirected here
def join_room():
    if request.method == "POST":
        room_name = request.form.get("room_name")
        room_code = request.form.get("room_code")
        db = get_db()
        check_rooms = db.execute("SELECT * FROM rooms WHERE room_name = ?", (room_name,))
        rows = check_rooms.fetchall()

        if len(rows) != 1 or rows[0]["room_code"] != room_code:  # Validate that room exists and code matches
            return render_template("/join_room.html")

        else:
            session['room'] = room_name
            return redirect("/")

    else:
        return render_template("/join_room.html")


@app.route("/leave_room")
def leave_room():
    session.clear()
    return redirect("/join_room")        


@app.route("/", methods = ["GET", "POST"])
def home():
    global statement 
    if 'room' in session:
        
        if request.method == "POST":
            player_name = request.form.get("player_name")  # Get player name
            valid_name_check = check_name(player_name)  # Check if name is not empty

            if valid_name_check:  # Check if name already in dict
                db = get_db()
                sql = "SELECT * FROM {} WHERE name = (?)".format(session["room"])
                cursor = db.execute(sql, (player_name,))
                row = cursor.fetchall()

                if len(row) != 1:  # If the name is not already in the database
                    sql = "INSERT INTO {} (name) VALUES (?)".format(session["room"])
                    db.execute(sql, (player_name,))
                    db.commit()

                    # Get list of players for display
                    sql = "SELECT * FROM {}".format(session["room"])
                    all_players = db.execute(sql)
                    rows = all_players.fetchall()
                    statement = "Add at least 10 players and then click Create Roles!"
                    return render_template("index.html", rows=rows, statement=statement, room=session['room'])

                else:
                    statement = "Name already exists!"
                    return redirect("/")

            else:
                statement = "Invalid Name!"
                return redirect("/")

        else:
            # Get list of players for display
            db = get_db()
            sql = "SELECT * FROM {}".format(session['room'])
            all_players = db.execute(sql)
            rows = all_players.fetchall()
            return render_template("index.html", rows=rows, statement=statement, room=session['room'])

    else:
        return redirect("/join_room")


@app.route("/delete/<name>")
def delete(name):
    if 'room' in session:

        # Delete player from game
        db = get_db()
        sql = "DELETE FROM {} WHERE name=(?)".format(session['room'])
        db.execute(sql,(name,))
        db.commit()

        # When a player is deleted, we must update the Winning Number
        global winning_number
        global statement
        sql = "SELECT COUNT('names') from {}".format(session['room'])
        cursor = db.execute(sql)
        temp_cursor = cursor.fetchone()
        total_player_count = temp_cursor[0]

        # If the player count is now less that 10, prompt user to add more players
        if total_player_count < 10:
            statement = "Add at least 10 players and then click Create Roles!"
            return redirect("/")

        # Otherwise, count the number of Christians remaining,
        roles = get_roles(total_player_count)
        christian_count = 0

        for item in roles:
            if item == "Christian":
                christian_count += 1

        winning_number = (christian_count - 1)  # and subtract 1 from the winning number, because of the deleted player
        statement = "The Winning Number is {}!".format(str(winning_number))
        return redirect('/')

    else:
        return redirect("/join_room")


@app.route("/clear_players")  # This deletes all players from the database and resets the statement
def clear_players():
    if 'room' in session:
        db = get_db()
        sql = "DELETE FROM {}".format(session['room'])
        db.execute(sql)
        db.commit()
        global statement 
        statement = "Add at least 10 players and then click Create Roles!"
        return redirect('/')

    else:
        return redirect('/join_room')


@app.route("/create_roles")  # This creates roles for all players
def create_roles():
    if 'room' in session:    
        db = get_db()
        sql = "SELECT COUNT('names') from {}".format(session["room"])
        cursor = db.execute(sql)
        temp_cursor = cursor.fetchone()
        total_player_count = temp_cursor[0]

        if total_player_count < 10:  # If there are less than 10 players, you cannot create roles
            return redirect("/")

        # Next we find the Winning Number
        roles = get_roles(total_player_count)  # This function prepares a list of roles for the players
        christian_count = 0
        for item in roles:
            if item == "Christian":
                christian_count += 1

        global winning_number
        winning_number = (christian_count - 1)
        global statement 
        statement = "The Winning Number is {}!".format(str(winning_number))

        # Then we iterate through roles list and UPDATE each player with role
        sql = "SELECT * FROM {}".format(session["room"])
        cursor = db.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            role = roles.pop()
            sql = "UPDATE {} SET role = (?) WHERE name = (?)".format(session["room"])
            db.execute(sql,(role, row['name'],))
            db.commit()
        return redirect('/')

    else:
        return redirect('/join_room')


@app.route("/info")  # This page explains how to use the app and play the game
def info():
    return render_template("info.html")


if __name__ == '__main__':
    app.run()