t=int(input())

for a in range(t):
    s=list(map(int, input().strip()))
    s.sort()
    
    result = []
    required = [9,8,7,6,5,4,3,2,1,0]
    
    for r in required:
        for d in s:
            if d>=r:
                result.append(d)
                s.remove(d)
                break
                
    print(''.join(map(str, result))) 
