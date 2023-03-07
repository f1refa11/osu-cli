import sys,pprint
nocolor = True
if not "-nc" in sys.argv:
    print("Importing colorama...")
    import colorama
    nocolor = True
print("Imporing os..")
import os
print("Getting console size...")
ch = os.get_terminal_size().lines - 2
os.system('cls')
helpListSrc = [
    "'new' - show new maps",
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
\n
osu!cli - osu! download client and osu!direct alternative
'h' to show all commands, 'x' to exit
\n""")
while 1:
    c = input("> ").split()
    os.system('cls')
    if c[0] == "h":
        if len(c) == 1:
            for x in helpList[0]:
                print(x)
            print("Page 1/%s. Use 'h [num]' to switch to another page"%len(helpList))
        else:
            for x in helpList[int(c[1])-1]:
                print(x)
            print("Page %s/%s. Use 'h [num]' to switch to another page"%(c[1],len(helpList)))
    elif c[0] == "x":
        break