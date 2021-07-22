from sqlite3.dbapi2 import connect
from flask import Flask, render_template, request, g
import sqlite3
from helpers import get_roles, check_name

from werkzeug.utils import redirect

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('./CSFP/CGA/players.db')
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

win_num = 0
w_n_statement = "Add at least 10 players and then click Create Roles!"

@app.route("/", methods = ["GET", "POST"])
def home():
    global w_n_statement

    if request.method == "POST":
        player_name = request.form.get("player_name")  # Get player name
        valid_name = check_name(player_name) # Check if valid
        if valid_name:
            db = get_db()
            db.execute("INSERT INTO players (name) VALUES (?)", (player_name,))
            db.commit()  # must push this to store in database!
            all_players = db.execute("SELECT * FROM players ORDER BY id DESC")  # Get dict of players
            rows = all_players.fetchall()
            w_n_statement = "Add at least 10 players and then click Create Roles!"
            return render_template("index.html", rows=rows, w_n_statement=w_n_statement)

        else: 
            w_n_statement = "Invalid Name!"
            return redirect("/")

    else:
        db = get_db()
        all_players = db.execute("SELECT * FROM players ORDER BY id DESC")  # Get dict of players
        rows = all_players.fetchall()
        return render_template("index.html", rows=rows, w_n_statement=w_n_statement)

@app.route("/delete/<name>")
def delete(name):
    db = get_db()
    db.execute("DELETE FROM players WHERE name=(?)", (name,))
    db.commit()

    # Produce new win number!
    # Get length of total number of players
    global win_num
    global w_n_statement

    cursor = db.execute("SELECT COUNT('names') from players")
    temp_cursor = cursor.fetchone()

    p_count = temp_cursor[0]  # Total player count

    if p_count < 10:
        w_n_statement = "Add at least 10 players and then click Create Roles!"
        return redirect("/")

    
    roles = get_roles(p_count)

    c_count = 0
    for item in roles:
        if item == "Christian":
            c_count += 1

    
    win_num = (c_count - 1)

    
    w_n_statement = "The Winning Number is {}!".format(str(win_num))

    return redirect('/')

@app.route("/clear_players")
def clear_players():
    db = get_db()
    db.execute("DELETE FROM players")
    db.commit()

    global w_n_statement 
    w_n_statement = "Add at least 10 players and then click Create Roles!"

    return redirect('/')


@app.route("/create_roles")
def create_roles():
    # Get length of total number of players
    db = get_db()
    cursor = db.execute("SELECT COUNT('names') from players")
    temp_cursor = cursor.fetchone()

    p_count = temp_cursor[0]  # Total player count

    if p_count < 10:
        return redirect("/")


    roles = get_roles(p_count)

    # Get winning number!
    c_count = 0
    for item in roles:
        if item == "Christian":
            c_count += 1

    global win_num
    win_num = (c_count - 1)

    global w_n_statement 
    w_n_statement = "The Winning Number is {}!".format(str(win_num))

    # Iterate through list and UPDATE each player with role
    cursor = db.execute("SELECT * FROM players ORDER BY id DESC")
    rows = cursor.fetchall()

    for row in rows:
        role = roles.pop()
        db.execute("UPDATE players SET role = ? WHERE id = ?", (role, row['id'],))
        db.commit()

    return redirect('/')

@app.route("/info")
def info():
    return render_template("info.html")

if __name__ == '__main__':
    app.run()