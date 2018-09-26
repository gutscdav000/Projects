/* key.h --- 
 * 
 * Filename: key.h
 * Description: 
 * Author: Bryce Himebaugh
 * completed by: David Gutsch 
 * Created: Thu Sep 15 16:36:21 2016
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
enum {NOCHAR, REGCHAR, UP, DOWN, LEFT, RIGHT, BADESC}; 

int read_escape(int *);

/* key.h ends here */
