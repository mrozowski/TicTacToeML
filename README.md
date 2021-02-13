# Q-learning TicTacToe
TicTacToe with implemented Q-learning where the agent gets only basic game rules. It learns how to play a game only by playing thousands of matches with itself. Without interaction with human. The program saves what he learned in files in ***'policy'*** catalog. It uses it later to play games with human.

## How it works
During training - playing games with itself it saves and updates every state of the board to the dictionary and adds value that tells how good this state is. The picture below shows a piece of code that does this thing. 
<br><br>

``` self.lr ```  - **L**earning **R**ate How quickly the agent learns new information and how long the user remembers old information. I keep this value as 0.1<br>
``` self.decay_gamma ```  - **D**ecay **R**ate This variable decides if early or late moves are more important for the result. Usually it has a value 0.8 or 0.9<br>
``` self.exp_rate ```  - **E**xploratory **R**ate Probability that the agend will choose completely random move. A bit of spontaneity is never a bad thing. Hawever, too high value brings too much randomness which causes worse result. I tried many values and the best are between 0.1 till 0.3
<br>
``` self.states_value ``` The dictionary contains all encountered states and values assigned to that states.
<br><br>
Later when an agent decide what move to make it checks all possible moves and chooses this one that has the highest value according to the dictionary. <br>
As a reward it takes:
* 1 - if the agent won a match
* 0 - tie
* -1 - lose

## User interface
For the user interface, I used PyQT because I used this library a few times already. Buttons and other elements I designed in **Figma** and export as png files. 
To separate logic from code related to design I used **MVP** pattern.<br><br>
```view.py``` -  Contains code that shows user interface. <br>
```presenter.py``` - There is code that does all business logic and connects with visual elements from ***view.py***.  <br>
```game.py``` - Code strictly related to TicTacToe game and machine learning<br>
