# milk-bot
Custom Discord Bot

# Information needed if you run your own version of this bot #
The quote commands use Mongodb, simply set up a vanilla Mongodb install on your server and the bot will create DBs as needed.
Before deploying your bot you also need to make changes to the !templink, and !info command.

!templink - Replace the hardcoded discord invite link with your own.  
!info - Replace your github link if you create your own branch.    

# Chaos commands - Unfinished
!chaos:   
newgame - Starts a new profile and asks you to pick a race.  
delete - Deletes all entries related to your existing profile.  
  
help - Links to milk-bot GitHub.
        
!mystats: Messages you your current stats.  
          castle - Messages you your castle's stats.  
          army - Messages you your army's stats.  
          race - Messages you your current race's stats.    
  
!castle : Messages you the amount of gold required for your next upgrade.  
          upgrade - Upgrades your castle defenses if you have enough gold.  

!top3 - Displays the names of the five top ranked players.

!intel: Messages you a short list of players with similar rank to you.  

!spy [player] - Attempts to collect information on a given player.

!attack [player] - Sends your soldiers to attack a given player. Messages you a battle report when combat is finished.
