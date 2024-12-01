#!/bin/bash

source env.sh

curl --cookie "session=$AOC_COOKIE" https://adventofcode.com/$1/day/$2/input > in.txt
