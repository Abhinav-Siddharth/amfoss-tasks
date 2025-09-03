```bash

import math

t=int(input())

for a in range(t):
    n=int(input())
    x, y=map(int, input().split())
    
    time_to_load = math.ceil(n/y)
    
    blended_during_load = x * time_to_load
    
    remaining = max (0, n - blended_during_load)
    
    time_extra = math.ceil(remaining/x)
    
    total_time = time_to_load + time_extra
    
    print(total_time)
