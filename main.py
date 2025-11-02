import requests, json, readchar, os, time

class menu:
    def __init__(self):
        self.CurOption = 0
        self.SelectedProjects = []

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")



    def Main(self):
        options = ["1. Add Plugin", "2. Quit"]
        CurOption = 0
        while True:
            self.clear()
            for i in range(len(options)):
                prefix = ">> " if CurOption == i else "   "
                title = options[i]
                print(f"{prefix}{title}")
            key = readchar.readkey()
            if key == readchar.key.UP and CurOption != 0:
                CurOption -= 1
            elif key == readchar.key.DOWN and CurOption != len(options):
                CurOption += 1
            elif key == readchar.key.ENTER:
                if CurOption == 0:
                    self.SearchProjects()
                elif CurOption == 1:
                    quit(1)
                else:
                    print("\n\n\n\n\n\nERROR ERROR ERROR\n\n\n")
                    quit(0)



    def SearchProjects(self):
        ####################################################################################################
        self.SearchQuery = input("Enter query\n  >>>")
        RequestParams = {
            "query": self.SearchQuery,
            "index": "relevance",
            "facets": json.dumps([["project_type:plugin"]])
        }
        RequestResponse = requests.get("https://api.modrinth.com/v2/search", params=RequestParams)
        ResponseData = RequestResponse.json()

        self.FoundPlugins = {}
        for i in ResponseData["hits"]:
            self.FoundPlugins[i["title"]] = {
                "title": i["title"],
                "downloads": i["downloads"]
            }

        self.DisplayResults()
        #for j in FoundPlugins:
        #    print(f"Title: {FoundPlugins[j]["title"]}\nDownloads: {FoundPlugins[j]["downloads"]:,}")
        ####################################################################################################

    def DisplayResults(self):
        while True:
            self.clear()
            for i, (title, project) in enumerate(self.FoundPlugins.items()):
                prefix = ">>>>> " if i == self.CurOption else ""
                title = project["title"]
                downloads = project["downloads"]
                print(f"{prefix}{title} -- {downloads} ⬇️")
                if i == self.CurOption:
                    self.SelectedOption = project

            if self.HandleInput():
                if not self.SelectedOption in self.SelectedProjects:
                    self.SelectedProjects.append(self.SelectedOption)
                    self.clear()
                    print(f"Added New Project To List:\n\n{project["title"]}\nDownloads: {project["downloads"]}\n  Description: NOT IMPLEMENTED")
                    time.sleep(1)
                break

    def HandleInput(self):
        key = readchar.readkey()
        if key == readchar.key.UP and self.CurOption != 0:
            self.CurOption -= 1
        
        elif key == readchar.key.DOWN and self.CurOption != len(self.FoundPlugins)-1:
            self.CurOption += 1
        
        elif key == readchar.key.ENTER:
            return True #gets handled by DisplayResults()
            


Menu = menu()

Menu.Main()