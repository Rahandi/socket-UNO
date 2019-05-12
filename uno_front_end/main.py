import pygame
from card import Cards

def render_hand(hand):
    slide = 50
    x = width/2 - (hand[0].width + ((len(hand)/2) * slide))
    for card in hand:
        y = 420
        if card.status == 1:
            y -= 20
        card.place(x, y)
        x += slide

pygame.init()
width, height = 1366, 720
screen = pygame.display.set_mode((width, height))
screen.fill(0)

deck = pygame.image.load('assets/PNGs/small/card_back_alt.png')
cards = Cards(pygame, screen)
cards.load('assets/PNGs/new/')

while(True):

    pygame.display.flip()
    screen.fill(0)

    screen.blit(deck, (1230,532))
    screen.blit(deck, (1231,532))
    screen.blit(deck, (1232,532))
    screen.blit(deck, (1233,532))
    screen.blit(deck, (1234,532))
    screen.blit(deck, (1235,532))

    hand = [cards[text] for text in ['draw-two_red_1', '2_blue_1', 'draw-two_blue_1', '2_red_1']]

    render_hand(hand)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            for h in hand:
                h.check_clicked()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()