import sys

interactive_mode = True
if len(sys.argv) > 1:
    interactive_mode = False


data_stack = []
list_stack = []
memory_stack = []
stash = []

std_dict = {
    ':': 'd_define()',
    'define': 'd_define_postfix(stack)',
    'set': 'd_set(stack)',
    '.': 'd_do(stack)',
    '+': 'd_add(stack)',
    '*': 'd_multiply(stack)',
    '-': 'd_subtract(stack)',
    '/': 'd_divide(stack)',
    '%': 'd_modulo(stack)',
    'floor': 'd_floor(stack)',
    'ceiling': 'd_ceiling(stack)',
    'round': 'd_round(stack)',
    'round_to': 'd_round_to(stack)',
    'true': 'd_true(stack)',
    'false': 'd_false(stack)',
    'max': 'd_max(stack)',
    'min': 'd_min(stack)',
    '>': 'd_greater_than(stack)',
    '<': 'd_less_than(stack)',
    '=': 'd_equals(stack)',
    'if': 'd_if(stack)',
    'not': 'd_not(stack)',
    'drop': 'd_drop(stack)',
    'copy': 'd_copy(stack)',
    'swap': 'd_swap(stack)',
    'clear': 'd_clear(stack)',
    'index': 'd_index(stack)',
    'slice': 'd_slice(stack)',
    'ascending': 'd_ascending(stack)',
    'descending': 'd_descending(stack)',
    '[': 'd_list_level_increment()',
    ']': 'd_list_level_decrement()',
    '@@': 'd_make_list_all(stack)',
    '@': 'd_make_list_some(stack)',
    'length': 'd_length(stack)',
    'depth': 'd_depth(stack)',
    "'": 'd_quote(stack)',
    'join': 'd_join(stack)',
    'flatten': 'd_flatten(stack)',
    'flat': 'd_flat(stack)',
    'map': 'd_map(stack)',
    'filter': 'd_filter(stack)',
    'reduce': 'd_reduce(stack)',
    'times': 'd_times(stack)',
    '?': 'd_if(stack)',
    'print': 'd_print(stack)',
    'show': 'd_show()',
    'stash': 'd_stash(stack)',
    'unstash': 'd_unstash(stack)',
    'unstash_all': 'd_unstash_all(stack)',
    'peek_stash': 'd_peek_stash(stack)',
    'words': 'd_words()',
    'see': 'd_see(stack)',
    'remember': 'd_remember()',
    'undo': 'd_undo()',
    'record': 'd_record()',
    'stop': 'd_stop(stack)',
    'input': 'd_input(stack)',
    'class': 'd_class(stack)',
    'to_int': 'd_to_int(stack)',
    'exit': 'exit()'
}

user_dict = {
    'numbers': [2, 5, 88, 1, 3, -1, -99, 292, 0, 52, 8, 31],
    'filter_split': ['stash', 'copy', 'peek_stash', 'filter', 'swap', 'unstash', '[', 'not', ']', 'join', 'filter'],
    'range': ['stash', 'copy', 'unstash', 'swap', '-', 1, '-', '[', 'copy', 1, '+', ']', 'swap', 'times', '@']

}

compile_context = False
next_definition = []

list_level = 0
list_builder = []

string_context = False
string_builder = ""

record_context = False
recording = []

if_branch = False
else_branch = False
discard_invalid_branch = False
branch_tokens = []

def d_define():
    global compile_context
    compile_context = True

def d_define_postfix(stack):
    name = stack.pop()
    definition = stack.pop()
    name = name[0]

    user_dict[name] = definition

def d_set(stack):
    name = stack.pop()
    definition = stack.pop()
    name = name[0]

    if is_list(definition):
        lst = ['[']
        for word in definition:
            lst.append(word)
        lst.append(']')
        definition = lst
    else:
        definition = [ definition ]
    user_dict[name] = definition

def d_do(stack):
    if len(stack) > 0:
        a = stack.pop()
        if is_list(a):
            parse(a, stack)
        else:
            stack.append(a)
    else:
        print("(!) No items on stack. '.' takes 1 argument")
    

def d_add(stack):
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        if a_and_b_are_numbers(a, b):
            stack.append(a + b)
        else:
            
            stack.append(str(b) + str(a))
    else:
        print("(!) Not enough items on stack. '+' takes 2 parameters.")

