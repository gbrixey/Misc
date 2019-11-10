#!/bin/bash

clear
    for ((;;))
    do
        for i in {1..360}
        do
            tput cup 0 0
            ruby qlobe.rb $i
            sleep 0.1
        done
    done
