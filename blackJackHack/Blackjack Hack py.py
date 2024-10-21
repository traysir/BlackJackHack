import tkinter as tk
from tkinter import messagebox
import pandas as pd
import re

class BlackjackAdvisorApp:
    def __init__(self, root, strategy_file):
        self.root = root
        self.root.title("Blackjack Advisor")
        
        # Load the strategy file
        self.strategy = pd.read_csv(strategy_file)
        
        # Set up casino-like colors
        self.root.configure(bg='green')
        
        # Setup GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Labels for input
        tk.Label(self.root, text="Player Hand (e.g., 10 or A,8):", bg='green', fg='gold', font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Dealer Up Card (e.g., 9 or A):", bg='green', fg='gold', font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        
        # Entry fields for player hand and dealer up card
        self.player_hand_entry = tk.Entry(self.root, font=("Arial", 12))
        self.dealer_up_card_entry = tk.Entry(self.root, font=("Arial", 12))
        self.player_hand_entry.grid(row=0, column=1, padx=10, pady=10)
        self.dealer_up_card_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Checkboxes for allowed actions
        self.split_var = tk.IntVar()
        self.double_var = tk.IntVar()
        self.surrender_var = tk.IntVar()
        
        tk.Checkbutton(self.root, text="Allow Splitting", variable=self.split_var, bg='green', fg='gold', font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, padx=10)
        tk.Checkbutton(self.root, text="Allow Doubling Down", variable=self.double_var, bg='green', fg='gold', font=("Arial", 12)).grid(row=3, column=0, sticky=tk.W, padx=10)
        tk.Checkbutton(self.root, text="Allow Surrender", variable=self.surrender_var, bg='green', fg='gold', font=("Arial", 12)).grid(row=4, column=0, sticky=tk.W, padx=10)
        
        # Submit button
        tk.Button(self.root, text="Get Advice", command=self.get_advice, bg='gold', fg='black', font=("Arial", 12)).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Label for displaying the recommendation
        self.recommendation_label = tk.Label(self.root, text="", font=("Arial", 16), bg='green')
        self.recommendation_label.grid(row=6, column=0, columnspan=2, pady=20)
        
    def get_advice(self):
        # Retrieve user input
        player_hand = self.normalize_hand(self.player_hand_entry.get().strip().upper())
        dealer_up_card = self.normalize_card(self.dealer_up_card_entry.get().strip().upper())
        
        # Debugging: Print the inputs to check them
        print(f"Normalized Player Hand: {player_hand}")
        print(f"Normalized Dealer Up Card: {dealer_up_card}")
        
        # Validate player hand and dealer up card
        if not player_hand or not dealer_up_card:
            self.show_recommendation("Invalid input format.", "red")
            return
        
        # Filter strategy based on input
        filtered_strategy = self.strategy[
            (self.strategy['Player Hand'] == player_hand) & 
            ((self.strategy['Dealer Up Card'] == dealer_up_card) | (self.strategy['Dealer Up Card'] == 'Any'))
        ]
        
        if filtered_strategy.empty:
            self.show_recommendation("No recommendation found for this hand.", "red")
            return
        
        # Get the recommended action
        recommended_action = filtered_strategy['Action'].values[0]
        
        # Modify recommendation based on allowed actions
        if not self.split_var.get() and 'Split' in recommended_action:
            recommended_action = "Hit"  # If splitting is not allowed, recommend hitting
        if not self.double_var.get() and 'Double' in recommended_action:
            recommended_action = "Hit"  # If doubling is not allowed, recommend hitting
        if not self.surrender_var.get() and 'Surrender' in recommended_action:
            recommended_action = "Hit"  # If surrendering is not allowed, recommend hitting
        
        # Color code the recommendation
        color = "green" if recommended_action == "Stand" else "red"
        
        # Display the recommendation
        self.show_recommendation(f"Recommended action: {recommended_action}", color)
    
    def show_recommendation(self, message, color):
        """ Display the recommendation in the main window """
        self.recommendation_label.config(text=message, fg=color)
    
    def normalize_hand(self, hand):
        """ Normalize the player's hand (e.g., 10, A,8) to match the CSV format """
        hand = hand.replace(' ', '')  # Remove spaces
        if ',' in hand:
            return hand.upper()  # For hands like A,8
        return hand  # For hands like 10, 9
    
    def normalize_card(self, card):
        """ Normalize the dealer's up card (e.g., 9, 10, A) to match the CSV format """
        card = card.strip()
        if card == 'A':
            return 'A'  # Ace
        if card.isdigit() and int(card) in range(2, 11):
            return card  # 2-10
        return None  # Invalid input

# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackAdvisorApp(root, 'blackjackbook.csv')
    root.mainloop()
