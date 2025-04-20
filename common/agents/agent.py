#version 2.1
import random
from common.base_agent import BaseAgent
from common.move import Move
from server.game import Game
import math

# Student scipers, will be automatically used to evaluate your code
SCIPERS = ["112233", "445566"]
class Agent(BaseAgent,Game):
    def get_move(self):
        """
        Called regularly called to get the next move for your train. Implement
        an algorithm to control your train here. You will be handing in this file.

        For now, the code simply picks a random direction between UP, DOWN, LEFT, RIGHT

        This method must return one of moves.MOVE
        """
        #will change game width into a coordinate system which is divided by cell size
        self.convert_gamewith() 
        print(self.all_trains)
        
        if len(self.all_trains[self.nickname]['wagons'])<4:
            passenger_coord=self.convert_grid(self.passengers[0]['position'])
            Dicth_onary,path_length=self.find_best_Path_coordonates(passenger_coord)
            next_move=self.find_best_Path_directions(Dicth_onary)
            return next_move       
        
        else:
            dropoff_coord=self.convert_grid(self.delivery_zone['position'])
            drop_path,pathlength=self.find_best_Path_coordonates(dropoff_coord)
            next_move=self.find_best_Path_directions(drop_path)
            return next_move
        

        
        '''
        (x,y)=self.convert_grid(self.all_trains[self.nickname]['position'])
        (nx,ny)=self.all_trains[self.nickname]['direction']

        if self.wall(x,y,nx,ny): #the next move has to be a spesific one, so that we don't collide into the wall
            return self.next_move
       
        # wo er härä geit we ke wand da isch woner chönt inefahre: hie müesse mir t optimierig dri tue!!!!
        self.next_move=Move.RIGHT
        if self.is_not_a_wall(x,y):
            return self.next_move
        '''
    
    def convert_grid(self,object):
        x,y=object
        x=int(x/self.cell_size)
        y=int(y/self.cell_size)
        return (x,y)
    
    def convert_gamewith(self):
        self.WIDTH=int(self.game_width/self.cell_size)
        self.HEIGHT=int(self.game_height/self.cell_size)

    def convert_list(self,object):
        new_obj=[]
        if object==[]:
            return new_obj
        for i in object:
            new_obj.append(self.convert_grid(i))
        return new_obj         

    def next_best_move(self):
        passenger_info={}
        for passenger_cord in self.convert_grid(self.passengers['positon']):
            passenger_info[self.passengers['value']]=(self.find_best_Path_coordonates(self,passenger_cord))
        return passenger_info
    '''
    def drop_passengers_off(self):
        x=self.convert_grid(self.delivery_zone['position'])
        local_next_move=self.find_best_Path_coordonates(x)
        return local_next_move
    '''


    def wall(self,x,y,nx,ny):
        """
        this will be the first condition we will check when planing the next move since we:
        - check if we have to do a spesific move, as not to drive into the wall (True).
        - if we are going straight into the wall we will change direction
        If this is not the case we will retrn False.
        """
        turn_before_wall=self.miss_the_wall(x,y,nx,ny)
        match turn_before_wall: #will dictate the next move if there is a chance to collide with it
            case 'DOWN':
                self.next_move= Move.DOWN
                return True
            case 'UP':
                self.next_move= Move.UP
                return True
            case 'DOWN OR UP':
                CHOISE=(Move.UP, Move.DOWN)
                self.next_move=random.choice(CHOISE) #random choise of the change of direction
                while not self.is_not_a_wall(x,y): #this will chose the next move until the chosen movement will not make us collide with the wall
                    self.next_move=random.choice(CHOISE)
                return True
            case 'RIGHT':
                self.next_move= Move.RIGHT
                return True
            case 'LEFT':
                self.next_move= Move.LEFT
                return True
            case 'RIGHT OR LEFT':
                CHOISE=(Move.LEFT,Move.RIGHT)
                self.next_move=random.choice(CHOISE) #random choise of the change of direction
                while not self.is_not_a_wall(x,y):#this will chose the next move until the chosen movement will not make us collide with the wall
                    self.next_move=random.choice(CHOISE)
                return True
        return False
   
    def miss_the_wall(self,x,y,nx,ny):
        """
        checks if there is a wall in front of the train where the next move would be if we don't change direction.
        This will then also tell us in which direction we can't turn because there is also a wall there.
        """
        if (x+nx)==self.WIDTH or (x+nx)<0: #The train is on the right or left boarder
            match y:
                case 0: #the train in on the top
                    return 'DOWN'
                case self.HEIGHT: #the train is on the bottom
                    return 'UP'
                case _:
                    return 'DOWN OR UP'
        elif (y+ny)==self.HEIGHT or (y+ny)<0: #the train is on the top or bottom of the playboard
            match x:
                case 0: #the train is next to the left boarder
                    return 'RIGHT'
                case self.WIDTH: #the train is next to the right boarder
                    return 'LEFT'
                case _:
                    return 'RIGHT OR LEFT'
               
    def is_not_a_wall(self,x,y):
        """
        we check that the next move would not lead us outside of the game
        """
        match self.next_move:
            case Move.UP:
                (Nx,Ny)=(0, -1)
            case Move.DOWN:
                (Nx,Ny)=(0, 1)
            case Move.RIGHT:
                (Nx,Ny)=(1, 0)
            case Move.LEFT:
                (Nx,Ny)=(-1, 0)
        if (x+Nx)==self.WIDTH or (x+Nx)<0 or (y+Ny)==self.HEIGHT or (y+Ny)<0:
            return False
        else:
            return True
        
    def find_best_Path_coordonates(self,find_coordinate):
        """We find the coordonates of the best path to the passenger"""
        find_coordinate=tuple(find_coordinate)
        B=0
        (OP_x,OP_y)=self.convert_grid(self.all_trains[self.nickname]['position'])
        (Ox,Oy)=self.all_trains[self.nickname]['direction']
        backpositon=tuple(((OP_x-Ox),(OP_y-Oy))) # going packwards is not possible and seen as an obstacle
        dict_pos={}
        dict_pos[0]=[(OP_x,OP_y)]
        dict_pos["inf"] = []
        dict_pos["B"]=[]
        dict_pos["-"]=[]
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                coordinate=tuple((i,j))
                if coordinate == find_coordinate: #find the spesific input of our function
                    dict_pos["B"].append(coordinate)
                for name in self.all_trains.keys():
                    if coordinate == self.convert_grid(self.all_trains[name]['position']) or coordinate in self.convert_list(self.all_trains[name]['wagons']) or coordinate == backpositon:
                        dict_pos["-"].append(coordinate)                      
                    else:
                        dict_pos["inf"].append((i,j)) 
        print(self.nickname, dict_pos["-"])             
        positions=((0,1),(0,-1),(1,0),(-1,0))
        counter=-1
        E=0
        while E==0: #filling the grid
            counter+=1
            dict_pos[counter+1]=[]
            for pt in dict_pos[counter]:
                for h in positions:
                    old_value=counter
                    index_x,index_y=pt
                    nx,ny=h
                    new_coordinate=tuple((index_x+nx, index_y+ny))
                    # check if we are out of bound
                    if self.HEIGHT==(index_y+ny) or self.WIDTH<(index_x+nx) or (index_y+ny)<0 or (index_x+nx)<0:
                        continue
                    if new_coordinate in dict_pos["inf"] or new_coordinate in dict_pos["B"]:
                        new_value=(old_value+1)
                        if new_coordinate == find_coordinate:
                            E=1
                            B=new_value
                            path_index=new_coordinate
                            break
                        dict_pos[new_value].append(new_coordinate)
                        #update all the values to be on the newest stand
                        if new_coordinate in dict_pos["inf"]:
                            dict_pos["inf"].remove(new_coordinate)
                if E==1:
                    break

        E=0 # finding a trace back up the grid to the starting point
        path=[]
        counter=B
        dict_pos["H"]=[]
        while E==0:
            counter-=1
            for pt in positions:
                pt_x,pt_y=path_index
                nx,ny=pt
                searching_pt=(pt_x+nx,pt_y+ny)
                if counter==0:
                    E=1
                    path.reverse()
                    path.append(find_coordinate)
                    return (path,B)
                elif searching_pt in dict_pos[(counter)]:
                    path.append(searching_pt)
                    path_index=searching_pt
                    dict_pos["H"].append((pt_y+ny, pt_x+nx))
                    dict_pos[counter].remove((pt_x+nx, pt_y+ny))
                    break

    def find_best_Path_directions(self, path):
        (x,y)=self.convert_grid(self.all_trains[self.nickname]["position"])
        (x1, y1) = path[0]
        Nx=(x1-x)
        Ny=(y1-y)
        match (Nx,Ny):
            case (1,0):
                return Move.RIGHT
            case(-1,0):
                return Move.LEFT
            case(0,-1):
                return Move.UP
            case(0,1):
                return Move.DOWN