def d_multiply(stack):
    if len(stack) >= 2:
        if a_and_b_are_numbers(stack[-1], stack[-2]):
            stack.append(stack.pop() * stack.pop())
    else:
        print("(!) Not enough items on stack. '*' takes 2 parameters.")

def d_subtract(stack):
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        if a_and_b_are_numbers(a, b):
            stack.append(b - a)
    else:
        print("(!) Not enough items on stack. '-' takes 2 parameters.")

def d_divide(stack):
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        if a == 0:
            stack.append(b)
            stack.append(a)
            print("Cannot divide by zero.")
        elif a_and_b_are_numbers(a, b):
            stack.append(b / a)
        else:
            stack.append(b)
            stack.append(a)
            print("Can only divide integers.")
    else: 
        print("(!) Not enough items on stack. '/' takes 2 parameters.")

def d_modulo(stack):
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        if a == 0:
            stack.append(b)
            stack.append(a)
            print("Cannot divide by zero.")
        elif a_and_b_are_numbers(a, b):
            stack.append(b % a)
        else:
            stack.append(b)
            stack.append(a)
            print("Can only divide integers.")
    else: 
        print("(!) Not enough items on stack. '/' takes 2 parameters.")

def d_floor(stack):
    if is_integer(stack[-1]):
        pass
    elif is_float(stack[-1]):
        stack.append(int(stack.pop()))

def d_ceiling(stack):
    if is_integer(stack[-1]):
        pass
    elif is_float(stack[-1]):
        stack.append(int(stack.pop()) + 1)


def d_round(stack):
    if is_number(stack[-1]):
        a = stack.pop()
        a_int = int(a)
        if a - a_int < 0.5:
            stack.append(a_int)
        else:
            stack.append(a_int + 1)

def d_round_to(stack):
    if len(stack) > 1:
        if a_and_b_are_numbers(stack[-1], stack[-2]):
            decimals = stack.pop()
            number = stack.pop()
            stack.append(round(number, decimals))

def d_true(stack):
    stack.append(-1)
def d_false(stack):
    stack.append(0)

def d_max(stack):
    if len(stack) >= 2:
        if a_and_b_are_numbers(stack[-1], stack[-2]):
            stack.append(max(stack.pop(), stack.pop()))
        else:
            print("(!) Can't call 'max' on non-number")
    else:
        print("(!) Not enough items on stack. 'max' takes 2 parameters.")

def d_min(stack):
    if len(stack) >= 2:
        if a_and_b_are_numbers(stack[-1], stack[-2]):
            stack.append(min(stack.pop(), stack.pop()))
        else:
            print("(!) Can't call 'min' on non-number.")
    else:
        print("(!) Not enough items on stack. 'min' takes 2 parameters.")

def d_greater_than(stack):
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        if a_and_b_are_numbers(a, b):
            if b > a:
                stack.append(-1)
            else:
                stack.append(0)
        else:
            stack.append(b)
            stack.append(a)
            print("(!) Can't call '>' on non-int.")
    else:
        print("(!) Not enough items on stack. '>' takes 2 parameters.")

def d_less_than(stack):
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        if a_and_b_are_numbers(a, b):
            if b < a:
                stack.append(-1)
            else:
                stack.append(0)
        else:
            stack.append(b)
            stack.append(a)
            print("(!) Can't call '<' on non-int.")
    else:
        print("(!) Not enough items on stack. '<' takes 2 parameters.")

def d_equals(stack):
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        if a == b:
            stack.append(-1)
        else:
            stack.append(0)
    else:
        print("(!) Not enough times on stack. '=' takes 2 parameters.")

def d_swap(stack):
    if len(stack) > 1:
        a = stack.pop()
        b = stack.pop()
        stack.append(a)
        stack.append(b)
    else:
        print("(!) Not enough items on stack. 'swap' takes 2 parameters.")

def d_clear(stack):
    while stack:
        stack.pop()


def d_map(stack):
    global list_stack
    function = stack.pop()
    iterable_list = stack.pop()

    if is_list(iterable_list):
        new_tokens = []
        for item in iterable_list:
            new_tokens.append(item)
            for word in function:
                new_tokens.append(word)
        parse(new_tokens, list_stack)
        if list_stack != []:
            parse(['['], data_stack)
            parse(list_stack, data_stack)
            parse(']', data_stack)
            list_stack = []
    else:
        print("(!) 'map' takes a List as its first argument. Got: "
            + str(iterable_list)
        )

