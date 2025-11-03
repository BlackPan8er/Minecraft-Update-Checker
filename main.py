from loguru import logger #logger (duh)
import sys                # needed by the logger to be used as a sink (output)
import readchar           # needed for the menus, detects when a key is pressed, like up-arrow
import os                 # needed for the menus to clear the screen, also will be needed by other stuff

DEBUG = True

logger.remove() #remove default sink because it also logs debug messages
logger.add(sys.stderr, format="|{time}| - |{level}| - | {message}", level="DEBUG" if DEBUG == True else "INFO") #add our own sink because we can control if it has debug messages or not



class MenuClass: #Inside these are all the menus, this make it easy to trigger menus by doing menu.menuyouwanttotrigger.execute()

    class MainClass:      #main menu, then one with the choices 'Edit Projects' and 'quit'
        def __init__(self):
            self.Options = ["Edit Projects", "Quit"] #the options of the menu
            self.CurOpt = 0 #the current option selected
        
        def Execute(self): #called to trigger (execute) the menu
            while True:
                menu.clear() #clear screen
                for i in range(len(self.Options)): #goes and prints every option on a new line, also adds a prefix (>>> ) to the selected option (CurOpt)
                    prefix = ">>>> " if self.CurOpt == i else "     "
                    title = self.Options[i]
                    print(f"{prefix}{title}")

                if self.HandleInput() == True: #Handles input (duh), see below for more. Returns True only if Enter is pressed, then we do the corresponding action to the current option selected, if its false we continue the While True loop
                    if self.CurOpt == 0: # Corresponds to Edit Projects
                        menu.EditProjectsMenu.execute()    
                    elif self.CurOpt == 1: # Corresponds to Quit
                        quit(0)
                

        
        def HandleInput(self): #Reads which key is pressed, then adjusts the CurOpt as needed
            key = readchar.readkey() #reads the key
            if key == readchar.key.UP and self.CurOpt != 0: # if up is pressed and its not already on the top-most option then go one option up
                self.CurOpt -= 1 
            elif key == readchar.key.DOWN and self.CurOpt != len(self.Options): #if down is pressed and its not already on the down-most option then go one option down
                self.CurOpt +=1
            elif key == readchar.key.ENTER: #if enter is pressed return True, then the above function runs the corresponding action
                return True
    
    class EditProjectsMenuClass:
        def __init__(self):
            self.Options = ["Add Projects", "Remove Projects", "View Info", "<-- Main Menu"]
            self.CurOpt = 0
        
        def execute(self):
            while True:
                menu.clear() #clear screen
                print(len(self.Options))
                for i in range(len(self.Options)):
                    prefix = ">>>> " if self.CurOpt == i else "     "
                    title = self.Options[i]
                    print(f"{prefix}{title}")

                if self.HandleInput() == True: #returned only if enter was pressed
                    if self.CurOpt == 0:
                        pass #TODO Add projects
                    elif self.CurOpt == 1:
                        pass #TODO remove projects
                    elif self.CurOpt == 2:
                        pass #TODO view projects
                    elif self.CurOpt == 3:
                        break #return to main menu

        
        def HandleInput(self):
            key = readchar.readkey()
            if key == readchar.key.UP and self.CurOpt != 0:
                self.CurOpt -= 1
            elif key == readchar.key.DOWN and self.CurOpt != len(self.Options):
                self.CurOpt +=1
            elif key == readchar.key.ENTER:
                return True








    def __init__(self):
        self.main = self.MainClass()
        self.EditProjectsMenu = self.EditProjectsMenuClass()
        logger.debug("MenuClass done")

    def clear(self):
        if os.name == 'posix': #linux or macOS
            os.system("clear")
        elif os.name == 'nt': #windows
            os.system("cls")
    
    def StartMenu(self, options: list, MenuTitle: str):
        CurOpt = 0
        while True:
            menu.clear()
            print(MenuTitle, "\n")
            for i in range(len(options)):
                prefix = ">>>> " if i == CurOpt else "     "
                title = options[i]
                print(f"{prefix}{title}")

            print("\n\n\nNavigate using the UP/DOWN arrows, select with ENTER and exit with Q")

            # Handle input
            key: readchar.key = readchar.readkey()
            
            if key == readchar.key.UP and CurOpt != 0:
                CurOpt -= 1
            elif key == readchar.key.DOWN and CurOpt < len(options):
                CurOpt += 1
            elif key == readchar.key.ENTER:
                return True
            elif key == "Q" or key == "q":
                break
                



menu = MenuClass()

menu.main.Execute()