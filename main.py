import re
import time
from typing import List

arrow = '->'
pointer = '.'


def get_left_symbol(string: str):
    string_split = string.split(arrow)
    return string_split[0]


def move_pointer(string: str, new_index: int):
    current_split = string.split(arrow)
    if current_split[1][0] == pointer:
        current_split[1] = current_split[1]
    right_side_split = current_split[1].split(pointer)
    symbol = right_side_split[1][0]
    statement = current_split[0] + arrow + right_side_split[0] \
        .replace(pointer, '') + symbol + pointer + right_side_split[1][1:-2] + f'{new_index}]'
    return statement


def find_parents(arr: List, symbol: str, index: str):
    p = re.compile(fr'^.*\.{symbol}+.*$')
    return list(set([s for s in arr if p.match(s) and s[-2] == index]))


# noinspection PyBroadException
def main() -> None:
    init_statement = ''
    rules = {}

    print('Enter the rules. The first rule should be init like S\' -> S')
    while True:
        tmp_input = input().replace(' ', '')

        if tmp_input == '':
            break
        split_arr = tmp_input.split(arrow)
        key = split_arr[0]
        if key not in rules:
            rules = {**rules, **{key: []}}
        if '|' not in split_arr[1]:
            if init_statement == '':
                init_statement = tmp_input
            rules.get(key).append(split_arr[1])
        else:
            for rule in split_arr[1].split('|'):
                if init_statement == '':
                    init_statement = f'{key}->{rule}'
                rules.get(key).append(rule)

    # rules = {'E': ['T', 'E+T'], 'T': ['P', 'T*P'], 'P': 'a'}
    print('OK. Enter the word.')
    word = input()
    # word = 'a+a*a'
    print(word)

    i = 0
    j = 0
    max_i = 0
    current = init_statement + f' [{i}, {j}]'
    current = current.split(arrow)
    current = current[0] + arrow + pointer + current[1]

    read_mode = False

    to_read = []
    working_arr = []
    done_arr = []
    working_arr.append(current)
    print(working_arr[0] + '  sytuacja startowa')
    while True:
        current_split = current.split(arrow)
        right_side = current_split[1]
        if right_side[right_side.index(pointer) + 1] != ' ':
            symbol = right_side[right_side.index(pointer) + 1]
            if not read_mode and symbol in word:
                to_read.append(current)
                working_arr.remove(current)

                try:
                    if read_mode and len(to_read) > 0:
                        read_statement = to_read.pop(0)
                        if len(to_read) == 0:
                            read_mode = False
                        if read_statement not in working_arr and read_statement not in done_arr and read_statement not in to_read:
                            working_arr.insert(0, read_statement)
                        else:
                            done_arr.append(read_statement)
                            while True:
                                if len(to_read) == 0:
                                    read_mode = False
                                    break
                                else:
                                    read_statement = to_read.pop(0)

                                if read_statement not in working_arr and read_statement not in done_arr and read_statement not in to_read:
                                    working_arr.insert(0, read_statement)
                                    break
                                else:
                                    done_arr.append(read_statement)
                    else:
                        read_mode = False
                    current = working_arr[0]

                except Exception:
                    read_statement = to_read.pop(0)
                    if len(to_read) == 0:
                        read_mode = False
                    if read_statement not in working_arr and read_statement not in done_arr and read_statement not in to_read:
                        working_arr.insert(0, read_statement)
                    else:
                        done_arr.append(read_statement)
                        while True:
                            if len(to_read) == 0:
                                read_mode = False
                                break
                            else:
                                read_statement = to_read.pop(0)

                            if read_statement not in working_arr and read_statement not in done_arr and read_statement not in to_read:
                                working_arr.insert(0, read_statement)
                                break
                            else:
                                done_arr.append(read_statement)

                    read_mode = True
                    current = working_arr[0]
                continue
            if symbol in rules:
                for el in rules[symbol]:
                    statement = symbol + arrow + pointer + el + f' [{i}, {i}]'
                    if statement in done_arr or statement in working_arr or statement in to_read:
                        continue
                    working_arr.append(statement)
                    print(statement + '  przewidywanie')

                    time.sleep(0.2)
                done_arr.append(current)
                working_arr.remove(current)
            if symbol not in rules and symbol not in word:
                done_arr.append(current)
                working_arr.remove(current)
        else:

            symbol = get_left_symbol(current)
            parents = find_parents(done_arr, symbol, current[-5])

            working_arr.remove(current)
            done_arr.append(current)
            for p in parents:
                statement = move_pointer(p, i)
                if statement not in working_arr and statement not in done_arr and statement not in to_read:
                    working_arr.append(statement)
                    print(statement + '  uzupelnienie')

        time.sleep(0.1)
        if read_mode:
            try:
                if symbol != word[int(current[-2])]:
                    working_arr.remove(current)
                    done_arr.append(current)

                else:
                    done_arr.append(current)
                    working_arr.remove(current)
                    right_side_split = current_split[1].split(symbol)
                    i = int(current[-2]) + 1
                    if i > max_i:
                        print(f'\ni={i}')
                        max_i = i
                    statement = current_split[0] + arrow + right_side_split[0] \
                        .replace(pointer, '') + symbol + pointer + ''.join(right_side_split[1:-1]) + right_side_split[-1][:-2] + str(i) + ']'
                    print(statement + '  wczytanie')
                    if statement not in working_arr and statement not in done_arr and statement not in to_read:
                        working_arr.append(statement)
            except Exception:
                break

        try:
            if read_mode and len(to_read) > 0:
                read_statement = to_read.pop(0)
                if len(to_read) == 0:
                    read_mode = False
                if read_statement not in working_arr and read_statement not in done_arr and read_statement not in to_read:
                    working_arr.insert(0, read_statement)
                else:
                    done_arr.append(read_statement)
                    while True:
                        if len(to_read) == 0:
                            read_mode = False
                            break
                        else:
                            read_statement = to_read.pop(0)

                        if read_statement not in working_arr and read_statement not in done_arr and read_statement not in to_read:
                            working_arr.insert(0, read_statement)
                            break
                        else:
                            done_arr.append(read_statement)

            else:
                read_mode = False
            current = working_arr[0]

        except Exception:
            read_statement = to_read.pop(0)
            if len(to_read) == 0:
                read_mode = False
            if read_statement not in working_arr and read_statement not in done_arr and read_statement not in to_read:
                working_arr.insert(0, read_statement)

            read_mode = True
            current = working_arr[0]


if __name__ == '__main__':
    main()
