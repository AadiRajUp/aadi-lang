## EXCEPTIONS 
class SymbolError(Exception):
    def __init__(self, message):
        super().__init__(message)
class SemicolonError(Exception):
    def __init__(self, message):
        super().__init__(message)


allowed_identifier_names = set("qwertyuiopasdfghjklzxcvbnm_1234567890")
numbers = set("1234567890")
operators = set("+-=*/,!&|")
for i in ["==","<=",">=","!=","<",">","&&","||"]:
    operators.add(i)



identifiers = dict()
def assignment(a, b):
    identifiers[a][1]=b
    return b
def add(a, b):
    return a + b 
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b
def divide(a, b):
    if b == 0:
        raise DivideByZeroError("your divisor is zero ligma")
    return a/b
def checkequal(a,b):
    return 1 if a == b else 0
def checkgreater(a,b):
    return 1 if a > b else 0
def checklesser(a,b):
    return 1 if a < b else 0
def checkgreaterequal(a,b):
    return 1 if checkgreater(a,b) or checkequal(a,b) else 0
def checklesserequal(a,b):
    return 1 if checklesser(a,b) or checkequal(a,b) else 0
def checknotequal(a,b):
    return 1 if a != b else 0
def ander(a,b):
    return 1 if a * b else 0
def orer(a,b):
    return 1 if a + b else 0

def negation(a):
    return 0 if a else 1


def tofloat_or_int(a):
    
    if (a.isdecimal()):
        return int(a)
    elif (isfloat(a)):
        return float(a)
    else:
        return a
    
def isfloat(a):
    if a.find('.')==-1:
        return False
    l = a.split(".")
    if len(l) !=2:
        return False
    return l[0].isdecimal() and l[1].isdecimal()

    
def handle_declaration(name,dtype):
    if name in identifiers:
        raise FileNotFoundError
    identifiers[name]=[dtype,0]


def check_type(ch):
    if ch in numbers:
        return "number"
    if ch in allowed_identifier_names.difference(numbers):
        return "identifier"
    if ch in operators:
        return "operator"
    if ch == ";":
        return "semicolon"
    if ch == ",":
        return "comma"

    return "none"

operators = {
    "=":[0,"assignment",assignment],
    "&&":[-1,"arithmetic",ander],
    "||":[-1,"arithmetic",orer],
    "==":[-1,"arithmetic",checkequal],
    "<=":[-1,"arithmetic",checklesserequal],
    ">=":[-1,"arithmetic",checkgreaterequal],
    "!":[-1,"arithmetic",negation],
    "!=":[-1,"arithmetic",checknotequal],
    ">":[-1,"arithmetic",checkgreater],
    "<":[-1,"arithmetic",checklesser],
    "+":[-2,"arithmetic",add],
    "-":[-2,"arithmetic",subtract],
    "*":[-3,"arithmetic",multiply],
    "/":[-3,"arithmetic",divide],

    
}
keywords = {
    "int": ["declarative"],
    "float":["declarative"],
    "if":["conditional"],
}
decleratives_list = {"int","float"}
skipset = set(" \n")
# for faster access
operator_set = set(operators.keys())

# i think storing 
#        VARIABLE_NAME : [type,value]
#
#  would be optimal as it could emulate smth like binary ig
#
#

#### TODAYS GOAL
# int a = 5 bhanda a:[int,5] banaune
# ideally line to line evaluate garna laune

def lexer(exp):
    token=["none",""]
    tokens =[]
    listoftokens =[]
    lineno = 0
    charno = 0
    for i in range(len(exp)-1):
        charno +=1
        curr= exp[i]
        peek = exp[i+1]
        if curr in skipset:
            if token[0]!="none":
                tokens.append(token[1])
                token[0]="none"
                token[1]=""
            
            if curr=="\n":
                lineno+=1
                if tokens != []:
                    listoftokens.append(tokens)
                    tokens =[]
                
            continue
        
        curr_type = check_type(curr)
        peek_type = check_type(peek)
        if token[0] == "none":
            
            token[0] = curr_type
        
        token[1]+=curr
        #print(token,curr,"'",peek,"'",curr_type,peek_type)
        if curr_type == "number" and peek_type == "identifier":
            raise SymbolError(f"Invalid symbol name. Identifier cannot begin with a number line = {lineno}")
        
        if peek_type != token[0]:
            if peek_type != "number" or token[0]!= "identifier":
                tokens.append(tofloat_or_int(token[1]))
                token[0]="none"
                token[1]=""
                continue
    return listoftokens 


###
#[['int', 'aadi', '=', 1], ['int', 'gadi', '=', 2, '+', 1, '-', 13],
#['gadi', '=', 'aadi', '+', 5, '+', 1], ['gadi', '=', 'gadi', '+', 1], ['aadi', '=', 'aadi', '+', 'aadi']]
#   esto khako list of lexems produce garxa lexer le ani tyo parser ma feed hunxa
#
#
#


def parser(exp):
    # as of today april 23 i have assumed that there are only two types of statement
    # Declerative and Arithmetic
    # if the 1st word in a line is identified to be keyword, it is defined to be a Declerative statement
    # if the 1st word in a line is not identified to be a keyword, we assume it is a variable
    # that is why the thing which differentiates these two is called a differentiator
    differentator = exp[0]
    print(exp[:-1])
    if differentator in keywords:
        if keywords[differentator][0]=="declarative":
            if exp[-1]!=";":
                raise SemicolonError("Error no semicolon")
            return parse_declarative(exp[:-1])
        # handle keyword and shii here
    else:
        # as differentiator wasnt in keywords, we assume the expression to be arithmetic
        
        if exp[-1]!=";":
            raise SemicolonError("Error no semicolon")
        return parse_tree(exp[:-1])
        
        
