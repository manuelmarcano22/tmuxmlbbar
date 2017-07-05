#!/bin/bash

if pgrep -x 'games.py' > /dev/null; 
then  
	exit 0
else
	python $HOME/tmux/games.py &
fi

