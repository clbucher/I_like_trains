#version 2.2
import random
from common.base_agent import BaseAgent
from common.move import Move
from server.game import Game
import math

#next optimasitaions
#TODO(Elina) debug the case where there are two trains (they will crash into the wall or into each other, don't know why)
#drop off optimisation
#last resort if next move would be wall or other train, then turn
#improve weight of distance to drop-off zone in comparison to passengers
#comment all of the code
#prevent head on collison (similar function to is_occupied)


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
        self.train_coordinate = self.convert_grid(self.all_trains[self.nickname]['position'])
        x,y = self.train_coordinate
        dx,dy = self.all_trains[self.nickname]["direction"]
        print(self.all_trains[self.nickname])
        position_collect=self.what_to_collect()
        print(f'positon: {position_collect}')
        Dicth_onary,path_length_passenger=self.find_best_Path_coordonates(self.train_coordinate, position_collect)
        next_move=self.find_best_Path_directions(Dicth_onary)
        '''if self.wall(x,y,dx,dy):
            if next_move in self.next_move:
                self.next_move=next_move
                if self.is_not_a_wall(x,y):
                return next_move
            else:
                return(self.next_move[0])'''

        return next_move  

        '''
        if len(self.all_trains[self.nickname]['wagons'])<4:
            passenger_number=0
            passenger_coord=self.convert_grid(self.passengers[passenger_number]['position'])
            Dicth_onary,path_length_passenger=self.find_best_Path_coordonates(self.train_coordinate, passenger_coord)
            next_move=self.find_best_Path_directions(Dicth_onary)
            return next_move       
        
        else:
            dropoff_coord=self.convert_grid(self.delivery_zone['position'])
            drop_path,path_length_dropoff=self.find_best_Path_coordonates(self.train_coordinate, dropoff_coord)
            next_move=self.find_best_Path_directions(drop_path)
            return next_move
        '''
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


    def what_to_collect(self):
        """gives us a dictionary with the fraction distance/value so that we can compare 
        the different passengers with each other"""
        previous_distance=math.inf

        #which is the best passenger to pick
        
        for number in range(len(self.passengers)):
            value=self.passengers[number]['value']
            position_passenger=self.convert_grid(self.passengers[number]['position'])
            (x,y)=position_passenger
            (Ox,Oy)=self.train_coordinate
            #we have chosen this estimator as the complexity is O(n) for the number of positons apart
            distance_passenger=((abs((x-Ox)))+(abs((y-Oy)))/value) 
            #TODO value wird i dere gliichig z fest gwichtet
            #distance_passenger=((abs((x-Ox)))+(abs((y-Oy)))) 
            if distance_passenger<previous_distance:
                previous_distance=distance_passenger
                solution=position_passenger
        
        #distance of the dropoff zone
        (drop_off_x,drop_off_y)=self.convert_grid(self.delivery_zone['position'])
        (drop_off2_x, drop_off2_y)=self.dropping_off_2_coordinates(drop_off_x,drop_off_y)
        if self.is_occupied((drop_off_x,drop_off_y)):
            distance_drop_off=math.inf
        else:
            distance_drop_off=(abs((drop_off_x-Ox))+abs((drop_off_y-Oy)))
        if self.is_occupied((drop_off2_x, drop_off2_y)):
            distance_drop_off2=math.inf
        else:
            distance_drop_off2=(abs((drop_off2_x-Ox))+abs((drop_off2_y-Oy)))

        if distance_drop_off<distance_drop_off2:
            nearest_drop_off=distance_drop_off
            nearest_drop_coordinate=(drop_off_x,drop_off_y)
        else:
            nearest_drop_off=distance_drop_off2
            nearest_drop_coordinate=(drop_off2_x, drop_off2_y)
        nb_wagons=len(self.all_trains[self.nickname]['wagons'])
        if nb_wagons==0:
            distance_wagon=math.inf
            """elif (drop_off_x,drop_off_y) in self.all_trains[self.nickname]["wagons"]:
            distance_wagon = math.inf""" #ds wär damit är nid i sich säuber dri fahrt bri drop off zone. aber mä müesst di zwöiti Koordinate ou no chegge
            """
        elif self.wagondropoff==1:
            return self.optimum_droping_off(drop_off_x,drop_off_y)
            """
        else:
            #distance_wagon=(nearest_drop_off/(nb_wagons+0.0000001))
            distance_wagon=(nearest_drop_off*(0.95**nb_wagons))
            #wagons werde hie ou viu z fest gwichtet!! 
            #z.b mit nearest_drop_off*(0.95^nb_wagon)??
            #distance_wagon=nearest_drop_off
        
        #should we go to the drop off zone or should we collect passengers
        if distance_wagon<previous_distance:
            return nearest_drop_coordinate
        else:
            return solution
        
    def is_occupied(self, coordinate):
        """ is checking if a spesific coordinate is already occupied, by a train or his wagons"""
        for name in self.all_trains.keys():
            #if self.all_trains[name]['alive'] == False:
                #continue
            if coordinate == self.convert_grid(self.all_trains[name]['position']) or coordinate in self.convert_list(self.all_trains[name]['wagons']):
                return True
        return False
        
    def dropping_off_2_coordinates(self, x1_coordinate, y1_coordinate):
        """opptimisez drop off"""
        print(f'delivery zone {self.delivery_zone}') 
        height,width=self.convert_grid((self.delivery_zone['height'],self.delivery_zone['width']))
        x2_coordinate=x1_coordinate+width-1
        y2_coordinate=y1_coordinate+height-1
        print(f'coordinates of first point {x1_coordinate, y1_coordinate}')
        print(f'coordinates of second point {x2_coordinate,y2_coordinate}') 
        return (x2_coordinate, y2_coordinate)

    
    def convert_grid(self,object):
        """converts the object number into our grid to use as coordinates"""
        x,y=object
        x=int(x/self.cell_size)
        y=int(y/self.cell_size)
        return (x,y)
    
    def convert_gamewith(self):
        """converts the height and width into a number for every cell"""
        self.WIDTH=int(self.game_width/self.cell_size)
        self.HEIGHT=int(self.game_height/self.cell_size)

    def convert_list(self,object):
        """converts a list ino a list of numers into our coorinates (one number per cell)"""
        new_obj=[]
        if object==[]:
            return new_obj
        for i in object:
            new_obj.append(self.convert_grid(i))
        return new_obj         

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
                self.next_move= [Move.DOWN]
                return True
            case 'UP':
                self.next_move= [Move.UP]
                return True
            case 'DOWN OR UP':
                self.next_move=[Move.UP, Move.DOWN]
                return True
            case 'RIGHT':
                self.next_move= [Move.RIGHT]
                return True
            case 'LEFT':
                self.next_move= [Move.LEFT]
                return True
            case 'RIGHT OR LEFT':
                self.next_move=[Move.LEFT,Move.RIGHT]
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
        

    def find_best_Path_coordonates(self,your_coordinate,find_coordinate):
        """We find a list of the coordonates of the best path to the passenger"""
        find_coordinate=tuple(find_coordinate)
        B=0
        (OP_x,OP_y)=your_coordinate
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
                for name in self.all_trains.keys():
                    #if self.all_trains[name]['position'] == [-1,-1]:
                    #    continue wiu i ha gseh ds wenn ä Zug tot isch het är d Koordinate [-1,-1] ha eifach wöue sicher si ds es nid ds isch
                    if coordinate == self.convert_grid(self.all_trains[name]['position']) or coordinate in self.convert_list(self.all_trains[name]['wagons']) or coordinate == backpositon:
                        dict_pos["-"].append(coordinate)                      
                    else:
                        dict_pos["inf"].append((i,j))
                """if find_coordinate in dict_pos["-"]:
                    luege was me denn söt mache, wöu itz killt er sech (wöu z feud isch e wall, drum nid dert druf!!)
                    cha si das das ou z problem mit de zwe bots isch!!
                    die die generelli funktion vo not wall bruche
                """
                if coordinate == find_coordinate: #find the spesific input of our function
                    dict_pos["B"].append(coordinate)

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
        """this translates the list of the path into movements that we have to do"""
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