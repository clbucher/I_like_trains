#version 2.2
#128.179.154.221
import random
from common.base_agent import BaseAgent
from common.move import Move
from server.game import Game
import math
from datetime import datetime

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
    
        train_coordinate = self.convert_grid(self.all_trains[self.nickname]['position'])
        x,y = train_coordinate
        position_collect=self.what_to_collect(x,y)
        #print(f'position to collect {position_collect}')
        next_direction=self.find_next_move(x,y,position_collect)
        next_move=self.convert_NM_coordinate(next_direction)

        #print(f'difference {time_difference}, time after {time_after}, time before {time_before}')
        #print(f'next, move and our current position {next_move, (x,y)}')
        return next_move
    
    def find_next_move(self,x,y,position_collect):
        all_directions=[tuple((0,1)),tuple((0,-1)),tuple((1,0)),tuple((-1,0))]
        our_direction=self.convert_direction(self.all_trains[self.nickname]['direction'])
        ox,oy=our_direction
        backposition=((ox*(-1)),(oy*(-1)))
        all_directions.remove(backposition)
        old_distance=math.inf
        old_direction=(0,0)
        old=[]
        new=[]
        #for x in range(3):
        for i in range(3):
            dx,dy=all_directions[i]
            nx=dx+x
            ny=dy+y
            px,py=position_collect
            #print(f'{nx,ny} nx,ny')
            if self.is_occupied(tuple((nx,ny))):
                #all_directions.remove(tuple((dx,dy)))
                continue
            new_distance=(abs((nx-px))+abs((ny-py)))
            new.append(new_distance)
            if new_distance<old_distance:
                old_distance=new_distance
                old_direction=(dx,dy)
                old.append(old_distance)
        if old_direction==(0,0):
            #print(all_directions, old)
            raise 'problem'
        #print(f'dictinary of all the distances{new,old}')
        return old_direction
            

    def convert_next_move(self,next_move):
        """ 
        converts next move into coordinates dx,dy
        """
        self.move_to_delta = {
            Move.UP:    (0, -1),
            Move.DOWN:  (0, 1),
            Move.RIGHT: (1, 0),
            Move.LEFT:  (-1, 0)
            }
        dx, dy = self.move_to_delta[next_move]
        return tuple((dx,dy))
        
    def convert_NM_coordinate(self,coordinate):
        """"""
        self.move_to_delta = {
            (0, -1): Move.UP,
            (0, 1): Move.DOWN,
            (1, 0): Move.RIGHT,
            (-1, 0): Move.LEFT
            }
        next_move=self.move_to_delta[coordinate]
        return next_move

    def what_to_collect(self,Ox,Oy):
        """
        chooses what to collect next or if it goes to the drop off zone.
        """
        previous_distance=math.inf

        #which is the best passenger to pick
        for number in range(len(self.passengers)):
            value=self.passengers[number]['value']
            position_passenger=self.convert_grid(self.passengers[number]['position'])
            (x,y)=position_passenger
            #we have chosen this estimator as the complexity is O(n) for the number of positons apart
            distance_passenger=((abs((x-Ox)))+(abs((y-Oy)))/(value/2)) 
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

        else:
            distance_wagon=(nearest_drop_off*(0.95**nb_wagons))
        
        #should we go to the drop off zone or should we collect passengers
        if distance_wagon<previous_distance:
            return nearest_drop_coordinate
        else:
            return solution
        
    def is_occupied(self, coordinate):
        """ 
        checks if a specific coordinate is already occupied, by a train or his wagons
        #modifiziert
        """
        x,y = coordinate
        occupied_list=[]
        for name in self.all_trains.keys():
            tx, ty = self.convert_grid(self.all_trains[name]["position"])
            tdx, tdy = self.convert_direction(self.all_trains[name]["direction"])
            wagon_list=self.convert_list(self.all_trains[name]['wagons'])
            occupied_list.append(tuple((tx,ty))) #the head of the train
            for i in wagon_list:
                occupied_list.append(i) #all the wagons
            if name != self.nickname:
                occupied_list.append(tuple((tx+tdx,ty+tdy))) #right in front of the other trains
        #
        # print(f'{occupied_list} occ. list')
        if (x,y) in occupied_list:
            return True
        elif (x == self.WIDTH) or (x < 0) or (y == self.HEIGHT) or (y < 0):
                return True
        else:
            return False
        
    def dropping_off_2_coordinates(self, x1_coordinate, y1_coordinate):
        """ finds the second coordinate of the drop off zone """
        height,width=self.convert_grid((self.delivery_zone['height'],self.delivery_zone['width']))
        x2_coordinate=x1_coordinate+width-1
        y2_coordinate=y1_coordinate+height-1
        return (x2_coordinate, y2_coordinate)
    
    def convert_grid(self,object):
        """converts the object number into a single digit grid to use as coordinates"""
        x=object[0]
        y=object[1]
        x=int(x/self.cell_size)
        y=int(y/self.cell_size)
        return (tuple((x,y)))
    
    def convert_direction(self,object):
        x=object[0]
        y=object[1]
        return(tuple((x,y)))
    
    def convert_gamewith(self):
        """converts the height and width into a single coordinate grid"""
        self.WIDTH=int(self.game_width/self.cell_size)
        self.HEIGHT=int(self.game_height/self.cell_size)

    def convert_list(self,object):
        """
        converts a list ino a list of numers into a single coorinates grid
        """
        new_obj=[]
        if object==[]:
            return new_obj
        for i in object:
            new_obj.append(self.convert_grid(i))
        return new_obj