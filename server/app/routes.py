from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_socketio import join_room, emit, send
import uuid
import json

from app import app, socketIO
from app.forms import LoginForm
from app.helpers import read_file
from app.game import Game
from app.player import Player

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
    print("PONG")
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
def on_create(data):
    """Create a game lobby"""
    print("Creating a new game!")
    curr_game = Game()
    # TODO: check for duplicate names
    player = Player(data['name'])
    curr_game.players[data['name']] = player
    ROOMS[curr_game.id] = curr_game
    join_room(curr_game.id)
    emit('set_user', data['name'])
    emit('join_room', {'room': curr_game.to_json()})
    print("sent code: " + curr_game.id)
    print(ROOMS)

@socketIO.on('join')
def on_join(data):
    """Join a game lobby"""
    print("Joining game! code: " + data['room'])
    room = data['room']
    print(ROOMS)
    if room in ROOMS:
        join_room(room)
        #send(ROOMS[room].to_json(), room=room)
        player = Player(data['name'])
        ROOMS[room].players[data['name']] = player
        emit('set_user', data['name'])
        emit('join_room', {'room': ROOMS[room].to_json()}, room=room)
        print("sent code: " + ROOMS[room].id)
    else:
        emit('error', {'error': 'Invalid game code.'})

@socketIO.on('connect')
def on_connect():
    """When a new user connects"""
    print("User joined!")

@socketIO.on('pingServer')
def pingServer(data):
    """Test websocket connection"""
    print(data)

@socketIO.on('setState')
def setState(data):
    """Set the game state"""
    print(data)
    room = data['room']
    if room in ROOMS and data['state'] == 'active':
        ROOMS[room].state = data['state']
        ROOMS[room].draw_black_card()
        ROOMS[room].assign_judge()
        # TODO: rename channel to reflect that it also updates
        emit('join_room', {'room': ROOMS[room].to_json()}, room=room)

@socketIO.on('playCard')
def playCard(data):
    """When a player selects a card for judging"""
    print("playCard event received")
    room = data['room']
    print(room)
    print(ROOMS)
    if room in ROOMS:
        print("playing card")
        player = ROOMS[room].find_player_by_name(data['player'])
        player.play_card(data['card'])
        if (ROOMS[room].has_all_played()):
            ROOMS[room].state = "judging"
        emit('join_room', {'room': ROOMS[room].to_json()}, room=room)
