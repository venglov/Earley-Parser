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
    init_statement = 'S\'' + arrow + 'E'
    rules = {}

    print('Enter the rules.')
    while True:
        tmp_input = input()
        if tmp_input == 'done':
            break
        split_arr = tmp_input.split(arrow)
        key = split_arr[0]
        if key not in rules:
            rules = {**rules, **{key: []}}
        rules.get(key).append(split_arr[1])
    # rules = {'E': ['T', 'E+T'], 'T': ['P', 'T*P'], 'P': 'a'}
    print('OK. Enter the word.')
    word = input()
    # word = 'a+a*a'
    print(word)

    i = 0
    j = 0
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
                    current = working_arr[0]

                except Exception:
                    working_arr.append(to_read.pop(0))

                    read_mode = True
                    current = working_arr[0]
                continue
            if symbol in rules:
                for el in rules[symbol]:
                    statement = symbol + arrow + pointer + el + f' [{i}, {i}]'
                    if statement in done_arr or statement in working_arr:
                        continue
                    working_arr.append(statement)
                    print(statement + '  przewidywanie')

                    time.sleep(0.2)
                done_arr.append(current)
                working_arr.remove(current)
        else:

            symbol = get_left_symbol(current)
            parents = find_parents(done_arr, symbol, current[-5])

            working_arr.remove(current)
            done_arr.append(current)
            for p in parents:
                statement = move_pointer(p, i)
                working_arr.append(statement)
                print(statement + '  uzupelnienie')

        time.sleep(0.1)
        if read_mode:
            read_mode = False
            try:
                if symbol != word[i]:
                    working_arr.remove(current)
                    done_arr.append(current)

                else:
                    done_arr.append(current)
                    working_arr.remove(current)
                    right_side_split = current_split[1].split(symbol)
                    i = i + 1
                    print(f'\ni={i}')
                    statement = current_split[0] + arrow + right_side_split[0] \
                        .replace(pointer, '') + symbol + pointer + right_side_split[1][:-2] + str(i) + ']'
                    print(statement + '  wczytanie')
                    working_arr.append(statement)
            except Exception:
                break

        try:
            current = working_arr[0]

        except Exception:
            working_arr.append(to_read.pop(0))

            read_mode = True
            current = working_arr[0]


if __name__ == '__main__':
    main()
