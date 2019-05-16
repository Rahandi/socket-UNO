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

tanda = 0

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
        if tanda:
            break
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
        if tanda:
            break
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
    if len(hand) == 0:
        return
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

background = pygame.image.load('assets/bg.png')
background = pygame.transform.scale(background, (1200, 676))
waiting = pygame.image.load('assets/waiting.png')
waiting = pygame.transform.scale(waiting, (1200, 676))
# load asset npc
kiri = pygame.image.load('assets/kiri.png')
kanan = pygame.image.load('assets/kanan.png')
atas = pygame.image.load('assets/atas.png')
kiri2 = pygame.image.load('assets/kiri.png')
kanan2 = pygame.image.load('assets/kanan.png')
atas2 = pygame.image.load('assets/atas.png')
# width, height npc
kiri = pygame.transform.scale(kiri, (90, 120))
kanan = pygame.transform.scale(kanan, (90, 120))
atas = pygame.transform.scale(atas, (120, 90))
kiri2 = pygame.transform.scale(kiri, (90, 120))
kanan2 = pygame.transform.scale(kanan, (90, 120))
atas2 = pygame.transform.scale(atas, (120, 90))

cards = Cards(pygame, screen)
cards.load('assets/PNGs/new/')

submit_button = Button(pygame, screen, 'assets/submit.png', 1050, 600)
start_button = Button(pygame, screen, 'assets/start.png', 831, 465)
draw_button = Button(pygame, screen, 'assets/draw.png', 950, 600)
skip_button = Button(pygame, screen, 'assets/skip.png', 950, 600)

submit_button.scale(94,40)
draw_button.scale(90,40)
skip_button.scale(56,40)

select_color = 0