def parse_declarative(exp):
    data_type = exp[0]
    rest_of_the_expression = exp[1:]
        
    # lets break rest of the expression into commas and shii
    expression_tree=[]
    mini_expressions=[data_type]
    for i in rest_of_the_expression:
        if i == ",":
            # comma aauda = xa bhane declarative ra arithmetic ma split garne
            # if comma xaina bhane just declarative mandine
            if "=" in mini_expressions:
                expression_tree.append(["declerative",mini_expressions[:2]])
                mini_expressions.pop(0)
                expression_tree.append(["arithmetic",mini_expressions])
                mini_expressions=[data_type]
            else:
                expression_tree.append(["declerative",mini_expressions[:2]])
                mini_expressions=[data_type]
            continue
        mini_expressions.append(i)
    if "=" in mini_expressions:
        expression_tree.append(["declerative",mini_expressions[:2]])
        mini_expressions.pop(0)
        expression_tree.append(["arithmetic",mini_expressions])
    else:
        expression_tree.append(["declerative",mini_expressions[:2]])
    
    return ["declerative",expression_tree]
    
    
        
def parse_tree(exp):
    if len(exp) == 0:
        return exp
    if len(exp)==1 and exp[0] not in operator_set :
        return exp[0]
        
    result = []
    highest_presidense = -99
    # Highest presidence nikalne ani identifiers haru lai ni haldine set ma
    
    for i in exp:
        if i in operator_set:
            highest_presidense = max(highest_presidense,operators[i][0]) # 0 as 0 holds the presidence and 1 holds function address
    # Divide and rule
    # Split in the fromat
    # left operator right 
    # [operator,left, right]
    # we proceed L2R cuz why not
    #             ^   
    #             |
    #             |
    # this is what i thought but 3/3*2 garda 3/3 evaluate suru ma garnu parne ani 1*3 garnu parne but suru ma 3*2 garera 3/6 garxa
    # which is wrong so aaba R2L janxa [::-1] garera reverse gareko lol
    
    for i in exp[::-1]:
        if i in operators.keys():
            # Highest presidense bhettaune sath dang dung
            if (operators[i][0]==highest_presidense):
                index = exp.index(i)
                result.append(exp[index])
                L = parse_tree(exp[:index])
                R = parse_tree(exp[index+1:])
                if i in ["+","-"]:
                    if L == []:
                        L=0
                    if R == []:
                        R=0
                result.append(L)
                result.append(R)

                break

                
    return ["arithmetic",result]

def evaluater(exp):
    if exp[0]=="arithmetic":
        return arithmetic_evaluater(exp[1])
        
    if exp[0]=="declerative":
        return declerative_evaluater(exp[1])

def declerative_evaluater(tree):
    
    for exp in tree:    
        if exp[0] == "declerative":
            final_result = handle_declaration(exp[1][1],exp[1][0])
        if exp[0] == "arithmetic":
            parsed = parse_tree(exp[1])
            final_result  = arithmetic_evaluater(parsed[1])
    return final_result

def arithmetic_evaluater(tree):
    
    
    # RHS will always need to be evaluated but for lhs
    # -> if the operation is arithmetic it will need resolution
    # -> if the operation is assignment it will not need resolution
    if type(tree[2]) == list:  

        tree[2] = evaluater(tree[2])

    if type(tree[2]) not in (float, int):
        if tree[2] in identifiers:
                    
            right_side_operand = identifiers[tree[2]][1] 
        else:
            print("WHAT THE FUCK EVEN IS ", tree[2],"?")
    else:
        right_side_operand = tree[2]
        
    operation = tree[0]
    operation_type = operators[operation][1]
    # if the operation is arithmetic the LHS will need resolution
    
    if  operation_type == "arithmetic":
        if type(tree[1]) == list:
            tree[1] = evaluater(tree[1])
        
        if type(tree[1]) not in (float, int):
            if tree[1] in identifiers:
                        
                left_side_operand = identifiers[tree[1]][1] 
            else:
                print("WHAT THE FUCK EVEN IS ", tree[1], "?")
        else:
            left_side_operand = tree[1]
    # if the operation is assignment, LHS wont need resolution
    elif operation_type == "assignment":
        # ya k error aauna sakxa bhane, if ramrai handle gareko xaina bhane compound stayements aauna sakxa
        # so tesko proper error handling garnu
        if tree[1] in identifiers:
            left_side_operand = tree[1]
        else:
            print("WHAT THE FUCK EVEN IS ",tree[1],"? You have never declared it bozo")

    
    required_function = operators[operation][2] # Function is kept in 2 position

    result = required_function(left_side_operand, right_side_operand)


    return result
    
    # return operators[ tree[0] ][1]( int(tree[1]), int(tree[2]), ['=', 'aadi', ['arithmetic', ['+', 'aadi', 'a']]]]
#{'a': ['int', 0 )  
    #                              ^
    # Imagine trying to understand | after a month or so
expression = """
int c=  5>5 - 1&&1;

"""
list_of_lexered = lexer(expression)
print("List of lexered: ",list_of_lexered)

for lexemes in list_of_lexered:
    
    parsed = parser(lexemes)
    print(parsed)
    evaluated = evaluater(parsed)
    print(evaluated)

    
# from my latest research
# (research means fiddling around in programiz c compiler)
# i have a hypothesis that 
# if there is a boolean algebra in the entire arithmetic statement the entire arithmetic statement goes under a huge normalization
# if the result was non zero 
print(identifiers)
