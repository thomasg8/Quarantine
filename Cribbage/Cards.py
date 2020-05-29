import pygame
from random import shuffle
from os import listdir
import numpy as np


class Cards():
    def __init__(self, card_width=150, card_height=231):
        """A deck of cards.
            - imgs: a dictionary mapping from card name to card img
            - card_back_img: the image of the back of a card
            - deck: a list of 52 cards
            - remaining: the non-used cards of a given deck
            - used: the used cards of a given deck
            - active_card: the card current action is being taken on"""
        self.imgs = dict(); self.card_width=150; self.card_height=231
        for card in [[c, pygame.transform.scale(pygame.image.load('Cards/'+c),
                (int(card_width), int(card_height)))] for c in listdir('Cards') if '-' in c]:
            self.imgs[card[0].replace('.png',"")] = card[1]
        self.card_back_img = pygame.transform.scale(pygame.image.load('Cards/red.png'),
                (int(card_width), int(card_height)))

        self.deck = list(self.imgs.keys())
        shuffle(self.deck)
        self.remaining = self.deck
        self.used = list()
        self.active_card = None
    def draw_card(self):
        """Grabs the top card off of the remaining deck."""
        self.active_card = self.remaining[0]
        self.used.append(self.active_card)
        self.remaining = list(set(self.remaining)-set([self.active_card]))
    def shuffle_cards(self):
        """Resets and shuffles cards"""
        shuffle(self.deck)
        self.active_card = None
        self.remaining = self.deck
        self.used = list()
