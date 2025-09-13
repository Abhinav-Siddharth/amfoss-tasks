```bash

t = int(input()) # number of test cases

for x in range(t):
    n = int(input()) # length of the binary string
    s = input().strip() #Take string inputs
    
    original_ones = s.count("1") # count how many 1s are in the original string
    total_ones = 0

    for i in range(n):
        if s[i] == '0':
            total_ones += original_ones + 1 # if current string is 0 so flipping it to 1 increases count of 1s by 1
        else:
            total_ones += original_ones - 1  # if current string is 1 so flipping it to 0 decreases count of 1s by 1
    
    print(total_ones)
