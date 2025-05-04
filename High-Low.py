import random
import statistics

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.cards = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        
        for _ in range(num_decks):
            for suit in suits:
                for value in values:
                    self.cards.append(Card(suit, value))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self):
        return self.cards.pop(0)

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self, card):
        self.cards.append(card)
        if card.value in ["J", "Q", "K"]:
            self.value += 10
        elif card.value == "A":
            self.value += 11
            self.aces += 1
        else:
            self.value += int(card.value)
        self.adjust_for_ace()
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class BlackjackSimulator:
    def __init__(self):
        self.deck = Deck(num_decks=6)
        self.deck.shuffle()
        self.profit = 0
        self.base_bet = 100
        self.hands_played = 0
        self.running_count = 0
        self.cards_dealt = 0
        self.card_values = {
            '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
            '7': 0, '8': 0, '9': 0,
            '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
        }
    
    def play_hand(self):
        player = Hand()
        dealer = Hand()
        
        try:
            for _ in range(2):
                card = self.deck.deal()
                player.add_card(card)
                self.update_count(card)
                
                card = self.deck.deal()
                dealer.add_card(card)
                self.update_count(card)
        except IndexError:
            return None  
        
        player_bj = player.value == 21
        dealer_bj = dealer.value == 21
        
        if player_bj or dealer_bj:
            if player_bj and dealer_bj:
                return 0  
            elif player_bj:
                return 1.5  
            return -1  
        
        
        while player.value < 18:
            try:
                card = self.deck.deal()
                player.add_card(card)
                self.update_count(card)
                if player.value > 21:
                    return -1  
            except IndexError:
                return None
        
        while dealer.value < 18:
            try:
                card = self.deck.deal()
                dealer.add_card(card)
                self.update_count(card)
                if dealer.value > 21:
                    return 1 
            except IndexError:
                return None
        
        if player.value > dealer.value:
            return 1
        elif player.value < dealer.value:
            return -1
        return 0

    def update_count(self, card):
        self.running_count += self.card_values.get(card.value, 0)
        self.cards_dealt += 1
    
    def get_true_count(self):
        remaining_decks = (len(self.deck.cards) / 52)
        if remaining_decks < 0.5:
            remaining_decks = 0.5 
        return self.running_count / remaining_decks
    
    def betting_strategy(self):
        true_count = self.get_true_count()
        
        if true_count < 1:
            return self.base_bet * 0.5
        elif 1 <= true_count < 2:
            return self.base_bet * 2
        elif 2 <= true_count < 3:
            return self.base_bet * 3
        elif 3 <= true_count < 4:
            return self.base_bet * 4
        else:
            return self.base_bet * 5
    
    
    def simulate(self):
        results = []
        while True:
            bet = self.betting_strategy()
            result = self.play_hand()
            
            if result is None:
                break
                
            self.hands_played += 1
            
            if result == 1.5:
                self.profit += bet * 1.5
            elif result == 1:
                self.profit += bet
            elif result == -1:
                self.profit -= bet
            
            results.append(result)
        
        if results:
            print(f"Profit: {self.profit:.2f}")
        else:
            print("No hands were played - deck was empty")
        return self.profit

def run_simulations(num_simulations=10000):
    profits = []
    for i in range(num_simulations):
        sim = BlackjackSimulator()
        sim.bet_amount = 100 
        final_profit = sim.simulate()
        profits.append(final_profit)
    
    mean_profit = statistics.mean(profits)
    print(f"\nMean profit after {num_simulations} simulations: {mean_profit:.2f}")
    return mean_profit

if __name__ == "__main__":
    run_simulations(10000)
