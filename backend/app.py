from flask import Flask, render_template, request, session, redirect, url_for
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from session_store import SimpleSessionStore
import os
import sys

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')

# Use the existing session store
store = SimpleSessionStore()

# Add parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session or 'session_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    session_id = session['session_id']
    chat_history = store.get_session_messages(session_id)
    if request.method == 'POST':
        message = request.form['message']
        store.add_message(session_id, role='user', content=message)
        chat_history = store.get_session_messages(session_id)
    return render_template('chat.html', chat_history=chat_history, user_id=user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        session['user_id'] = user_id
        # Create a new session for the user
        session_id = store.create_session(user_id=user_id)
        session['session_id'] = session_id
        return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('session_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
