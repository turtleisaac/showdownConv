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
* If no arguments are provided when ran from Terminal/cmd, input is read from your clipboard and output is written in Terminal/cmd
  * If ran inside an IDE, it will likely think it is being run via double-clicking. In which case, just run it from Terminal/cmd within your IDE.
* If ran by double-clicking showdownConv.py, input is read from your clipboard and output is written to your clipboard
  * The input text read from your clipboard will be written to the file `last_input.txt` as a backup
```
usage: showdownConv.py [-h] [-i INPUT] [-o OUTPUT] [-co] [--whole-trainer] [-s]

showdownConv: Converts Showdown/Smogon trainer format to hg-engine trainer format

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file containing Smogon-format team(s) - clipboard is used as input if omitted
  -o OUTPUT, --output OUTPUT
                        output file
  -co, --clipboard-out  writes Smogon format team(s) to clipboard instead of output file
  --whole-trainer       writes the data for the entire trainer, not just the party
  -s, --silent          silences output except for errors and result output if -o or -co are not used
```

### Parsing Multiple Teams
If you want to parse multiple teams at once, Showdown can export all teams with each separated by a line that starts and ends with `===` and has the team name in between. You can specify the trainer ID by including the number in the trainer name itself as shown in the following example: `Red [260]`

## Future
* bug fixes as stuff is brought to my attention
* feel free to contribute by forking and making PR's!
* integration into the main hg-engine repo (idk why I didn't do that in the first place...)
* need to work on making it support specifying alt forms, right now have no way to do that. need some sort of translation table maybe...
