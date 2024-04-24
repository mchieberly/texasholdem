"""
Contains the Player class
"""

class Player:
    """A player of the poker game."""
    
    def __init__(self, player_number, chips):
        """Initializes a player object."""
        self.hand = []
        self.num = player_number
        self.chips = chips
        self.current_bet = 0
    
    def bet(self, amount):
        """Bets the specified amount of chips. If there are insufficient chips, go all in."""
        if amount > self.chips:
            return self.all_in()
        self.chips -= amount
        self.current_bet += amount
        return amount
    
    def all_in(self):
        """Player bets all their remaining chips."""
        all_in_amount = self.chips
        self.current_bet += all_in_amount
        self.chips = 0
        return all_in_amount
    
    def fold(self):
        """Discard current cards."""
        self.hand = []
    
    def add_card(self, card):
        """Adds a card."""
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
