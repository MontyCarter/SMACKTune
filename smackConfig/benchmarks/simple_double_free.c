#include <stdio.h>
#include <stdlib.h>
#include "smack.h"

// @flag --unroll=2
// @expect verified

#define MAXSIZE 10
#define RESET 0

int main() {
  int *a = (int*)malloc(MAXSIZE * sizeof(int));

  free(a);
  free(a);
  return 0;
}