def d_filter(stack):
    global list_stack
    function = stack.pop()
    iterable_list = stack.pop()

    if is_list(iterable_list):
        new_tokens = []
        for item in iterable_list:
            new_tokens.append(item)
            new_tokens.append('copy')
            for word in function:
                new_tokens.append(word)
            new_tokens.append('if')
            new_tokens.append('else')
            new_tokens.append('drop')
            new_tokens.append('then')
        parse(new_tokens, list_stack)
        if list_stack != []:
            parse(['['], data_stack)
            parse(list_stack, data_stack)
            parse(']', data_stack)
            list_stack = []
    else:
        print("(!) 'filter' takes a List as its first argument. Got: "
            + str(iterable_list)
        )

def d_reduce(stack):
    global list_stack
    function = stack.pop()
    iterable_list = stack.pop()
    if is_list(iterable_list):
        head = iterable_list[0]
        tail = iterable_list[1:]
        new_tokens = [head]
        for item in tail:
            new_tokens.append(item)
            for word in function:
                new_tokens.append(word)
        parse(new_tokens, list_stack)
        if list_stack != []:
            parse(['['], data_stack)
            parse(list_stack, data_stack)
            parse(']', data_stack)
            list_stack = []
    else:
        print("(!) 'filter' takes a List as its first argument. Got: "
            + str(iterable_list)
        )

def d_times(stack):
    # 'function number times
    if len(stack) > 1:
        iterations = stack.pop()
        function = stack.pop()

        if is_list(function) and is_integer(iterations):
            for i in range(iterations):
                parse(function, stack)
                    

def d_if(stack):
    global if_branch
    global else_branch
    global discard_invalid_branch
    condition = stack.pop()
    if condition:
        if_branch = True
    else:
        else_branch = True
        discard_invalid_branch = True

def d_stash(stack):
    stash.append(stack.pop())

def d_unstash(stack):
    stack.append(stash.pop())

def d_unstash_all(stack):
    while stash:
        stack.append(stash.pop())

def d_peek_stash(stack):
    stack.append(stash[-1])

def d_not(stack):
    a = stack.pop()
    if a:
        stack.append(0)
    else:
        stack.append(-1)

def d_drop(stack):
    stack.pop()

def d_copy(stack):
    if len(stack) > 0:
        stack.append(stack[-1])
    else:
        print("(!) Not enough items on stack. 'copy' takes 1 parameter.")

def d_string(stack):
    global string_context
    string_context = not string_context


def d_index(stack):
    index = stack.pop()
    lst = stack[-1]

    index_string = ''
    if is_list(index):
        for num in index:
            index_string += '[' + str(num) + ']'
        get_index = str(lst) + index_string
        stack.append(eval(get_index))

def d_slice(stack):
    if len(stack) > 1:
        if a_and_b_are_numbers(stack[-1], stack[-2]) and is_list(stack[-3]):
            end = stack.pop()
            begin = stack.pop()
            lst = stack.pop()
            stack.append(lst[begin:end])

def d_ascending(stack):
    if len(stack) > 0:
        if is_list(stack[-1]):
            a = stack.pop()
            stack.append(sorted(a))

def d_descending(stack):
    if len(stack) > 0:
        if is_list(stack[-1]):
            a = stack.pop()
            stack.append(sorted(a, reverse=True))

def d_list_level_increment():
    global list_level
    list_level += 1

def d_list_level_decrement():
    global list_level
    list_level -= 1

def d_make_list_all(stack):
    new_list = ['[']
    for item in stack:
        new_list.append(item)
    new_list.append(']')
    while stack:
        stack.pop()
    parse(new_list, stack)

def d_make_list_some(stack):
    if len(stack) > 0:
        new_list = ['[']
        index_of_last_list = -1
        for i in range(len(stack)):
            item = stack[i]
            if is_list(item):
                index_of_last_list = i
        for item in stack[index_of_last_list+1:]:
            new_list.append(item)
        new_list.append(']')
        while len(stack) > index_of_last_list + 1:
            stack.pop()
        parse(new_list, stack)
    else:
        print("(!) Empty stack. '@' takes at least 1 argument.")

def d_length(stack):
    if len(stack) > 0:
        if is_list(stack[-1]):
            stack.append(len(stack[-1]))
        else:
            print("'length' takes a List as its argument.")
    else:
        print("(!) Empty stack. 'length' takes 1 List argument.")

def d_depth(stack):
    stack.append(len(stack))


