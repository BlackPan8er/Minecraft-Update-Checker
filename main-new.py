from loguru import logger
import sys
import readchar
import os

DEBUG = True

logger.remove() #remove default sink because it also logs debug messages
logger.add(sys.stderr, format="|{time}| - |{level}| - | {message}", level="DEBUG" if DEBUG == True else "INFO") #add our own sink because we can control if it has debug messages or not



class MenuClass:

    class MainClass:
        def __init__(self):
            self.Options = ["Edit Projects", "Quit"]
            self.CurOpt = 0
        
        def Execute(self):
            while True:
                menu.clear() #clear screen
                for i in range(len(self.Options)):
                    prefix = ">>>> " if self.CurOpt == i else "     "
                    title = self.Options[i]
                    print(f"{prefix}{title}")

                if self.HandleInput() == True: #returned only if enter was pressed
                    if self.CurOpt == 0:
                        pass #edit projects
                    elif self.CurOpt == 1:
                        quit(0)
                

        
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
        logger.debug("MenuClass done")

    def clear(self):
        if os.name == 'posix': #linux or macOS
            os.system("clear")
        elif os.name == 'nt': #windows
            os.system("cls")

menu = MenuClass()

menu.main.Execute()