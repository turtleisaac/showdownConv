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
The following statement(s) only hold true if you are not using the `-h` argument:
* You must either use `-i` and specify an input file, or use `-ci` and have the input Smogon-formatted team in your clipboard
```
usage: showdownConv.py [-h] [-i INPUT] [-ci] [-o OUTPUT] [-co]
                       [--whole-trainer] [-s]

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
  --whole-trainer       writes the data for the entire trainer, not just the party
  -s, --silent          silences output except for errors and result output if -o or -co are not used
```

## Future
* bug fixes as stuff is brought to my attention
* feel free to contribute by forking and making PR's!
* integration into the main hg-engine repo (idk why I didn't do that in the first place...)
* need to work on making it support specifying alt forms, right now have no way to do that. need some sort of translation table maybe...