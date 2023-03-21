import ossapi,json,requests,os,re,zipfile,shutil
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
def reloadLocalization():
    global l,helpList
    if config["lang"] == "ru":
        l = openJSON("lang/ru.json")
    elif config["lang"] == "en":
        l = openJSON("lang/en.json")
    helpList = [l["helpList"][i:i + ch] for i in range(0, len(l["helpList"]), ch)]
config = openJSON("config.json")
langList = ["en", "ru"]
reloadLocalization()
privateData = openJSON("private_data.json")
api = ossapi.Ossapi(privateData["id"], privateData["key"])
print(l["welcome"])
if config["dir"] == "":
    print(l["warningDir"])
while 1:
    c = input("> ").split()
    os.system('cls')
    if len(c) != 0:
        if c[0] == "setup":
            print(l["setupDirDesc"])
            loc = input(l["setupDir"])
            config["dir"] = loc
            saveJSON(config, "config.json")
            print(l["saveConfigSuccess"])
        elif c[0] == "new":
            print(l["newMapSearchProgress"])
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
                print(l["idError1"])
            else:
                print(l["mirrorConnect"])
                url = "https://beatconnect.io/b/%s/"%int(c[1])
                r = requests.get(url, stream=True)
                d = r.headers['content-disposition']
                fname = re.findall("filename=(.+)", d)[0]
                fname = re.sub('[";]', '', fname)
                totalSize = int(r.headers.get("content-length", 0))
                print(l["mirrorSuccess"]%fname)
                with open("beatmaps/"+fname, "wb") as f:
                    pbar = tqdm(total=totalSize,desc="Progress: ",ncols=cols,unit="iB",unit_scale=True)
                    for i,data in enumerate(r.iter_content(1024)):
                        size = f.write(data)
                        pbar.update(len(data))
                pbar.close()
                print(l["downloadSuccess"]%fname)
        elif c[0] == "l":
            print("Refreshing 'beatmaps/' folder...")
            beatmapList = []
            for file in os.listdir("beatmaps"):
                if file.endswith(".osz"):
                    beatmapList.append(os.path.splitext(file)[0])
            result = [beatmapList[i:i + (ch-1)] for i in range(0, len(beatmapList), (ch-1))]
            if len(beatmapList) == 0:
                print("No beatmaps found! You can download them using download commands - 'di', 'du', 'ds' or 'dl'")
            else:
                os.system('cls')
                print("List of imported beatmaps:")
                if len(c) == 1:
                    for x in result[0]:
                        print(x)
                    print(l["pageList"]%(1,len(helpList)))
                else:
                    for x in result[int(c[1])-1]:
                        print(x)
                    print(l["pageList"]%(c[1],len(helpList)))
        elif c[0] == "da":
            print("Importing beatmaps...")
            pbar = tqdm(total=len(os.listdir("beatmaps")),desc="Progress: ",ncols=cols)
            os.chdir("beatmaps")
            for beatmap in os.listdir("."):
                if beatmap.endswith(".osz"):
                    dirName = os.path.splitext(beatmap)[0]
                    os.mkdir(dirName)
                    pbar.update(8/7/4)
                    zipFile = zipfile.ZipFile(beatmap, "r")
                    pbar.update(8/7/4)
                    zipFile.extractall(dirName)
                    pbar.update(8/7/4)
                    shutil.move(dirName, os.path.join(config["dir"], "Songs", dirName))
                    pbar.update(8/7/4)
            pbar.close()
        elif c[0] == "lang":
            if len(c) == 1:
                print("List of supported language codes:")
                for x in langList:
                    print('"%s"'%x)
            else:
                if c[1] in langList:
                    config["lang"] = c[1]
                    saveJSON(config, "config.json")
                    print(l["saveConfigSuccess"])
                    reloadLocalization()
                    print(l["reloadLocalizationSuccess"])
                else:
                    print(l["langNotInList"])
        elif c[0] == "h":
            if len(c) == 1:
                for x in helpList[0]:
                    print(x)
                print(l["pageHelp"]%(1,len(helpList)))
            else:
                for x in helpList[int(c[1])-1]:
                    print(x)
                print(l["pageHelp"]%(c[1],len(helpList)))
        elif c[0] == "x":
            break
        else:
            print(l["unknownCommand"]%c[0])