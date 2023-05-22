#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <fmem.h>

static fmem fm;

int main() {
    FILE *f = fmem_open(&fm, "w+");
    assert(f);
    fclose(f);
}
