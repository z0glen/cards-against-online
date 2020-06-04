from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_socketio import join_room, emit, send
import uuid

from app import app, socketIO
from app.forms import LoginForm
from app.helpers import read_file
from app.game import Game

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J.K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

ROOMS = {} # dict for tracking active games

@app.route("/", methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit() and form.password.data == app.password:
        flash('Logged in')
        return redirect(url_for('game'))
    flash('test')
    return render_template("home.html", form=form)

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/ping")
def ping():
    return jsonify('pong!')

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False

@app.route('/cards')
def get_cards():
    calls = read_file('calls.json')
    responses = read_file('responses.json')
    response_object = {'calls': calls, 'responses': responses}
    return jsonify(response_object)

@socketIO.on('create')
def on_create():
    """Create a game lobby"""
    curr_game = Game()
    ROOMS[curr_game.id] = curr_game
    join_room(curr_game)
    emit('join_room', {'room': curr_game.id})

@socketIO.on('join')
def on_join(data):
    """Join a game lobby"""
    room = data['room']
    if room in ROOMS:
        join_room(room)
        send(ROOMS[room].to_json(), room=room)
    else:
        emit('error', {'error': 'Invalid game code.'})
