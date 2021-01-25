import re
import time
from typing import List

arrow = '->'
pointer = '.'


def get_left_symbol(string: str) -> str:
    string_split = string.split(arrow)
    return string_split[0]


def swap(string: str, i: int, j: int) -> str:
    string = list(string)
    string[i], string[j] = string[j], string[i]
    return ''.join(string)


def extract_indexes(statement):
    m = re.search(r'\[(.+?)]', statement)
    found = m.group(1)
    found = found.split(', ')
    return found


def move_pointer(string: str, new_index: int) -> str:
    pointer_index = string.index(pointer)
    statement = swap(string, pointer_index, pointer_index + 1)
    border = (1 + len(extract_indexes(statement)[1])) * -1
    statement = statement[:border] + str(new_index) + ']'
    return statement


def find_parents(arr: List, symbol: str, index: str) -> List:
    p = re.compile(fr'^.*\.{symbol}+.*$')
    return list(set([s for s in arr if p.match(s) and int(re.search(r'\[(.+?)]', s).group(1).split(', ')[1]) == index]))


def read(read_mode, to_read, working_arr, done_arr):
    read_statement = to_read.pop(0)

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

    return read_mode, to_read, working_arr, done_arr


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
    final_statement = init_statement + f'. [0, {len(word)}]'
    i = 0
    j = 0
    max_i = 0
    current = init_statement + f' [{i}, {j}]'
    current = current.split(arrow)
    current = current[0] + arrow + pointer + current[1]

    read_mode = False
    successful = False

    word_to_indexes = {}
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
                        read_mode, to_read, working_arr, done_arr = read(read_mode, to_read, working_arr, done_arr)
                    current = working_arr[0]

                except Exception:
                    read_mode, to_read, working_arr, done_arr = read(read_mode, to_read, working_arr, done_arr)
                    read_mode = True
                    current = working_arr[0]

                continue
            if symbol in rules:
                for el in rules[symbol]:
                    statement = symbol + arrow + pointer + el + f' [{i}, {i}]'
                    if statement in done_arr or statement in working_arr or statement in to_read:
                        continue
                    working_arr.append(statement)
                    word_to_indexes.update({statement: (i, i)})
                    print(statement + '  przewidywanie')

                done_arr.append(current)
                working_arr.remove(current)
            if symbol not in rules and symbol not in word:
                done_arr.append(current)
                working_arr.remove(current)
        else:

            symbol = get_left_symbol(current)
            statement_x, _ = word_to_indexes.get(current)
            parents = find_parents(done_arr, symbol, statement_x)

            working_arr.remove(current)
            done_arr.append(current)
            for p in parents:
                statement = move_pointer(p, i)
                if statement not in working_arr and statement not in done_arr and statement not in to_read:
                    working_arr.append(statement)
                    if statement == final_statement:
                        print(statement + '  uzupelnienie' + ' <----------- słowo należy do języka')
                        successful = True
                    else:
                        print(statement + '  uzupelnienie')

                    found = extract_indexes(statement)
                    word_to_indexes.update({statement: (int(found[0]), int(found[1]))})

        if read_mode:
            try:
                found = extract_indexes(current)
                if symbol != word[int(found[1])]:
                    working_arr.remove(current)
                    done_arr.append(current)
                    if len(to_read) == 0:
                        read_mode = False

                else:
                    done_arr.append(current)
                    working_arr.remove(current)
                    i = int(found[1]) + 1
                    if i > max_i:
                        print(f'\ni={i}')
                        max_i = i
                    statement = swap(current, current.index(pointer), current.index(pointer) + 1)
                    found = extract_indexes(statement)
                    border = (1 + len(found[1])) * -1
                    statement = statement[:border] + str(i) + ']'
                    print(statement + '  wczytanie')
                    found = extract_indexes(statement)
                    word_to_indexes.update({statement: (int(found[0]), int(found[1]))})
                    if len(to_read) == 0:
                        read_mode = False
                    if statement not in working_arr and statement not in done_arr and statement not in to_read:
                        working_arr.append(statement)
            except Exception:
                break

        try:
            if read_mode and len(to_read) > 0:
                read_mode, to_read, working_arr, done_arr = read(read_mode, to_read, working_arr, done_arr)
            current = working_arr[0]

        except Exception:
            try:
                read_statement = to_read.pop(0)
            except Exception:
                break
            if read_statement not in working_arr and read_statement not in done_arr and read_statement not in to_read:
                working_arr.insert(0, read_statement)

            read_mode = True
            current = working_arr[0]

    if not successful:
        print("\nLooks like there is no statement to proceed")
        print("Please check the rules and the word")
        print("If they are valid, the most likely the word does not belong to this language")
        print("It is highly recommended to check all the output because the bug is not excluded")


if __name__ == '__main__':
    main()
