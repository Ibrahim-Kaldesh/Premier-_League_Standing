import csv
from collections import deque

class Match:
  def __init__(self,round,date,homeGoals,awayGoals,result):
    self.round=round
    self.date=date
    self.homeGoals=homeGoals
    self.awayGoals=awayGoals
    self.result=result

class Team:
  def __init__(self,teamName):
    self.teamName=teamName
    self.matchPlayed=0
    self.wins=0
    self.drawns=0
    self.loses=0
    self.goalsFor=0
    self.goalsAgainst=0
    self.goalsDiff=0
    self.points=0

# O(1)
def dateToInt(s):
  day,month,year=int(s[0:2]),int(s[3:5]),int(s[6:])
  return year*10000+month*100+day

# O(V+E)
def standing_by_round(choice):

  # Time  Complexity : O(V+E)
  # Space Complexity : O(V+E)

  q.append(1)
  vis[1]=1
  while q: # -> O(V)
    u = q.popleft()
    for v in adj[u]: # -> O(E)
      match = v[1]
      if match.round <= choice:   # -> O(1)  
        teams[u].goalsFor += match.homeGoals
        teams[v[0]].goalsAgainst += match.homeGoals
        teams[v[0]].goalsFor += match.awayGoals     
        teams[u].goalsAgainst += match.awayGoals
        teams[u].matchPlayed+=1
        teams[v[0]].matchPlayed+=1

        if match.result == "H":
          teams[u].wins+=1                           
          teams[u].points+=3
          teams[v[0]].loses+=1

        elif match.result == "A":                         
          teams[v[0]].wins+=1                        
          teams[v[0]].points+=3
          teams[u].loses+=1

        else:
          teams[u].drawns+=1
          teams[u].points+=1
          teams[v[0]].drawns+=1
          teams[v[0]].points+=1

      if not vis[v[0]]:      # -> O(1)
        q.append(v[0])                             
        vis[v[0]]=1

# O(V+E)
def standing_by_date(choice):

  # Time  Complexity : O(V+E)
  # Space Complexity : O(V+E)

  q.append(1)
  vis[1]=1
  while q:  # -> O(V)
    u = q.popleft()
    for v in adj[u]:  # -> O(V)
      match = v[1]
      if match.date <= choice:    # -> O(1)
        teams[u].goalsFor += match.homeGoals
        teams[v[0]].goalsAgainst += match.homeGoals
        teams[v[0]].goalsFor += match.awayGoals
        teams[u].goalsAgainst += match.awayGoals
        teams[u].matchPlayed+=1
        teams[v[0]].matchPlayed+=1

        if match.result == "H":
          teams[u].wins+=1
          teams[u].points+=3
          teams[v[0]].loses+=1

        elif match.result == "A":          
          teams[v[0]].wins+=1
          teams[v[0]].points+=3
          teams[u].loses+=1

        else:
          teams[u].drawns+=1
          teams[v[0]].drawns+=1
          teams[u].points+=1
          teams[v[0]].points+=1

      if not vis[v[0]]:        # -> O(1)
        q.append(v[0])
        vis[v[0]]=1


if __name__ == '__main__':

  nteam  = 0
  stoint = {}
  inttos = {}

  # Take Intput from csv file
  # O(E lg V)
  # where E (edges) number of played matches
  # where V(vertices) number of Teams
  try:
    with open('epl_results.csv','r') as f:
      inp_file = list(csv.reader(f))[1:]
      for record in inp_file:       # -> O(E) where E (edges) number of played matches 
        homeTeam = record[2]        # -> O(1)
        if homeTeam not in stoint:  # -> O(lg V) where V(vertices) number of Teams
          nteam+=1
          stoint[homeTeam] = nteam
          inttos[nteam] = homeTeam

      adj=[[] for i in range(nteam+1)]   # -> O(V) where V(vertices) number of Teams
      for record in inp_file:            # -> O(E) where E (edges) number of played matches 
        try:
          round,date,homeTeam,awayTeam,homeGoals,awayGoals,result = int(record[0]),dateToInt(record[1]),record[2],record[3],int(record[4]),int(record[5]),record[6]
          m = Match(round,date,homeGoals,awayGoals,result)   # -> O(1)
          adj[stoint[homeTeam]].append([stoint[awayTeam],m]) # -> O(1)
        except:pass
  except FileNotFoundError:pass
  finally:
    f.close()

  while (True):

    q = deque()
    vis=[0 for i in range(nteam+1)]      # -> O(V) where V(vertices) number of Teams
    teams = ['-']
    for team in inttos:                  # -> O(V) where V(vertices) number of Teams
      teams.append(Team(inttos[team]))   # -> O(1)

    print()
    print('='*30)
    print("\n1 - search by round\n\n2 - search by date\n")
    print('='*30)

    pole = int(input("\nPlease , Enter your choice :")) # -> O(1)
    if (pole == 1): # -> O(1)
      choice = int(input("Enter the round number : ")) # -> O(1)
      standing_by_round(choice)    # -> O(V+E)

    else:
      choice = dateToInt(input("Enter the date in the form 'dd/mm/year' : ")) # -> O(1)
      standing_by_date(choice)     # -> O(V+E)

    # Store results of standindg in a list and sort them
    teams = teams[1:]
    teams=sorted(teams,
      key=lambda x:(x.points,x.goalsDiff,x.goalsFor),reverse=True) # -> O(V lg v)

    # Show Output in csv file
    try:
      with open ('output.csv','w',newline='') as f:
        out_file = csv.writer(f)
        out_file.writerow(["#","Team","M Played","Wins",
        "Drawns","Loses","G For","G Against","G Diff","Points"]) # -> O(1)
        cnt=1
        for team in teams:   # -> O(V)
          out_file.writerow([
            cnt,team.teamName,team.matchPlayed,team.wins, 
            team.drawns,team.loses,team.goalsFor, 
            team.goalsAgainst,team.goalsFor-team.goalsAgainst, 
            team.points 
          ])                 # -> O(1)
          cnt+=1

    except FileNotFoundError:pass

    finally:
      f.close()