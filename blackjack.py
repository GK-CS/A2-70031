import random

# Function used to draw cards into a hand.
def draw(pickups_to_make):
    drawn_cards = []
    # The deck is defined as a list of tuples.
    # Each tuple is a card.
    # Each item in the tuple is a card property.
    # The first property of each card is the string
    # used to refer to the card in a sentence.
    # The second property of each card is an integer
    # used to score the card.
    deck = [("an Ace", 1), ("a 2", 2), ("a 3", 3), ("a 4", 4),
    ("a 5", 5), ("a 6", 6), ("a 7", 7), ("an 8", 8), ("a 9", 9),
    ("a 10", 10), ("a Jack", 10), ("a Queen", 10), ("a King", 10)]
    # Loop that allows more than one card to be picked-up at once.
    for pickups in range(pickups_to_make):
            drawn_cards.append(random.choice(deck))
    # Returns a list of tuples. Cards are tuples!
    return drawn_cards

# Function that takes a hand and scores it.
# Note that an Ace can be worth either 11 points or 1 point,
# Depending on whether 11 points would result in a bust.
# The value of the same Ace in the same hand
# will sometimes be different in different calls of score().
def score(hand):
    hand_value = 0
    ace_count = 0
    # Loop that checks whether each card is an Ace
    # and scores the non-Ace cards.
    for card in hand:
        # Condition where card is an Ace.
        if (card[1] == 1):
            ace_count += 1
        # Condition where card is a number or face card.
        else:
            hand_value += card[1]
    # Loop that scores each Ace.
    for ace in range(0, ace_count):
        # Condition where the Ace
        # being worth 11 would cause a bust.
        if ((hand_value + 11) > 21):
            hand_value += 1
        # Condition where the Ace
        # being worth 11 would not cause a bust.
        else:
            hand_value += 11
    return hand_value

# Function that takes a hand and returns a string.
# The string contains the names of each card in the hand,
# in the order they were drawn.
# The string is grammatical, with the correct placement of
# commas and the word "and".
def describe(hand):
    # Begins the string with the name of the
    # first card in the hand.
    hand_description = hand[0][0]
    # A loop that concatenates to the string the names of
    # all cards in the hand other than the first and last.
    # Also correctly places commas.
    for card in (hand[1:-1]):
        hand_description += f", {card[0]}"
    # Concatenates to the string the name of
    # the final card in the hand.
    # Also correctly places the word "and".
    hand_description += f" and {hand[-1][0]}."
    return hand_description

# Function that asks the player whether they want to play again.
# Used to exit the program.
def play_again_prompt():
    # Loop that does not end until the user provides valid input.
    while True:
        play_again_ans = input("Do you want to play again? (y/n) ").lower()
        if (play_again_ans == "y"):
            break # The loop and function will end.
        if (play_again_ans == "n"):
            print("Goodbye.\n")
            exit() # The program's only exit condition.
        else: # Condition where the player's input is invalid.
            print("Please input either a 'y' or an 'n', "
            "without spaces or quotation marks.")



