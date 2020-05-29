This repository stores my short-term projects that I have been playing around with during quarantine. 

# 1. Cribbage 
During quarantine, my mom and I play two-player Cribbage every day. That inspired me to create a class that can simulate cribbage games. The model chooses the best 4-card hand from the initial 6 cards by calculating the hand with the greatest expected points (based on the mean score of the combinations). The class scores a hand in approximately 1 millescond and chooses the 'best' hand in 0.16 seconds. The model does not take into account pegging, which player has the crib, or affinity for risk. 

After 1000 hand simulations, the average hand score was 8.39, which is slightly (0.5) higher than suggested after a quick search. The average crib score was 4.77, which is the same as my search results. I expect that the hands were slighly higher scoring for two main reasons. First, The momputer does not take into account the crib. Second, the model uses way more math than an average human player in choosing hands. 

To Do: Add pegging functionality, make UI (model-model and model-human), train different model to play

Code: https://github.com/thomasg8/Quarantine/blob/master/Cribbage/Cribbage.py

Rules of Cribbage can be found here: https://bicyclecards.com/how-to-play/cribbage/

# 2. Simple Ecosystem Simulations 

## Procedural Land Generation
I initialized an n x n map with values of 1 or 0 based on a given probability of being land, denoting 1 to be land and denoting 0 to be water. Then, I used Cellular Automata to smooth the random values into land masses. Through my testing, this method creats solid land masses for smaller maps, but creates archipelagoes for larger maps. It is possible to increase the amount of land by tweaking the probability of land; however, it is very sensitive to changes. I am currently tweaking the parameters to determine the amount of land that I want for my ecosystem.

50x50 with 50% probability of land            |  150x150 with 50% probability of land
:-------------------------:|:-------------------------:
![](Imgs/land_generation50.gif)  |  ![](Imgs/land_generation150.gif)

50x50 with 57% probability of land            |  150x150 with 57% probability of land
:-------------------------:|:-------------------------:
![](Imgs/land_generation50_57.gif)  |  ![](Imgs/land_generation150_57.gif)

** Reload the page to reset gifs. Currently troubleshooting this. 

Lowering the land probability creates islands, which would isolate certain populations if the animals could not swim; therefore, I will be using higher land probabilities to create lake biomes rather than archipelagoes.

Code: https://github.com/thomasg8/Quarantine/blob/master/TerrainGeneration.ipynb

To Do: Create environment in pygame or Unity, add animals to enviorment, make animals compete aginst each other (functionality and model)
