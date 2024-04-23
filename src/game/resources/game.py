from src.game.resources.deck import Deck
from src.game.resources.player import Player

from collections import Counter

class Game:
    """Game class for a poker game."""
    
    def __init__(self, players):
        """Initializes a Game object."""
        self.deck = Deck()
        self.deck.shuffle()
        self.players = players
        self.community_cards = []
        self.pot = 0
    
    def deal_hole_cards(self):
        for player in self.players:
            player.add_card(self.deck.deal())
            player.add_card(self.deck.deal())
    
    def betting_round(self):
        for player in self.players:
            # Simplified betting logic for demonstration
            bet = player.bet(10)  # Each player bets 10 chips
            self.pot += bet
    
    def deal_flop(self):
        # Burn a card
        self.deck.deal()
        # Deal the flop
        for _ in range(3):
            self.community_cards.append(self.deck.deal())

    def deal_turn_or_river(self):
        # Burn a card
        self.deck.deal()
        # Deal one card
        self.community_cards.append(self.deck.deal())
    
    def show_community_cards(self):
        return f"Community Cards: {[str(card) for card in self.community_cards]}"
    
    def evaluate_winner(self):
        # Evaluates the best hand among players and decides the winner
        scores = {}
        for player in self.players:
            all_cards = player.hand + self.community_cards
            scores[player] = self.rank_hand(all_cards)
        winner = max(scores, key=scores.get)
        print(f"The winner is: {winner} with a score of {scores[winner]}")

    def rank_hand(self, cards):
        """Simple ranking system based on counts of card ranks"""
        rank_counts = {rank: 0 for rank in range(1, 14)}
        for card in cards:
            rank_counts[card.rank] += 1

        pairs = 0
        for count in rank_counts.values():
            if count == 2:
                pairs += 1
        
        if pairs == 1:
            return 2  # One pair
        elif pairs == 2:
            return 3  # Two pair
        else:
            return 1  # High card

    def play_round(self):
        self.deal_hole_cards()
        self.betting_round()
        self.deal_flop()
        self.betting_round()
        self.deal_turn_or_river()
        self.betting_round()
        self.deal_turn_or_river()
        self.betting_round()

        self.evaluate_winner()

        print(self.show_community_cards())
        for player in self.players:
            print(player)

if __name__ == "__main__":
    players = [Player(100), Player(100)]
    game = Game(players)
    game.play_round()
