

#include <iostream>
#include "Calculator.h"
//#include <emscripten/bind.h>

using namespace emscripten;
using namespace std;

class Calculator {

public: 
  CELL *stack;
  
  construct {
    // set initial val to 0 and next to null
    stack->val = 0;
    stack->next = NULL;
  }
    
};

//Binding code 
EMSCRIPTEN_BINDINGS(Calculator) {
  class_<Calculator>("Calculator")
    .constructor<>()
    .class_function("push", &Calculator::push)
    .class_function("pop", &Calculator::pop)
    .class_function("stackOperator", &Calculator::stackOperator)
    .property("stack", &Calculator)
}


void Calculator::push(int val) {
  CELL *c = (CELL *)malloc(sizeof(CELL));

  if(c) {
    c->val = val;
    c-> next = stack;
    stack = c; // pushes new cell on stack
  } else { /*handle error*/
    printf("something went wront:\n cell memory did not get allocated properly\n");
    exit(1);
  }
}

int Calculator::pop() {
  CELL *c = stack;
  
  if(c) {
    stack = stack->next; //pop
    int val = c->val;
    free(c);
    return val;
  } else {
    printf("The stack is empty\n");
    exit(1);
  }
}

float Calculator::stackOperator(char op, int length) {
  float result;
  int numbers[length];
  int i;

  
  //pop all numbers from the stack since last operation read them into array
  for(i = length; i >= 0; i--)
    numbers[i] = pop();

  //sets initial value for result FIRST ITERATIOn
  switch((int)op) {
  case 42:
    result = (((float)numbers[0]) * numbers[1]);
    break;
  case 43:
    result = (((float)nubers[0]) + numbers [1]);
    break;
  case 45:
    result = (((float)numbers[0]) - numbers[1]);
    break;
  case 47:
    result = (((float)numbers[0]) / numbers[1]);
  default:
    printf("\nERROR:::\n");
    exit(1);
  }

  //calculates result for array items [2, length]
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

void Calculator::stackClearer() {
  while(stack)
    pop();

  return;
}


   
