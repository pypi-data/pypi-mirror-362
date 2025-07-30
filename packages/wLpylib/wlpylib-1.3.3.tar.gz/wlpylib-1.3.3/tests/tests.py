from wLpylib.exporter import *
from wLpylib.parser   import *

# by Bouboufez
# https://scratch.mit.edu/users/bouboufez/

def wLtest(input, shouldFail, log=False):
    obj = {}

    try:
        obj = load(input)
    except (LoadFileError) as e :
        if shouldFail:
            if (log):
                print("\x1b[32;20m", end="") # Green
                print("===== TEST:", input, " =====")
                print(">>>>>>>> TEST PASSED <<<<<<<<\n")
                print("\x1b[0m", end="") # Reset
            return True
        else:
            print("\x1b[34;20m", end="") # Blue
            print("===== TEST:", input, " =====")
            print(">>>>>>>> ERROR RAISED (" + repr(e) + ") <<<<<<<<\n")
            print("\x1b[0m", end="") # Reset
            return False
    except Exception as e :
        print("\x1b[31;20m", end="") # Red
        print("===== TEST:", input, " =====")
        print(f">>>>>>>> TEST CRASHED (PARSING) : {e} <<<<<<<<\n")
        print("\x1b[0m", end="") # Reset
        return False
    
    try :
        output = export(obj, ExportConfig({'do_lines' : False}))
    except Exception as e :
        print("\x1b[31;20m", end="") # Red
        print("===== TEST:", input, " =====")
        if (log):
            print("    Object:", obj)
        print(f">>>>>>>> TEST CRASHED (PRINTING) : {e} <<<<<<<<\n")
        print("\x1b[0m", end="") # Reset
        return False

    if (input.strip() == output.strip() and not shouldFail) or (input.strip() != output.strip() and shouldFail):
        if (log):
            print("\x1b[32;20m", end="") # Green
            print("===== TEST:", input, " =====")
            print("    Object:", obj)
            print("    Output:", output, end="")
            print(">>>>>>>> TEST PASSED <<<<<<<<\n")
            print("\x1b[0m", end="") # Reset
        return True

    # else
    print("\x1b[33;20m", end="") # Yellow
    print("===== TEST:", input, " =====")
    if (log):
        print("    Object:", obj)
    print("    Output:", output, end="")
    if (shouldFail): 
        print(">>>>>>>> Should have raised an exception instead? <<<<<<<<\n")
        ret = False
    else :
        print(">>>>>>>> Input and output differs, check the test <<<<<<<<\n")
        ret = True
    print("\x1b[0m", end="") # Reset
    return ret

