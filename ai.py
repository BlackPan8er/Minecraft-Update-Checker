import requests
import json
import readchar
import os
import re
from prettytable import PrettyTable

# pip install readchar prettytable requests

class ModrinthPluginChecker:
    def __init__(self):
        self.selected_plugins = []

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def search_plugins(self):
        query = input("Enter plugin name to search:\n  >>> ").strip()
        if not query:
            return

        params = {
            "query": query,
            "index": "relevance",
            "facets": json.dumps([["project_type:plugin"]]),
            "limit": 15
        }

        try:
            resp = requests.get("https://api.modrinth.com/v2/search", params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"Error fetching data: {e}")
            input("Press Enter to continue...")
            return

        hits = data.get("hits", [])
        if not hits:
            print("No results found.")
            input("Press Enter to continue...")
            return

        plugins = [{"slug": h["slug"], "title": h["title"], "downloads": h["downloads"]} for h in hits]

        cur = 0
        selected = set()

        while True:
            self.clear()
            print(f"Results for '{query}' — select with [SPACE], confirm with [ENTER], quit with [q]\n")
            for i, plugin in enumerate(plugins):
                prefix = ">> " if i == cur else "   "
                mark = "[x]" if plugin["slug"] in selected else "[ ]"
                downloads = f"{plugin['downloads']:,}".replace(",", ".")
                print(f"{prefix}{mark} {plugin['title']} ({downloads} ⬇️)")

            key = readchar.readkey()

            if key == readchar.key.UP and cur > 0:
                cur -= 1
            elif key == readchar.key.DOWN and cur < len(plugins) - 1:
                cur += 1
            elif key == " ":
                slug = plugins[cur]["slug"]
                if slug in selected:
                    selected.remove(slug)
                else:
                    selected.add(slug)
            elif key == readchar.key.ENTER:
                for p in plugins:
                    if p["slug"] in selected and p not in self.selected_plugins:
                        self.selected_plugins.append(p)
                break
            elif key.lower() == "q":
                break

    def get_versions_for_plugin(self, slug):
        try:
            url = f"https://api.modrinth.com/v2/project/{slug}/version"
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"Error fetching versions for {slug}: {e}")
            return set()

        versions = set()
        for v in data:
            for game_ver in v.get("game_versions", []):
                # Only include normal releases: X.Y.Z
                if re.match(r"^\d+\.\d+\.\d+$", game_ver):
                    versions.add(game_ver)
        return versions

    def make_table(self):
        if not self.selected_plugins:
            print("No plugins selected.")
            input("Press Enter to continue...")
            return

        all_versions = set()
        plugin_versions = {}

        print("Fetching version data for selected plugins...\n")
        for plugin in self.selected_plugins:
            versions = self.get_versions_for_plugin(plugin["slug"])
            plugin_versions[plugin["slug"]] = versions
            all_versions |= versions

        all_versions = sorted(all_versions, reverse=True)

        # Ensure unique column names for PrettyTable
        titles = []
        seen = {}
        for p in self.selected_plugins:
            title = p["title"]
            slug = p["slug"]
            if title in seen:
                seen[title] += 1
                title = f"{title} ({seen[title]})"
            else:
                seen[title] = 1
            titles.append(title)

        table = PrettyTable()
        table.field_names = ["Minecraft Version"] + titles

        for mc_ver in all_versions:
            row = [mc_ver]
            for plugin in self.selected_plugins:
                if mc_ver in plugin_versions[plugin["slug"]]:
                    row.append("✅")
                else:
                    row.append("❌")
            table.add_row(row)

        self.clear()
        print("=== Minecraft Plugin Compatibility Table ===\n")
        print(table)
        input("\nPress Enter to return...")

    def run(self):
        while True:
            self.clear()
            print("==== Modrinth Plugin Version Checker ====\n")
            print("1. Search for plugins")
            print("2. Generate compatibility table")
            print("3. Quit")

            choice = input("\nSelect option: ").strip()
            if choice == "1":
                self.search_plugins()
            elif choice == "2":
                self.make_table()
            elif choice == "3":
                break

if __name__ == "__main__":
    ModrinthPluginChecker().run()
