#!/bin/bash

# Remove previous one
rmmod myk
rm /dev/myk

# Insert kernel module and device file
insmod myk.ko
mknod /dev/myk c 297 0
chmod 777 /dev/myk
