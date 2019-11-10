#!/bin/bash

# Font styles
REGULAR=$(tput sgr0)
BOLD=$(tput bold)

# Prints one line of the ambulance progress bar.
# Pass in a percent and a time to sleep.
progress_bar_ambulance_line () {
    printf "\r🏥"
    local SPACES_BEHIND_AMBULANCE=$(((40 * $1) / 100))
    local SPACES_IN_FRONT_OF_AMBULANCE=$((40 - $SPACES_BEHIND_AMBULANCE))
    printf " "
    printf %${SPACES_IN_FRONT_OF_AMBULANCE}s
    printf "🚑"
    if [ "$1" -ge "100" ]; then
        printf " "
    else
        printf "💨"
    fi
    printf %${SPACES_BEHIND_AMBULANCE}s
    printf "${BOLD}($1%%)${REGULAR}"
    sleep $2
}

progress_bar_ambulance () {
	local PROGRESS=0
    while [ $PROGRESS -lt 100 ]
    do
        PROGRESS=$((PROGRESS + 5))
        progress_bar_ambulance_line $PROGRESS 0.4
    done
    printf "\n"
}

progress_bar_ambulance
