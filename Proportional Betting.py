import random
import statistics

k = 200  
p = 0.05  

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
        self.bankroll = k  
        self.hands_played = 0
    
    def betting_strategy(self):
        bet = self.bankroll * p
        return max(1, bet)
    
    def play_hand(self):
        try:
            bet = self.betting_strategy()
            if bet > self.bankroll:
                return None  
            
            player = Hand()
            dealer = Hand()
            
            player.add_card(self.deck.deal())
            dealer.add_card(self.deck.deal())
            player.add_card(self.deck.deal())
            dealer.add_card(self.deck.deal())
            
            player_bj = player.value == 21
            dealer_bj = dealer.value == 21
            
            if player_bj or dealer_bj:
                if player_bj and dealer_bj:
                    result = 0 
                elif player_bj:
                    result = 1.5  
                else:
                    result = -1  
            else:
                while player.value < 18:
                    player.add_card(self.deck.deal())
                    if player.value > 21:
                        result = -1
                        break
                else:
                    while dealer.value < 18:
                        dealer.add_card(self.deck.deal())
                        if dealer.value > 21:
                            result = 1
                            break
                    else:
                        if player.value > dealer.value:
                            result = 1
                        elif player.value < dealer.value:
                            result = -1
                        else:
                            result = 0
            
            self.bankroll += bet * result
            self.hands_played += 1
            
            return result
            
        except IndexError:
            return None  
    
    def simulate(self):
        while True:
            result = self.play_hand()
            if result is None:
                break
        
        return self.bankroll - k  

def run_simulations(num_simulations=10000):
    profits = []
    for _ in range(num_simulations):
        sim = BlackjackSimulator()
        final_profit = sim.simulate()
        profits.append(final_profit)
    
    mean_profit = statistics.mean(profits)
    median_profit = statistics.median(profits)
    
    print(f"Mean Profit: ${mean_profit:.2f}")
    print(f"Median Profit: ${median_profit:.2f}")
    
    return profits

if __name__ == "__main__":
    run_simulations(10000)

if __name__ == "__main__":
    run_simulations(10000)
