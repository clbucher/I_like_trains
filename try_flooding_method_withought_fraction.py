import math
with open("I_like_trains-1.1.0/playboard.txt") as f:
    L=[list(line.strip()) for line in f]

wall='-'
free='.'
end='B'
start='A'



distanz=[[math.inf]*len(L[0]) for _ in range(len(L))]

for y, rowCA in enumerate(L):
    for x, caracter in enumerate(rowCA):
        match L[y][x]:
            case '-':
                distanz[y][x]='_'
            case 'A':
                distanz[y][x]=0
                OP_x=x
                OP_y=y
            case 'B':
                distanz[y][x]='B'
                EP=(x,y)

E=0
positions=((0,1),(0,-1),(1,0),(-1,0))
updated_pt={0:[(OP_x,OP_y)]} #all of the points with a spesific denominator
points=[(OP_x,OP_y)]
counter=0
while E!=1: #filling the grid
    for pt in updated_pt[counter]:
        for h in positions:
            index_x,index_y=pt
            nx,ny=h
            old_value=distanz[index_y][index_x]
            if len(distanz)==(index_y+ny) or len(distanz[0])<(index_x+nx) or (index_y+ny)<0 or (index_x+nx)<0:
                continue
            if distanz[index_y+ny][index_x+nx]==math.inf or distanz[index_y+ny][index_x+nx]=='B':
                new_value=(old_value+1)
                distanz[index_y+ny][index_x+nx]=new_value
                #update all the values to be on the newest stand
                if new_value in updated_pt: #dictionary with all the valued positions with a certain distance
                    updated_pt[new_value].append(((index_x+nx),(index_y+ny)))
                else:
                    updated_pt[new_value]=[(index_x+nx,index_y+ny)]
                points.append((index_x+nx,index_y+ny)) #we add the new distance values
            if L[index_y+ny][index_x+nx]=='B':
                E=1
                print('you have arrived at B')
                break
        for x in distanz:
            print(x)
        if E==1:
            break
        print(" ")
    if E==1:
        break
    counter+=1

# finding a trace back up the grid to the starting point
E=0
#while E!=0:
