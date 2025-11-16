from loguru import logger #logger (duh)
import sys                # needed by the logger to be used as a sink (output)
import readchar           # needed for the menus, detects when a key is pressed, like up-arrow
import os                 # needed for the menus to clear the screen, also will be needed by other stuff
import time
import json
import requests
import re
from prettytable import PrettyTable

DEBUG = True

logger.remove() #remove default sink because it also logs debug messages
logger.add(sys.stderr, format="|{time}| - |{level}| - | {message}", level="DEBUG" if DEBUG == True else "INFO") #add our own sink because we can control if it has debug messages or not


class TableClass:
    def __init__(self):
        pass

    def getVersions(self):
        projectIDs = []
        for project in projects.selectedProjects.values():
            projectIDs.append(project['ID'])

        parameters = {
            "ids": json.dumps(projectIDs)
        }

        response = requests.get("https://api.modrinth.com/v2/projects", params=parameters)

        projectVersions = {}

        for i in response.json():
            projectVersions[i["slug"]] = i["game_versions"]
        
        return projectVersions


    def create(self):
        table = PrettyTable()
        
        projectVersions = self.getVersions()

        allVersions = []
        releasePattern = re.compile(r"^\d+\.\d+\.\d+$")

        for key, versions in projectVersions.items():
            for version in versions:
                if not version in allVersions:
                    if releasePattern.match(version):
                        allVersions.append(version)
        

        sorted_versions = sorted(
            allVersions, 
            key=lambda v: [int(x) for x in v.split(".")],  # convert each part to int
            reverse=True
        )

        allVersions = sorted_versions

        table.add_column("Versions", allVersions)



        for project, versions in projectVersions.items():
            versionsResult = []
            for versionToCheck in allVersions:
                if versionToCheck in versions:
                    versionsResult.append("| x |")
                else:
                    versionsResult.append("|   |")
            
            table.add_column(project, versionsResult)

        print(table)
        print("\n press ENTER to exit")
        while True:
            key = readchar.readkey()
            if key == readchar.key.ENTER:
                break
        


            






class ProjectsClass:
    def __init__(self):
        self.addProjects = self.AddProjectsClass()
        self.selectedProjects = {}

    class AddProjectsClass:
        def __init__(self):
            self.projectsToAdd = {}

        def bySearch(self):
            self.projectsToAdd = {}
            menu.clear()

            query = input("\nEnter Search Query\n  >>>>")
            print(f">>>> Searching for '{query}'...")
            requestParams = {
                "query": query,
                "facets": json.dumps([["project_type:plugin"]]),
                "limit": 20
            }

            requestResponse = requests.get("https://api.modrinth.com/v2/search", params=requestParams)
            for i in requestResponse.json()["hits"]:
                self.projectsToAdd[i["title"]] = {
                    "title": i["title"],
                    "downloads": i["downloads"],
                    "author": i["author"],
                    "ID": i["project_id"]
                }

            self.ProjectsToAddFormatted = []
            for i in self.projectsToAdd.values():
                self.ProjectsToAddFormatted.append(f"{i['title']}   -   {i['downloads']:,} downloads   -   {i['author']}    ({i['ID']})")
            
            self.projectsToAddNum = menu.StartMenu(list(self.ProjectsToAddFormatted), "Request Results", True)
            
            if not self.projectsToAddNum == None:
                for i in self.projectsToAddNum:
                    title = list(self.projectsToAdd.keys())[i]
                    projects.selectedProjects[title] = self.projectsToAdd[title]


    
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
    
    def ViewProjects(self):
        Title = "Selected Projects"
        optionsRaw: dict = projects.selectedProjects
        options = []

        for i in optionsRaw.values():
            options.append(f"{i['title']}   -   {i['downloads']:,} downloads   -   {i['author']}    ({i['ID']})")
        
        menu.StartMenu(options, Title, False)

class MenuClass: #Inside these are all the menus, this make it easy to trigger menus by doing menu.menuyouwanttotrigger.execute()

    class MainClass:      #main menu, then one with the choices 'Edit Projects' and 'quit'
        def __init__(self):
            self.Options = ["Edit Projects", "Generate table", "Quit"] #the options of the menu
            self.CurOpt = 0 #the current option selected
            self.MenuName = "Main Menu"
        
        def Execute(self): #called to trigger (execute) the menu
            Result = menu.StartMenu(self.Options, self.MenuName, False)
            if not Result == None:
                if Result == 0:
                    menu.EditProjects.execute()
                if Result == 1:
                    table.create()
                if Result == 2:
                    quit(0)
    
    class EditProjectsMenuClass:


        class AddProjectsMenuClass:
            def execute(self):
                projects.addProjects.bySearch() #originally there was another function (by ID) but it didnt quite work out so it got scrapped
  


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
                    projects.ViewProjects()
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
table = TableClass()


while True:
    menu.main.Execute()

