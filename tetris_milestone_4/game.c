/* game.c --- 
 * 
 * Filename: game.c
 * Description: 
 * Author: Bryce Himebaugh
 * Completed by: David Gutsch 
 * Created: Tue Sep  6 11:08:59 2016
 * Last-Updated: 08/26/2017
 *           By: David Gutsch
 *     Update #: 0
 * Keywords: 
 * Compatibility: 
 * 
 */

/* Commentary: 
 * 
 * 
 * 
 */

/* Change log:
 * 
 * 
 */

/* Copyright (c) 2016 The Trustees of Indiana University and 
 * Indiana University Research and Technology Corporation.  
 * 
 * All rights reserved. 
 * 
 * Additional copyrights may follow 
 */

/* Code: */
#include <unistd.h> 
#include <ncurses.h>
#include <time.h>
#include "highscore.h"
#include "game.h"
#include "well.h"
#include "tetris.h"
#include "tetromino.h"
#include "key.h"

void init_game(void) {
  int x,y;
}

highscore_t *game(highscore_t *highscores) {
  static int state = SPLASH_SCREEN;
  tetromino_t *next = NULL;
  tetromino_t *current = NULL;
  well_t *w;
  int x,y;
  int c;
  int arrow;
  struct timespec tim = {0,1000000};
  struct timespec tim_ret;
  int move_counter = 0;
  int move_timeout = 500;
  int status;
  int counter = 0;
  int lines_cleared = 0;
  int score = 0;
  char str[80];  
  char initials[3];
  while(1) {
    switch(state) {
    case INIT:               // Initialize the game, only run one time 
      //initscr();
      clear();
      nodelay(stdscr,TRUE);  // Do not wait for characters using getch.  
      noecho();              // Do not echo input characters 
      getmaxyx(stdscr,y,x);  // Get the screen dimensions 
      w = init_well(((x/2)-(WELL_WIDTH/2)),3,WELL_WIDTH,WELL_HEIGHT);
      draw_well(w);
      srand(time(NULL));     // Seed the random number generator with the time. Used in create tet. 
      display_score(score, w->upper_left_x-15,w->upper_left_y);  
      //state = ADD_PIECE;
      state = ADD_PIECE;
      break;
    case SPLASH_SCREEN:
      initscr();
      start_color();
      nodelay(stdscr, FALSE);
      getmaxyx(stdscr,y,x);
      mvprintw(2,x/2-5,"%s", "Welcome Friend");
      mvprintw(3,x/2-5,"this is");
      mvprintw(4,x/2-5,"Davids Tetris");
      mvprintw(16,x/2-5,"Hit a button to begin");
      getch();
      /*if( c == 's') {
        state = ADD_PIECE;
        nodelay(stdscr,TRUE);
       }*/
      state = INIT;
      break;

    case ADD_PIECE:          // Add a new piece to the game
      if (next) {
	current = next;
        move_tet(current, (w->upper_left_x + (w->width / 2)), w->upper_left_y);
	next = create_tetromino (w->upper_left_x - 15, w->upper_left_y + 10);
        // this is where we display the next tetromino
        mvprintw(6, w->upper_left_x - 25, "*** Next Tetromino ***");
        display_tetromino(next);
      }
      else {
	current = create_tetromino ((w->upper_left_x+(w->width/2)), w->upper_left_y);
	next = create_tetromino (w->upper_left_x - 15, w->upper_left_y + 10);
        mvprintw(6, w->upper_left_x - 25, "*** Next Tetromino ***");
        display_tetromino(next);
      }

      if(check_collision(current) == MOVE_FAILED) {
	// if the score needs to be inserted go ask for initials else go straight to game over screen
            if(compare_highscore(highscores, score, 10)) {
              state = USER_INITIALS;
              clear();
            }
            else {
	      state = GAME_OVER;
            }
      }
      else {
            display_tetromino(current);
            state = MOVE_PIECE;
      }
      break;
    case USER_INITIALS:
      //clear(); 
      printf("%s", "please enter your first and last name initials (ex: dg):\n");
      scanf("%2s", initials);
      highscores = insert_score(highscores,initials, score);
      state = GAME_OVER;
      break;
            
    case MOVE_PIECE:         // Move the current piece 
      if ((arrow = read_escape(&c)) != NOCHAR) {
	if (arrow == UP) {
	  undisplay_tetromino(current);
	  rotate_ccw(current);
	  display_tetromino(current);
	}
	else if (arrow == DOWN) {
	  undisplay_tetromino(current);
	  rotate_cw(current);
	  display_tetromino(current);
	}
	else if (arrow == LEFT) {
	  undisplay_tetromino(current);
	  move_tet(current,current->upper_left_x-1,current->upper_left_y);
	  display_tetromino(current);
	}
	else if (arrow == RIGHT) {
	  undisplay_tetromino(current);
	  move_tet(current,current->upper_left_x+1,current->upper_left_y);
	  display_tetromino(current);
	}
      	else if (arrow == REGCHAR) {
	  if (c == ' ') {
	    move_timeout = DROP_RATE;
 	  }
	  if (c == 'q') {
	    state = GAME_OVER;
 	  }
	}
      } 
      if (move_counter++ >= move_timeout) {
	counter++;
	undisplay_tetromino(current);
	status = move_tet(current,current->upper_left_x,current->upper_left_y+1);
	display_tetromino(current);
	if (status == MOVE_FAILED) {
	  state = ADD_PIECE;
	  move_timeout = BASE_FALL_RATE;
          // this is where we check for completed lines
          int temp_score = prune_well(w);
          //this is where we add the score from this turn to the total score
          score = compute_score(score, temp_score);
	  display_score(score, w->upper_left_x - 15, w->upper_left_y);
	  // undisplay the next tetromino so that it may be redefined
	  undisplay_tetromino(next);
          
	}
	move_counter = 0;
      }
      break;
    case GAME_OVER:
      nodelay(stdscr,FALSE);
      clear();
      getmaxyx(stdscr,y,x);
      mvprintw(1,x/2-5,"  GAME_OVER  ");
      // cast a int(longer than 1 int) to a char to print score
      //char scr = (char)&score; 
      mvprintw(2,x/2-5,"%8d", score);
      mvprintw(3,x/2-5,"#############");
      mvprintw(16,x/2-5,"Hit q to exit");
      
      
      int i;
       
      highscore_t temp_hs = *highscores;
      
      for(i = 0; i < 9; i++) {
	mvprintw(i + 4, x/2, "%2s\t%d",temp_hs.initials,temp_hs.score);
        temp_hs = *(temp_hs.next);
      }
      
      getch(); // Wait for a key to be pressed. 
      /*if( c =='q') {
        state = EXIT;
	}*/
      state = EXIT;
      break;
    case EXIT:
      return(highscores);  // Return the highscore structure back to main to be stored on disk. 
      break;
    }
    refresh();
    nanosleep(&tim,&tim_ret);
  }
}

/* game.c ends here */
