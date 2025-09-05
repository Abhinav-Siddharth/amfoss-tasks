```bash

t = int(input())

for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    arr.sort()
    
    if arr[0] % 2 == arr[-1] % 2: 
        print(0)
    else:
        left = 0
        right = n - 1
        operations = 0
        
        while left < right and arr[left] % 2 != arr[right] % 2:
            left += 1
            operations += 1
        
        if left < right and arr[left] % 2 == arr[right] % 2:
            print(operations)
        else:
            operations = 0
            left = 0
            right = n - 1
            while left < right and arr[left] % 2 != arr[right] % 2:
                right -= 1
                operations += 1
            print(operations)
