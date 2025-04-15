import random
from .base_agent import BaseAgent
from common.move import Move
from server.game import Game

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