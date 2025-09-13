```bash

t = int(input()) #Take in the no. of cases

for _ in range(t):
    n = int(input()) #Take the length of arrays
    arr = list(map(int, input().split())) #Take the arrays
    arr.sort() #Sort them
    
    if arr[0] % 2 == arr[-1] % 2: #Check if first and last number make perfect array
        print(0)
    else: #start eliminating numbers from left
        left = 0
        right = n - 1
        operations = 0
        
        while left < right and arr[left] % 2 != arr[right] % 2: 
            left += 1
            operations += 1
        
        if left < right and arr[left] % 2 == arr[right] % 2:
            print(operations)
        else: #If left couldn't get shorter answer go and eliminate from the right.
            operations = 0
            left = 0
            right = n - 1
            while left < right and arr[left] % 2 != arr[right] % 2:
                right -= 1
                operations += 1
            print(operations)