while(True):
    if game_status == None:
        pygame.display.flip()
        screen.fill([255,255,255])
        screen.blit(waiting, (0, 0))
        if player_id == '0':
            start_button.draw()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if start_button.check_clicked():
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
        if game_status['end']:
            pygame.display.flip()
            screen.fill([255,255,255])
            bg_skor = pygame.image.load('assets/scoreboard.jpg')
            screen.blit(bg_skor, (0, 0))
            user_rank = '1' # font.render(text, False, (0,0,0)) -> get from json data
            user_name = 'yoshi'
            user_score = 978
            screen.blit(user_rank, (500,300))
            screen.blit(user_name, (525,300))
            screen.blit(user_score, (600,300))
            # scoreboard layout
            continue
        pygame.display.flip()
        screen.fill([255,255,255])
        screen.blit(background, (0, 0))
        turn_text = font.render(game_status['turn'] + '\'s turn', False, (0,0,0))
        screen.blit(turn_text, (10,10))
        # posisi kartu npc
        if game_status['total_player'] > 1:
            screen.blit(kiri, (200, 150))
        if game_status['total_player'] > 2:
            screen.blit(atas, (400, 50))
        if game_status['total_player'] > 3:
            screen.blit(kanan, (850, 150))
        if game_status['total_player'] > 4:
            screen.blit(kiri2, (200, 300))
        if game_status['total_player'] > 5:
            screen.blit(atas2, (600, 50))
        if game_status['total_player'] > 6:
            screen.blit(kanan2, (850, 300))

        hand = game_status[username]['cards']
        hand = [cards[text] for text in hand]

        middle = cards[game_status['current']]
        middle.place(570,293)

        if game_status['turn'] == username and (game_status['drawed'] or game_status['error']):
            if game_status['drawed']:
                drawed = cards[game_status['drawed']]
                drawed.scale(2)
                drawed.place(510, 203)
                yes_button = Button(pygame, screen, 'assets/yes.png', 510, 490)
                no_button = Button(pygame, screen, 'assets/no.png', 660, 490)
                yes_button.scale(57, 40)
                no_button.scale(53,40)
                yes_button.draw()
                no_button.draw()
            if game_status['error']:
                error_text = font.render(game_status['error'], False, (0,0,0))
                text_width, text_height = font.size(game_status['error'])
                position = ((width/2) - (text_width/2), (height/2) - (text_height/2))
                screen.blit(error_text, position)
                oke_button = Button(pygame, screen, 'assets/submit.png', 570, (height/2)+(text_height/2)+20)
                oke_button.draw()
        elif select_color == 1:
            yellow = Button(pygame, screen, 'assets/PNGs/new/yellow_free.png', 450, 323)
            blue = Button(pygame, screen, 'assets/PNGs/new/blue_free.png', 550, 323)
            green = Button(pygame, screen, 'assets/PNGs/new/green_free.png', 650, 323)
            red = Button(pygame, screen, 'assets/PNGs/new/red_free.png', 750, 323)
            yellow.scale(60, 90)
            blue.scale(60, 90)
            green.scale(60, 90)
            red.scale(60, 90)
            yellow.draw()
            blue.draw()
            green.draw()
            red.draw()
        elif select_color == 2:
            yellow = Button(pygame, screen, 'assets/PNGs/new/yellow_draw-four.png', 450, 323)
            blue = Button(pygame, screen, 'assets/PNGs/new/blue_draw-four.png', 550, 323)
            green = Button(pygame, screen, 'assets/PNGs/new/green_draw-four.png', 650, 323)
            red = Button(pygame, screen, 'assets/PNGs/new/red_draw-four.png', 750, 323)
            yellow.scale(60, 90)
            blue.scale(60, 90)
            green.scale(60, 90)
            red.scale(60, 90)
            yellow.draw()
            blue.draw()
            green.draw()
            red.draw()
        else:
            render_hand(hand)
            if game_status['draw_flag'] == 0:
                submit_button.draw()
                draw_button.draw()
            else:
                submit_button.draw()
                skip_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if game_status['turn'] == username and (game_status['drawed'] or game_status['error']):
                    if game_status['drawed']:
                        if yes_button.check_clicked():
                            send = 'yes'
                            cards.reset_size()
                            if 'free_wild' in drawed.name:
                                select_color = 1
                            elif 'draw-four_wild' in drawed.name:
                                select_color = 2
                            game_status['drawed'] = None
                            message.put(send)
                        elif no_button.check_clicked():
                            send = 'no'
                            cards.reset_size()
                            message.put(send)
                    if game_status['error']:
                        if oke_button.check_clicked():
                            pass
                elif select_color != 0:
                    if yellow.check_clicked():
                        send = 'yellow'
                        message.put(send)
                        select_color = 0
                    elif blue.check_clicked():
                        send = 'blue'
                        message.put(send)
                        select_color = 0
                    elif green.check_clicked():
                        send = 'green'
                        message.put(send)
                        select_color = 0
                    elif red.check_clicked():
                        send = 'red'
                        message.put(send)
                        select_color = 0
                else:
                    for index in range(len(hand)):
                        if game_status['draw_flag'] == 1:
                            if 'draw-two' in hand[index].name:
                                hand[index].check_clicked()
                            elif 'draw-four' in hand[index].name:
                                hand[index].check_clicked()
                        elif game_status['draw_flag'] == 2:
                            if 'draw-four' in hand[index].name:
                                hand[index].check_clicked()
                        else:
                            hand[index].check_clicked()
                    if game_status['draw_flag'] == 0:
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
                            if 'free_wild' in hand[int(send[-1])].name:
                                select_color = 1
                            elif 'draw-four_wild' in hand[int(send[-1])].name:
                                select_color = 2
                        if draw_button.check_clicked():
                            send = 'draw'
                            message.put(send)
                    else:
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
                            if 'free_wild' in hand[int(send[-1])].name:
                                select_color = 1
                            elif 'draw-four_wild' in hand[int(send[-1])].name:
                                select_color = 2
                        if skip_button.check_clicked():
                            send = 'skip'
                            message.put(send)