def d_quote(stack):
    if len(stack) > 0:
        a = stack.pop()
        if is_list(a):
            stack.append(a)
        else:
            stack.append([a])
    else:
        print("(!) Not enough items on stack. '\'' takes 1 argument.")

def d_join(stack):
    if len(stack) > 1:
        a = stack.pop()
        b = stack.pop()
        if is_list(a) and is_list(b):
            for item in a:
                b.append(item)
            stack.append(b)
        else:
            stack.append(b)
            stack.append(a)
            print("(!) Not enough items on stack. 'join' takes 2 Lists as arguments.")

def d_flatten(stack):
    # Doesn't work yet if other functions are called right after
    flat_list = []
    for sublist in stack:
        for item in sublist:
            flat_list.append(item)
    
    while stack:
        stack.pop()
    parse(flat_list, stack)

def d_flat(stack):
    if len(stack) > 0:
        a = stack.pop()
        if is_list(a):
            for item in a:
                stack.append(item)
        else:
            parse(a, stack)
    else:
        print("(!) No items on stack. 'flat' takes 1 argument")


def d_print(stack):
    if len(stack) > 0:
        print(stack.pop())
    else:
        print("(!) Stack is empty.")

def d_show():
    print(data_stack)

def d_words():
    for word in user_dict:
        print(str(word) + ': ' + str(user_dict[word]))

def d_see(stack):
    a = stack.pop()
    for word in a:
        print(user_dict[word])

def d_remember():
    print(str(memory_stack))

def d_undo():
    global data_stack
    memory_stack.pop()
    data_stack = memory_stack.pop()

def d_record():
    global record_context
    record_context = True

def d_stop(stack):
    global record_context
    global recording
    record_context = False
    stack.append(recording[:-1])
    recording = []

def d_input(stack):
    a = input('')
    stack.append(a)

def d_class(stack):
    class_name = stack.pop()
    s = '\n'.join([
        "class " + str(class_name) + ":",
        "\tdef __init__(self, name, age):",
        "\t\tself.name = name",
        "\t\tself.age = age",
    ])
    
    eval(s)


def d_to_int(stack):
    a = stack.pop()
    if is_integer(a) or is_float(a):
        stack.append(int(float(a)))
    else:
        stack.append(a)

def is_integer(n):
    try:
        float(n)
    except (TypeError, ValueError):
        return False
    else:
        return float(n).is_integer()

def is_float(n):
    try:
        a = float(n)
    except (TypeError, ValueError):
        return False
    else:
        return True

def is_number(n):
    if is_integer(n) or is_float(n):
        return True
    else:
        return False

def is_list(n):
    if isinstance(n, list):
        return True
    else:
        return False

def a_and_b_are_numbers(a, b):
    if is_number(a) and is_number(b):
        return True
    else:
        return False

def is_compilable_token(token):
    # token in std_dict.keys() or token in user_dict.keys():

    if token in std_dict.keys() or token in user_dict.keys():
        return True
    elif token in ['else', 'then']:
        return True
    elif token[0] == '[':
        return True
    else:
        return False


def parse_if_branch(token, stack):
    global if_branch
    global branch_tokens
    global discard_invalid_branch

    if token == 'then':
        if_branch = False
        discard_invalid_branch = False
        parse(branch_tokens, stack)
        branch_tokens = []
    elif token in ['if', '?']:
        condition = branch_tokens.pop()
        if not condition:
            if_branch = False
        
    elif discard_invalid_branch:
        pass
    elif token in ['else', '!']:
        discard_invalid_branch = True
    elif is_integer(token):
        branch_tokens.append(int(float(token)))
    else:
        branch_tokens.append(token)

def parse_else_branch(token, stack):
    global else_branch
    global branch_tokens
    global discard_invalid_branch

    if token == 'then':
        else_branch = False
        parse(branch_tokens, stack)
        branch_tokens = []
    elif token == 'else':
        discard_invalid_branch = False
    elif discard_invalid_branch:
        pass
    elif is_integer(token):
        branch_tokens.append(int(float(token)))
    else:
        branch_tokens.append(token)

def parse_string_context(token, stack):
    global string_context
    global string_builder

    if token == '"':
        string_context = False
        stack.append(string_builder)
        string_builder = ""
    elif token[-1] == '"':
        string_context = False
        token = token[:-1]
        string_builder += token
        stack.append(string_builder)
        string_builder = ""
    elif token == '\s':
        string_builder += ' '
    else:
        string_builder += token
        string_builder += ' '
    
