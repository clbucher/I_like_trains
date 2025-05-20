#version 2.2
#128.179.154.221
import random
from common.base_agent import BaseAgent
from common.move import Move
from server.game import Game
import math
import datetime

#TODO(Elina) 
#comment all of the code
#trouver tout les case de drop_off_zone
#evt. fonces vers le train avec le highscore

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
        #time_before=datetime.now()
        #will change game width into a coordinate system which is divided by cell size
        self.convert_gamewith()
    

        self.train_coordinate = self.convert_grid(self.all_trains[self.nickname]['position'])
        x,y = self.train_coordinate
        position_collect=self.what_to_collect()
        
        self.Dicth_onary,path_length_passenger=self.find_best_Path_coordonates(self.train_coordinate, position_collect)
        next_move = self.find_best_Path_directions(self.Dicth_onary)
        #if our next move still gets us into a situation we would die
        if self.check_if_collision_train(next_move,x,y):
           next_move=self.next_move_prevent_collision(next_move,x,y)
        """
        time_after=datetime.now()
        time_after2=datetime.timestamp(time_after)
        time_before2=datetime.timestamp(time_before)
        time_difference=time_after2-time_before2
        print(f'difference {time_difference}, time after {time_after}, time before {time_before}')
        """
        return next_move

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
        return (dx,dy)
    
    def check_if_collision_train(self,next_move,x,y):
        """ it will check if the next move would make us collide with another train or with the head of another train
        - return: True if we will collide with our next move
        """
        dx,dy=self.convert_next_move(next_move)
        target_pos = (x + dx, y + dy)

        this_train = False
        if self.is_occupied(target_pos): #checking to see if the next move will drive us into anything
            for name, train in self.all_trains.items():
                train_pos = self.convert_grid(train["position"])
                tail_pos = self.convert_grid(train["wagons"][-1]) if train["wagons"] else None
                tx, ty = self.convert_grid(train["position"])
                tdx, tdy = self.convert_direction(train["direction"])
                #if it is the "head" of a train the we have to check if this train is faster or not to avoid a collision
                if target_pos == train_pos: 
                    #if len(train["wagons"]) <= len(self.all_trains[self.nickname]["wagons"]):
                    tx1, ty1 = self.convert_direction(train["direction"])
                    tx2, ty2 = self.convert_direction(self.all_trains[self.nickname]["direction"])
                    #if (-tx1, -ty1) != (tx2, ty2) and len(train["wagons"])== 0: 
                            #checking to see if it will be a head on collison
                    #        break
                    this_train = True
                elif target_pos == tail_pos or target_pos in self.convert_list(train["wagons"]):
                    #if it is a wagon in the middle of the train we cannnot take this path
                    this_train = True
                elif (tx+tdx, ty +tdy) == target_pos and name != self.nickname:
                    this_train = True
        return(this_train)
                
    def next_move_prevent_collision(self,next_move,x,y):
        """ 
        this will tell us what move we have to do, as to not collide with another train on time
        """
        next_move=next_move
        dx, dy = self.convert_next_move(next_move)
        fallback_moves = [[0,1], [0,-1], [1,0], [-1,0]]
        if [dx, dy] in fallback_moves:
            fallback_moves.remove([dx, dy])  # remove current blocked direction
        back_dir = [-i for i in self.convert_direction(self.all_trains[self.nickname]["direction"])]
        if back_dir in fallback_moves:
            fallback_moves.remove(back_dir)  # don't go backward
        # Remove fallback moves that are also occupied
        fallback_moves = [m for m in fallback_moves if not self.is_occupied((x + m[0], y + m[1]))]
        if fallback_moves:
            dx, dy = random.choice(fallback_moves)
            delta_to_move = {(1,0): Move.RIGHT, (-1,0): Move.LEFT, (0,1): Move.DOWN, (0,-1): Move.UP}
            new_move = delta_to_move[(dx, dy)]
        return new_move

    def what_to_collect(self):
        """
        chooses what to collect next or if it goes to the drop off zone.
        """
        previous_distance=math.inf

        #which is the best passenger to pick

        #which is the best passenger to pick
        for number in range(len(self.passengers)):
            value=self.passengers[number]['value']
            position_passenger=self.convert_grid(self.passengers[number]['position'])
            (x,y)=position_passenger
            (Ox,Oy)=self.train_coordinate
            #we have chosen this estimator as the complexity is O(n) for the number of positons apart
            distance_passenger=((abs((x-Ox)))+(abs((y-Oy)))/(value/2)) 
            if distance_passenger<previous_distance:
                previous_distance=distance_passenger
                solution=position_passenger
        
        #distance of the dropoff zone

        #distance to the dropoff zone
        (drop_off_x,drop_off_y)=self.convert_grid(self.delivery_zone['position'])
        (drop_off2_x, drop_off2_y)=self.dropping_off_2_coordinates(drop_off_x,drop_off_y)
        distance_drop_off=(abs((drop_off_x-Ox))+abs((drop_off_y-Oy)))
        distance_drop_off2=(abs((drop_off2_x-Ox))+abs((drop_off2_y-Oy)))
        if distance_drop_off<distance_drop_off2:
            nearest_drop_off=distance_drop_off
        else:
            nearest_drop_off=distance_drop_off2
        """
        DO_coordinate_list=self.dropping_off_2_coordinates(drop_off_x,drop_off_y)
        nearest_drop_off=math.inf
        
        for DO in DO_coordinate_list:
            if self.is_occupied(DO):
                distance_drop_off=math.inf
            else:
                DO_x,DO_y=DO
                distance_drop_off=(abs((DO_x-Ox))+abs((DO_y-Oy)))
            if distance_drop_off<nearest_drop_off:
                nearest_drop_off=distance_drop_off
                nearest_drop_coordinate=DO
        """
        nb_wagons=len(self.all_trains[self.nickname]['wagons'])
        if nb_wagons==0:
            distance_wagon=math.inf

        else:
        
        #should we go to the drop off zone or should we collect passengers
            distance_wagon=(nearest_drop_off*(0.95**nb_wagons))
        
        #should we go to the drop off zone or should we collect passengers
        if distance_wagon<previous_distance:
            return nearest_drop_off
        else:
            return solution
        
    def is_occupied(self, coordinate):
        """ 
        checks if a specific coordinate is already occupied, by a train or his wagons
        """
        x,y = coordinate
        for name in self.all_trains.keys():
            tx, ty = self.convert_grid(self.all_trains[name]["position"])
            tdx, tdy = self.convert_direction(self.all_trains[name]["direction"])
            if coordinate == self.convert_grid(self.all_trains[name]['position']) or coordinate in self.convert_list(self.all_trains[name]['wagons']):
                return True
            elif x == self.WIDTH or x < 0 or y == self.HEIGHT or y < 0:
                return True
            elif ((tx+tdx, ty+tdy) == coordinate) and (name != self.nickname):
                return True
        return False
        
    def dropping_off_2_coordinates(self, x1_coordinate, y1_coordinate):
        """ finds the second coordinate of the drop off zone 
        height,width=self.convert_grid((self.delivery_zone['height'],self.delivery_zone['width']))
        drop_off_zone=[tuple((x1_coordinate,y1_coordinate))]
        for y in range(1,(width+1)):
            for i in range(1,(height+1)):
                x2_coordinate=x1_coordinate+y
                y2_coordinate=y1_coordinate+i
                drop_off_zone.append(tuple((x2_coordinate,y2_coordinate)))
        return (drop_off_zone)
        """
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

    def find_best_Path_coordonates(self,your_coordinate,find_coordinate):
        """
        We find a list of the coordonates of the best path to the passenger using the Dijkstra's Algorithm
        """
        B=0
        (OP_x,OP_y)=your_coordinate
        (Ox,Oy)=self.convert_direction(self.all_trains[self.nickname]['direction'])
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
                    if (coordinate == self.convert_grid(self.all_trains[name]['position'])) or (coordinate in self.convert_list(self.all_trains[name]['wagons'])) or (coordinate == backpositon):
                        dict_pos["-"].append(coordinate)                      
                    else:
                        dict_pos["inf"].append((i,j))
                if coordinate == find_coordinate: #find the spesific input of our function
                    dict_pos["B"].append(coordinate)
        
        B,dict_pos, find_coordinate,path_index=self.flood_grid(dict_pos, find_coordinate)
        path,B=self.find_path_pack(B,dict_pos, find_coordinate,path_index)
        return (path,B)

    def flood_grid(self, dict_pos, find_coordinate):
        """
        This function floods our grid with the distance to our curent position, until we arrive 
        to our end destination. 
        Input: dictionary with the positional values, coordinate we want to go to
        Output: distance value to our final coordinate, updated dictonary with all the correct values,
                find coordinate, 
        """
        positions=((0,1),(0,-1),(1,0),(-1,0))
        counter=-1
        E=0
        print("before while")
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
        print("nach while")
        return(B,dict_pos, find_coordinate, path_index)
        
    def find_path_pack(self, B,dict_pos, find_coordinate,path_index):
        """ 
        We go through our flooded grid and find the shortest path pack to the initial position.
        return: a list of coordinate
        """
        positions=((0,1),(0,-1),(1,0),(-1,0))
        path=[]
        counter=B
        dict_pos["H"]=[]
        for E in range(B):
            counter-=1
            for pt in positions:
                pt_x,pt_y=path_index
                nx,ny=pt
                searching_pt=(pt_x+nx,pt_y+ny)
                if counter==0:
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
        """this translates the list of the best path into movements we have to do next"""
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