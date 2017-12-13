# Sokoban Game
	Sokoban is a japanese transport puzzle game originally developped by Hiroyuki Imabayashi in 1982. The name comes from Japan and means "warehouse keeper". The player pushes boxes or crates around in a warehouse, trying to get them to storage locations. This implementation is based on Python & pyGame Library.

## System Requirements
	Python 2.7 

	Install xQuartz (https://www.xquartz.org)
	Install SDL(`brew install sdl sdl_image sdl_mixer sdl_ttf portmidi`)
	Install others `brew tap homebrew/headonly; brew install smpeg`


## Level-Set

	Level-Sets can be created under the 'levels' folder. Each level set contains different levels where 
	each level is represented by a file names as 'levelXX' where 'XX' are incrementing numbers.
	For this project there are 25 levels generated  in the increasing order of complexity for a human 
	player. 

 	Each level can be represented in a textual format within the level file.

	The different components of a level are 

	| Level element         |  Character |
	| --------------------- |:----------:|
	| Wall                  | #          |
	| Player                | @          |
	| Player on goal square | +          |
	| Box                   | $          |
	| Box on goal square    | *          |
	| Goal square	        | .          |
	| Floor                 | (Space)    |

	A typical level looks like this:

	```
	   #########
	  ##   ##  ######
	###     #  #    ###
	#  $ #$ #  #  ... #
	# # $#@$## # #.#. #
	#  # #$  #    . . #
	# $    $ # # #.#. #
	#   ##  ##$ $ . . #
	# $ #   #  #$#.#. #
	## $  $   $  $... #
	 #$ ######    ##  #
	 #  #    ##########
	 ####
	```

## How to play the game

	For human playing the game can be started with the following command 
	`python sokoban.py -m human -s project_levels -l 5`
	On successful completion of a level , the next level is initialized automatically.

	Use arrows keys to move player
	U   => Undo move
	R   => Reset level
	ESC => Exit game

	The game can also be initialized for algorithms to play using the -m option. The various values
	(algorithms) that can be passed for '-m' option are provided in the commands section.


## COMMAND
	The game can be initialized/started using the command 'python sokoban.py' with various options

			python sokoban.py -l [Default 1] -s [Level Set] -t [Timeout in seconds] [-c] [Cost function] [-f] [heuristic]


## OPTIONS 

-l 		-l or '--level' is used to choose a level, the level must be present in the 'levels/level-set' 
		folder.	The level files must be in the format 'levelXX' where 'XX' is an incrementing number.On successful completion of a level the next level gets initialized by itself.

-s 		-s or '--set' is used to pass the level-set and this folder must be present under the 'levels'
		folder. 

-m 		-m or '--method' option is used to chose the player type/algorithm for the game. The various values 		are as follows
		human 	: for human player(DEFAULT)
		dfs		: Depth First Search
		bfs		: Breadth First Search
		ucs		: Uniform Cost Search
		astar	: A star
		dfsid	: Depth First Search with Iterative Deepening

-t 		-t can be used to pass the timeout value in seconds when algorithms are playing the game. It is 	
		observed that this feature doesnot work on windows environment.

-c 		-c option is used to pass the cost function for the UCS algorithm. There are two cost functions 	
		implemented

		default :  Move -> 1, Push ->2 , PushOut -> 10
		cost2	:  Move -> 1, Push ->2 , PushOut -> 2
		
-f      -f option is used to pass the heuristic function for the A* algorithm. The various heuristics are
		as desrcibed below:
		manhattan : min distance using manhattan distance
		euclidean : min distance using euclidean distance
		hungarian : hungarian distance using manhattan distance
		hungarian_euclidean : hungarian distance using euclidean distance


## Metrics
	Whenever game is initialized/started for an algorithm , the statistics of the run are captured in a file
	named as 'algorithm' or 'algorith_cost function' or 'algorithm_heuristic'
	eg. astar_euclidean.txt , astar_hungarian_euclidean.txt, back.txt, dfsid.txt etc.
	The metrics are captured as
	LEVEL-SET, 		LEVEL, METHOD, 	TIMETAKEN, 		NUMBER_OF_STEPS, STATES_EXPLORED
	project_levels,	5,		astar,	326.152099609,	34,					733
	project_levels,	6,		astar,	1948.15698242,	75,					4874
	project_levels,	7,		astar,	929.625976562,	17,					1138
	project_levels,	8,		astar,	8657.69311523,	31,					13913
	project_levels,	9,		astar,	3116.33007812,	23,					6162

##Examples 
	python sokoban.py -m dfs -s project_levels -l 6
	python sokoban.py -m dfsid -s project_levels -l 5
	python sokoban.py -m bfs -s project_levels -l 5
   	python sokoban.py -m ucs -s project_levels -l 5 -c cost2
   	python sokoban.py -m astar -s project_levels -l 5 -f manhatten
  	python sokoban.py -m astar -s project_levels -l 5 -f euclidean
  	python sokoban.py -m astar -s project_levels -l 5 -f hungarian_euclidean









