

#include <iostream>
#include "Calculator.h"
#include <emscripten/bind.h>

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
  
  //member function declarations
  void push(int val);
  int pop();
  float stackOperator(char op, int length);
  void stackClearer();

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
  
}

int Calculator::pop() {

}

float Calculator::stackOperator(char op, int length) {

}

void Calculator::stackClearer() {

}


   
