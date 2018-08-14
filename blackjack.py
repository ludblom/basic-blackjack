#!/usr/bin/env python3

# Simple snake game (C) Ludvig Blomkvist under MIT License

import math
import random
import sys


class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def getColor(self):
        return self.color

    def getValue(self):
        return self.value


class Deck:
    def __init__(self, deck):
        self.deck = deck

    def getDeck(self):
        return self.deck

    def draw(self, num):
        drawnCards = []
        if(len(self.deck) != 0):
            for i in range(num):
                drawnCards.append(self.deck.pop())
        else:
            return None

        return drawnCards


class Player:
    def __init__(self):
        self.cards = []
        self.score = 0

    def getCards(self):
        return self.cards

    def addCard(self, card):
        self.cards += card

    def getScore(self):
        return self.score

    def updateScore(self, score):
        self.score += score

    def clearCards(self):
        self.cards = []
        self.score = 0


def printCards(player):
    cards = player.getCards()
    for card in cards:
        print("%s %s" % (card.getColor(), card.getValue()))
    print("Score: " + str(player.getScore()))


def printDealersCards(player):
    cards = player.getCards()
    print("********** Dealer **********")
    print("%s %s" % (cards[0].getColor(), cards[0].getValue()))
    print("%s %s" % (chr(9611), chr(9611)))
    print("Score: " + str(player.getScore()))
    print("****************************")


def calculate(player):
    vals = {"A": 11,
            "J": 10,
            "Q": 10,
            "K": 10}

    for card in player.getCards():
        if(vals.get(card.getValue()) is None):
            player.updateScore(int(card.getValue()))
        else:
            player.updateScore(vals.get(card.getValue()))


def createDeck(decks):
    colors = [chr(9824), chr(9829), chr(9827), chr(9830)]
    dressed = ["J", "Q", "K", "A"]

    fullDeck = []

    numeric = [Card(str(value), color)
               for value in range(2, 11)
               for color in colors]

    dressed = [Card(value, color)
               for value in dressed
               for color in colors]

    deck = numeric + dressed

    for mergeDecks in range(decks):
        fullDeck += deck

    return fullDeck


def shuffleDeckHelper(deck):
    newDeck = []
    for i in range(len(deck)):
        card = random.randint(0, math.floor(len(deck))-1)
        newDeck.append(deck.pop(card))
    return newDeck


def shuffleDeck(deck, numShuffles):
    for shuffles in range(numShuffles):
        deck = shuffleDeckHelper(deck)
    return Deck(deck)


def play(deck):
    dealer = Player()
    player = Player()

    while(len(deck.getDeck()) > 0):
        # Clean round
        dealer.clearCards()
        player.clearCards()

        # Draw cards
        dealer.addCard(deck.draw(2))
        player.addCard(deck.draw(2))

        # Print cards
        calculate(dealer)
        printDealersCards(dealer)

        calculate(player)
        printCards(player)
        print("********************")

        while(input("(D)raw, (s)tay: ") is not "s"):
            calculate(player)
            player.addCard(deck.draw(1))
            printCards(player)


if __name__ == "__main__":
    try:
        decks = int(input("Number of decks [6]: ") or 6)
        shuffles = int(input("Number of shuffles [4]: ") or 4)
    except ValueError:
        print("Please, enter a number. Exiting")
        sys.exit()

    # Create a deck, shuffle them and add it to Deck class
    deck = shuffleDeck(createDeck(decks), shuffles)

    # Play the game
    play(deck)
