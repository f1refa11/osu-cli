import sys,ossapi,json
import os
ch = os.get_terminal_size().lines - 2
os.system('cls')
def openJSON(filename):
    with open(filename, encoding="utf-8") as f:
        return json.load(f)
def saveJSON(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f)
config = openJSON("config.json")
privateData = openJSON("private_data.json")
api = ossapi.Ossapi(privateData["id"], privateData["key"])
helpListSrc = [
    "'new' - show new maps",
    "'sm' - open search menu"
    "'du [url]' - download via url",
    "'dl [num]' - download from current list",
    "'di [id]' - download by id",
    "'ds' - download selected beatmap(use sel)",
    "'sel [num]' - select beatmap from the current list",
    "'selid [id]' - select beatmap by id",
    "'selurl [url] - select beatmap via url",
    "'p [num]' - switch to the page",
    "'setup' - configure osu! directory",
    "'x' - exit the program"
]
helpList = [helpListSrc[i:i + ch] for i in range(0, len(helpListSrc), ch)]
print("""
osu!cli - osu! download client and osu!direct alternative
'h' to show all commands, 'x' to exit""")
if config["dir"] == "":
    print("[Warning] osu! folder location is not specified. Use 'setup' to fix this.")
while 1:
    c = input("> ").split()
    os.system('cls')
    if c[0] == "setup":
        print("Please type the location to your osu! instance folder below. To paste the directory here press CTRL+SHIFT+V or right click with your mouse.")
        loc = input("Directory: ")
        config["dir"] = loc
        saveJSON(config, "config.json")
        print("Config file successfully changed")
    elif c[0] == "new":
        print("Searching recent beatmaps...")
        searchResult = api.search_beatmapsets()
        os.system('cls')
        for x in range(8):
            print("["+str(searchResult.beatmapsets[x].id)+"] "+searchResult.beatmapsets[x].artist+" - "+searchResult.beatmapsets[x].title)
    elif c[0] == "h":
        if len(c) == 1:
            for x in helpList[0]:
                print(x)
            print("Page 1/%s. Use 'h [num]' to switch to another page."%len(helpList))
        else:
            for x in helpList[int(c[1])-1]:
                print(x)
            print("Page %s/%s. Use 'h [num]' to switch to another page."%(c[1],len(helpList)))
    elif c[0] == "x":
        break
    else:
        print("Unknown command: %s. Use 'h' to show list of all commands.")