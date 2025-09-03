```bash
t = int(input())

for x in range(t):
    n = int(input())
    s = input().strip()
    
    original_ones = s.count("1")
    total_ones = 0

    for i in range(n):
        if s[i] == '0':
            total_ones += original_ones + 1
        else:
            total_ones += original_ones - 1
    
    print(total_ones)
