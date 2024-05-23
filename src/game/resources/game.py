import src.constants as constants
from src.game.resources.deck import Deck
from src.game.resources.player import Player
from src.game.utilities import print_hand_info

from collections import Counter
from itertools import combinations

class Game:
    """Game class for a poker game."""
    
    def __init__(self, players, small_blind_amount=10, big_blind_amount=20, ante_amount=0):
        """Initializes a Game object."""
        self.deck = Deck()
        self.players = players
        self.community_cards = []
        self.pot = 0
        self.small_blind_amount = small_blind_amount
        self.big_blind_amount = big_blind_amount
        self.ante_amount = ante_amount
        self.small_blind_index = 0
        
    def post_blinds_and_antes(self):
        """Post antes and rotate blinds among players."""
        # Post antes
        if self.ante_amount > 0:
            for player in self.players:
                self.pot += player.bet(self.ante_amount)
        
        # Rotate small blind
        num_players = len(self.players)
        small_blind_player = self.players[self.small_blind_index]
        big_blind_player = self.players[(self.small_blind_index + 1) % num_players]

        # Post small and big blinds
        self.pot += small_blind_player.bet(self.small_blind_amount)
        self.pot += big_blind_player.bet(self.big_blind_amount)

        # Rotate the small blind index for the next game
        self.small_blind_index = (self.small_blind_index + 1) % num_players
    
    def deal_hole_cards(self):
        """Deals two cards to each player."""
        for player in self.players:
            player.add_card(self.deck.deal())
            player.add_card(self.deck.deal())
    
    def betting_round(self):
        """Conducts a betting round."""
        for player in self.players:
            bet = player.bet(10)  # Simplified betting logic
            self.pot += bet
    
    def deal_flop(self):
        """Deals the flop after burning a card."""
        self.deck.deal()  # Burn a card
        for _ in range(3):
            self.community_cards.append(self.deck.deal())

    def deal_turn_or_river(self):
        """Deals the turn or the river after burning a card."""
        self.deck.deal()  # Burn a card
        self.community_cards.append(self.deck.deal())
    
    def show_community_cards(self):
        """Returns a formatted string of the community cards."""
        return f"Community Cards: {[str(card) for card in self.community_cards]}"
    
    def evaluate_winner(self):
        hand_scores = {}
        for player in self.players:
            all_cards = player.hand + self.community_cards
            hand_scores[player] = self.rank_hand(all_cards)
        
        # Find the highest score based on hand rank and kicker information
        highest_score = max(hand_scores.values(), key=lambda x: (x[0], x[1]))
        potential_winners = [player for player, score in hand_scores.items() if score == highest_score]

        if len(potential_winners) == 1:
            winner = potential_winners[0]
            hand_info = print_hand_info(highest_score[0], highest_score[1])
            print(f"The winner is {winner} with {hand_info}.")
        else:
            # Check for exact ties, including all kickers
            best_kickers = sorted(hand_scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)
            winning_kickers = best_kickers[0][1][1]
            top_winners = [player for player, score in hand_scores.items() if score[1] == winning_kickers]

            if len(top_winners) == 1:
                winner = top_winners[0]
                kicker_that_decided = next((kicker for kicker in winning_kickers if kicker not in (score[1] for player, score in hand_scores.items() if player != winner)), None)
                hand_info = print_hand_info(highest_score[0][0], highest_score[1])
                print(f"The winner is {winner} with {hand_info} and a {kicker_that_decided} kicker.")
            else:
                print("It's a tie between the following players:")
                for winner in top_winners:
                    hand_info = print_hand_info(highest_score[0], highest_score[1])
                    print(f"{winner} with {hand_info}")
                    
    def rank_hand(self, cards):
        # Get all 5-card combinations
        all_combinations = list(combinations(cards, 5))
        best_rank = None

        for combo in all_combinations:
            hand_rank, kickers = self.evaluate_combination(combo)
            if not best_rank or (hand_rank > best_rank[0] or (hand_rank == best_rank[0] and kickers > best_rank[1])):
                best_rank = (hand_rank, kickers)

        return best_rank

    def evaluate_combination(self, cards):
        values = sorted((card.rank for card in cards), reverse=True)
        suits = [card.suit for card in cards]

        is_flush = len(set(suits)) == 1
        is_straight = all(values[i] - values[i + 1] == 1 for i in range(4)) or values == [14, 5, 4, 3, 2]  # Special case for A-5 straight

        if is_flush and values == [14, 13, 12, 11, 10]:
            return constants.HAND_RANKS["Royal Flush"], values
        elif is_flush and is_straight:
            return constants.HAND_RANKS["Straight Flush"], values
        elif is_straight:
            return constants.HAND_RANKS["Straight"], values
        elif is_flush:
            return constants.HAND_RANKS["Flush"], values

        counts = Counter(values).most_common()
        counts.sort(key=lambda x: (-x[1], -x[0]))  # Sort by count first, then by value

        if counts[0][1] == 4:
            return constants.HAND_RANKS["Four of a Kind"], [counts[0][0], counts[1][0]]
        elif counts[0][1] == 3 and counts[1][1] == 2:
            return constants.HAND_RANKS["Full House"], [counts[0][0], counts[1][0]]
        elif counts[0][1] == 3:
            return constants.HAND_RANKS["Three of a Kind"], [counts[0][0]] + sorted((value for value, count in counts[1:]), reverse=True)
        elif counts[0][1] == 2 and counts[1][1] == 2:
            return constants.HAND_RANKS["Two Pair"], [counts[0][0], counts[1][0]] + [counts[2][0]]
        elif counts[0][1] == 2:
            return constants.HAND_RANKS["One Pair"], [counts[0][0]] + sorted((value for value, count in counts[1:]), reverse=True)
        else:
            return constants.HAND_RANKS["High Card"], values

    def play_round(self):
        """Plays a round of poker."""
        self.community_cards = []
        self.deck.shuffle()
        self.post_blinds_and_antes()
        self.deal_hole_cards()
        self.betting_round()
        self.deal_flop()
        self.betting_round()
        self.deal_turn_or_river()
        self.betting_round()
        self.deal_turn_or_river()
        self.betting_round()
        self.evaluate_winner()
        for player in self.players:
            print(player)
            player.fold()
        self.deck.reset()
        self.pot = 0  # Reset the pot after the round
        
    def deal_test_cards(self, hand1, hand2, hand3):
        self.players[0].add_card(self.deck.deal_specific_cards(hand1[0]))
        self.players[0].add_card(self.deck.deal_specific_cards(hand1[1]))
        self.players[1].add_card(self.deck.deal_specific_cards(hand2[0]))
        self.players[1].add_card(self.deck.deal_specific_cards(hand2[1]))
        self.players[2].add_card(self.deck.deal_specific_cards(hand3[0]))
        self.players[2].add_card(self.deck.deal_specific_cards(hand3[1]))
        
    def deal_test_community_cards(self, cards):
        for card in cards:
            self.community_cards.append(self.deck.deal_specific_cards(card))
        
if __name__ == "__main__":
    players = [Player(1, 1000), Player(2, 1000), Player(3, 1000)]
    game = Game(players)
    for _ in range(10):
        game.play_round()
        print(game.show_community_cards())
        print()
    game.deck.reset()
        
    # players = [Player(1, 1000), Player(2, 1000), Player(3, 1000)]
    # game = Game(players)
    
    # game.community_cards = []
    # game.deck.shuffle()
    # game.post_blinds_and_antes()
    # game.deal_test_cards(((9, "Hearts"), (5, "Spades")), (("King", "Hearts"), ("Jack", "Diamonds")), ((9, "Clubs"), (3, "Clubs")))
    # game.betting_round()
    # game.deal_test_community_cards(((5, "Clubs"), (10, "Spades"), (10, "Diamonds"), ("Ace", "Spades"), ("Ace", "Diamonds")))
    # game.evaluate_winner()
    # for player in game.players:
    #     print(player)
    #     player.fold()
    # print(game.show_community_cards())
    # game.deck.reset()
