import random
import os

class Game:
    def __init__(self):
        self.deck = []
        self.players = []
        self.turn = 0
        self.draw_stack = 0
        self.draw_flag = 0
        self.current_card = None
        self.clockwise = 1
        self.graveyard = []
        self.rank = {}
        self.start = 0
        self.end = 0

        self.card_types = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'reverse', 'skip', 'draw-two']
        self.card_color = ['green', 'yellow', 'red', 'blue']
        self.wild_cards = ['free_wild', 'draw-four_wild']

    def add_player(self):
        self.players.append([])

    def change_turn(self):
        player_num = len(self.players)
        while True:
            if self.clockwise == 1:
                turn = self.turn + 1
                if turn >= player_num:
                    turn = 0
            elif self.clockwise == -1:
                turn = self.turn - 1
                if turn <= -1:
                    turn = player_num-1
            if len(self.players[turn]) == 0:
                self.turn = turn
            else:
                break
        if self.clockwise == 1:
            self.turn += 1
            if self.turn >= player_num:
                self.turn = 0
        else:
            self.turn -= 1
            if self.turn <= -1:
                self.turn = player_num-1

    def check_cards(self, cards):
        arr_type = []
        t = 0
        for a in range(len(cards)):
            type, _, _ = cards[a].split('_')
            arr_type.append(type)
        for i in range(len(arr_type)):
            if i > 0:
                if arr_type[i] == arr_type[0]:
                    t += 1
        if t == len(arr_type)-1:
            return True
        else:
            return False
            
    def check_cards_current(self, cards):
        current_type, current_color, _ = self.current_card.split('_')
        check_type, check_color, _ = cards[0].split('_')
        if check_color == 'wild':
            return True
        if check_color != current_color and check_type != current_type:
            return False
        return True

    def create_deck(self):
        card_deck = []
        for type in self.card_types:
            for color in self.card_color:
                card = type + '_' + color
                card_deck.append(card + '_1')
                if type != '0':
                    card_deck.append(card + '_2')
        for wild in self.wild_cards:
            for number in range(4):
                card_deck.append(wild + '_' + str(number+1))
        random.shuffle(card_deck)
        self.deck = card_deck

    def do_cards(self, cards, function, *args):
        if not self.check_cards(cards) or not self.check_cards_current(cards):
            print('cards not allowed')
            return False
        type, color, _ = cards[0].split('_')
        change_card = cards[-1]
        print(change_card)
        if color == 'wild':
            color = function(*args)
            change_card = change_card.replace('wild', color)
        print(change_card)
        if type == 'reverse':
            for _ in range(len(cards)):
                self.reverse()
        elif type == 'skip':
            for _ in range(len(cards)):
                self.skip()
        elif type == 'draw-two':
            for _ in range(len(cards)):
                self.draw_two()
        elif type == 'draw-four':
            for _ in range(len(cards)):
                self.draw_four()
        self.current_card = change_card
        return True

    def draw_card(self, player_id, number_of_card):
        if number_of_card >= len(self.deck):
            self.deck.extend(self.graveyard)
            self.graveyard = []
            random.shuffle(self.deck)
        for _ in range(number_of_card):
            popped = self.deck.pop()
            self.players[player_id].append(popped)
        return popped

    def draw_four(self):
        self.draw_stack += 4
        self.draw_flag = 2
        
    def draw_two(self):
        self.draw_stack += 2
        self.draw_flag = 1

    def execute_draw_stack(self):
        self.draw_card(self.turn, self.draw_stack)
        self.draw_stack = 0
        self.draw_flag = 0

    def find_index_cards_by_color(self, cards, colors):
        found = []
        for iterate in range(len(cards)):
            _, color, _ = cards[iterate].split('_')
            if color in colors:
                found.append(iterate)
        return found

    def find_index_cards_by_type(self, cards, types):
        found = []
        for iterate in range(len(cards)):
            type, _, _ = cards[iterate].split('_')
            if type in types:
                found.append(iterate)
        return found

    def reverse(self):
        self.clockwise *= -1

    def show_card(self, cards):
        for card in range(len(cards)):
            print(str(card) + '. ' + cards[card])

    def skip(self):
        self.change_turn()

    def spread_card(self):
        for _ in range(1):
            for iterate in range(len(self.players)):
                self.players[iterate].append(self.deck.pop())

    def starting_card(self):
        while True:
            card = self.deck.pop()
            if 'wild' not in card:
                self.current_card = card
                self.graveyard.append(card)
                return
            self.deck.append(card)
            random.shuffle(self.deck)

    def take_out_card(self, player_id, card_index):
        sorted_index = sorted(card_index, reverse=True)
        for index in sorted_index:
            self.graveyard.append(self.players[player_id].pop(index))
        if len(self.players[player_id]) == 0:
            if player_id not in self.rank:
                count = 0
                for item in self.players:
                    if len(item) != 0:
                        count += 1
                point = (count / len(self.players)) * 100
                self.rank[player_id] = int(point)

if __name__ == '__main__':
    game = Game()
    game.add_player()
    game.add_player()
    game.add_player()
    game.create_deck()
    game.spread_card()
    game.starting_card()
    while True:
        if len(game.rank) == len(game.players) - 1:
            print("The Game is Over !\n")
            print('RANK')
            for i in range(len(game.rank)):
                print(str(i+1) + ": Player " + str(game.rank[i]))
            print(str(len(game.rank)+1) + ": Player " + str(game.turn))
            break

        print('=================================================')
        print('Player ' + str(game.turn) + ' Turn')

        current_player_cards = game.players[game.turn]
        current_card = game.current_card
        current_player = game.turn

        if game.draw_flag != 0:
            if game.draw_flag == 1:
                allowed_index = game.find_index_cards_by_type(current_player_cards, ['draw-two', 'draw-four'])    
            elif game.draw_flag == 2:
                allowed_index = game.find_index_cards_by_type(current_player_cards, ['draw-four'])
            if len(allowed_index) == 0:
                game.execute_draw_stack()
                game.change_turn()
                print('=================================================')
                continue
            allowed_cards = []
            for index in range(len(current_player_cards)):
                if index in allowed_index:
                    allowed_cards.append(current_player_cards[index])
                else:
                    allowed_cards.append('Card not allowed')
            current_player_cards = allowed_cards

        print('Current card: ' + current_card)
        game.show_card(current_player_cards)

        user_input = input('card number: ')
        if game.draw_flag == 0:
            if user_input.lower() == 'draw':
                drawed = game.draw_card(game.turn, 1)
                print('you got ' + drawed)
                if game.check_cards_current([drawed]):
                    user_input = input('you can play the card, would you play it? (y/n) ')
                    if user_input.lower() in ['yes', 'y']:
                        card_number = [len(current_player_cards)-1]
                        game.do_cards([drawed], input, 'color: ')
                        game.take_out_card(current_player, card_number)
                game.change_turn()
                print('=================================================')
                continue
        else:
            if user_input.lower() == 'skip':
                game.execute_draw_stack()
                game.change_turn()
                print('=================================================')
                continue
                
        card_number = [int(item) for item in user_input.split(',')]
        selected_cards = [current_player_cards[int(iterate)] for iterate in card_number]
        
        if game.do_cards(selected_cards, input, 'color: '):
            game.take_out_card(current_player, card_number)
            game.change_turn()
        print('=================================================') []