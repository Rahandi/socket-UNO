import pygame
import operator
import socket
import json
import threading
import tkinter
import time
from card import Cards
from button import Button
from queue import LifoQueue

#TKINTER PART
def get_input():
    global input_username, root, username
    username = input_username.get()
    root.destroy()

root = tkinter.Tk()
root.title('Input Your Username')

tkinter.Label(root, text="Username:     ").grid(row=0)
input_username = tkinter.Entry(root)
input_username.focus_set()

input_username.grid(row=0, column=1)

tkinter.Button(root, text='Play', command=get_input).grid(row=2, column=1)

username = ""

root.mainloop()

#SOCKET PART
client = socket.socket()
client.connect(('127.0.0.1', 8443))
message = LifoQueue()
game_status = None
client.send(username.encode('utf-8'))
player_id = client.recv(2048).decode('utf-8')
def send_to_server():
    while True:
        while message.not_empty:
            send_message = {
                'username' : username,
                'action' : message.get()
            }
            client.send(json.dumps(send_message).encode('utf-8'))
            time.sleep(1)

def receive_from_server():
    global game_status
    while True:
        data = client.recv(2048)
        data = data.decode('utf-8')
        data = json.loads(data)
        game_status = data

send = threading.Thread(target=send_to_server)
receive = threading.Thread(target=receive_from_server)
send.start()
receive.start()

#PYGAME PART
def render_hand(hand):
    slide = 25
    x = width/2 - (hand[0].width + ((len(hand)/2) * slide))
    for index in range(len(hand)):
        y = 520
        if hand[index].status == 1:
            y -= 10
        hand[index].place(x, y)
        x += slide
        if index == len(hand)-1:
            hand[index].front = True
        else:
            hand[index].front = False

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

width, height = 1200, 676
screen = pygame.display.set_mode((width, height))
screen.fill(0)

deck = pygame.image.load('assets/PNGs/small/card_back_alt.png')
cards = Cards(pygame, screen)
cards.load('assets/PNGs/new/')

submit_button = Button(pygame, screen, 'assets/submit.png', 1150, 600)
draw_button = Button(pygame, screen, 'assets/submit.png', 1050, 600)

select_color = False

while(True):
    if game_status == None:
        pygame.display.flip()
        screen.fill([255,255,255])
        if player_id == '0':
            submit_button.draw()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if submit_button.check_clicked():
                        send = 'start'
                        message.put(send)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
    else:
        pygame.display.flip()
        screen.fill([255,255,255])
        turn_text = font.render(game_status['turn'], False, (0,0,0))
        screen.blit(turn_text, (0,0))

        hand = game_status[username]['cards']
        hand = [cards[text] for text in hand]

        middle = cards[game_status['current']]
        middle.place(570,293)

        if game_status['turn'] == username and (game_status['drawed'] or game_status['error']):
            if game_status['drawed']:
                drawed = cards[game_status['drawed']]
                drawed.scale(2)
                drawed.place(510, 203)
                yes_button = Button(pygame, screen, 'assets/submit.png', 510, 490)
                no_button = Button(pygame, screen, 'assets/submit.png', 660, 490)
                yes_button.draw()
                no_button.draw()
            if game_status['error']:
                error_text = font.render(game_status['error'], False, (0,0,0))
                text_width, text_height = font.size(game_status['error'])
                position = ((width/2) - (text_width/2), (height/2) - (text_height/2))
                screen.blit(error_text, position)
                oke_button = Button(pygame, screen, 'assets/submit.png', 570, (height/2)+(text_height/2)+20)
                oke_button.draw()
        elif select_color:
            pass
        else:
            render_hand(hand)
            submit_button.draw()
            draw_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if game_status['turn'] == username and (game_status['drawed'] or game_status['error']):
                    if game_status['drawed']:
                        if yes_button.check_clicked():
                            send = 'yes'
                        if no_button.check_clicked():
                            send = 'no'
                        drawed.scale(1)
                        message.put(send)
                    if game_status['error']:
                        if oke_button.check_clicked():
                            pass
                else:
                    for index in range(len(hand)):
                        hand[index].check_clicked()

                    if submit_button.check_clicked():
                        active = {}
                        send = []
                        for index in range(len(hand)):
                            if hand[index].status == 1:
                                active[index] = hand[index].status_time
                        active = sorted(active.items(), key=operator.itemgetter(1))
                        for item in active:
                            send.append(str(item[0]))
                        send = ','.join(send)
                        message.put(send)
                        if 'wild' in hand[int(send[-1])].name:
                            select_color = True
                    if draw_button.check_clicked():
                        send = 'draw'
                        message.put(send)