"""
Developed by turtleisaac <https://github.com/turtleisaac>

This file is part of showdownConv <https://github.com/turtleisaac/showdownConv>

This program converts the Smogon/Pokemon Showdown team format to the format used by hg-engine <https://github.com/BluRosie/hg-engine>

As the Smogon/Pokemon Showdown team format does not contain all of the possible data that a trainer in hg-engine can have, please refer to the following link to see that data and examples of it:
    https://github.com/BluRosie/hg-engine/wiki/Trainer-Pok%C3%A9mon-Structure-Documentation
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional
from enum import Enum
import pyperclip as pc
import re

engine_format = '\t\t// mon %s\n' \
                '\t\tivs %s\n' \
                '\t\tabilityslot %s\n' \
                '\t\tlevel %i\n' \
                '\t\tpokemon SPECIES_%s\n' \
                '\t\titem ITEM_%s\n' \
                '\t\tmove MOVE_%s\n' \
                '\t\tmove MOVE_%s\n' \
                '\t\tmove MOVE_%s\n' \
                '\t\tmove MOVE_%s\n' \
                '\t\tability ABILITY_%s\n' \
                '\t\tsetivs %i, %i, %i, %i, %i, %i // hp, atk, def, spd, spatk, spdef\n' \
                '\t\tsetevs %i, %i, %i, %i, %i, %i\n' \
                '\t\tnature NATURE_%s\n' \
                '\t\tshinylock %i\n' \
                '\t\tadditionalflags %s\n' \
                '\t\tnickname %s\n' \
                '\t\tballseal 0\n'

trainer_format = 'trainerdata %s // %s\n' \
                 '\ttrainermontype  %s\n' \
                 '\ttrainerclass INSERT_CLASS_HERE\n' \
                 '\tbattletype SINGLE_BATTLE\n' \
                 '\tnummons %i\n' \
                 '\titem ITEM_NONE\n' \
                 '\titem ITEM_NONE\n' \
                 '\titem ITEM_NONE\n' \
                 '\titem ITEM_NONE\n' \
                 '\taiflags INSERT_AI_FLAGS_HERE\n' \
                 '\tbattletype2 0\n' \
                 '\tendentry\n\n' \
                 '\tparty INSERT_NUMBER_HERE\n'

stats = ['hp', 'atk', 'def', 'spe', 'spa', 'spd']

IRREGULAR_SPECIES_NAMES = {
    '-----': 'NONE',
    'NIDORAN♀': 'NIDORAN_F',
    'NIDORAN♂': 'NIDORAN_M',
    'FARFETCH’D': 'FARFETCHD',
    'FARFETCH’_D': 'FARFETCHD',
    'MR. MIME': 'MR_MIME',
    'MR._MIME': 'MR_MIME',
    'HO-OH': 'HO_OH',
    'MIME JR.': 'MIME_JR',
    'MIME_JR.': 'MIMEJR',
    'PORYGON-Z': 'PORYGON_Z'
}

IRREGULAR_ABILITIES = {
    'COMPOUNDEYES': 'COMPOUND_EYES',
    'LIGHTNINGROD': 'LIGHTNING_ROD',
}

IRREGULAR_ITEMS = {
    'KING’S_ROCK': 'KINGS_ROCK',
    'SILVER_POWDER': 'SILVERPOWDER',
    'TINY_MUSHROOM': 'TINYMUSHROOM',
    'TWISTED_SPOON': 'TWISTEDSPOON',
    'DEEP_SEA_SCALE': 'DEEPSEASCALE',
    'DEEP_SEA_TOOTH': 'DEEPSEATOOTH',
    'NEVER_MELT_ICE': 'NEVERMELTICE',
}

IRREGULAR_MOVES = {
    'SMOKE_SCREEN': 'SMOKESCREEN',
    'SELFDESTRUCT': 'SELF_DESTRUCT',
    'SOFTBOILED': 'SOFT_BOILED',
}


class Rule(Enum):
    TRAINER_DATA_TYPE_MOVES = 0
    TRAINER_DATA_TYPE_ITEMS = 1
    TRAINER_DATA_TYPE_ABILITY = 3
    TRAINER_DATA_TYPE_IV_EV_SET = 4
    TRAINER_DATA_TYPE_NATURE_SET = 5
    TRAINER_DATA_TYPE_SHINY_LOCK = 6
    TRAINER_DATA_TYPE_ADDITIONAL_FLAGS = 7


default_evs = dict()
for stat in stats:
    default_evs[stat] = 0

default_ivs = dict()
for stat in stats:
    default_ivs[stat] = 31


def upper_snake_case(s: str) -> str:
    return '_'.join(
        re.sub(
            '([A-Z][a-z]+)',
            r' \1',
            re.sub(
                '([A-Z]+)',
                r' \1',
                s.replace('-', ' ')
            )
        ).split()
    ).upper()


def sanitize(name: str, sanitation_dict: dict[str, str]) -> str:
    snake = upper_snake_case(name)
    if snake == '':
        return 'NONE'

    if snake in sanitation_dict:
        return sanitation_dict[snake]

    return snake


def format_nickname(name: str) -> str:
    if name == '':
        return ''
    if len(name) > 10:
        name = name[:10]
    s = ''
    for c in name:
        if c.islower() and not c.isnumeric():
            s += '_%s_, ' % c
        else:
            s += '_%s, ' % c
    s += '_endstr, '
    s += '0, ' * (10 - len(name))
    s = s[:-2]

    return s


class Team:
    def __init__(self, name='INSERT_NAME_HERE', id='INSERT_NUMBER_HERE'):
        self.mons = list()
        if '[' in name and ']' in name:
            self.name = name[name.index(']')+1:].strip()
        else:
            self.name = name
        self.id = id


class Mon:
    def __init__(self, species, nickname):
        self.species = sanitize(species, IRREGULAR_SPECIES_NAMES)
        self.nickname = nickname
        self.level = 100
        self.item = 'NONE'
        self.ability = 'NONE'
        self.nature = ''
        self.evs = dict()
        for stat in stats:
            self.evs[stat] = 0
        self.ivs = dict()
        for stat in stats:
            self.ivs[stat] = 31
        self.moves = list()
        self.shiny = False
        self.ev_temp = list()
        self.iv_temp = list()

    def verify(self):
        for ev in self.ev_temp:
            self.evs[ev.split(' ')[1]] = int(ev.split(' ')[0])

        for iv in self.iv_temp:
            self.ivs[iv.split(' ')[1]] = int(iv.split(' ')[0])

        while len(self.moves) < 4:
            self.moves.append('NONE')

        if self.ability == 'NO_ABILITY':
            self.ability = 'NONE'

    def __str__(self):
        s = engine_format % ('%i', '%i', '%i',
                             self.level, self.species, self.item,
                             self.moves[0], self.moves[1], self.moves[2], self.moves[3],
                             self.ability,
                             self.ivs['hp'], self.ivs['atk'], self.ivs['def'], self.ivs['spe'], self.ivs['spa'],
                             self.ivs['spd'],
                             self.evs['hp'], self.evs['atk'], self.evs['def'], self.evs['spe'], self.evs['spa'],
                             self.evs['spd'],
                             self.nature, self.shiny, '%s', format_nickname(self.nickname))
        return s


def parse(data: str = '') -> List[Team]:
    data = data.strip()
    if data == '':
        return list()

    teams = list()
    lines = data.splitlines()

    multi_teams = data.count('===') > 2

    if not multi_teams:
        teams.append(Team())

    found_mon = False
    for line in lines:
        if found_mon:
            if line.startswith('Ability: '):
                teams[-1].mons[-1].ability = sanitize(line[9:].strip().upper(), IRREGULAR_ABILITIES)
            elif 'Nature' in line:
                teams[-1].mons[-1].nature = line.split(' ')[0].strip().upper()
            elif line.startswith('Level: '):
                teams[-1].mons[-1].level = int(line[8:])
            elif line.startswith('Shiny: '):
                teams[-1].mons[-1].shiny = line[7:] == 'Yes'
            elif line.startswith('EVs: '):
                teams[-1].mons[-1].ev_temp = line[5:].lower().split(' / ')
            elif line.startswith('IVs: '):
                teams[-1].mons[-1].iv_temp = line[5:].lower().split(' / ')
            elif line.startswith('- '):  # moves
                teams[-1].mons[-1].moves.append(sanitize(line[2:].upper(), IRREGULAR_MOVES))
            elif line == '':
                found_mon = False
        else:
            if line.startswith('===') and line.endswith('==='):
                md = line.replace('===', '').strip()
                if line.count('[') == 2:
                    teams.append(Team(md[:md.rindex('[')].strip(), md[md.rindex('[')+1:md.rindex(']')].strip()))
                else:
                    teams.append(Team(md))
                continue

            if line != '':
                arr = line.split(' @ ')
                arr = [arr[idx].strip() for idx in range(len(arr))]

                if '(' in arr[0] and ')' in arr[0]:
                    species = arr[0][arr[0].index('(') + 1:arr[0].index(')')].upper().strip()
                    nickname = arr[0][:arr[0].index('(')].strip()
                else:
                    species = arr[0].upper()
                    nickname = ''

                found_mon = True
                teams[-1].mons.append(Mon(species, nickname))
                if len(arr) == 2:
                    teams[-1].mons[-1].item = sanitize(arr[1].upper(), IRREGULAR_ITEMS)
                else:
                    continue

    return teams


def process(teams: List[Team]):
    for idx in range(len(teams)):
        for sub_idx in range(len(teams[idx].mons)):
            mon = teams[idx].mons[sub_idx]
            mon.verify()


def determine_rules(mons: List[Mon]) -> List[Rule]:
    rules = list()
    for mon in mons:
        if len(mon.moves) != 0:
            if Rule.TRAINER_DATA_TYPE_MOVES not in rules:
                rules.append(Rule.TRAINER_DATA_TYPE_MOVES)
        if mon.item != 'NONE':
            if Rule.TRAINER_DATA_TYPE_ITEMS not in rules:
                rules.append(Rule.TRAINER_DATA_TYPE_ITEMS)
        if mon.nature != '':
            if Rule.TRAINER_DATA_TYPE_NATURE_SET not in rules:
                rules.append(Rule.TRAINER_DATA_TYPE_NATURE_SET)
        if mon.shiny:
            if Rule.TRAINER_DATA_TYPE_SHINY_LOCK not in rules:
                rules.append(Rule.TRAINER_DATA_TYPE_SHINY_LOCK)
        if mon.ability != 'NONE':
            if Rule.TRAINER_DATA_TYPE_ABILITY not in rules:
                rules.append(Rule.TRAINER_DATA_TYPE_ABILITY)
        if mon.nickname != '':
            if Rule.TRAINER_DATA_TYPE_ADDITIONAL_FLAGS not in rules:
                rules.append(Rule.TRAINER_DATA_TYPE_ADDITIONAL_FLAGS)
        if mon.ivs != default_ivs or mon.evs != default_evs:
            if Rule.TRAINER_DATA_TYPE_IV_EV_SET not in rules:
                rules.append(Rule.TRAINER_DATA_TYPE_IV_EV_SET)

    return rules


def convert(teams: List[Team], whole_trainer: bool = False) -> str:
    output = ''
    for team in teams:
        output += convert_team(team, whole_trainer)

    return output


def convert_team(team: Team, whole_trainer: bool = False) -> str:
    mons = team.mons
    if len(mons) == 0:
        return 'No valid Smogon-format mons detected\n'

    rules = determine_rules(mons)
    output = ''
    if whole_trainer:
        trainermontype = ''
        for rule in rules:
            trainermontype += rule.name + ' | '
        trainermontype += '0'
        output += trainer_format % (team.id, team.name,trainermontype, len(mons))

    for idx in range(len(mons)):
        mon = mons[idx]
        lines = str(mon).splitlines(keepends=True)
        new_lines = list()
        for line in lines:
            s = line.strip()
            if not ((s.startswith('item') and Rule.TRAINER_DATA_TYPE_ITEMS not in rules)
                    or (s.startswith('move') and Rule.TRAINER_DATA_TYPE_MOVES not in rules)
                    or (s.startswith('ability') and not s.startswith('abilityslot') and Rule.TRAINER_DATA_TYPE_ABILITY not in rules)
                    or (s.startswith('setivs') and Rule.TRAINER_DATA_TYPE_IV_EV_SET not in rules)
                    or (s.startswith('setevs') and Rule.TRAINER_DATA_TYPE_IV_EV_SET not in rules)
                    or (s.startswith('nature') and Rule.TRAINER_DATA_TYPE_NATURE_SET not in rules)
                    or (s.startswith('shinylock') and Rule.TRAINER_DATA_TYPE_SHINY_LOCK not in rules)
                    or (s.startswith('additionalflags') and Rule.TRAINER_DATA_TYPE_ADDITIONAL_FLAGS not in rules)
                    or (s.startswith('nickname') and mon.nickname == '')):
                if not whole_trainer:
                    new_lines.append(line[2:])
                else:
                    new_lines.append(line)
        if mon.ivs['hp'] == mon.ivs['atk'] == mon.ivs['def'] == mon.ivs['spe'] == mon.ivs['spa'] == mon.ivs['spd']:
            iv = mon.ivs['hp'] * 255 / 31
        else:
            iv = 250
        if mon.nickname != '':
            nickname_flag = 'TRAINER_DATA_EXTRA_TYPE_NICKNAME'
        else:
            nickname_flag = '0'

        data = ''.join(new_lines)

        if Rule.TRAINER_DATA_TYPE_ADDITIONAL_FLAGS in rules:
            data = data % (idx, iv, 0, nickname_flag)
        else:
            data = data % (idx, iv, 0)
        output += data + '\n'

    output = output[:-1]
    if whole_trainer:
        output += '\tendparty\n\n'
    return output


def main(argv: List[str] = None) -> None:
    parser = argparse.ArgumentParser(
        description='showdownConv: Converts Showdown/Smogon trainer format to hg-engine trainer format')

    parser.add_argument('-i', '--input', type=Path,
                        help='input file containing Smogon-format team(s) - must use if -ci is not specified. ')
    parser.add_argument('-ci', '--clipboard-in', action='store_true',
                        help='reads Smogon format team(s) from clipboard instead of input file - must use if -i is not specified')
    parser.add_argument('-o', '--output', type=Path,
                        help='output file')
    parser.add_argument('-co', '--clipboard-out', action='store_true',
                        help='writes Smogon format team(s) to clipboard instead of output file')
    parser.add_argument('--whole-trainer', action='store_true',
                        help='writes the data for the entire trainer, not just the party')
    parser.add_argument('-s', '--silent', action='store_true',
                        help='silences output except for errors and result output if -o or -co are not used')
    # parser.add_argument('--generate-assets', action='store_true',
    #                     help='generates translation dict needed to get the correct names for hg-engine\n')

    args = parser.parse_args(argv)

    input_file = args.input
    output_file = args.output
    clipboard_in = args.clipboard_in
    clipboard_out = args.clipboard_out
    silent = args.silent
    whole_trainer = args.whole_trainer
    generate_assets_flag = args.generate_assets

    if generate_assets_flag:
        generate_assets()
        return

    if input_file is None and clipboard_in is False:
        parser.error('need to specify an input type (-i or -ci)')

    if input_file is not None and clipboard_in:
        parser.error('specify either -i or -ci, not both')
    if output_file is not None and clipboard_out:
        parser.error('specify either -o or -co, not both')

    if input_file is not None and clipboard_in is False:
        with open(input_file, 'r') as f:
            data = f.read()
    elif input_file is None and clipboard_in:
        data = pc.paste()

    teams = parse(data)
    process(teams)
    output = convert(teams, whole_trainer)

    if output == 'No valid Smogon-format mons detected':
        parser.error(output)

    if not silent:
        print('Conversion success. Output can be found ', end='')

    if output_file is not None and clipboard_out is False:  # write to file
        if not silent:
            print('at: %s' % output_file)
        with open(output_file, 'w') as f:
            f.write(output)
    elif output_file is None and clipboard_out:  # copy to clipboard
        if not silent:
            print('in your clipboard.')
        pc.copy(output)
    elif output_file is None and clipboard_out is False:  # cmd print output (default mode)
        if not silent:
            print('below:\n')
        print(output)


def generate_assets():
    pass


if __name__ == '__main__':
    main()
