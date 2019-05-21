from game import Game
from _thread import start_new_thread
from queue import LifoQueue
import socket
import json
import operator

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8443))
server.listen(10)
list_of_client = []
username_to_id = {}
id_to_username = []
game = Game()
message_queue = LifoQueue()
rank = {}

def get_message(turn):
    while True:
        message = message_queue.get()
        if username_to_id[message['username']] == turn:
            print(message)
            return message['action']

def generate_data(error=None, drawed=None):
    data = {}
    data['turn'] = id_to_username[game.turn]
    for index in range(len(id_to_username)):
        data[id_to_username[index]] = {
            'total' : len(game.players[index]),
            'cards' : game.players[index]
        }
    data['total_player'] = len(game.players)
    data['current'] = game.current_card
    data['error'] = error
    data['drawed'] = drawed
    data['draw_flag'] = game.draw_flag
    data['score_board'] = generate_score()
    data['end'] = game.end
    print(data)
    return data

def generate_score():
    used = {}
    for key, value in rank.items():
        if key in username_to_id:
            used[key] = value
    rank_sorted = sorted(used.items(), key=operator.itemgetter(1), reverse=True)
    return rank_sorted

def load_rank():
    global rank
    file = open('rank', 'r')
    rank = json.loads(file.read())
    file.close()

def save_rank():
    file = open('rank', 'w')
    file.write(json.dumps(rank))
    file.close()

def convert_rank():
    for player in id_to_username:
        if player not in rank:
            rank[player] = 0
    for player_id, value in game.rank.items():
        rank[id_to_username[int(player_id)]] += value

def play_game(embo):
    while True:
        if message_queue.not_empty:
            message = message_queue.get()
            if username_to_id[message['username']] == 0:
                if message['action'] == 'start':
                    game.start = 1
                    break
    game.create_deck()
    game.spread_card()
    game.starting_card()
    while True:
        try:
            if len(game.rank) == len(game.players) - 1:
                game.end = 1
                convert_rank()
                save_rank()
                broadcast(generate_data())
                break
            broadcast(generate_data())

            current_player_cards = game.players[game.turn]
            current_player = game.turn

            if game.draw_flag != 0:
                if game.draw_flag == 1:
                    allowed_index = game.find_index_cards_by_type(current_player_cards, ['draw-two', 'draw-four'])
                elif game.draw_flag == 2:
                    allowed_index = game.find_index_cards_by_type(current_player_cards, ['draw-four'])
                if len(allowed_index) == 0:
                    game.execute_draw_stack()
                    game.change_turn()
                    continue

            user_input = get_message(game.turn)
            if game.draw_flag == 0:
                if user_input.lower() == 'draw':
                    drawed = game.draw_card(game.turn, 1)
                    send_drawed = generate_data(drawed=drawed)
                    send_drawed = json.dumps(send_drawed)
                    if game.check_cards_current([drawed]):
                        list_of_client[game.turn].send(send_drawed.encode('utf-8'))
                        user_input = get_message(game.turn)
                        if user_input.lower() in ['yes', 'y']:
                            card_number = [len(current_player_cards)-1]
                            game.do_cards([drawed], get_message, game.turn)
                            game.take_out_card(current_player, card_number)
                    game.change_turn()
                    continue
            else:
                if user_input.lower() == 'skip':
                    game.execute_draw_stack()
                    game.change_turn()
                    continue

            card_number = [int(item) for item in user_input.split(',')]
            selected_cards = [current_player_cards[int(iterate)] for iterate in card_number]

            if game.draw_flag != 0:
                for item in card_number:
                    if item not in allowed_index:
                        sends = generate_data(error='cards not allowed')
                        list_of_client[game.turn].send(json.dumps(sends).encode('utf-8'))
                        continue

            if game.do_cards(selected_cards, get_message, game.turn):
                game.take_out_card(current_player, card_number)
                game.change_turn()
            else:
                sends = generate_data(error='cards not allowed')
                list_of_client[game.turn].send(json.dumps(sends).encode('utf-8'))
        except:
            pass

def client_thread(conn, addr):
    while True:
        try:
            message = conn.recv(2048)
            if message:
                message = message.decode('utf-8')
                message = json.loads(message)
                message_queue.put(message)
            else:
                remove(conn)
        except Exception as e:
            print(e)

def broadcast(message):
    for client in list_of_client:
        try:
            client.send((json.dumps(message)).encode('utf-8'))
        except Exception:
            client.close()
            remove(client)

def remove(conn):
    if conn in list_of_client:
        list_of_client.remove(conn)

start_new_thread(play_game, (1,))
load_rank()
while True:
    conn, addr = server.accept()
    list_of_client.append(conn)
    message = conn.recv(2048)
    message = message.decode('utf-8')
    print(message + ' joined')
    username_to_id[message] = len(username_to_id)
    id_to_username.append(message)
    game.add_player()
    conn.send(str(len(username_to_id)-1).encode('utf-8'))

    start_new_thread(client_thread, (conn, addr))