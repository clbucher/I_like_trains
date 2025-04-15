import math
with open("I_like_trains-1.1.0/playboard.txt") as f:
    L=[list(line.strip()) for line in f]

wall='-'
free='.'
end='B'
start='A'

def calculate_distance(O,E):
    x1,y1=O
    x2,y2=E
    d=math.sqrt(math.pow((x1-x2),2))+math.sqrt(math.pow((y1-y2),2))
    return d

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
d=calculate_distance(((OP_x),(OP_y)), EP)
updated_distances=[d] #all of the denominators
updated_pt={d:[(OP_x,OP_y)]} #all of the points with a spesific denominator
point_eigenschaften={(OP_x,OP_y):[]}
#there has to be another way to do the counter!!!!!!
counter=0
while E!=1:
    dist=min(updated_distances)
    counter+=1
    for h in positions:
        index_x,index_y=(updated_pt[dist][0])
        nx,ny=h
        if len(distanz)<(index_y+ny) or len(distanz[0])<(index_x+nx) or (index_y+ny)<0 or (index_x+nx)<0:
            continue
        print((index_y+ny),(index_x+nx),ny,nx,updated_distances, dist)
        #print(updated_pt)
        if distanz[index_y+ny][index_x+nx]==math.inf or distanz[index_y+ny][index_x+nx]=='B':
            print(len(distanz), len(distanz[0]),(index_y+ny),(index_x+nx))
            d=calculate_distance(((index_x+nx),(index_y+ny)), EP)
            print(d,'this is d')
            new_d=(d+counter)
            print(new_d)
            bruch=(counter/new_d)
            distanz[index_y+ny][index_x+nx]=bruch

            #update all the values to be on the newest stand
            if new_d in updated_pt: #dictionary with all the valued positions with a certain distance
                updated_pt[new_d].append(((index_x+nx),(index_y+ny)))
            else:
                updated_pt[new_d]=[(index_x+nx,index_y+ny)]
            updated_distances.append(new_d) #we add the new distance values
        if L[index_y+ny][index_x+nx]=='B':
            E=1
            print('you have arrived at B')

    updated_pt[dist].remove((index_x, index_y)) #we remove the coordinate of the value we just used
    if updated_pt[dist] ==[]:
        del updated_pt[dist]
    updated_distances.remove(dist) #we take the distance value we just used out of the list
    print(counter)
    for x in distanz:
        print(x)


