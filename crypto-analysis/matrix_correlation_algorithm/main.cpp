#include <string>
#include <vector>
#include <cmath>
#include <iostream>
#include <string.h>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdlib.h>
#include <time.h>

using namespace std;


// macros
#define named(outter) goto outter; outter##_skip: if (0) outter:

#define break(blockname) goto blockname##_skip;




//function prototypes
vector<string>* splitStr(char *buff, vector<string> *v, char delim);
long double**  loadMatrix(string fileName, vector<string>* labels);
vector<long double>* splitDbl(char *buff, vector<string> *v, char delim);
long double quality_function(long double **matrix, vector<int> *v);
void random_swap(vector<int> *v);

int main(void) {
  
  vector<string> labels;
  vector<int> *v = new vector<int>();
  
  // load matrix data
  printf("loading matrix\r\n");
  long double** matrix;
  matrix = loadMatrix("crypto_pearson.txt", &labels);
  printf("finished loading\r\n");
  
  // fill index vector
  for(int i = 0; i < labels.size(); i++)
    v->push_back(i);

  // print matrix
  for(int i = 0; i < labels.size(); i++) {
    for(int j = 0; j < labels.size(); j++) {
      printf("%llf  ", matrix[i][j]);
    }
    printf("\r\n");
  }

  // test loop for vector
  for(int i = 0; i < 10; i++) {
    printf("print vector\r\n");
    //for(int i = 0; i < v->size(); i++)
    //  printf("%d  ", (*v)[i]);
    //printf("\r\n");
    
    random_swap(v);
  }
  
  printf("quality function:\t%llf\r\n",  quality_function(matrix, v));

  return 0;
}


//function implementations
vector<string>* splitStr(char *buff, vector<string> *v, char delim) {
  const char d[2] = {delim};
  char *tokens = strtok(buff, d); //char or string? pretty sure char

  while(tokens) {
    //append token to vector
    v->push_back(tokens);
    //pass null pointer and delimeter for next iteration
    tokens = strtok(NULL, d);
  }
  return v;
}

vector<long double>* splitDbl(char *buff, vector<long double> *v, char delim) {
  const char d[2] = {delim};
  char *tokens = strtok(buff, d); //char or string? pretty sure char

  long double tmp;
  while(tokens) {
    //append token to vector
    tmp = strtold(tokens, '\0');
    v->push_back(tmp);
    //pass null pointer and delimeter for next iteration
    tokens = strtok(NULL, d);
  }
  return v;
}

long double**  loadMatrix(string fileName, vector<string>* labels) {
    
  // open file
  ifstream file(fileName.c_str());
  string pars1;
  
  // read in first line
  getline(file, pars1);
  // split list of currencies
  labels = splitStr(((char*)pars1.c_str()), labels, ',');
  
  // truncate extra space 
  for(size_t i = 0; i < labels->size(); i++) {
    string hold = labels->at(i);
    //s.erase(s.find_last_not_of(" \n\r\t")+1);
    int len = hold.length();
    if(i == 0)
      (*labels)[i] = hold.substr(2, len - 3);
    else if(i == labels->size() - 1)
      (*labels)[i] = hold.substr(2, len - 5);
    else 
      (*labels)[i] = hold.substr(2, len - 3);
    
    //cout << labels->at(i) << endl;
    //cout << labels->at(i).length() << endl;
  }
  
  // Dynamically allocate 2d array
  long double** matrix;
  matrix = (long double **)malloc(sizeof(long double*) * labels->size() * labels->size());
  
  
  if(matrix == NULL)
    cout << "Memory was not allocated." << endl;
  
  // allocate inner array's
  for(int i = 0; i < labels->size(); i++) {
    matrix[i] = (long double*)malloc(sizeof(long double) * labels->size());
    
    // error handling
    if(matrix[i] == NULL)
      cout << "Memory was not allocated." << endl;
  }

  //vector<long double> *numbers =(long double *)malloc(sizeof(long double) * labels->size());
  
  
  int i = 0, j = 0;
  while(i < labels->size() && getline(file, pars1)) {
    // read strings into long double vector 
    vector<long double> *numbers = new vector<long double>();
    numbers = splitDbl((char*)pars1.c_str(), numbers, ',');

    // fill the matrix
    for(int j = 0; j < labels->size(); j++) {
      matrix[i][j] = (*numbers)[j];
    } 
    ++i;
  }
  file.close();
  
  return matrix;
}


long double quality_function(long double **matrix, vector<int> *v) {
  long double sum = 0.00;
  bool acabado = false;

  //named(outter)
  for(int i = 0; i < v->size() - 1; i++) {
    for(int j = i + 1;j < v->size() ; j++ ) {
      /*if((*v)[i] > (*v)[j]) {
	acabado = true;
	break;
	}*/
     
      printf("%llf  ", matrix[i][j]);
      sum += (matrix[(*v)[i]][(*v)[j]] / abs(i - j));
    }
    printf("\r\n");
    if(acabado) break;
  }
  return sum;
}


void random_swap(vector<int> *v) {

  //random seed && two random values within vector
  srand(time(NULL));
  //int r1 = rand() % (v->size() - 1);
  //int r2 = rand() % (v->size() - 1);
  printf("%d\r\n", random);
  // swap the vector values
  //int hold = (*v)[r1];
  //(*v)[r1] = (*v)[r2];
  //(*v)[r2] = hold;

}
