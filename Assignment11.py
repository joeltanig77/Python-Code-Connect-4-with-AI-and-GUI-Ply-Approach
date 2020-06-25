from tkinter import *
from random import choice
from time import sleep


class Player:
    def __init__(self, ox , tbt , ply):
        self.ox = ox
        self.tbt = tbt
        self.ply = ply


    def scoresFor(self,b,ox,ply):
        """Returns a list of scores and scores each col based on the human moves/ply and the AI moves/ply."""
        scoresList = []
        if ox == 'Red': #I do this in order to figure out who is the human and who is the AI
            human = 'Yellow'
        else:
            human = 'Red'

        for col in range(b.width): #For each col in the board
            if ply == 0: #This is the base case and when it reaches 0, it will stop the recursion and if it does not allow the move it will append a -1. But if it allows the move it will append 50 to the list. It will not check for wins for 0 ply
                if b.allowsMoveGUI(col) == False: #If the move is not allowed
                    scoresList.append(-1) #Insert -1 into the list
                else:
                    scoresList.append(50) #Catch all statement of appending 50
            else:
                if b.allowsMoveGUI(col) == True: #If the move is allowed
                    b.addGUIMove(col,ox)   #Add the move
                    if b.winsForGUI(ox) == True: #If you add the move and it is a win
                        scoresList.append(100)  # Append 100 into the list
                    elif ply > 1: #If the ply is greater than 1
                        scoresList.append(100-max(self.scoresFor(b,human,ply-1))) #Use recursion to call back this same functions and test for the human moves.If the human gets 100 for a potential win, append 100 into the list and the final list that is appended would be zero. As 100 -100  = 0.Which 0 meaning you have lost.
                    else:
                        scoresList.append(50) #if there are no wins for the col, append 50 to the list.
                    b.delGUIMove(col) #Delete all the moves when the for loop is complete

                else:
                    scoresList.append(-1) #If the board is full, append -1
        print(scoresList)
        return scoresList #At the end of everything, return the of the list

    def nextMove(self,b):
        tieBreakList = [] #Makes an empty list
        for colMove,score in enumerate(self.scoresFor(b,self.ox,self.ply)): # I am iterating through the list and returning one item at the time and returning thr index as well.
            if score == 100 and max(self.scoresFor(b,self.ox,self.ply)) == 100: # If the score is 100 and and the mox of the list is 100
                tieBreakList.append(colMove)    #Then I will append the index of the max values into the list and return it
            elif score == 50 and max(self.scoresFor(b,self.ox,self.ply)) == 50: ## If the score is 50 and and the mox of the list is 50
                tieBreakList.append(colMove) #Then I will append the index of the max values into the list and return it
            elif score == 0 and max(self.scoresFor(b,self.ox,self.ply)) == 0:  # # If the score is 0 and and the mox of the list is 0
                tieBreakList.append(colMove)    #Then I will append the index of the max values into the list and return it
            else:
                continue #A catch all statement to keep running the for loop.
        print(tieBreakList)
        return self.tieBreakMove(tieBreakList) #I want to return a interger and use self.tieBreakMove to index the right spot depending on what is inputted into self.tbt



    def tieBreakMove(self,scores):
        if self.tbt == "Left":
            return scores[0] #Return the first thing in the list as that represents left
        if self.tbt == "Right":
            return scores[-1] #Returns the last thing in the list as that represents the right index in the list
        if self.tbt == "Random":
            return choice(scores)  #Returns a random thing in the list which are just indexes and uses the choice finction for randomness.


