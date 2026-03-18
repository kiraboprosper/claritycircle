from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE SETUP
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# POLL DATA
poll_data = {
    "Mindset": 10,
    "Finance": 5,
    "Wellness": 3
}

# AI LOGIC
def ai_response(msg):
    msg = msg.lower()
    if "join" in msg:
        return "Click signup to join the Clarity Circle community."
    elif "event" in msg:
        return "Check the calendar section for upcoming events."
    elif "book" in msg:
        return "We recommend Atomic Habits and Deep Work."
    elif "vote" in msg:
        return "Go to polls and click a topic to vote."
    else:
        return "Ask me about topics, books, or events!"

# ROUTES
@app.route('/')
def home():
    return render_template('index.html', poll_data=poll_data, user=session.get("user"))

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
        conn.commit()
        conn.close()

        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid login"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/vote', methods=['POST'])
def vote():
    option = request.json['option']
    if option in poll_data:
        poll_data[option] += 1
    return jsonify(poll_data)

@app.route('/ai', methods=['POST'])
def ai():
    msg = request.json['message']
    return jsonify({"response": ai_response(msg)})

if __name__ == "__main__":
    app.run(debug=True)