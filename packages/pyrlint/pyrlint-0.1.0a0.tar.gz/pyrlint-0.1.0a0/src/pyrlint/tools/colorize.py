from pyrlint.tokenizer import RTokenizer, RTokenType


def colorize(statements):
    result_str = ''
    rt = RTokenizer(statements)
    while True:
        t = rt.next_token()
        if not t:
            break
        if t.type == RTokenType.ID:
            result_str += f'\033[34m' + t.content + f'\033[0m'
        elif t.type == RTokenType.OPER:
            result_str += f'\033[33m' + t.content + f'\033[0m'
        elif t.type == RTokenType.STRING:
            result_str += f'\033[36m' + t.content + f'\033[0m'
        elif t.type == RTokenType.UOPER:
            result_str += f'\033[35m' + t.content + f'\033[0m'
        elif t.type == RTokenType.NUMBER:
            result_str += f'\033[32m' + t.content + f'\033[0m'
        elif t.type == RTokenType.COMMENT:
            result_str += f'\033[31m' + t.content + f'\033[0m'
        elif t.is_comma or t.is_whitespace or t.is_right_bracket or t.is_left_bracket:
            result_str += t.content
        else:
            result_str += f'<{t}>' + t.content
    return result_str


def colorize_main():
    import sys
    file_names = sys.argv[1:]
    for fn in file_names:
        if len(file_names) > 1:
            print('** File:', fn)
        with open(fn, encoding='utf8') as  fi:
            result = colorize(fi.read())
        print(result)
