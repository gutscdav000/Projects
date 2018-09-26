/* well.h --- 
 * 
 * Filename: well.h
 * Description: 
 * Author: Bryce Himebaugh
 * completed by: David Gutsch 
 * Created: Tue Sep  6 14:10:53 2016
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

typedef struct well {
  int upper_left_x;
  int upper_left_y;
  int width;
  int height;
  char draw_char;
  char color[3];
} well_t;

well_t *init_well(int, int, int, int);
void draw_well(well_t *);
int prune_well(well_t * well);

/* well.h ends here */
