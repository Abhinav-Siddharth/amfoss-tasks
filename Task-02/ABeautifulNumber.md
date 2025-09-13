```bash

t = int(input()) #number of test cases

for a in range(t):
    s = list(map(int, input().strip())) #Take input as stringa
    s.sort() #Sort in ascending order
    
    result = []
    required = [9,8,7,6,5,4,3,2,1,0] #List of required digits in desending order
    
    for r in required: #For loop
        for d in s: #Check available digits
            if d>=r: #If digits are greater than or equal to the required digit
                result.append(d) #Take it
                s.remove(d) #And remove it from the available digits
                break #Stop checking and move on to next digit

    #join the digits in result to form the final number string             
    print(''.join(map(str, result))) 
