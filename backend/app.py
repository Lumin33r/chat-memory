

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from session_store import SimpleSessionStore

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')

# Use the existing session store
store = SimpleSessionStore()

# Add parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Route to start a new chat session
@app.route('/new_chat', methods=['POST'])
def new_chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    session_id = store.create_session(user_id=session['user_id'])
    session['session_id'] = session_id
    return jsonify({'success': True, 'redirect': url_for('chat')})
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


# List all sessions for the current user
@app.route('/sessions', methods=['GET'])
def list_sessions():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    user_id = session['user_id']
    sessions = store.list_sessions(user_id=user_id)
    # Add first message as 'first_message' for each session
    sessions_with_titles = []
    for s in sessions:
        session_data = store.get_session(s['session_id'])
        first_message = ''
        if session_data and session_data.get('messages'):
            first_message = session_data['messages'][0]['content']
        s_copy = dict(s)
        s_copy['first_message'] = first_message
        sessions_with_titles.append(s_copy)
    return jsonify({'sessions': sessions_with_titles})

# Route to load a past session as the active chat session
@app.route('/load_session/<session_id>', methods=['POST'])
def load_session(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    # Optionally, check if the session_id belongs to the user
    sessions = store.list_sessions(user_id=session['user_id'])
    if not any(s['session_id'] == session_id for s in sessions):
        return jsonify({'error': 'Session not found or not authorized'}), 404
    session['session_id'] = session_id
    return jsonify({'success': True, 'redirect': url_for('chat')})

# Route to delete a session
@app.route('/delete_session/<session_id>', methods=['POST'])
def delete_session(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    # Only allow deleting sessions belonging to the user
    sessions = store.list_sessions(user_id=session['user_id'])
    if not any(s['session_id'] == session_id for s in sessions):
        return jsonify({'error': 'Session not found or not authorized'}), 404
    success = store.delete_session(session_id)
    return jsonify({'success': success})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# List all sessions for the current user
@app.route('/sessions', methods=['GET'])
def list_sessions():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    user_id = session['user_id']
    sessions = store.list_sessions(user_id=user_id)
    return jsonify({'sessions': sessions})

# Route to load a past session as the active chat session
@app.route('/load_session/<session_id>', methods=['POST'])
def load_session(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    # Optionally, check if the session_id belongs to the user
    sessions = store.list_sessions(user_id=session['user_id'])
    if not any(s['session_id'] == session_id for s in sessions):
        return jsonify({'error': 'Session not found or not authorized'}), 404
    session['session_id'] = session_id
    return jsonify({'success': True, 'redirect': url_for('chat')})

# Route to delete a session
@app.route('/delete_session/<session_id>', methods=['POST'])
def delete_session(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    # Only allow deleting sessions belonging to the user
    sessions = store.list_sessions(user_id=session['user_id'])
    if not any(s['session_id'] == session_id for s in sessions):
        return jsonify({'error': 'Session not found or not authorized'}), 404
    success = store.delete_session(session_id)
    return jsonify({'success': success})
