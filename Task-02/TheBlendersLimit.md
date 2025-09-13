```bash

import math

t = int(input()) #number of test cases

for a in range(t):
    n = int(input())  #total number of fruits to be blended
    x, y = map(int, input().split()) #x = blending rate per unit time, y = loading rate per unit time
    
    time_to_load = math.ceil(n/y)  #time needed to load all fruits
    
    blended_during_load = x * time_to_load #fruits blended during load
    
    remaining = max (0, n - blended_during_load) #Remaining fruits after blending during load
    
    time_extra = math.ceil(remaining/x) #Extra time needed to blend the remaining fruits
    
    total_time = time_to_load + time_extra #Total time
    
    print(total_time)
