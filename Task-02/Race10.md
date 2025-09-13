```bash

t = int(input())      # number of test cases
for _ in range(t):    # repeat for each test case
    a, x, y = map(int, input().split())  # read 3 numbers
    if x > y:         # making sure x is the smaller one
        x, y = y, x   #swap x and y
    if a < x or a > y:  # check if 'a' is outside the [x,y] range
        print("YES") #if outside
    else:
        print("NO")  #if inside

