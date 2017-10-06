


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
CELL * push(int val);
popReturn * pop(CELL *);
void stringInnitializer(char *p);
int stackOperator(char op);
