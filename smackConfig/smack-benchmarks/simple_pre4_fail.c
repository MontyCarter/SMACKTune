#include <stdio.h>
#include <stdlib.h>
#include "smack.h"

// @flag --unroll=2
// @expect error

short incr(short x) {
  return ++x;
}

int main(void) {
  short a;

  a = -2;
  a = incr(a);
  assert(a > -1);
  return a;
}

