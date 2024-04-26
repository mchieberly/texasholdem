from src.game.deck import Deck
from src.game.utilities import print_hand_info

from collections import Counter

class Game:
    """Game class for managing poker rounds."""
    
    def __init__(self, players, small_blind_amount=10, big_blind_amount=20, ante_amount=0):
        """Initializes a Game object."""
        self.deck = Deck()
        self.players = players
        self.community_cards = []
        self.pot = 0
        self.side_pots = []
        self.current_highest_bet = 0
        self.small_blind_amount = small_blind_amount
        self.big_blind_amount = big_blind_amount
        self.ante_amount = ante_amount
        self.small_blind_index = 0
        
    def handle_bets(self, player, amount):
        """Handles bet logic including side pot creation for all-in situations."""
        if amount >= player.chips:
            self.create_side_pot(player, amount)
        else:
            self.pot += player.bet(amount)
            self.current_highest_bet = max(self.current_highest_bet, amount)
    
    def create_side_pot(self, player, amount):
        """Create or update side pots when a player goes all-in."""
        all_in_amount = player.all_in()
        self.pot += all_in_amount  # Add the all-in amount to the main pot first

        for sp in self.side_pots:
            if sp['max_contribution'] > player.chips:
                sp['amount'] += player.chips
            else:
                sp['amount'] += sp['max_contribution']

        # Check if a new side pot needs to be created
        existing_contributions = sum(sp['max_contribution'] for sp in self.side_pots if player.chips >= sp['max_contribution'])
        if player.chips > existing_contributions:
            new_side_pot = {
                'amount': player.chips - existing_contributions,
                'players': [p for p in self.players if p.chips > existing_contributions and p.is_active],
                'max_contribution': player.chips
            }
            self.side_pots.append(new_side_pot)

    def evaluate_winner(self):
        # Evaluation logic should now handle side pots
        base_pot_winner = None  # This will be your normal pot evaluation logic
        print(f"The winner for the main pot is {base_pot_winner}")

        for sp in self.side_pots:
            side_pot_winner = None  # This will involve similar logic to your base pot but restricted to the players in 'sp['players']'
            print(f"The winner for the side pot of {sp['amount']} is {side_pot_winner}")
    
    def post_blinds_and_antes(self):
        """Post antes if any and handle blinds rotation among players."""
        ante_amount = 10
        small_blind_amount = 20
        big_blind_amount = 40

        # Collect antes if applicable
        for player in self.players:
            if player.chips > ante_amount:
                # If antes are treated as separate from the normal betting cycle, we might not need current_highest_bet
                self.pot += player.bet(ante_amount, 0)  # Assuming ante doesn't require matching previous bets
            else:
                self.pot += player.all_in()

        # Handle blinds
        num_players = len(self.players)
        small_blind_player = self.players[self.small_blind_index % num_players]
        big_blind_player = self.players[(self.small_blind_index + 1) % num_players]

        # Players post small and big blinds
        # Since blinds start a new betting cycle, small blind doesn't need a higher current_highest_bet.
        self.pot += small_blind_player.bet(small_blind_amount, 0)
        self.current_highest_bet = small_blind_amount  # Update after small blind is posted
        self.pot += big_blind_player.bet(big_blind_amount, self.current_highest_bet)
        self.current_highest_bet = big_blind_amount  # Update after big blind

        # Rotate the small blind index for the next game
        self.small_blind_index = (self.small_blind_index + 1) % num_players
            
    def play_round(self):
        # Clear previous round details
        self.deck.shuffle()
        self.deal_cards()
        self.betting_round()
        # Additional round details like dealing community cards would go here

    def deal_cards(self):
        """Deals two cards to each player."""
        for player in self.players:
            player.add_card(self.deck.deal())
            player.add_card(self.deck.deal())

    def betting_round(self):
        """Handles a round of betting among players."""
        for player in self.players:
            if player.is_active:
                print(f"Current highest bet: {self.current_highest_bet}")
                decision = input(f"Player {player.num}, choose 'fold', 'check', 'call', 'bet', or 'all-in': ").strip().lower()
                if decision == 'fold':
                    player.fold()
                elif decision == 'check':
                    if self.current_highest_bet > 0 and player.current_bet < self.current_highest_bet:
                        print("Cannot check, there is an active bet.")
                        continue  # Ask for a new decision
                    player.check()
                elif decision == 'call':
                    if self.current_highest_bet == 0:
                        print("Nothing to call; you might want to check.")
                        continue  # Ask for a new decision
                    self.pot += player.call(self.current_highest_bet)
                elif decision == 'bet':
                    while True:
                        amount = int(input("Enter bet amount: "))
                        if amount < 2 * self.current_highest_bet:
                            print(f"Bet must be at least twice the current highest bet, which is {2 * self.current_highest_bet}.")
                            continue
                        self.pot += player.bet(amount)
                        self.current_highest_bet = max(self.current_highest_bet, amount)
                        break
                elif decision == 'all-in':
                    self.pot += player.all_in()
                print(f"Player {player.num} now has {player.chips} chips.")
    
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
        ranks = [card.rank if card.rank != 1 else 14 for card in cards]
        suits = [card.suit for card in cards]

        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)

        sorted_ranks_by_count_then_value = sorted(rank_counts.items(), key=lambda item: (-item[1], item[0]))
        sorted_by_rank = sorted(ranks, reverse=True)

        is_flush = False
        flush_cards = []
        for suit, count in suit_counts.items():
            if count >= 5:
                is_flush = True
                flush_suit = suit
                flush_cards = sorted([card.rank for card in cards if card.suit == suit], reverse=True)

        # Checking for straights, considering Aces both high and low
        is_straight, straight_high_card = self.check_straight(sorted_by_rank)

        # Checking for straight flush or royal flush
        if is_flush and is_straight:
            if self.check_straight_flush(cards, flush_suit, straight_high_card):
                if straight_high_card == 14:  # Royal Flush
                    return (10, [14])  # Ace high
                return (9, [straight_high_card])
            return (6, flush_cards[:5])  # Regular Flush

        # Evaluate other hands
        if sorted_ranks_by_count_then_value[0][1] == 4:
            four_rank = sorted_ranks_by_count_then_value[0][0]
            kicker = max(rank for rank in sorted_by_rank if rank != four_rank)
            return (8, [four_rank, kicker])

        if sorted_ranks_by_count_then_value[0][1] == 3:
            three_rank = sorted_ranks_by_count_then_value[0][0]
            if len(sorted_ranks_by_count_then_value) > 1 and sorted_ranks_by_count_then_value[1][1] == 2:
                pair_rank = sorted_ranks_by_count_then_value[1][0]
                return (7, [three_rank, pair_rank])  # Full House
            kickers = [rank for rank in sorted_by_rank if rank != three_rank][:2]
            return (4, [three_rank] + kickers)  # Three of a Kind

        if sorted_ranks_by_count_then_value[0][1] == 2:
            pairs = [(rank, count) for rank, count in sorted_ranks_by_count_then_value if count == 2]
            pairs = sorted(pairs, reverse=True, key=lambda x: x[0])  # Ensure highest pairs are first
            if len(pairs) > 1:
                high_pair, low_pair = pairs[0][0], pairs[1][0]
                kicker = max(rank for rank in sorted_by_rank if rank not in (high_pair, low_pair))
                return (3, [high_pair, low_pair, kicker]) # Two Pair
            pair_rank = pairs[0][0]
            kickers = [rank for rank in sorted_by_rank if rank != pair_rank][:3]
            return (2, [pair_rank] + kickers)  # One Pair

        if is_straight:
            return (5, [straight_high_card])  # Straight

        if is_flush:
            return (6, flush_cards)  # Flush

        return (1, sorted_by_rank[:5])  # High Card

    def check_straight(self, ranks):
        """Check for a straight and return the highest card if a straight exists."""
        rank_set = set(ranks)
        # Consider Ace as high and low for straight checks
        if 14 in rank_set:
            rank_set.add(1)  # Add Ace as low

        for high in range(14, 4, -1):
            if all(rank in rank_set for rank in range(high, high - 5, -1)):
                return True, high
        if all(rank in rank_set for rank in [5, 4, 3, 2, 1]):  # Check specifically for the low Ace straight
            return True, 5
        return False, None

    def check_straight_flush(self, cards, flush_suit, straight_high_card):
        """Check if the flush cards form a straight flush."""
        flush_cards = sorted([card.rank for card in cards if card.suit == flush_suit], reverse=True)
        if 14 in flush_cards:
            flush_cards.append(1)  # Consider Ace as low as well

        for high in range(14, 4, -1):
            if all(rank in flush_cards for rank in range(high, high - 5, -1)):
                return True
        if all(rank in flush_cards for rank in [5, 4, 3, 2, 1]):  # Check specifically for the low Ace straight
            return True
        return False

    def play_round(self):
        """Plays a round of poker."""
        self.deck.shuffle()
        self.community_cards = []
        self.post_blinds_and_antes()
        self.deal_cards()
        self.betting_round()
        self.deal_flop()
        self.betting_round()
        self.deal_turn_or_river()
        self.betting_round()
        self.deal_turn_or_river()
        self.betting_round()
        self.evaluate_winner()
        self.pot = 0  # Reset the pot after the round