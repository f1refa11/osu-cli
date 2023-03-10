import ossapi,json,requests,os,re
from tqdm import tqdm
terminalData = os.get_terminal_size()
ch = terminalData.lines - 2
cols = terminalData.columns
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
print("""osu!cli - osu! download client and osu!direct alternative
'h' to show all commands, 'x' to exit""")
if config["dir"] == "":
    print("[Warning] osu! folder location is not specified. Use 'setup' to fix this.")
while 1:
    c = input("> ").split()
    os.system('cls')
    if len(c) != 0:
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
            if len(c) == 1:
                for x in range(ch):
                    print("["+str(searchResult.beatmapsets[x].id)+"] "+searchResult.beatmapsets[x].artist+" - "+searchResult.beatmapsets[x].title)
            else:
                for x in range(int(c[1])):
                    print("["+str(searchResult.beatmapsets[x].id)+"] "+searchResult.beatmapsets[x].artist+" - "+searchResult.beatmapsets[x].title)
        elif c[0] == "di":
            if len(c) == 1:
                print("[Error] No ID specified")
            else:
                print("Connecting to Beatconnect...")
                url = "https://beatconnect.io/b/%s/"%int(c[1])
                r = requests.get(url, stream=True)
                d = r.headers['content-disposition']
                fname = re.findall("filename=(.+)", d)[0]
                fname = re.sub('[";]', '', fname)
                totalSize = int(r.headers.get("content-length", 0))
                print("Connected! Downloading as '%s'..."%fname)
                with open("beatmaps/"+fname, "wb") as f:
                    pbar = tqdm(total=totalSize,desc="Progress: ",ncols=cols,unit="iB",unit_scale=True)
                    for i,data in enumerate(r.iter_content(1024)):
                        size = f.write(data)
                        pbar.update(len(data))
                pbar.close()
                print("Done! Saved in beatmaps/%s. Use 'ir' to install the most recent downloaded beatmap or 'l' to check list of all downloaded beatmaps."%fname)
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
            print("Unknown command: '%s'. Use 'h' to show list of all commands."%c[0])
#1683963
