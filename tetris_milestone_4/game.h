/* game.h --- 
 * 
 * Filename: game.h
 * Description: 
 * Author: Bryce Himebaugh
 * Completed by: David Gutsch 
 * Created: Tue Sep  6 11:16:03 2016
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

typedef struct terminal_dimensions {
  int maxx;
  int maxy;
} terminal_dimensions_t;

// Delay timers for the main game loop.
#ifndef DELAY_US
#define DELAY_US 100000
#endif

// Game States
enum {INIT, ADD_PIECE, MOVE_PIECE, ADJUST_WELL, GAME_OVER, EXIT, SPLASH_SCREEN, USER_INITIALS};

void init_game(void);
highscore_t *game(highscore_t *);



/* game.h ends here */
