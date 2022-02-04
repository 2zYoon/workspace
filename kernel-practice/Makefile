obj-m := myk.o

KDIR := /lib/modules/`uname -r`/build
CC := gcc
CFLAGS := -w -O3

SAMPLES := sample_1 sample_2

all: myk sample

sample:
	for i in $(SAMPLES); do $(CC) -o samples/$$i samples/$$i.c ; done


myk:
	make -C $(KDIR) M=`pwd` modules

clean:
	make -C $(KDIR) M=`pwd` clean
