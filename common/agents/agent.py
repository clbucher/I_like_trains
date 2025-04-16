import random
from common.base_agent import BaseAgent
from common.move import Move
from server.game import Game
import math

# Student scipers, will be automatically used to evaluate your code
SCIPERS = ["112233", "445566"]
class Agent(BaseAgent):
    def get_move(self):
        """
        Called regularly called to get the next move for your train. Implement
        an algorithm to control your train here. You will be handing in this file.

        For now, the code simply picks a random direction between UP, DOWN, LEFT, RIGHT

        This method must return one of moves.MOVE
        """
        print(self.all_trains)
        print(self.passengers)
        print(self.delivery_zone)

        (x,y)=self.all_trains[self.nickname]['position']
        (nx,ny)=self.all_trains[self.nickname]['direction']

        if self.wall(x,y,nx,ny): #the next move has to be a spesific one, so that we don't collide into the wall
            return self.next_move
       
        # wo er härä geit we ke wand da isch woner chönt inefahre: hie müesse mir t optimierig dri tue!!!!
        self.next_move=Move.RIGHT
        if self.is_not_a_wall(x,y):
            return self.next_move
       


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
        if (x+(nx*self.cell_size))==self.game_width or (x+(nx*self.cell_size))<0: #The train is on the right or left boarder
            match y:
                case 0: #the train in on the top
                    return 'DOWN'
                case self.game_height: #the train is on the bottom
                    return 'UP'
                case _:
                    return 'DOWN OR UP'
        elif (y+(ny*self.cell_size))==self.game_height or (y+(ny*self.cell_size))<0: #the train is on the top or bottom of the playboard
            match x:
                case 0: #the train is next to the left boarder
                    return 'RIGHT'
                case self.game_width: #the train is next to the right boarder
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
        if (x+(Nx*self.cell_size))==self.game_width or (x+(Nx*self.cell_size))<0 or (y+(Ny*self.cell_size))==self.game_height or (y+(Ny*self.cell_size))<0:
            return False
        else:
            return True
    def find_best_Path(self):
        (OP_x,OP_y)=self.all_trains[self.nickname]['position']
        dict_pos={}
        dict_pos[0]=[(x,y)]
        dict_pos["inf"] = []
        dict_pos["B"]=[]
        dict_pos["-"]=[]
        for i in range(self.game_width):
            for j in range(self.game_height):
                if (i,j) in self.passengers:
                    dict_pos["B"].append((i,j))
                for name in self.all_trains:
                    if (i,j) in self.all_trains[name]['position'] or self.all_trains[name]['carts']:
                        dict_pos["-"].append((i,j))
                else:
                    dict_pos["inf"].append((i,j))
        positions=((0,1),(0,-1),(1,0),(-1,0))
        points=[(OP_x,OP_y)]
        counter=-1
        while dict_pos["B"]: #filling the grid
            counter+=1
            dict_pos[counter+1]=[]
            for pt in dict_pos[counter]:
                for h in positions:
                    old_value=counter
                    index_x,index_y=pt
                    nx,ny=h
                    if self.game_height==(index_y+ny) or self.game_width<(index_x+nx) or (index_y+ny)<0 or (index_x+nx)<0:
                        continue
                    if (index_x+nx, index_y+ny) in dict_pos["inf"] or (index_x+nx, index_y+ny) in dict_pos["B"]:
                        new_value=(old_value+1)
                        dict_pos[new_value].append((index_x+nx, index_y+ny))
                        #update all the values to be on the newest stand
                        if (index_x+nx, index_y+ny) in dict_pos["inf"]:
                            dict_pos["inf"].remove((index_x+nx, index_y+ny))
                        else:
                            dict_pos["B"].remove((index_x+nx, index_y+ny))
                            B=new_value
                            path_index=(index_x+nx,index_y+ny)
                            print('you have arrived at B')
                            break
        
        E=0 # finding a trace back up the grid to the starting point
        path=[]
        print(B)
        counter=B
        dict_pos["H"]=[]
        while E!=1:
            counter-=1
            for pt in positions:
                pt_x,pt_y=path_index
                nx,ny=pt
                searching_pt=(pt_x+nx,pt_y+ny)
                print(searching_pt)
                if searching_pt in dict_pos[(counter)]:
                    path.append(searching_pt)
                    path_index=searching_pt
                    print(path)
                    dict_pos["H"].append(pt_y+ny, pt_x+nx)
                    dict_pos[counter].remove(pt_x+nx, pt_y+ny)
                    break
                if counter==0:
                    E=1
                    break
        (x,y)=self.all_trains[self.nickname]["position"]
        (x1, y1) = path[0]
        match self.all_trains[self.nickname]["direction"]:
            case (1,0):
                return('RIGHT')
            case(0,-1):
                return('RIGHT')
            case(-1,0):
                return('LEFT')
            case(0,1):
                return('LEFT')
        #Hie müesse mer no mache ds es öppis returnt wo när macht ds dr Zug sich bewegt. Mi Vorschlag wär ds 
        #die Funktion vor Funktion get_move ufgrüeft wird und so öppis wie "RIGHT" usegit. Und när chönnte mer mache,
        #ds d funktion is wall ou so öppis usegit und när chönnt mä luege ob dr Nächsti Move id Wand würd gah oder nid
        
                
            



                
                    
                    


                    
    
