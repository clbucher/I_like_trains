#version 2.2
#128.179.154.221
import random
from common.base_agent import BaseAgent
from common.move import Move
from server.game import Game
import math


# Student scipers, will be automatically used to evaluate your code
SCIPERS = ["391884", "398510"]
class Agent(BaseAgent):
    def get_move(self):
        """
        Called regularly called to get the next move for your train. Implement
        an algorithm to control your train here
        """
        #will change game width into a coordinate system which is divided by cell size
        self.convert_gamewith()

        train_coordinate = self.convert_grid(self.all_trains[self.nickname]['position'])
        x,y = train_coordinate
        (drop_off_x,drop_off_y)=self.convert_grid(self.delivery_zone['position'])
        (drop_off2_x, drop_off2_y)=self.dropping_off_2_coordinates(drop_off_x,drop_off_y) 
        othername=[]
        for name in self.all_trains.keys():
                    if name != self.nickname:
                        othername.append(name)
        match len(self.all_trains):
            case 2: #killing other train
                if self.we_are_best() and self.we_not_on_bestrun() and self.best_scores[self.nickname]>50:
                    difference_score=self.best_scores[self.nickname]-self.all_trains[othername[0]]['score']
                    if (difference_score>30):
                        next_move=self.kill_other(x,y,othername)
                        return next_move
                
            case 3: #killing method around dropoff
                if drop_off_x and drop_off_y and drop_off2_x and drop_off2_y:
                    if self.we_are_best() and self.we_not_on_bestrun() and self.best_scores[self.nickname]>60:
                        next_move=self.circle_dropoff(x,y)
                        return next_move
            case 4: #killing the train with the closest score to ours
                difference_score=math.inf
                if self.we_are_best() and self.we_not_on_bestrun() and self.best_scores[self.nickname]>70:
                    for i in range(len(othername)):
                        difference_score_new=self.best_scores[self.nickname]-self.all_trains[othername[0]]['score']
                        if difference_score_new<difference_score:
                            difference_score=difference_score_new
                            train_to_kill=othername[i]
                    if difference_score<25:
                        next_move=self.kill_other(x,y,train_to_kill)
                        return next_move

        position_collect=self.what_to_collect(x,y)
        next_direction=self.find_next_move(x,y,position_collect)
        next_move=self.convert_NM_coordinate(next_direction)
        return next_move
    
    def kill_other(self,x,y,othername):
        """ 
        Is called when we should go kill the other train. 
        x, y is our trains position
        othername is the nickname of the train we are trying to kill. Cannot be our own name
        Returns the next move we have in order to kill someone
        """
        position_collect=self.convert_grid(self.all_trains[othername]['position'])
        next_direction=self.kill_find_next_move(x,y,position_collect)
        next_move=self.convert_NM_coordinate(next_direction)  
        return next_move
    
    def circle_dropoff(self,x,y):
        """ 
        Is called when we want to make it hard for the others to go dropoff their wagons. 
        x, y is our trains position
        Returns the next move we have to make in order to get to the nearest drop-off zone (Doesn't see a field if we are currently occupying it) 
        """
        distance_wagon,position_collect=self.nearest_dropoff(x,y)
        next_direction=self.kill_find_next_move(x,y,position_collect)
        next_move=self.convert_NM_coordinate(next_direction)  
        return next_move
        
    def we_are_best(self):
        """ 
        Checks if we are the ones leading the highscore.
        We only want to go kill other trains if we are currently the best and want to
        avoid other trains catching up to us. 
        Returns True or False
        """
        if self.best_scores=={}:
            return False
        if self.nickname not in self.best_scores.keys():
            return False
        list_bestscores=[]
        for name in self.best_scores.keys():
            list_bestscores.append(self.best_scores[name])

        if self.best_scores[self.nickname]==max(list_bestscores):
            return True
        else:
            return False

    def we_not_on_bestrun(self):
        """ 
        Checks if our momentaraly run is not changing our highscore. 
        We don't want to go kill someone if we are currently setting a new highscore
        Returns True or False
        """
        if self.all_trains[self.nickname]['score'] < (self.best_scores[self.nickname]-1):
            return True
        else:
            return False
        
    def kill_find_next_move(self,x,y,position_collect):
        """ 
        Finds the best next move, ignoring if we drive into something killing us. 
        x, y are our trains positions
        position_collect is what we want to get to (In this case the head of another train) in the form of a tuple
        Returns the next move that will take us closer to our target
        """
        all_directions=[tuple((0,1)),tuple((0,-1)),tuple((1,0)),tuple((-1,0))]
        our_direction=self.convert_direction(self.all_trains[self.nickname]['direction'])
        ox,oy=our_direction
        backposition=((ox*(-1)),(oy*(-1)))
        all_directions.remove(backposition)
        old_distance=math.inf
        old_direction=our_direction
        for i in range(3):
            dx,dy=all_directions[i]
            nx=dx+x
            ny=dy+y
            px,py=position_collect
            new_distance_x=abs((nx-px))
            new_distance_y=abs((ny-py))
            distance_x=abs((x-px))
            distance_y=abs((y-py))
            distance=distance_x+distance_y
            new_distance=new_distance_x+new_distance_y
            if distance<new_distance and (new_distance_x==0 or new_distance_y==0):
                continue
            if new_distance<=old_distance:
                old_distance=new_distance
                old_direction=(dx,dy)
        return old_direction
        
    def find_next_move(self,x,y,position_collect):
        """ 
        Finds the best next move, making us closer to our end goal
        x, y are our trains positions
        position_collect is what we want to get to (Either drop-off zone or Passengers) in the form of a tuple
        Returns the next move that will take us closer to our target
        """
        all_directions=[tuple((0,1)),tuple((0,-1)),tuple((1,0)),tuple((-1,0))]
        our_direction=self.convert_direction(self.all_trains[self.nickname]['direction'])
        ox,oy=our_direction
        backposition=((ox*(-1)),(oy*(-1)))
        all_directions.remove(backposition)
        old_distance=math.inf
        old_direction=our_direction
        for i in range(3):
            dx,dy=all_directions[i]
            nx=dx+x
            ny=dy+y
            px,py=position_collect
            if self.is_occupied(tuple((nx,ny))) or self.is_beside_train(tuple((nx,ny))):
                continue
            new_distance_x=abs((nx-px))
            new_distance_y=abs((ny-py))
            distance_x=abs((x-px))
            distance_y=abs((y-py))
            distance=distance_x+distance_y
            new_distance=new_distance_x+new_distance_y
            if distance<new_distance and (new_distance_x==0 or new_distance_y==0):
                continue
            if new_distance<=old_distance:
                old_distance=new_distance
                old_direction=(dx,dy)
        return old_direction
            

    def convert_next_move(self,next_move):
        """ 
        converts next move into coordinates dx,dy
        next_move is currently in the form of MOVE.SOMETHING
        Returns the corresponding tuple 
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
        """
        Converts directional coordinate into a move
        Coordinate is the direction of our next move
        Returns the corresponding move (The way the function get_move has to return it)
        """
        self.move_to_delta = {
            (0, -1): Move.UP,
            (0, 1): Move.DOWN,
            (1, 0): Move.RIGHT,
            (-1, 0): Move.LEFT
            }
        next_move=self.move_to_delta[coordinate]
        return next_move

    def nearest_passenger(self,Ox,Oy):
        """ finds the smalest passenger_value fraction to compare which passenger should get collected. 
        returns the passenger_value fraction and the position of the passenger with the smallest one.
        Ox, Oy are the coordinates of our train
        Returns the position of the best passenger we can collect (tuple) and the "importance" of this passenger (int)"""
        previous_distance=math.inf
        for number in range(len(self.passengers)):
            value=self.passengers[number]['value']
            position_passenger=self.convert_grid(self.passengers[number]['position'])
            (x,y)=position_passenger
            #we have chosen this estimator as the complexity is O(n) for the number of positons apart
            distance_passenger=((abs((x-Ox)))+(abs((y-Oy)))/(value/2)) 
            if distance_passenger<previous_distance:
                previous_distance=distance_passenger
                solution=position_passenger
        return solution,previous_distance
    
    def nearest_dropoff(self,Ox,Oy):
        """considers the two extreme points of the dropoff zone, to find which one is closer to us.
        returns our comparison fraction (float), which we will use to compare with the passenger distance_value fraction
        and the coordinate (tuple) of the closest drop-off expreme point.
        Ox, Oy are the coordinates of our train"""
        #distance of the dropoff zone
        (drop_off_x,drop_off_y)=self.convert_grid(self.delivery_zone['position'])
        (drop_off2_x, drop_off2_y)=self.dropping_off_2_coordinates(drop_off_x,drop_off_y)
        #if the dropoff is occupied, mark it as infinite
        if self.is_occupied((drop_off_x,drop_off_y)):
            distance_drop_off=math.inf
        else:
            distance_drop_off=(abs((drop_off_x-Ox))+abs((drop_off_y-Oy)))
        #if the dropoff is occupied, mark it as infinite
        if self.is_occupied((drop_off2_x, drop_off2_y)):
            distance_drop_off2=math.inf
        else:
            distance_drop_off2=(abs((drop_off2_x-Ox))+abs((drop_off2_y-Oy)))
        #compare the distance of the drop-off points
        if distance_drop_off<distance_drop_off2:
            nearest_drop_off=distance_drop_off
            nearest_drop_coordinate=(drop_off_x,drop_off_y)
        else:
            nearest_drop_off=distance_drop_off2
            nearest_drop_coordinate=(drop_off2_x, drop_off2_y)
        # creates comparisson fraction    
        nb_wagons=len(self.all_trains[self.nickname]['wagons'])
        if nb_wagons==0:
            distance_wagon=math.inf
        else:
            distance_wagon=(nearest_drop_off*(0.95**nb_wagons))
        return distance_wagon,nearest_drop_coordinate

    def what_to_collect(self,Ox,Oy):
        """ compares the two comparisson fractions. 
        the distance to the drop-off zone (DDO) fraction: DDO*(0.95**numberWagons)
        and the passenger distance_value fraction: distance/(value/2).
        The lowest fraction (float) of both will be the coordinate we return out of the function, 
        since this is the next coordinate (tuple) to go to.
        Ox, Oy are the coordinates of our train. """
        solution,previous_distance=self.nearest_passenger(Ox,Oy)
        distance_wagon,nearest_drop_coordinate=self.nearest_dropoff(Ox,Oy)

        #should we go to the drop off zone or should we collect passengers
        if distance_wagon<previous_distance:
            return nearest_drop_coordinate
        else:
            return solution
        
    def is_beside_train(self,coordinate):
        """
        Checks if a spesific coordinate is right next to the head of another train. 
        The direction to the right, to the left, up and down.
        Coordinate is the field we want to chek
        Returns True (if the field is not next to the head of a train) or False (if the field is next to the head of a player)
        """
        occupied_list=[]
        for name in self.all_trains.keys():
            if self.all_trains[name]['alive']:
                if name != self.nickname: #around the head
                    tx, ty = self.convert_grid(self.all_trains[name]["position"])
                    occupied_list.append(tuple((tx+1,ty)))
                    occupied_list.append(tuple((tx,tx+1)))
                    occupied_list.append(tuple((tx-1,ty)))
                    occupied_list.append(tuple((tx,ty-1)))
        if coordinate in occupied_list:
            return True
        return False
            
    def is_occupied(self, coordinate):
        """ 
        checks if a specific coordinate is already occupied, by a train or his wagons
        Coordinate is the field we want to check
        Returns True (if there is currently no train on this field and it is not out of bounds) 
        or False (if there is currently a train on this field or if it is out of bounds)
        """
        x,y = coordinate
        occupied_list=[]
        for name in self.all_trains.keys():
            if self.all_trains[name]['alive']:
                tx, ty = self.convert_grid(self.all_trains[name]["position"])
                wagon_list=self.convert_list(self.all_trains[name]['wagons'])
                occupied_list.append(tuple((tx,ty))) #the head of the train
                for i in wagon_list:
                    occupied_list.append(i) #all the wagons
        
        if (x,y) in occupied_list:
            return True
        elif (x == self.WIDTH) or (x < 0) or (y == self.HEIGHT) or (y < 0):
                return True
        else:
            return False
        
    def dropping_off_2_coordinates(self, x1_coordinate, y1_coordinate):
        """ 
        Finds the second coordinate of the drop off zone 
        x1_coordinate, y1_coordinate the coordinates of our train
        Returns the coordinates of the secon dropoff zone (int, int)
        """
        height,width=self.convert_grid((self.delivery_zone['height'],self.delivery_zone['width']))
        x2_coordinate=x1_coordinate+width-1
        y2_coordinate=y1_coordinate+height-1
        return (x2_coordinate, y2_coordinate)
    
    def convert_grid(self,object):
        """
        Converts the object number into a single digit grid to use as coordinates
        Object is a list with two entrys. The first one represents the x-coordinate and the second 
        entry represents the y-coordinate
        Returns a tuple of the coordinate (as if the cell size is 1)
        """
        x=object[0]
        y=object[1]
        x=int(x/self.cell_size)
        y=int(y/self.cell_size)
        return (tuple((x,y)))
    
    def convert_direction(self,object):
        """
        Converts the direction into a tuple
        Object is a list with two entrys. The first one represents the x-coordinate direction and the second 
        entry represents the y-coordinate direction
        Returns a tuple of the direction 
        """
        x=object[0]
        y=object[1]
        return(tuple((x,y)))
    
    def convert_gamewith(self):
        """
        Converts the height and width into a single coordinate grid
        Doesn't return anything but rather modifies something
        """
        self.WIDTH=int(self.game_width/self.cell_size)
        self.HEIGHT=int(self.game_height/self.cell_size)

    def convert_list(self,object):
        """
        Fonverts a list ino a list of numers into a single coorinates grid
        Object is a list of numbers
        Returns the modified list (as if the cell size was 1)
        """
        new_obj=[]
        if object==[]:
            return new_obj
        for i in object:
            new_obj.append(self.convert_grid(i))
        return new_obj