


/*   Author:   David Gutsch
     Date:     08/29/2017       */


/*  struct  */
typedef struct cell {
  int val;
  struct cell *next;
} CELL;

typedef struct popReturn {
  int curVal;
  CELL curStack;
} popReturn;

// linked list 
CELL *stack;

/* function prototypes */
void push(int val);
int  pop();
void stringInnitializer(char *);
float stackOperator(char,int);
void stackClearer();
void stackPrinter();
