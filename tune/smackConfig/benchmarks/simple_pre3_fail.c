#include <stdio.h>
#include <stdlib.h>
#include "smack.h"

// @flag --unroll=2
// @expect error

int returnOne() {
  return 1;
}

int main(void) {
  int a;

  a = -1;
  a = returnOne();
  assert(a == -1 || a == 2);
  return a;
}

