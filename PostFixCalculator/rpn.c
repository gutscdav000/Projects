

/*   Author:   David Gutsch
     Date:     08/2017         */

#include <stdio.h>
#include <stdlib.h>
#include "rpn.h"
#include <ctype.h>

extern CELL *stack;


/* function implementations */
CELL * push(int val) {
  CELL *c = (CELL *)malloc(sizeof(CELL));
  //stack = (CELL *)malloc(sizeof(CELL));

  if(c) {
    c->val = val;
    c->next = stack;  
    return c;
  } else {
    /*handle error*/
    printf("something went wrong:\ncell memory did not get allocated properly\n");
    return NULL;
  }
}

popReturn * pop(CELL * s) {
  // create pointer to struct that returns current value and current cell
  popReturn* p = (popReturn *)malloc(sizeof(popReturn));
  if(s->next == 0x0) {
    p->curVal = s->val;
    return p;
  }
  //return value
  p->curVal = s->val;
  //free stack of current cell
  CELL *hold = (CELL *)malloc(sizeof(CELL));
  if(hold == NULL) 
    printf("\nsomething went wrong with memory allocation of hold\n");
  
  hold = s->next;
  //free(stack);
  //reallocate stack to the next cell
  //stack = (CELL *)realloc(stack, sizeof(CELL));
  if(stack == NULL)
    printf("\nsomething went wrong with memory allocation of stack\n");
  
  p->curStack = *hold;
  //stack = hold;
  free(hold);

  return p;
}

int stackOperator(char op) {
 
  float opVal;
  int first;
  int second;

  while(1) {
    //if the stack is empty return the value 
    if(stack->next == 0x0) {
      //push(stack->val);
      return -1;
    }

    // perform the operation on the next two numbers on the stack
    popReturn *curPop = (popReturn *)malloc(sizeof(popReturn));

    switch(((int)op)) {
    case 42:
      curPop = pop(stack);
      first = curPop->curVal;
      *stack = curPop->curStack;
      second = curPop->curVal;
      *stack = curPop->curStack;
      opVal = first - second;;
      break;
    case 43:
      curPop = pop(stack);
      first = curPop->curVal;
      *stack = curPop->curStack;
      curPop = pop(stack);
      second = curPop->curVal;
      *stack = curPop->curStack;
      opVal = first + second;
      break;
    case 45: 
      curPop = pop(stack);
      first = curPop->curVal;
      *stack = curPop->curStack;
      opVal = first * second;
      break;
    case 47: 
      curPop = pop(stack);
      first = curPop->curVal;
      *stack = curPop->curStack;
      second = curPop->curVal;
      *stack = curPop->curStack;
      opVal = first / second;
    default:
      printf("an error occured\n");
    }
    // push the calculated number back on the stack
    printf("opVal %f\n",opVal);
    stack = push(((int)opVal));
    if(stack->next == NULL)
      break;
  }
}

void stringInnitializer(char *p) {
  int i;
  for(i = 0; i < 100; i++) {
    *p = 'x';
  }
  return;
}

int main(void) {
  int returnValue = 0;
  char cur;

  //initialize stack
  stack = (CELL *)malloc(sizeof(CELL));
  stack->val = 0;
  stack->next = NULL;
 
  // continuously start reading input
  while(1) {
    //read input
    scanf("%c", &cur);
    // if it's not a space keep checking else move to the next
    if(!isspace(cur)) {
      // if it's a digit push it on the stack
      if(isdigit(cur)) {
	printf("pushing %d\n",(cur - 48));
	stack = push((cur - 48));
      }
      // operate on the stack
      else if( cur == '/' || cur == '*' || cur == '+' || cur == '-') {
	printf("+-*/\n");
	int operationReturn = stackOperator(cur);
	printf("after calculation %f\n",operationReturn);
	if(operationReturn == -1) {
	  return 0;
	}
      }
    }
  }
  return 0;
  }
