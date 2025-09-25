# Casino50
#### Video Demo:  <https://www.youtube.com/watch?v=etHAjBSZYt0>
#### Description:

My project is called Casino50, and it is allows you to play 3-card-poker and blackjack against a computer. There is a currency in the game (not real money) which allows you to place bets, just like a real casino. It has a login page where you put in your credientials to access the website. To sign up, you click on the sign up button and your account will be created. You can change your password and add extra money if you would like.

The login page will take a username and password and check if they are in the SQL database, and if they are you will be able to access the website. If they are not in the database, you will be prompted to try again.

The registration page asks you to input a username, a password, and the same password for confirmation. If the username is already in the database, you will be told to choose a different username. If the password and confirmation password don't match, you will be told so as well, and will be asked to try again. Once you register, your username, password hash, and default cash will be put into the database. By default, every user has $100.00 in their account.

The home page includes 2 games you can play: blackjack and 3-card-poker. If you choose 3-card-poker or blackjack, you will be taken to the betting page, where you decide how much you want to bet on the game. There is a home button at the top to return to this page, a profile button where you can access resetting your password and adding money and seeing your current balance, and a logout button.

The betting page asks you how much you would like to bet, and displays your current cash so you know. If you don't have enough cash to make a bet, you will not be allowed to play and you will be informed of this. You may return go to your profile to add cash or simply return home from here.

If you select 3-card-poker and have enough cash to play, you will see your cards but not the dealer's, and will be asked whether you would like to fold or play. If you fol, you will lose your initial bet. If you play and win, you win back your initial bet along with an amount equal to your initial bet given by the dealer. If you decide to play and lose though, you lose your inital bet and the extra bet you made (equal to the intial bet) when you decided to play. If the dealer has a hand of jack high or worse, it is a push, and no one wins or loses, but the hand is over.

If you select blackjack, you will be taken to the same betting screen where you will be taken to the game if you have enough money to play. You can see your cards but not the dealer's cards, and you may decide to hit (get an extra card) or stand (end your turn). If you go over 21, you bust and lose your bet. If you don't bust, and beat the dealer, you win back your inital bet plus your inital bet again. If the dealer bets you though, you lose your initial bet as well. Your cash will be automatically tracked after game, and you may see it at any time.

When you are done, you my log out, and you will be taken back to the login page, where you will have to input your credentials if you would like to play again.
