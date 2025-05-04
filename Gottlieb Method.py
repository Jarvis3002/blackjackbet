import random
import math 
import statistics

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self, num_decks=6):
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
        self.bet_amount = 100  
        self.hands_played = 0
        self.running_count = 0
    
    def update_count(self, card):
        self.running_count += 1

    def betting_strategy(self):
        cards_drawn = self.running_count
        d = 6
        p = cards_drawn / 52 * d
        theta = 1.21
        c0 = 0.00067
        sigma = math.sqrt(5.992559489 * 0.001)
        sigma_prime = sigma * math.sqrt(52)
        alpha = math.asin(math.sqrt(p)) - math.sqrt(p * (1-p))

        if p == 0:
            self.bet_amount = 100
        else:
            self.bet_amount = (p * c0 / 2 + sigma_prime / math.sqrt(d) * alpha / math.sqrt(2 * math.pi)) / (theta * p)

        return self.bet_amount
    
    def play_hand(self):
        player = Hand()
        dealer = Hand()
        
        try:
            player.add_card(self.deck.deal())
            dealer.add_card(self.deck.deal())
            player.add_card(self.deck.deal())
            dealer.add_card(self.deck.deal())
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
                player.add_card(self.deck.deal())
                if player.value > 21:
                    return -1 
            except IndexError:
                return None  
        
        while dealer.value < 18:
            try:
                dealer.add_card(self.deck.deal())
                if dealer.value > 21:
                    return 1 
            except IndexError:
                return None  
        
        if player.value > dealer.value:
            return 1
        elif player.value < dealer.value:
            return -1
        return 0  # Push
    
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