def runTests(tests, log):
    count = 0
    passed = 0
    i = 0
    
    assert(len(tests) % 2 == 0)
    while i < len(tests):
        test = tests[i]
        shouldFail = tests[i+1]
        count +=1
        if (wLtest(test, shouldFail, log)):
            passed += 1
        i += 2
    print("###### TOTAL:", passed, "of", count, "tests passed (" + str(1000 * passed // count / 10) + "%) ######")

runTests([
    # No tag
    '', False,
    '\n', False,
    '\t', False,
    '\v', False,
    '\r', False,
    'toto', False,
    '!', True,
    '=', True,
    'null', False,
    
    # Playing with quotes
    '"', True,
    "'", True,
    '""', True,
    '\'\'', False,
    '\'"', True,
    '"\'', True,
    '"<quote>"<!>', True,
    '<quote>"<!>"', True,
    '"<quote><!>"', True,
    '<"quote><!"><!>', True,
    '<\'quote><a="b"<!\'><!>', True,
    '<je t\'aime><!>', True,
    '<"je t\'aime"><!>', True,
    '<je t"aime><!>', True,
    '<\'je t"aime\'><!>', False,
    '<j\'te kiff\'.><!>', True,
    '<j"te kiff".><!>', True,
    '<\'j"te kiff".\'><!>', False,
    '<"j\'te kiff\'."><!>', False,
    '<\'quote><a="b"<!\'><!>', True,
    '<"quote><a="b"<!"><!>', True,
    '<"quote><a=b""<!"><!>', True,
    '<\'><!>', True,
    '<"><!>', True,
    '<"\'"><!>', False,
    '<\'"\'><!>', False,
    
    # Simple content tag
    '<"test"="42">', False,
    '<"test"=\'42\'>', False,
    '<"test"="\'42\'">', False,
    '<"test"="42">', False,
    '<hello world="42">', False,
    '<"hello world"="42">', False,
    '<"1"="1+1">', False,
    '<"1"=1+1>', False,
    '<=>', True,
    '<""="">', True,
    '<"a"=>', False,
    '<"a"="">', False,
    '<="b">', True,
    '<""="b">', True,
    '<c=d=>', True,
    '<"c"="d=">', False,
    '<"c=d"="">', True,
    '<=e=>', True,
    '<"=e"=>', True,
    '<f==g>', True,
    '<f=="g">', True,
    '<"f"="=g">', False,
    '<"f="=g>', True,
    '<===>', True,
    '<"="="=">', True,
    '<!>', True,
    '<"a"=!>', False,
    '<"a"="!">', False,
    '<"ah!"="brogn!ard">', True,
    '<\n="\n">', True,
    '<\t="\t">', True,
    '<\v="\v">', True,

    # Playing with angle brackets
    '<', True,
    '>', True,
    '<>', True,
    '<<>', True,
    '<>>', True,
    '<"<"><!>', True,
    '<">"><!>', True,
    '<"<>"><!>', True,
    '><', True,

    # Simple list tags (empty lists)
    '<"void"><!>', False,
    '<"void">', True,
    '<"void"="vide"><!>', True,
    '<"void=vide"><!>', True,
    '<!><!>', True,
    '<"!"><!>', True,
    '<=gale><!>', True,
    '<egal=><!>', True,
    '<=><!>', True,
    '<"=gale"><!>', True,
    '<"egal="><!>', True,
    '<"="><!>', True,
    '<!!!><!>', True,
    '<"!!!"><!>', True,
    '<bonjour!><!>', True,
    '<!hola><!>', True,
    '<sa!ut><!>', True,
    '<"bonjour!"><!>', True,
    '<"!hola"><!>', True,
    '<"sa!ut"><!>', True,
    '<><!>', True,
    '<\n><!>', True,
    '<\t><!>', True,
    '<\v><!>', True,
    '<"null"><!>', False,
    '<""><!>', True,
    '<"\n"><!>', True,
    '<"\t"><!>', True,
    '<"\v"><!>', True,
    '<\'null\'><!>', False,

    '<"void"><"vide">', True,
    '<"void"><>', True,
    '<"void"><!!>', True,
    '<"void"><">', True,
    '<"void"><"!">', True,
    '<"void"><\t!\t>', True,
    '<"void"><\n!\n>', True,
    '<"void"><\v!\v>', True,
    '<"void"><"\t!\t">', True,
    '<"void"><"\n!\n">', True,
    '<"void"><"\v!\v">', True,
    '<"void"><=>', True,
    '<"void"><hey!>', True,
    '<"void"><!ho>', True,
    '<"void"><h!hi>', True,
    '<"void"><"=">', True,
    '<"void"><"hey!">', True,
    '<"void"><"!ho">', True,
    '<"void"><"h!hi">', True,

    # Nesting tags
    '<"void"><!><!>', True,
    '<"hello"><!><!><"world">', True,
    '<"void"><"vide"><!>', True,
    '<"hello"="world"><"nested"><!>', False,
    '<"hello"="world"><"bonjour"="monde"><!>', True,
    '<"helloworld"><"bonjour"="monde"><!>', False,
    '<"helloworld"><"bonjourmonde"><!><!>', False,
    '<"hello"="world"><"bonjourmonde"><!><!>', True,
    '<"helloworld"><"bonjour"="monde"><!><!>', True,

    # Sequence of tags
    '<"a"="1"><"b"="2">', False,
    '<"a"="1"><"b"="2"><"c"="3">', False,
    '<"a"><!><"b"><!>', False,
    '<"a"><!><"b"="1"><"c"><!><"d"="2">', False,
    '<"a"><"b"><!><!><"c"="1"><"d"><"e"="f"><!><"g"="2">', False,

    # Same data
    '<"a"><!><"a"><!>', True,
    '<"a"><!><"A"><!>', False,
    '<"a"><"a"><!><!>', False,
    '<1+1><!><2><!>', False,
    '<"1+1"><!><"2"><!>', False,
    '<"a"="1"><"a"="1">', True,
    '<"a"="1"><"a"="2">', True,
    '<"a"="1"><"A"="2">', False,
    '<1+1="1"><2="2">', False,
    '<"1+1"="1"><"2"="2">', False,
    '<"a"><!><"a"="a">', True,
    '<"a"="a"><"a"><!>', True,
    '<"a"><!><"A"="A">', False,
    '<"a"="a"><"A"><!>', False,
], False)
#  True will also show passed tests