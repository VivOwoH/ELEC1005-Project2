# ELEC1005Y2022PROJECT2

(*put any links you think important here*)

Report: https://unisydneyedu-my.sharepoint.com/:w:/g/personal/weha7612_uni_sydney_edu_au/EfSMiCQLXwFDgoNNdjwQKLIBUfmHyUfVMpO_09A0Y4aIlw?e=5eraSc


## Requirements (*please tick off when complete a requirement*)
### Must Have 
- [x] Random object appears at a random location when snake eats. 
- [x] When snake eats, snake increases in length by 1. 
- [x] When snake eats basic objects, score increases by 1. 
- [x] Snake movement direction is determined by arrow keys only. 
- [x] Snake does not crash when it touches wall (screen wraparound) 

### Should Have 
- [x] A ‘Eating’ sound is generated whenever snake eats object. 
- [x] A ‘punching’ sound is generated when snake crashes. 
- [ ] Main menu 
	- [ ] Top 10 Scoreboard to record scores of players (Need sign-in area) 
	- [x] New game 
	- [ ] Continue game 
	- [ ] (**WIP**) Instructions/Tutorial level
	- [x] Difficulties (easy, medium, hard) 
	- [x] Exit 
- [ ] In-game menu (pause overlay) 
	- [ ] Restart 
	- [ ] Quit to main menu 

### Could Have 
- [ ] Powerup (each with different timers, could also dance around screens to make them difficult to eat) 
	- [x] Objects that give more score  
	- [ ] Objects that allow snake to lose half of its length 
- [ ] Different Themes (main menu option) 
	- [ ] Retro Nokia-style theme 
	- [ ] Minecraft theme(?) 
- [ ] Snake speed increases as game goes on to increase difficulty (*repetitive, consider to delete*) 


### Non-functional Requirements 
- [ ] Go button should load in-game page within a few seconds. 
- [ ] Quit button should send user out of the game within a few seconds. 
- [ ] Exit button should send user back to main menu page from in-game page within a few seconds. 

## Test Coverage report
Name           Stmts   Miss  Cover

game.py          137      7    95%
test_game.py     157      0   100%

TOTAL            294      7    98%

