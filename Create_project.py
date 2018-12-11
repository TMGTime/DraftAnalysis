import datetime
from operator import attrgetter
#Returns a bunch of recursive lists with information about the draft
def read_file(file):
    drafts = open(file,'r')
    sublist = []
    lists = []
    teams = []
    games = []
    word = ''
    lines = drafts.read()
    for char in lines:
        # - characters are used to separate words
        if char == '-':
            sublist.append(word)
            word = ''
        # spaces are used to separate entitities (playername,heroname,drafted)
        elif char == ' ':
            sublist.append(word)
            lists.append(sublist)
            sublist = []
            word = ''
        # newlines are used to separate teams and game info (team1,team2,gameInfo)
        elif char == '\n':
            #if the teams and game info is already at 3, a  second newline indicates
            #a new game~
            if len(teams) == 3:
                games.append(teams)
                teams = []
                sublist = []
                word = ''
            else:
                sublist.append(word)
                lists.append(sublist)
                teams.append(lists)
                lists = []
                sublist = []
                word = ''
        else:
            word = word + char
    return games

#gets the winrate for a player, hero, in what phase of draft (added map and date paramteters)
def get_winrate(games, player, hero = "N/A", drafthalf = "N/A", gameMap = "N/A", dateStart = "N/A", dateEnd = "N/A"):
    wins = 0
    losses = 0
    for game in games:
        format_str = "%m/%d/%Y"
        #if the datetimes are in the wrong format (NA), they'll raise an exception
        try:
            start_datetime = datetime.datetime.strptime(dateStart,format_str)
            end_datetime = datetime.datetime.strptime(dateEnd,format_str)
        except:
            start_datetime = "N/A"
            end_datetime = "N/A"
        game_datetime = datetime.datetime.strptime(game[2][0][2],format_str)
        i = 0
        playerInGame = False
        for team in game:
            i += 1
            for item in team:
                #TODO: Fix this line so that datetime wont crash the program if not in datetime format or == str("N/A"). This works for now.
                if item[0] == player and ((((item[1] == hero or hero == "N/A") and (item[2] == drafthalf or drafthalf == "N/A")) and (game[2][0][1] == gameMap or gameMap == "N/A")) and ((dateStart == "N/A" and dateEnd == "N/A") or (start_datetime <= game_datetime and end_datetime >= game_datetime))):
                    playerInGame = True
                    break
                if playerInGame:
                    break
            if playerInGame:
                break
        if playerInGame:
            if (game[2][0][0] == "Team1Win" and i == 1) or (game[2][0][0] == "Team2Win" and i == 2):
                wins += 1
            else:
                losses += 1
    if wins == 0 and losses == 0:
        print("No games found with these search parameters")
        return "N/A"
    print("Winrate: ", wins * 100 / (wins + losses), "percent")
    return wins * 100 / (wins + losses)

def create_NameCounts(item,item_list):
    class NameCount:
        def __init__(self,name,count,wincount):
            self.name = name
            self.count = count
            self.wincount = wincount
    inList = False
    for obj in item_list:
        if obj.name == item:
            inList = True
            obj.count += 1
    if not inList:
        item_list.append(NameCount(item,1,0))

def check_wins(item,item_list):
    for obj in item_list:
        if obj.name == item:
            obj.wincount += 1
            
def get_hero_stats(games,hero):
    class NameCount:
        def __init__(self,name,count,wincount):
            self.name = name
            self.count = count
            self.wincount = wincount
    wins = 0
    losses = 0
    sublist = []
    players = []
    maps = []
    phases = []
    dates = []
    for game in games:
        heroInGame = False
        i = 0
        for team in game:
            i += 1
            for item in team:
                if item[1] == hero:
                    player = item[0]
                    draftphase = item[2]
                    heroInGame = True
                    break
            if heroInGame:
                break
        if heroInGame:
            date = game[2][0][2]
            gameMap = game[2][0][1]
            #creates lists with object NameCounts that has the object name, game count, and win count
            create_NameCounts(date,dates)
            create_NameCounts(gameMap,maps)
            create_NameCounts(draftphase,phases)
            create_NameCounts(player,players)
                
            if (game[2][0][0] == "Team1Win" and i == 1) or (game[2][0][0] == "Team2Win" and i == 2):
                wins += 1
                check_wins(gameMap,maps)
                check_wins(date,dates)
                check_wins(player,players)
                check_wins(draftphase,phases)
            else:
                losses += 1
    gameCount = 0
    banCount = 0
    for game in games:
        gameCount += 1
        for item in game[4]:
            if hero in item:
                banCount += 1
        for item in game[3]:
            if hero in item:
                banCount += 1
                
    print("Top player(s):")
    i = 0
    while( i < 3):
        try:
            maxplayer = max(players,key=attrgetter('wincount'))
        except:
            print("---")
            i += 1
            continue
        print(maxplayer.name,"(",maxplayer.wincount,"-",maxplayer.count - maxplayer.wincount,")")
        players.remove(maxplayer)
        i += 1
    print()
    print("Best maps:")
    i = 0
    while( i < 2):
        try:
            bestmap = max(maps,key=attrgetter('wincount'))
        except:
            print("---")
            i += 1
            continue
        print(bestmap.name,"(",bestmap.wincount,"-",bestmap.count - bestmap.wincount,")")
        maps.remove(bestmap)
        i += 1
    print()
    maxphase = max(phases,key=attrgetter('wincount'))
    if "1" in maxphase.name or "2" in maxphase.name:
        print("Most commonly drafted in first phase")
    else:
        print("Most commonly drafted in second phase")
    print("Wins: ",wins)
    print("Losses: ",losses)
    print(round(wins*100/(losses + wins),1),"% winrate")
    print(round((banCount*100/gameCount),1),"% banrate")
    print(round((wins + losses)*100 / gameCount,1),"% pickrate")
    print(round((banCount*100/gameCount) + ((wins + losses)*100 / gameCount),1),"% overall involvement")
