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
4. Move `showdownConv.py` into a **NEW FOLDER** named `showdownConv` inside of your cloned hg-engine directory
    * Do not move the folder it came in into the hg-engine directory because this will just cause annoying git crap for your local hg-engine repo due to invalid VCS mappings
5. Run the program from its new directory in Terminal/cmd using the `--generate-assets` argument
   * if you are reading this line, then this isn't done yet so right now the tool only knows Garchomp exists lol

## Usage
The following statement(s) only hold true if you are not using the `-h` or `--generate-assets` arguments:
* You must either use `-i` and specify an input file, or use `-ci` and have the input Smogon-formatted team in your clipboard
```
usage: showdownConv.py [-h] [-i INPUT] [-ci] [-o OUTPUT] [-co]
                       [--whole-trainer] [-s] [--generate-assets]

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
  --generate-assets     generates translation dict needed to get the correct names for hg-engine
```

## Future
* bug fixes as stuff is brought to my attention
* feel free to contribute by forking and making PR's!
* integration into the main hg-engine repo (idk why I didn't do that in the first place...)