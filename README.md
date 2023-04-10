# showdownConv
## About
Converts the Smogon/Pokemon Showdown team format to the format used by [hg-engine](https://github.com/BluRosie/hg-engine)

 ## Creators
* [turtleisaac](https://github.com/turtleisaac)

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Future](#future)

## Setup Instructions
1. Have python installed
2. If on Linux, use your package manager to install `xclip`, `xsel`, or `wl-clipboard`
3. Clone/download repo, then navigate to the repo directory in Terminal/cmd and run `pip install -r requirements.txt`

## Usage
You must either use `-i` and specify an input file, or use `-ci` and have the input Smogon-formatted team in your clipboard
```
usage: showdownConv.py [-h] [-i INPUT] [-ci] [-o OUTPUT] [-co] [-s]

showdownConv: Converts Showdown/Smogon trainer format to hg-engine trainer
format

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file containing Smogon-format team(s) - must use if -ci is not specified.
  -ci, --clipboard-in   reads Smogon format team(s) from clipboard instead of input file - must use if -i is not specified
  -o OUTPUT, --output OUTPUT
                        output file
  -co, --clipboard-out  writes Smogon format team(s) to clipboard instead of output file
  -s, --silent          silences output except for errors and result output if -o or -co are not used
```

## Future
* bug fixes as stuff is brought to my attention
* feel free to contribute by forking and making PR's!