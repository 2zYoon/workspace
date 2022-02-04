#include <stdio.h>
#include <omp.h>
#include <unistd.h>

#define Nt 4

int glob;
#pragma omp threadprivate(glob)

int main(){
    int some_shared = 0;
    omp_set_num_threads(Nt);

    // basic parallel
    #pragma omp parallel
    printf("[%d]", omp_get_thread_num());
    printf("\n");

    // parallel for (1)
    #pragma omp parallel for
    for (int i = 0; i < 11; i++)
        printf("[%d %d]", omp_get_thread_num(), i);
    printf("\n");

    // parallel for (2)
    // nested
    #pragma omp parallel for
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            printf("[%d %d %d]", omp_get_thread_num(), i, j);
    printf("\n");

    // parallel, inner initialization
    #pragma omp parallel default(shared)
    {
        int my_var = 15; // private
        some_shared++; // danger! just for practice

        my_var += omp_get_thread_num();
        printf("[%d %d %d]", omp_get_thread_num(), my_var, some_shared);
    }
    printf("\n");

    // parallel, critical section
    some_shared = 0;
    #pragma omp parallel default(shared)
    {
        int my_var = 999;
        #pragma omp critical
        {
            my_var = some_shared++; 
        }
        printf("[%d %d]", omp_get_thread_num(), my_var);
    }
    printf("\n");

    // parallel, atomic
    some_shared = 0;
    #pragma omp parallel default(shared)
    {
        #pragma omp atomic
        some_shared++;
    }
    printf("[shared: %d]\n", some_shared);

    // parallel, private
    int a1 = 123;
    #pragma omp parallel default(shared) private(a1)
    {
        printf("[%d %d]", omp_get_thread_num(), a1);
    }
    printf("\n");

    // parallel, firstprivate
    int a2 = 123;
    #pragma omp parallel default(shared) firstprivate(a2)
    {
        printf("[%d %d]", omp_get_thread_num(), a2);
    }
    printf("\n");

    // barrier
    #pragma omp parallel
    {
        if (omp_get_thread_num() == 2)
            usleep(1000);

        #pragma omp barrier
        printf("[%d]", omp_get_thread_num());
    }
    printf("\n");

    // without barrier, but implicitly waits in a region
    #pragma omp parallel
    {
        if (omp_get_thread_num() == 2)
            usleep(1000);

        printf("[%d]", omp_get_thread_num());
    }
    printf("\n");

    // without barrier, but implicitly waits in a for-loop
    #pragma omp parallel
    {
        if (omp_get_thread_num() == 2)
            usleep(1000);

        #pragma omp for
        for (int i = 0; i < 8; i++)
            printf("[%d %d]", omp_get_thread_num(), i);
        printf("[DONE %d]", omp_get_thread_num());
    }
    printf("\n");

    // nowait
    #pragma omp parallel
    {
        if (omp_get_thread_num() == 2)
            usleep(1000);

        #pragma omp for nowait
        for (int i = 0; i < 8; i++)
            printf("[%d %d]", omp_get_thread_num(), i);
        printf("[DONE %d]", omp_get_thread_num());
    }
    printf("\n");
    
    // threadprivate
    #pragma omp parallel
    {
        glob = omp_get_thread_num();      
    }
    #pragma omp parallel
    {
        glob += omp_get_thread_num();
        printf("[%d %d]", omp_get_thread_num(), glob);        
    }
    printf("\n");
    
    // threadprivate: what happens if thnum changes?
    // 5, 6: zero val at init... maybe not initialized
    #pragma omp parallel
    {
        glob = omp_get_thread_num();      
    }
    omp_set_num_threads(Nt+2);
    #pragma omp parallel
    {
        glob += omp_get_thread_num();
        printf("[%d %d]", omp_get_thread_num(), glob);        
    }
    printf("\n");
    omp_set_num_threads(Nt);

    // thread num without parallel region? 0
    printf("[THNUM: %d]\n", omp_get_thread_num());

    // master 0
    #pragma omp master
    printf("[MASTER: %d]\n", omp_get_thread_num());

    // single (others blocked)
    #pragma omp single
    printf("[SINGLE: %d]\n", omp_get_thread_num());

    // scheduling
    #pragma omp parallel 
    {
        int cnt_static = 0;
        int cnt_dynamic = 0;
        int cnt_guided = 0;

        // static (default)
        #pragma omp for schedule(static)
        for (int i = 0; i < 36; i++)
            cnt_static++;
        printf("[STATIC %d %d]", omp_get_thread_num(), cnt_static);
        cnt_static = 0;

        #pragma omp barrier
        #pragma omp single
        printf("\n");

        // static, bigger chunk
        #pragma omp for schedule(static, 14)
        for (int i = 0; i < 36; i++)
            cnt_static++;
        printf("[STATIC_BIGGER %d %d]", omp_get_thread_num(), cnt_static);
        cnt_static = 0;        

        #pragma omp barrier
        #pragma omp single
        printf("\n");

        // static, smaller chunk
        #pragma omp for schedule(static, 6)
        for (int i = 0; i < 36; i++)
            cnt_static++;
        printf("[STATIC_SMALLER %d %d]", omp_get_thread_num(), cnt_static);
        cnt_static = 0;        

        #pragma omp barrier
        #pragma omp single
        printf("\n");

        // dynamic, smaller chunk
        #pragma omp for schedule(dynamic, 6)
        for (int i = 0; i < 36; i++)
            cnt_dynamic++;
        printf("[DYNAMIC_SMALLER %d %d]", omp_get_thread_num(), cnt_dynamic);
        cnt_dynamic = 0;        

        #pragma omp barrier
        #pragma omp single
        printf("\n");

        // dynamic, bigger chunk
        #pragma omp for schedule(dynamic, 19)
        for (int i = 0; i < 36; i++)
            cnt_dynamic++;
        printf("[DYNAMIC_BIGGER %d %d]", omp_get_thread_num(), cnt_dynamic);
        cnt_dynamic = 0;        

        #pragma omp barrier
        #pragma omp single
        printf("\n");

        // guided, smaller chunk
        #pragma omp for schedule(guided, 7)
        for (int i = 0; i < 36; i++)
            cnt_guided++;
        printf("[GUIDED_SMALLER %d %d]", omp_get_thread_num(), cnt_guided);
        cnt_guided = 0;        

        #pragma omp barrier
        #pragma omp single
        printf("\n");

        // guided, bigger chunk
        #pragma omp for schedule(guided, 17)
        for (int i = 0; i < 36; i++)
            cnt_guided++;
        printf("[GUIDED_BIGGER %d %d]", omp_get_thread_num(), cnt_guided);
        cnt_guided = 0;        

        #pragma omp barrier
        #pragma omp single
        printf("\n");

        // additional
        int tmp = 0;
        #pragma omp for schedule(static, 10000000)
        for (int i = 0; i < 10000010; i++)
            tmp++;
        printf("[ADDITIONAL %d %d]", omp_get_thread_num(), tmp);

        #pragma omp barrier
        #pragma omp single
        printf("[CALL %d]", omp_get_thread_num());
    }

    printf("\n");
    
    // section
    #pragma omp parallel
    {
        int cnt = 0;
        
        // less section
        #pragma omp sections
        {
            #pragma omp section
            cnt++;

            #pragma omp section
            cnt++;
        }
        printf("[%d %d]", omp_get_thread_num(), cnt);
        cnt = 0;

        #pragma omp barrier
        #pragma omp single
        printf("\n");
        
        // more section -> no guarantee of fairness
        #pragma omp sections
        {
            #pragma omp section
            cnt++;

            #pragma omp section
            cnt++;
            
            #pragma omp section
            cnt++;
            
            #pragma omp section
            cnt++;
            
            #pragma omp section
            cnt++;
        }
        printf("[%d %d]", omp_get_thread_num(), cnt);
        cnt = 0;

        #pragma omp barrier
        #pragma omp single
        printf("\n");
    }

    // for reduction - sum
    int sum = 0;
    #pragma omp parallel for reduction(+:sum)
    for (int i = 1; i < 101; i++)
        sum += i;

    printf("[SUM: %d]\n", sum);

}