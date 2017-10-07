

/*   Author:   David Gutsch
     Date:     08/2017         */

#include <stdio.h>
#include <stdlib.h>
#include "rpn.h"
#include <ctype.h>

extern CELL *stack;


/* function implementations */
void push(int val) {
  CELL *c = (CELL *)malloc(sizeof(CELL));

  if(c) {
    c->val = val;
    c->next = stack;  
    stack  = c; // pushes new cell on stack
  } else {   /*handle error*/
    printf("something went wrong:\ncell memory did not get allocated properly\n");
  }
}

int pop() {
  CELL *c = stack;
  
  if(c) {
    
    stack = stack->next; //pop
    int val = c->val;
    free(c);
    return val;
  }
  else {
    printf("The stack is empty\n");
    exit(1);
  }

}

float stackOperator(char op, int length) {
  float result;
  int numbers[length];
  int i;
  
  //pop all numbers from the stack since last operation and read them into an array
  for(i = length - 1; i >= 0; i--) 
    numbers[i] = pop();

  //sets initial value for result FIRST ITERATION
  switch((int)op) {
  case 42:
    result = (((float)numbers[0]) * numbers[1]);
    break;
  case 43:
    result = (((float)numbers[0]) + numbers[1]);
    break;
  case 45:
    result =  (((float)numbers[0]) - numbers[1]);
    break;
  case 47:
    result = (((float)numbers[0]) / numbers[1]);
    break;
  default:
    exit(1);
    break;
  }
  
  //calculates result for array items [2,length]
  for(i = 2; i < length; i++) {
    
    switch((int)op) {
    case 42:
      result = result * numbers[i];
      break;
    case 43:
      result = result + numbers[i];
      break;
    case 45:
      result = result - numbers[i];
      break;
    case 47:
      result = result / numbers[i];
      break;
    }
  }
  return result;
}

void stackClearer() {
  while(stack)
    pop();
  
  return;
}

void stackPrinter() {
  int i = 0;
  CELL *copyStack = stack;
  if(copyStack) {
    printf("\tIndex\tValue\n");
    printf("-------------------\n");
  
  while(copyStack) {
    printf("\t%d\t%d\n",i, copyStack->val);
    copyStack = copyStack->next;
    i++;
  }
  printf("-------------------\n");
  }
  else {
    printf("the stack is empty\n");
  }
  return;
}


int main(void) {
  int stack_counter = 0;
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
	push((cur - 48));
	stack_counter++; //increment stack counter
      }
      // operate on the stack
      else if( cur == '/' || cur == '*' || cur == '+' || cur == '-') { 
	float result;
	printf("+-*/\n");
	
	if(stack && stack->next) {
	  //int first = pop();
	  //int second = pop();
	  result = stackOperator(cur, stack_counter);
	  push((int)result);
	  //reset stack counter 
	  //(1 because the one result from computation get's pushed back onto stack)
	  stack_counter = 1; 
	}
	else {
	  printf("the stack doesn't have enough numbers upon which to operate\n");
	}
	
	printf("after calculation %f\n stack value: %d\n", result, stack->val);
      }
      else if(isalpha(cur)) {
	// this will be for p,f,c,q commands
	switch(cur) {
	case 'c':
	  stackClearer();
	  break;
	case 'p':
	  printf("peek:\t%d\n",stack->val);
	  break;
	case 'q':
	  return 0;
	  break;
	case 'f':
	  stackPrinter();
	  break;
	case EOF:
	  return 0;
	  break;
	}
      }
      // EOF isn't an alpha character so it needs its own stopping condition
      else if(cur == EOF) return 0; 
    }
  }
  return 0;
}
