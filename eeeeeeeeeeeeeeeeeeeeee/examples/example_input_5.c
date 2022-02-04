/* code that possibly causing conflict */
#include <stdio.h>
/* do not use ee in both case:
#define ee (something)
#define (something) ee
*/
#define ee 155


int main(){
    int a = 0;
#ifdef eeeee
    printf("eeeee: This should not be printed\n");
    return -1;
#endif

#ifndef eeeeee
    a++;
#endif
    if (a != 1){
        printf("eeeeee: This should not be printed\n");
        return -1;
    }
    

#if defined (eeee)
    printf("eeee: This should not be printed\n");
    return -1;
#endif

#if defined(eeeeeee)
    printf("eeeeeee: This should not be printed\n");
    return -1;
#endif


#if defined(eeeeeeee) | defined (eeeeeeeeeeeeeeee)
    printf("This should not be printed\n");
    return -1;
#endif



    printf("ADD: %d\n", ee);
    return 0;
}
