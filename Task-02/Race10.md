```bash

t = int(input())
for _ in range(t):
    a, x, y = map(int, input().split())
    if x > y:
        x, y = y, x
    if a < x or a > y:
        print("YES")
    else:
        print("NO")
