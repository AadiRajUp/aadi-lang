
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


operators = {
    "=":[0,"assignment",assignment],
    "+":[-1,"arithmetic",add],
    "-":[-1,"arithmetic",subtract],
    "*":[-2,"arithmetic",multiply],
    "/":[-2,"arithmetic",divide],
}
keywords = {
    "int": ["declarative"],
    "float":["declarative"],
    "if":["conditional"],
}
decleratives_list = {"int","float"}

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
    allowed_identifier_names = set("qwertyuiopasdfghjklzxcvbnm_1234567890")
    symbols = set("+-=*/,")
    
    exp_removed_newline=""
    
    for i in exp:
        if i == "\n":
            continue
        exp_removed_newline+=i
    lis = exp_removed_newline.split(";")[:-1]
    word_list=[]
    line_builder=[]
    word_builder=""
    for line in lis:
        for char in line:
            if char in allowed_identifier_names:
                word_builder += char
            if char == " ":
                if word_builder != "":
                    line_builder.append(tofloat_or_int(word_builder))
                word_builder = ""
            if char in symbols: # BUG HERE word_list ma '' append hunxa tyo hatauna paryo
                if word_builder != "":
                    line_builder.append(tofloat_or_int(word_builder))
                line_builder.append(char)
                
                word_builder=""
                
        line_builder.append(tofloat_or_int(word_builder))
        word_list.append(line_builder)
        word_builder =""
        line_builder=[]
    
    return word_list


def parser(exp):
    # as of today april 23 i have assumed that there are only two types of statement
    # Declerative and Arithmetic
    # if the 1st word in a line is identified to be keyword, it is defined to be a Declerative statement
    # if the 1st word in a line is not identified to be a keyword, we assume it is a variable
    # that is why the thing which differentiates these two is called a differentiator
    differentator = exp[0]
    if differentator in keywords:
        if keywords[differentator][0]=="declarative":
            return parse_declarative(exp)
        # handle keyword and shii here
    else:
        # as differentiator wasnt in keywords, we assume the expression to be arithmetic
        return parse_tree(exp)
        
        
def parse_declarative(exp):
    data_type = exp[0]
    rest_of_the_expression = exp[1:]
        
    # lets break rest of the expression into commas and shii
    expression_tree=[]
    mini_expressions=["int"]
    for i in rest_of_the_expression:
        if i == ",":
            # comma aauda = xa bhane declarative ra arithmetic ma split garne
            # if comma xaina bhane just declarative mandine
            if "=" in mini_expressions:
                expression_tree.append(["declerative",mini_expressions[:2]])
                mini_expressions.pop(0)
                expression_tree.append(["arithmetic",mini_expressions])
                mini_expressions=["int"]
            else:
                expression_tree.append(["declerative",mini_expressions[:2]])
                mini_expressions=["int"]
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
    if len(exp)==1:
        return exp[0]
        
    result = []
    highest_presidense = -3
    # Highest presidence nikalne ani identifiers haru lai ni haldine set ma
    
    for i in exp:
        if i in operator_set:
            highest_presidense = max(highest_presidense,operators[i][0]) # 0 as 0 holds the presidence and 1 holds function address
    # Divide and rule
    # Split in the fromat
    # left operator right 
    # [operator,left, right]
    # we proceed L2R cuz why not
    for i in exp:
        if i in operators.keys():
            # Highest presidense bhettaune sath dang dung
            if (operators[i][0]==highest_presidense):
                index = exp.index(i)
                result.append(exp[index])
                L = parse_tree(exp[:index])
                R = parse_tree(exp[index+1:])
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
            handle_declaration(exp[1][1],exp[1][0])
        if exp[0] == "arithmetic":
            parsed = parse_tree(exp[1])
            return arithmetic_evaluater(parsed[1])
            

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
                print("WHAT THE FUCK EVEN IS ", tree[1],"?")
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
    
    # return operators[ tree[0] ][1]( int(tree[1]), int(tree[2]) )  
    #                              ^
    # Imagine trying to understand | after a month or so
expression = """
int gadi = 2+1-13;
gadi = gadi +1;
"""
list_of_lexered = lexer(expression)


for lexemes in list_of_lexered:
    
    parsed = parser(lexemes)
    evaluated = evaluater(parsed)

    
print(identifiers)