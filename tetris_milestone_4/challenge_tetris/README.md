# tetris
tetris that is designed to run in a text terminal using ANSI escape sequences. This project was given to me in my first c class as our final project. We were given a repository that had some incomplete functions as well as a few missing functions, and had a final project with 4 different milestones to complete the tetris game. This included getting the game running, scoring the game, and maintaining state persistence and keep track of high scores

you can run the program after you have pulled the repository with the following steps:

1) you must compile all of the c files using the make files
 
 make clean all
 
2) you must run the game and provide a high scores file(which I have alread provided) 
  
 ./tetris high_scores.txt
 
 3) after the game is over in order to get rid of all of the .o files run the following command
 
 make clean
