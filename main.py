from loguru import logger #logger (duh)
import sys                # needed by the logger to be used as a sink (output)
import readchar           # needed for the menus, detects when a key is pressed, like up-arrow
import os                 # needed for the menus to clear the screen, also will be needed by other stuff
import time
import json
import requests

DEBUG = True

logger.remove() #remove default sink because it also logs debug messages
logger.add(sys.stderr, format="|{time}| - |{level}| - | {message}", level="DEBUG" if DEBUG == True else "INFO") #add our own sink because we can control if it has debug messages or not


class ProjectsClass:
    def __init__(self):
        self.addProjects = self.AddProjectsClass()
        self.selectedProjects = {}

    class AddProjectsClass:
        def __init__(self):
            self.projectsToAdd = {}

        def bySearch(self):
            menu.clear()

            query = input("\nEnter Search Query\n  >>>>")
            print(f">>>> Searching for '{query}'...")
            requestParams = {
                "query": query,
                "index": "relevance",
                "facets": json.dumps([["project_type:plugin"]]),
                "limit": 20
            }

            requestResponse = requests.get("https://api.modrinth.com/v2/search", params=requestParams)
            for i in requestResponse.json()["hits"]:
                self.projectsToAdd[i["title"]] = {
                    "title": i["title"],
                    "downloads": i["downloads"],
                    "ID": i["project_id"]
                }
            
            self.projectsToAddNum = menu.StartMenu(list(self.projectsToAdd.keys()), "Request Results", True)
            
            if not self.projectsToAddNum == None:
                for i in self.projectsToAddNum:
                    title = list(self.projectsToAdd.keys())[i]
                    projects.selectedProjects[title] = self.projectsToAdd[title]


        def byID(self):
            menu.clear()
            print("!not implemented!")
            time.sleep(1)
    
    def RemoveProjects(self):
        Title = "Remove Projects"
        options = list(projects.selectedProjects.keys())
        
        numsToRemove = menu.StartMenu(options, Title, True)

        if not numsToRemove == None:
            titlesToRemove = []
            for i in numsToRemove:
                titlesToRemove.append(options[i])


            for title in titlesToRemove:
                del projects.selectedProjects[title]
        

class MenuClass: #Inside these are all the menus, this make it easy to trigger menus by doing menu.menuyouwanttotrigger.execute()

    class MainClass:      #main menu, then one with the choices 'Edit Projects' and 'quit'
        def __init__(self):
            self.Options = ["Edit Projects", "Quit"] #the options of the menu
            self.CurOpt = 0 #the current option selected
            self.MenuName = "Main Menu"
        
        def Execute(self): #called to trigger (execute) the menu
            Result = menu.StartMenu(self.Options, self.MenuName, False)
            if not Result == None:
                if Result == 0:
                    menu.EditProjects.execute()
                if Result == 1:
                    quit(0)
    
    class EditProjectsMenuClass:


        class AddProjectsMenuClass:
            def __init__(self):
                self.Options = ["Search", "Add by ID"]
                self.MenuTitle = "Add projects"
                self.CurOpt = 0
            def execute(self):
                result = menu.StartMenu(self.Options, self.MenuTitle, False)
                if not result == None:
                    if result == 0:
                        projects.addProjects.bySearch()
                    elif result == 1:
                        projects.addProjects.byID()
  


        def __init__(self):
            self.AddProjectsMenu = self.AddProjectsMenuClass()

            self.Options = ["Add Projects", "Remove Projects", "View Info", "<< Back"]
            self.MenuTitle = "Edit Projects"
            self.CurOpt = 0
        
        def execute(self):
            Result = menu.StartMenu(self.Options, self.MenuTitle, False)
            if not Result == None:
                if Result == 0:
                    menu.EditProjects.AddProjectsMenu.execute() # Add projects
                elif Result == 1:
                    projects.RemoveProjects()
                elif Result == 2:
                    pass # View Projects
                elif Result == 3:
                    pass # Back to main menu
    


    def __init__(self):
        self.main = self.MainClass()
        self.EditProjects = self.EditProjectsMenuClass()
        logger.debug("MenuClass done")

    def clear(self):
        if os.name == 'posix': #linux or macOS
            os.system("clear")
        elif os.name == 'nt': #windows
            os.system("cls")
    
    def StartMenu(self, options: list, MenuTitle: str, isSelection: bool):

        if isSelection == True:
            
            CurOpt = 0
            selectedOptions = []
            while True:
                menu.clear()
                print(MenuTitle, "\n")
                for i in range(len(options)):
                    prefix = ">>>> " if i == CurOpt else "     "
                    selectionPrefix = "[x] " if i in selectedOptions else "[]  "
                    title = options[i]
                    print(f"{prefix}{selectionPrefix}{title}")

                print("\n\n\nNavigate using the UP/DOWN arrows, select with ENTER and exit with Q")

                # Handle input
                key: readchar.key = readchar.readkey()
                
                if key == readchar.key.UP and CurOpt != 0:
                    CurOpt -= 1

                elif key == readchar.key.DOWN and CurOpt != len(options)-1:
                    CurOpt += 1

                elif key == readchar.key.SPACE:
                    if not CurOpt in selectedOptions:
                        selectedOptions.append(CurOpt)
                    else:
                        selectedOptions.remove(CurOpt)

                elif key == readchar.key.ENTER:
                    return selectedOptions
                elif key == "Q" or key == "q":
                    return None

        else:

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
                elif key == readchar.key.DOWN and CurOpt != len(options)-1:
                    CurOpt += 1
                elif key == readchar.key.ENTER:
                    return CurOpt
                elif key == "Q" or key == "q":
                    return None
                



menu = MenuClass()
projects = ProjectsClass()


while True:
    menu.main.Execute()

