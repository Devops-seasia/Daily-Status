#!/bin/bash

# Loop using for loop
echo "Printing numbers 1 to 5 using a for loop:"
for i in {1..5}
do
  echo $i
done

# Loop using while loop
echo "Printing numbers 1 to 5 using a while loop:"
j=1
while [ $j -le 5 ]
do
  echo $j
  j=$((j+1))
done
