#version 2.2
#128.179.154.221
import random
from common.base_agent import BaseAgent
from common.move import Move
from server.game import Game
import math

#TODO(Elina) 
#improve weight of distance to drop-off zone in comparison to passengers
#comment all of the code
#prevent head on collison (similar function to is_occupied)

#INFO: Aso I ha jetzt mau es paar vo dä Sache glöscht woni z gfühl ha ds mer sä nümme wärde bruche. 
#Faus du glich no öppis bruchsch i ha aues kopiert. I gloubs mir chönnte theoretisch ou ds mit dr Wand lösche
#Wiu i ha ds jetzt eigentlech ids is_occupied tah. I gloubs dr main bug isch wüklech es Problem vo ihne wiu i ha
#wöue ufem Forum frage und es het ou scho öpper anders dä Fähler bemerkt. I ha jetzt voraum probiert ds es nümm i sich säuber
#oder anderi Züg dri fahrt

#TODO(Celia) I versueche usezfinde ob mä cha gseh gseh ob ä Zug grad am Passengers uflade isch oder nid. De 
#chönnt mäh nämlech no nächer hinder dä anderä Züg düre. Plus i wott probiere ds avoide ds mä ine Zug inefahr
#wenn är vor Site chunt und uf ds gliche Fäudli wott wie mir!



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
        position_collect=self.what_to_collect()
        Dicth_onary,path_length_passenger=self.find_best_Path_coordonates(self.train_coordinate, position_collect)
        next_move = self.find_best_Path_directions(Dicth_onary)
        print(f'first_next_move {next_move}')
        if self.check_if_collision(next_move,x,y):
            print(f'second next move {next_move}')
            next_move=self.next_move_prevent_collision(next_move,x,y)
            print(f'third next move {next_move}')
        print('')
        return next_move
        
   

    def check_if_collision(self,next_move,x,y):
        """ it will check if the next move would make us collide with another train or with the head of another train
        - returns True if we will collide with our next move
        """
        self.move_to_delta = {
            Move.UP:    (0, -1),
            Move.DOWN:  (0, 1),
            Move.RIGHT: (1, 0),
            Move.LEFT:  (-1, 0)
        }
        dx, dy = self.move_to_delta[next_move]
        target_pos = (x + dx, y + dy)

        this_train = False
        if self.is_occupied(target_pos):
            '''checking to see if the next move will drive us into anything'''
            for name, train in self.all_trains.items():
                train_pos = self.convert_grid(train["position"])
                tail_pos = self.convert_grid(train["wagons"][-1]) if train["wagons"] else None
                tx, ty = self.convert_grid(train["position"])
                tdx, tdy = train["direction"]
           
                if target_pos == train_pos: 
                    #TODO müesse mir endere, dörfe nie dri fahre!!
                    '''if it is the "head" of a train the we have to check if this train is faster or not to avoid a collision'''
                    if len(train["wagons"]) <= len(self.all_trains[self.nickname]["wagons"]):
                        tx1, ty1 = train["direction"]
                        tx2, ty2 = self.all_trains[self.nickname]["direction"]
                        if (-tx1, -ty1) != (tx2, ty2) and len(train["wagons"])== 0:
                            '''checking to see if it will be a head on collison'''
                            break
                    this_train = True
                elif target_pos == tail_pos or target_pos in self.convert_list(train["wagons"]):
                    '''if it is a wagon in the middle of the train we cannnot take this path'''
                    #I probiere no ds mä eigentlech ds hindere Ändi vom Zug nid muess umgah aber drfür müessti usefinde ob dr Zug momentan öpper am
                    #uflade isch oder nid. Wiu wenn är niemert ufladet wird sech ds hinderste Wägeli im nächste Move wägbewegt ha
                    #wenn är aber no öpper am uflade isch denn isch der im nächste Move immer no es Wägeli. Darum hanis jetzt mau ganz drus gnoh
                    this_train = True
                elif (tx+tdx, ty +tdy) == target_pos and name != self.nickname:
                    this_train = True
        return(this_train)
                
    def next_move_prevent_collision(self,next_move,x,y):
        """ this will tell us what move we have to do, as to not collide with another train on time
        """
        # List possible fallback directions
        dx, dy = self.move_to_delta[next_move]
        fallback_moves = [[0,1], [0,-1], [1,0], [-1,0]]
        if [dx, dy] in fallback_moves:
            fallback_moves.remove([dx, dy])  # remove current blocked direction
        back_dir = [-i for i in self.all_trains[self.nickname]["direction"]]
        if back_dir in fallback_moves:
            fallback_moves.remove(back_dir)  # don't go backward
        # Remove fallback moves that are also occupied
        fallback_moves = [m for m in fallback_moves if not self.is_occupied((x + m[0], y + m[1]))]
        if fallback_moves:
            #TODO z random chöi mir de no optimiere
            dx, dy = random.choice(fallback_moves)
            delta_to_move = {(1,0): Move.RIGHT, (-1,0): Move.LEFT, (0,1): Move.DOWN, (0,-1): Move.UP}
            new_move = delta_to_move[(dx, dy)]
        return new_move

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
            distance_passenger=((abs((x-Ox)))+(abs((y-Oy)))/(value/2)) 
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

        #elif nb_wagons >= 8:
            #distance_wagon=0
        else:
            #distance_wagon=(nearest_drop_off/(nb_wagons+0.0000001))
            distance_wagon=(nearest_drop_off*(0.95**nb_wagons))
            #wagons werde hie ou viu z fest gwichtet!! 
            #z.b mit nearest_drop_off*(0.95^nb_wagon)??
            #distance_wagon=nearest_drop_off
            #I weiss nid obs nume isch wenns 2 Züg het aber jetzt geit är fasch nie ga drop offe und
            #je länger ds dr Zug isch desto afälliger für Fähler. Aso i würd es Limit mache ab däm mä sicher geit
            #ga drop offe. 
        
        #should we go to the drop off zone or should we collect passengers
        if distance_wagon<previous_distance:
            return nearest_drop_coordinate
        else:
            return solution
        
    def is_occupied(self, coordinate):
        """ is checking if a specific coordinate is already occupied, by a train or his wagons"""
        x,y = coordinate
        for name in self.all_trains.keys():
            #if self.all_trains[name]['alive'] == False:
                #continue
            tx, ty = self.convert_grid(self.all_trains[name]["position"])
            tdx, tdy = self.all_trains[name]["direction"]
            if coordinate == self.convert_grid(self.all_trains[name]['position']) or coordinate in self.convert_list(self.all_trains[name]['wagons']):
                return True
            elif x == self.WIDTH or x < 0 or y == self.HEIGHT or y < 0:
                return True
            elif (tx+tdx, ty+tdy) == coordinate and name != self.nickname:
                return True
        return False
        
    def dropping_off_2_coordinates(self, x1_coordinate, y1_coordinate):
        """optimisez drop off"""
        height,width=self.convert_grid((self.delivery_zone['height'],self.delivery_zone['width']))
        x2_coordinate=x1_coordinate+width-1
        y2_coordinate=y1_coordinate+height-1
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
    """
    def wall(self,x,y,nx,ny):
        
        this will be the first condition we will check when planing the next move since we:
        - check if we have to do a spesific move, as not to drive into the wall (True).
        - if we are going straight into the wall we will change direction
        If this is not the case we will retrn False.
        
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
        
        checks if there is a wall in front of the train where the next move would be if we don't change direction.
        This will then also tell us in which direction we can't turn because there is also a wall there.
        
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
        
        we check that the next move would not lead us outside of the game
        
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
        
    """

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
                if find_coordinate in dict_pos["-"]:
                    ''' eigentlech nomau ds gliche wie dobe. I weiss ehrlechgseit nid obs ds wük brucht. Aber essentially suechts eifach es "target" grad näbem originale "target" '''
                    for name, train in self.all_trains.items():
                        this_train = False
                        train_pos = self.convert_grid(train["position"])
                        tail_pos = self.convert_grid(train["wagons"][-1]) if train["wagons"] else None
    
                        if find_coordinate == train_pos:
                            if len(train["wagons"]) <= len(self.all_trains[self.nickname]["wagons"]):
                                    tx1, ty1 = train["direction"]
                                    tx2, ty2 = self.all_trains[self.nickname]["direction"]
                                    if (-tx1, -ty1) != (tx2, ty2):
                                        break
                            this_train = True
                        elif find_coordinate == tail_pos or find_coordinate in self.convert_list(train["wagons"]):
                            this_train = True

                        if this_train:
                            Moves=[[0,1],[0,-1],[1,0],[-1,0]]
                            x,y = find_coordinate
                            back_dir = [-i for i in self.all_trains[self.nickname]["direction"]]
                            if back_dir in Moves:
                                Moves.remove(back_dir)  # don't go backward
                            # Remove fallback moves that are also occupied
                            Moves = [m for m in Moves if not self.is_occupied((x + m[0], y + m[1]))]
                            next = random.choice(Moves)
                            dx,dy = tuple(next)
                            find_coordinate = (x+dx, y+dy)
                            break
                if coordinate == find_coordinate: #find the spesific input of our function
                    dict_pos["B"].append(coordinate)
        
        B,dict_pos, find_coordinate,path_index=self.flood_grid(dict_pos, find_coordinate)
        path,B=self.find_path_pack(B,dict_pos, find_coordinate,path_index)
        return (path,B)

    def flood_grid(self, dict_pos, find_coordinate):
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
        return(B,dict_pos, find_coordinate,path_index)
        
    def find_path_pack(self, B,dict_pos, find_coordinate,path_index):
        E=0 # finding a trace back up the grid to the starting point
        positions=((0,1),(0,-1),(1,0),(-1,0))
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