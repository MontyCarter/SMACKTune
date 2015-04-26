#include "smack.h"

// @flag --unroll=2
// @expect verified

signed int gcd_test(signed int a, signed int b)
{
    signed int t;

    if (a < 0) a = -a;
    if (b < 0) b = -b;

    while (b != 0) {
        t = b;
        b = a % b;
        a = t;
    }
    return t;
}


int main()
{
    //signed int x = __SMACK_nondet();
    //signed int y = __SMACK_nondet();
    signed int x = 12;
    signed int y = 4;
    signed int g;

    if (y > 0 && x % y == 0) {
	    g = gcd_test(x, y);
	    assert(g == y);
    }

    return 0;
}