def parse_list_level(token, stack):
    global list_level
    global list_builder

    s = 'list_builder'

    if token == ']':
        list_level -= 1
        if list_level == 0:
            stack.append(list_builder)
            list_builder = []
    elif token == '[':
        for i in range(list_level - 1):
            s += '[-1]'
        s += ".append([])"
        eval(s)
        list_level += 1
    elif is_number(token):
        if is_integer(token):
            token = int(float(token))
        elif is_float(token):
            token = float(token)
        for i in range(list_level - 1):
            s += '[-1]'
        s += '.append(token)'
        eval(s)
    elif token[-1] == ']':
        token = token[:-1]
        if is_integer(token):
            token = int(float(token))
        list_builder.append(token)
        list_level -= 1
        if list_level == 0:
            stack.append(list_builder)
            list_builder = []
    else:
        for i in range(list_level - 1):
            s += '[-1]'
        s += '.append(token)'
        eval(s)

def parse_compile_context(token):
    global compile_context
    global next_definition

    if token == ';': 
        compile_context = False
        user_dict[next_definition[0]] = next_definition[1:]
        print(next_definition[0] + ':', next_definition[1:])
        next_definition = []
    elif next_definition == [] or is_compilable_token(token):
        next_definition.append(token)
    elif is_integer(token):
        next_definition.append(int(float(token)))
    elif token[0] == "'":
        next_definition.append('[')
        next_definition.append(token[1:])
        next_definition.append(']')
    else:
        next_definition.append(token)

def parse_default_context(token, stack):

    if is_list(token):
        stack.append(token)
    elif token in std_dict.keys():
        eval(std_dict[token])
    elif token in user_dict.keys():
        parse(user_dict[token], stack)
    elif is_integer(token):
        stack.append(int(float(token)))
    elif is_float(token):
        stack.append(float(token))
    elif token[0] == "'":
        stack.append([token[1:]])
    elif token[0] == '"':
        #eval(std_dict['"'])
        d_string(stack)
        if len(token) > 1:
            if token[-1] == '"':
                parse_string_context(token[1:], stack)
            else:
                parse_string_context(token[1:], stack)
        else:
            parse_string_context('\s', stack)
    elif token[0] == '[':
        eval(std_dict['['])
        if token[-1] == ']':
            parse_list_level(token[1:-1], stack)
            parse_list_level(']', stack)
        else:
            parse_list_level(token[1:], stack)
    else:
        stack.append(token)

def parse(tokens, stack):
    '''
        Parse list of tokens and push results to chosen stack.
    '''
    global compile_context
    for i in range(len(tokens)):
        token = tokens[i]
        if if_branch:
            parse_if_branch(token, stack)
        elif else_branch:
            parse_else_branch(token, stack)
        elif string_context:
            parse_string_context(token, stack)
        elif list_level > 0:
            parse_list_level(token, stack)
        elif compile_context:
            parse_compile_context(token)
        else:
            parse_default_context(token, stack)
    

def save_stack():

    new_list = []
    for item in data_stack:
        new_list.append(item)

    memory_stack.append(new_list)


def stack_print_builder(item, string):
    if is_list(item):
        pass
    



def nest_level(stack):
    if type(stack) != list:
        return 0

    max_level = 0
    for item in stack:
        max_level = max(max_level, nest_level(item))
    
    return max_level + 1
    

def REPL():
    global compile_context
    global recording

    print("Type 'exit' to leave REPL")
    while True:
        save_stack()
        if record_context:
            line = input('rec> ')
        elif list_level:
            prefix = 'level' + str(list_level) + '> '
            line = input(prefix)
        elif if_branch:
            line = input("?... ")
        elif else_branch:
            line = input("!... ")
        elif not compile_context:
            line = input('>>> ')
        else:
            line = input('... ')
        tokens = line.split()
        if record_context:
            for token in tokens:
                recording.append(token)
        try:
            parse(tokens, data_stack)
        except Exception as e:
            print("(!) " + str(e))
        
        if list_level:
            print(list_builder)
        elif not compile_context:
            print(data_stack)

        

def run_program():
    file = sys.argv[1]
    f = open(file, "r")
    
    try:
        for line in f:
            tokens = line.split()
            parse(tokens, data_stack)
    except Exception as e:
        print("(!) " + str(e))

    f.close()
    print(data_stack)
    

if interactive_mode:
    REPL()
else:
    run_program()
    REPL()