"""
Contains the Player class
"""

from src.constants import CARD_WIDTH
import src.game.utilities as utilities

class Player:
    """A player of the poker game."""

    def __init__(self, player_number, chips, pos, screen):
        """Initializes a player object."""
        self.hand = []
        self.num = player_number
        self.chips = chips
        self.current_bet = 0
        self.pos = pos
        self.is_active = True
        
    def draw(self, screen):
        for idx, card in enumerate(self.hand):
            card_pos = (self.pos[0] + idx * (CARD_WIDTH + 5), self.pos[1])
            utilities.draw_card(screen, card.get_key(), card_pos)

    def bet(self, amount, current_highest_bet):
        """Places a bet or raise, considering the minimum required bet."""
        if self.chips <= amount:
            return self.all_in()

        minimum_required_bet = 2 * current_highest_bet if current_highest_bet > 0 else amount
        if amount < minimum_required_bet:
            raise ValueError(f"Bet must be at least twice the current highest bet: {minimum_required_bet}")
        
        self.chips -= amount
        self.current_bet += amount
        return amount
    
    def call(self, current_highest_bet):
        """Matches the current highest bet."""
        if self.chips + self.current_bet < current_highest_bet:
            return self.all_in()
        bet_difference = current_highest_bet - self.current_bet
        self.chips -= bet_difference
        self.current_bet += bet_difference
        return bet_difference
    
    def check(self, current_highest_bet):
        """Checks if no bet is necessary to stay in the game."""
        if self.current_bet < current_highest_bet:
            raise ValueError("Cannot check, there is an active bet.")
        return 0
    
    def all_in(self):
        """Player bets all their remaining chips."""
        all_in_amount = self.chips
        self.chips = 0
        self.current_bet += all_in_amount
        return all_in_amount
    
    def fold(self):
        """Discard current cards and forfeit the round."""
        self.hand = []
        self.is_active = False
    
    def add_card(self, card):
        """Adds a card to the player's hand if not exceeding two cards."""
        if len(self.hand) < 2:
            self.hand.append(card)

    def __str__(self):
        """String representation of the player's hand and chips."""
        temp_hand = list(self.hand)
        if len(temp_hand) == 2:
            if temp_hand[0].rank < temp_hand[1].rank:
                temp_hand[0], temp_hand[1] = temp_hand[1], temp_hand[0]
        hand_description = ', '.join(str(card) for card in temp_hand)
        return f"Player {self.num} with hand: {hand_description}; and chips: {self.chips}"