# Function that contains the core logic of the game.
# It runs fresh with each new round of the game.
def play_round():

    # Function called when a round-end condition is reached.
    # For scope reasons, it is defined inside play_round().
    def show_results():
        print(f"«« Round Results »»")
        print(f"Your total is {score(player_hand)}.")
        print(f"The dealer's total is {score(dealer_hand)}.")
        print(f"Your hand contains {describe(player_hand)}")
        print(f"The dealer's hand contains {describe(dealer_hand)}\n")


    # Initializes hands as lists.
    # Later, they will become lists of tuples. Each card is a tuple.
    player_hand = []
    dealer_hand = []
    print("«« Round Start »»")
    dealer_hand += draw(2) # Puts 2 cards into dealer_hand.
    print(f"The dealer draws {dealer_hand[0][0]} and a hidden card.")
    player_hand += draw(2) # Puts 2 cards into player_hand.
    print(f"You draw {player_hand[0][0]} and {player_hand[1][0]}. ", end="")

    # The rare condition where the player's first 2 cards
    # form a Blackjack.
    # A special message is provided to the player,
    # and the player is not prompted to take a turn.
    if score(player_hand) == 21:
        print("That's Blackjack! A natural 21!\n")
    # The ordinary condition. The ordinary message is provided.
    # The player is prompted to take a turn.
    else:
        print(f"Your total is {score(player_hand)}.\n")
        print("«« Your Turn »»")

    # Within a round of play, all player input is controlled
    # and validated by this loop.
    # The player only gets a choice of action when the player's
    # score is less than 21.
    # In a round where the player's first 2 cards form a Blackjack,
    # the user has no input at all.
    while score(player_hand) < 21:
        player_move = input("Will you hit or stand? (h/s) ").lower()
        if (player_move == "h"):
            player_hand += draw(1) # Player draws 1 card.
            print(f"You draw {player_hand[-1][0]}. "
            f"Your total is now {score(player_hand)}. ")
        elif (player_move == "s"):
            print("You stand!\n")
            break # Player's turn ends.
        # Condition where the player's input is invalid.
        else:
            print("Please input either an 'h' or an 's', "
            "without spaces or quotation marks.")

    # Condition where the player is forced to stand
    # after having previously made at least 1 hit.
    if ((score(player_hand) == 21) and (len(player_hand) > 2)):
        print("You must stand!\n") # Player's turn ends.
    # Round-end condition where the player busts.
    if (score(player_hand) > 21):
        print("You have busted! The dealer wins!\n")
        show_results()
        return 0 # Ends the round. win_count will not increase.

    print("«« The Dealer's Turn »»")
    print(f"The dealer's hidden card is {dealer_hand[1][0]}. "
    f"The dealer's total is {score(dealer_hand)}.")

    # Within a round of play, all behaviour of the dealer
    # is provided by this loop.
    # The dealer draws until the dealer's hand is worth 17 or more.
    while score(dealer_hand) < 17:
        dealer_hand += draw(1) # Dealer draws 1 card.
        print(f"The dealer draws {dealer_hand[-1][0]}. "
        f"The dealer's total is now {score(dealer_hand)}.")

    # if-else block containing the 4 round-end conditions
    # that are possible when the player has not busted.
    if (score(dealer_hand) > 21):
        print("The dealer has busted! You win!\n")
        show_results()
        return 1 # Ends the round. win_count will increase by 1.
    elif (score(player_hand) > score(dealer_hand)):
        print("The dealer stands! You win!\n")
        show_results()
        return 1 # Ends the round. win_count will increase by 1.
    elif (score(player_hand) < score(dealer_hand)):
        print("The dealer stands! And wins!\n")
        show_results()
        return 0 # Ends the round. win_count will not increase.
    else:
        print("The dealer stands! You have tied the dealer, "
        "but the dealer wins anyway!\n")
        show_results()
        return 0 # Ends the round. win_count will not increase.



# The first line of program execution.
print("\n" + ("♣♥♦♠" * 6) + "   WELCOME TO BLACKJACK   " + ("♠♦♥♣" * 6))

# The only 2 global variables.
round_count = 0
win_count = 0

# Loop that controls the iteration of the program
# over multiple rounds of play.
while True:
    round_count += 1
    print("\n\n" + ("★☆" * 15) + f"   ROUND  {round_count}   "
    + ("☆★" * 15) + "\n")
    # A round of play begins when this line is run.
    # play_round() contains the core of the game
    # and will return a 1 or a 0, where 1 indicates a win.
    win_count = win_count + play_round()
    print(f"Rounds played: {round_count}\nRounds won: {win_count}")
    # The only end to this loop is program exit,
    # which is contained within play_again_prompt().
    play_again_prompt()
