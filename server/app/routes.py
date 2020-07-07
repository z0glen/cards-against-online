from flask import jsonify
from flask_socketio import join_room, emit
import sys

from app import app, socketIO
from app.helpers import read_file
from app.game import Game
from app.player import Player

ROOMS = {}  # dict for tracking active games

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
    player = Player(data['name'], curr_game)
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
        player = Player(data['name'], ROOMS[room])
        ROOMS[room].add_player(player)
        emit('set_user', data['name'])
        emit('join_room', {'room': ROOMS[room].to_json()}, room=room)
        print("sent code: " + ROOMS[room].id)
    else:
        emit('error', {'error': "Game not found :("})

@socketIO.on('connect')
def on_connect():
    """When a new user connects"""
    print("User joined!")

@socketIO.on('disconnect')
def on_disconnect():
    """When a user closes the window"""
    # TODO check if user in game and remove
    print("User exited")

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
    print("playCard event received: " + str(data))
    room = data['room']
    if room in ROOMS:
        player = ROOMS[room].find_player_by_name(data['player'])
        print(player)
        # played_cards = ROOMS[room].played_cards[data['player']]
        if data['player'] in ROOMS[room].played_cards:
            ROOMS[room].played_cards[data['player']].append(player.play_card(data['card']))
        else:
            ROOMS[room].played_cards[data['player']] = [player.play_card(data['card'])]
        print(player)
        if ROOMS[room].has_all_played():
            ROOMS[room].state = "judging"
        emit('played_cards', list(ROOMS[room].played_cards.values()), room=room)
        emit('join_room', {'room': ROOMS[room].to_json()}, room=room)
    else:
        print("invalid room: " + room, file=sys.stderr)
        print("available rooms")
        print(str(ROOMS))

@socketIO.on('judgeCard')
def judgeCard(data):
    """When the judge chooses a card to win the round"""
    print("judgeCard event received")
    room = data['room']
    if room in ROOMS:
        ROOMS[room].award_point(data['card'])
        ROOMS[room].state = "active"
        print(ROOMS[room])
        emit('join_room', {'room': ROOMS[room].to_json()}, room=room)

@socketIO.on('joinRoom')
def joinRoom(room):
    """On refresh, need to re-join the socket io room"""
    if room in ROOMS:
        join_room(room)
        emit('join_room', {'room': ROOMS[room].to_json()}, room=room)
