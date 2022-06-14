#include <stdio.h>
#include <stdlib.h>

struct temp {
    int a;
    int b;
    int *c;
};


int main(){
    int *a = (int*)malloc(sizeof(int)); 
    struct temp *hi = (struct temp*)malloc(sizeof(struct temp)); 
    hi->a = 15;
    hi->b = 100;
    hi->c = a;

    int *d = hi->c;

    printf("malloc. %d %d %d %d\n", hi->a, hi->b, hi->c, d);

    free(hi);

    printf("free. %d %d %d %d\n", hi->a, hi->b, hi->c, d);


    printf("hello\n");
}