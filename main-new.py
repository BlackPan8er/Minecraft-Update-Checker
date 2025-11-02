from loguru import logger
import sys
import readchar

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
                for i in range(len(self.Options)):
                    prefix = ">>>> " if self.CurOpt == i else ""
                    title = self.Options[i]

    def __init__(self):
        self.main = self.MainClass()
        logger.debug("MenuClass done")

menu = MenuClass()

menu.main.Execute()