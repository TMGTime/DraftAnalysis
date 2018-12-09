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

#gets the winrate for a player, hero, in what phase of draft
def get_winrate(games, player, hero = "N/A", drafthalf = "N/A", gameMap = "N/A", dateStart = "N/A", dateEnd = "N/A"):
    wins = 0
    losses = 0
    for game in games:
        i = 0
        playerInGame = False
        for team in game:
            i += 1
            for item in team:
                if item[0] == player and (((item[1] == hero or hero == "N/A") and (item[2] == drafthalf or drafthalf == "N/A")) and (game[2][0][1] == gameMap or gameMap == "N/A")):
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
        print("No games found with", player, "on hero", hero, "in phase", drafthalf)
        return "N/A"
    print("Winrate: ", wins * 100 / (wins + losses), "percent")
    return wins * 100 / (wins + losses)

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
                    draftphase = NameCount(item[2],1,0)
                    heroInGame = True
                    break
            if heroInGame:
                break
        if heroInGame:
            date = NameCount(game[2][0][2],1,0)
            dates.append(date)
            phases.append(draftphase)
            inList = False
            for item in players:
                    if item.name == player:
                        inList = True
                        item.count += 1
            if not inList:
                players.append(NameCount(player,1,0))
            if (game[2][0][0] == "Team1Win" and i == 1) or (game[2][0][0] == "Team2Win" and i == 2):
                wins += 1
            else:
                losses += 1
    for item in players:
        print(item.name,item.count)
    print("Wins: ",wins)
    print("Losses: ",losses)