class Connect4:

    def __init__(self, width, height, window):
        """This __init__the board and sets variables to what each thinh is. It also sets up the board
         and makes a list inside a list while also setting each element into an empty space string"""
        self.width = width
        self.height = height

        self.window = window #Makes the window for the game
        self.frame = Frame(window)
        self.frame.pack()
        self.messageSize = 75
        self.diameter = self.width*10
        self.initialColor = 'white'
        self.newGameButton = Button(self.frame, text = 'New Game', command = self.newGame)
        self.newGameButton.pack(side = RIGHT)
        self.quitButton = Button(self.frame, text='Quit', command=self.quitGame)
        self.quitButton.pack(side = LEFT)
        self.thePly = 0
        self.cSlider = Scale(window, orient=HORIZONTAL,from_=0,to=4,length=200, label='Difficulty -->',command= self.fixThePly)
        self.cSlider.pack()
        self.cSlider.get()

        self.message = Label(self.window, text = 'Connect 4',font='Courier 22', fg = 'black')
        self.message.pack()
        self.draw = Canvas(window, height = self.height*75, width = self.width*72,bg='dark blue')
        self.draw.bind('<Button-1>', self.mouseInput)
        self.draw.pack()
        self.clearBoard()
        self.playTheGame = False
        self.turn = True


    def clearBoard(self):
        self.draw.delete("all")
        self.circles = []
        self.colors = []

        y = 0
        for row in range(self.height):
            circleRow = []
            colorRow = []
            x = 0
            for col in range(self.width):
                circleRow += [self.draw.create_oval(x+7, y+9, x + self.diameter, y + self.diameter, fill=self.initialColor)]
                colorRow += [self.initialColor]
                x += self.diameter

            self.circles += [circleRow]
            self.colors += [colorRow]
            y += self.diameter


    def newGame(self):
        self.playTheGame = True
        self.ai = Player('Yellow','Random',self.thePly)
        self.clearBoard()



    def addGUIMove(self,col,color):
        for row in range( self.height ):
            if self.colors[row][col] != self.initialColor: #If it is not a empty space
                self.draw.itemconfig(self.circles[row-1][col], fill=color) #If you put 5 in row it kinda works
                self.colors[row-1][col] = color
                print('true')
                return
        self.draw.itemconfig(self.circles[self.height-1][col], fill=color)
        self.colors[self.height-1][col] = color  #Subtract the height as the board is getting used up

    def delGUIMove(self, col):
        """Delets the move the person wants to undo. Uses same logic as addMove()"""
        for row in range( self.height ):
            if self.colors[row][col] != self.initialColor: #If it is not a empty space
                self.draw.itemconfig(self.circles[row][col], fill=self.initialColor) #If you put 5 in row it kinda works
                self.colors[row][col] = self.initialColor
                return

    def fixThePly(self,ply):
        self.thePly = int(ply)
        print('Ply', ply)

    def mouseInput(self, event):
        col = int(event.x / self.diameter) #Should only be mouse input
        row = int(event.y/self.diameter)
        print('board[%s]' % (col))
        if self.turn == True:
            if self.playTheGame == True:
                self.message.config(text='Playing the game')
                if self.allowsMoveGUI(col) == True:
                    self.addGUIMove(col,'Red')
                    self.window.update()
                    self.ai = Player('Yellow','Random',self.thePly)
                    if self.isFullGui() == False:
                        if self.winsForGUI('Red'):
                            self.message.config(text='You win')
                            self.turn = False
                            self.window.update()
                        else:
                            self.window.update()
                            self.window.after(500)
                            self.message.config(text='Your Move')
                            self.addGUIMove(self.ai.nextMove(self),'Yellow')
                            self.ai = Player('Yellow','Random',self.thePly)
                        if self.isFullGui() == False:
                            if self.winsForGUI('Yellow'):
                                self.message.config(text='You lose')
                                self.window.update()
                                self.turn = False
                    else:
                        self.message.config(text='Tie Game')
                        self.turn = False

                else:
                    self.message.config(text='Can\'t place a move there')
        else:
            return





    def quitGame(self):
        self.window.destroy()



    def winsForGUI(self,color):
          # check for horizontal wins
        for row in range(0,self.height):
            for col in range(0,self.width-3):
                if self.colors[row][col] == color and \
                    self.colors[row][col+1] == color and \
                    self.colors[row][col+2] == color and \
                    self.colors[row][col+3] == color:
                        return True

        for row in range(0,self.height-3):  #Checks for vertical wins and checks for rows
            for col in range(0,self.width):
                if self.colors[row][col] == color and \
                    self.colors[row+1][col] == color and \
                    self.colors[row+2][col] == color and \
                    self.colors[row+3][col] == color:
                        return True

        for row in range(0,self.height-3):  #Checks for diagonal win #1
            for col in range(0,self.width-3): #Set height and width -3 as we are checking 3 in a row diagonal wins. Also uses slope of 1
                if self.colors[row][col] == color and \
                    self.colors[row+1][col+1] == color and \
                    self.colors[row+2][col+2] == color and \
                    self.colors[row+3][col+3] == color:
                        return True

        for row in range(0,self.height-3): #Checks for the other diagonol win #2
            for col in range(3,self.width): #Same logic as diagonal win #1 but checks for slope of -1
                if self.colors[row][col] == color and \
                    self.colors[row+1][col-1] == color and \
                    self.colors[row+2][col-2] == color and \
                    self.colors[row+3][col-3] == color:
                        return True
        return False



    def isFullGui(self):
        for col in range(self.width):
            if self.allowsMoveGUI(col) == True: #If the board can allow the move for all of the columns, It is not full
                    return False
        return True #Else, it is Full

    def allowsMoveGUI(self,col):
        """Checks if the move is allowed or not"""
        if 0 <= col < self.width and self.colors[0][col] == self.initialColor:
            print(self.colors)
            return True
        else:
            return False    #Or it is not true








def main():
    """Acts a point of excusion of any program, controls when and where its excuted"""
    root = Tk()
    root.title('Connect 4')
    myScreen = Connect4(7,6,root)
    root.mainloop() #Keeps running the root window and tkinter until I decide to destroy it
    #player = Player('o','Random',3)
    #print(player.nextMove(board))
    #board.playGameWith(player)


if __name__ == '__main__':
    main()
