from copy import deepcopy
import itertools
import collections
import time
    
def readInput():
    global number_of_queries
    input_file = open("input.txt", "r")
    line_number = -1
    i = -1
    j = -1
    for each_line in input_file:
        line_number += 1
        if line_number == 0:
            number_of_queries = int(each_line.rstrip(''))
        elif line_number < number_of_queries + 1:
            i += 1
            ####print each_line.rstrip('\n') + ""
            query = str(each_line.rstrip('\n'))
            query = query.replace(" ", "")

            if query not in queries_dict:
                queries_dict[i] = query
        elif line_number == number_of_queries + 1:
            number_of_sentences_in_KB = each_line.rstrip('') 
        else:
            j += 1
            ####print  + ""
            x = str(each_line.rstrip('\n'))
            sentences_dict[j] = x            
    
def isCapitalAlphabet(c):
    if(c >= 'A' and c <= 'Z'):
        return True
    return False

def preprocessInput(current_str):
    ###print ""
    ###print "Original Sentence - "+current_str
    current_str = current_str.replace(" ", "")
    flag = True
    new_str = deepcopy(current_str)
    global predicate_count
    for i in range(len(current_str)):
        if (isCapitalAlphabet(current_str[i]) and flag):
            ####print current_str[i]
            current_starting_index_of_predicate = i
            flag = False
        elif current_str[i] == ')':
            #for j in range(i-1, -1, -1):
            if current_str[i - 1] != ')':
                current_predicate = current_str[current_starting_index_of_predicate: i+1]
                if current_predicate not in predicates_dict:
                    predicates_dict[current_predicate] = "V"+str(predicate_count)
                    predicate_count += 1
                ####print current_predicate
                new_str = new_str.replace(current_predicate, predicates_dict[current_predicate])
                ####print current_str
                flag = True
        elif current_str[i] == '=' and current_str[i+1] == '>':
            new_str = new_str.replace('=>', '>')
        elif current_str[i] == ' ':
            new_str = new_str.replace(' ', '')
    ####print ""
    ####print "After Preprocessing - " +new_str  
    return new_str
def reverse(current_str):
    new_str = deepcopy(current_str)
    new_str = ''.join(reversed(current_str))
    rev =""
    for i in range(len(new_str)):
        if new_str[i] == '(':
            rev += ')'
        elif new_str[i] == ')':
            rev += '('
        else:
            rev += new_str[i]
    ####print "Reversed String - "+rev
    return rev

def precedence(op):
    if op == '~':
        return 4
    elif op == '&':
        return 3
    elif op == '|':
        return 2
    elif op == '>':
        return 1
    elif op == '(':
        return 0
    elif op == ')':
        return 0
    
def isOperator(op):
    return op == '&' or op == '|' or op == '~' or op == '>'

def performInfixToPrefix(current_str):
    output_str = ""
    stack_s = list()
    for i in range(len(current_str)):
        c = current_str[i]
        if(isOperator(c) == False and c != '(' and c != ')'):
            output_str += c
        elif c == '(':
            stack_s.insert(0, c)
        elif c == ')':
            while stack_s[0] != '(':
                output_str += stack_s.pop(0)
            stack_s.pop(0)
        elif isOperator(c) == True:
            while len(stack_s) != 0 and precedence(c) <= precedence(stack_s[0]):
                output_str += stack_s.pop(0)
            stack_s.insert(0, c)
    while(len(stack_s) != 0):
        output_str += stack_s.pop(0) 
    output_str = reverse(output_str)
    ###print "Prefix Form of Input - " + output_str
    
    prefix_list = []
    ####print len(output_str)
    prev = len(output_str)-1
    for i in range(len(output_str)-1, -1, -1):
        c = ""
        if i>prev:
            continue
        flag = False
        if isOperator(output_str[i]) == False:
            if output_str[i] != 'V': 
                for j in range(i, -1, -1):
                    if output_str[j] != 'V':
                        c += output_str[j]
                    else:
                        c += 'V'
                        flag = True
                        prev = j
                        break
                if flag == False:
                    c += 'V'
                c = reverse(c)
                prefix_list.insert(0, [c])
        else:
            if output_str[i] == '~':
                temp = ['~', prefix_list.pop(0)]
                prefix_list.insert(0, temp)
            elif output_str[i] == '|':
                temp = ['|', prefix_list.pop(0), prefix_list.pop(0)]
                prefix_list.insert(0, temp)
            elif output_str[i] == '&':
                temp = ['&', prefix_list.pop(0), prefix_list.pop(0)]
                prefix_list.insert(0, temp)
            elif output_str[i] == '>':
                temp = ['>', prefix_list.pop(0), prefix_list.pop(0)]
                prefix_list.insert(0, temp)
                
    ####print prefix_list[0]    
    return prefix_list[0]

def negationOf(e):
    if len(e) == 1:
        e = [e]
        e.insert(0, '~')
    else:
        if len(e) == 2:
            #Only one element(i.e. ~A) So make it positive
            e = e[1]
        else:
            if e[0]  == '&':
                e[0] = '|'
            else:
                e[0] = '&'
            e[1] = negationOf(e[1])
            e[2] = negationOf(e[2])  
    return e 
def removeImplications(e):
    if len(e)<2:
        return e
    else:
        operator = e[0]
        if operator == '~':
            e[1] = removeImplications(e[1])
        else:
            e[1] = removeImplications(e[1])
            e[2] = removeImplications(e[2])
        if operator == '>':
            e[0] = '|'
            e[1] = negationOf(e[1])
        return e
def moveNegationInwards(e):
    if len(e)<2:
        return e
    else:
        operator = e[0]
        if operator == '~':
            e[1] = moveNegationInwards(e[1])
        else:
            e[1] = moveNegationInwards(e[1])
            e[2] = moveNegationInwards(e[2])
        if operator == '~' and len(e[1])>1:
            e = e[1]
            e = negationOf(e)
    return e

def distributeAndOverOr(e):
    if len(e)<2 :
        return e
    operator = e[0]
    if operator == '~':
        e[1] = distributeAndOverOr(e[1])
    else:
        e[1] = distributeAndOverOr(e[1])
        e[2] = distributeAndOverOr(e[2])

    if operator == '|':
        operand1 = e[1]
        operand2 = e[2]
        if operand1[0] == '&':
            x1 = ['|', operand1[1], operand2]
            x2 = ['|', operand1[2], operand2]
            e[0] = '&'
            e[1] = x1
            e[2] = x2
        elif operand2[0] == '&':
            x1 = ['|', operand1, operand2[1]]
            x2 = ['|', operand1, operand2[2]]
            e[0] = '&'
            e[1] = x1
            e[2] = x2
    
            
    return e

def convertToCNF(e):
    e = removeImplications(e)
    ####print e
    e = moveNegationInwards(e)
    ####print e
    e = distributeAndOverOr(e)
    ####print e
    return e
def flatten(current_expr):
    s =""
    ####print current_expr
    if len(current_expr) < 2:
        return ''.join(current_expr)
    else:
        if len(current_expr) == 3:
            s += ''.join(flatten(current_expr[1])+str(current_expr[0])+flatten(current_expr[2]))
        elif len(current_expr) == 2:
            s+= ''.join(str(current_expr[0])+flatten(current_expr[1]))
    ####print s
    return s

def getSentences(current_str):
    ###print current_str
    start_index = 0
    for i in range(len(current_str)):
        if current_str[i] == '&':
            Kb_sentenes_list.append(current_str[start_index:i])
            start_index = i+1
    Kb_sentenes_list.append(current_str[start_index: len(current_str)])
    
def convertPreprocessedSentences(current_Kb_sentences_list):
    for each_sentence in current_Kb_sentences_list:
        new_sentence = deepcopy(each_sentence)
        temp_sentence = deepcopy(each_sentence)
        prev = len(new_sentence)-1
        for i in range(len(new_sentence)-1, -1, -1):
            ch = ''
            if i > prev:
                continue
            flag = False
            if isOperator(new_sentence[i]) == False:
                if new_sentence[i] != 'V': 
                    for j in range(i, -1, -1):
                        if new_sentence[j] != 'V':
                            ch += new_sentence[j]
                        else:
                            ch += 'V'
                            flag = True
                            prev = j
                            break
                    
                    ch = reverse(ch)
                    for key, value in predicates_dict.iteritems():
                        if ch == value:
                            temp_sentence = temp_sentence[:prev]+key+temp_sentence[i+1:]
                            #temp_sentence = temp_sentence.replace(ch, key)
                    
                    
        '''
        for key, value in predicates_dict.iteritems():
            if value in new_sentence:
                new_sentence = new_sentence.replace(value, key)
        '''
        if temp_sentence  not in KnowledgeBase:
            KnowledgeBase.append(temp_sentence) 
                
def findArguments(current_predicate):
    for i in range(len(current_predicate)):
        if current_predicate[i] == '(':
            current_predicate = current_predicate[i+1:len(current_predicate)-1]
            break
    
    args = current_predicate.split(',')
    return args

def findPredicate(current_str):
    temp = current_str.split('(')
    return temp[0]

def tellKB(K, current_KB):
    global global_count
    for each_sentence in K:
        each_sentence = standardizeVariablesInKB(each_sentence)
        ###print each_sentence
        current_predicates = each_sentence.split('|')
        temp = dict()
        for each_current_predicates in current_predicates:
            predicate = findPredicate(each_current_predicates)
            if predicate[0] == '~':
                predicate = predicate.replace('~', '')
                neg = True
            else:
                neg = False 
            if predicate not in temp:
                temp[predicate]=[]
            lst = list()
            lst.append(neg)
            lst.append(findArguments(each_current_predicates))
            lst.append(global_count)
            global_count += 1
            temp[predicate].append(lst)
        if temp not in current_KB:
            current_KB.append(temp)
    return current_KB

def standardizeArguments(current_clause):
    global global_count, argument_count
    new_clause = deepcopy(current_clause)
    argument_dict = dict()

    for keys, values in current_clause.items():
        for i in range(len(current_clause[keys])):
            values[i][2] = global_count                
            global_count += 1
            for j in range(len(values[i][1])):      
                ####print values[i][1][j][0]
                if values[i][1][j][0] < 'A' or values[i][1][j][0] > 'Z':
                    #Needs to be replaced
                    if values[i][1][j] not in argument_dict:
                        argument_dict[values[i][1][j]] = "arg"+str(argument_count)
                        argument_count += 1
                    values[i][1][j] = argument_dict[values[i][1][j]]
    
    return current_clause

def unifyVar(var, x, substitution):
    val_var = ""
    val_x = ""
    if substitution != None:
        for i in range(len(substitution)):
            if substitution[i][0] == var:
                val_var = substitution[i][1]
        
        for i in range(len(substitution)):
            if substitution[i][0] == x:
                val_x = substitution[i][1]
    else:
        substitution = []
    if val_var != "":
        return unify(val_var, x, substitution)
    elif val_x != "":
        return unify(var, val_x, substitution)
    else:
        substitution.append([var, x])
        return substitution
    
def unify(x, y, substitution):
    ###print "Unify - ", x, y, substitution
    if substitution == 'failure':
        return 'failure'
    elif x == y:
        return substitution
    elif len(x) == 1 and len(y) == 1:
        if x[0][0].islower():
            return unifyVar(x[0], y[0], substitution)
        elif y[0][0].islower():
            return unifyVar(y[0], x[0], substitution)
        else:
            return 'failure'
    elif len(x[0]) == 1 and x[0].islower():
        if isinstance(x, collections.MutableSequence):
            return unifyVar(x[0], y, substitution)
        return unifyVar(x, y, substitution)
    elif len(y[0]) == 1 and y[0].islower():
        if isinstance(y, collections.MutableSequence):
            return unifyVar(y[0], x, substitution)
        return unifyVar(y, x, substitution)
    elif isinstance(x, collections.MutableSequence) and isinstance(y, collections.MutableSequence):
            return unify(x[1:], y[1:], unify(x[0], y[0], substitution))
    else:
        return 'failure'

def unification(ci, cj, keys, location):
    global global_count, argument_count
    res = []
    ###print "Inside Unification - "
    for predicate_key, predicate_location in itertools.izip(keys, location):
        ###print "\tCurrent Predicate - ", predicate_key
        ###print "\tComplements at Location - ", predicate_location
        unification_clause1 = deepcopy(ci)
        unification_clause2 = deepcopy(cj)
        ###print "\tPerforming Unification..."
        ###print "\tClauses - Before - "
        ###print "\t\tClause 1 - ", unification_clause1
        for predicate_key_clause1, predicate_value_clause1 in unification_clause1.items():
            for position in range(len(unification_clause1[predicate_key_clause1])):
                if predicate_value_clause1[position][2] == predicate_location[0]:
                    args_for_clause1 = predicate_value_clause1[position][1]
        ###print "\t\t\tArguments for Clause 1 - ", args_for_clause1 
        ###print "\t\tClause 2 - ", unification_clause2
        for predicate_key_clause2, predicate_value_clause2 in unification_clause2.items():
            for position in range(len(unification_clause2[predicate_key_clause2])):
                if predicate_value_clause2[position][2] == predicate_location[1]:
                    args_for_clause2 = predicate_value_clause2[position][1]
        ###print "\t\t\tArguments for Clause 2 - ", args_for_clause2
        
        substitution = []
        theta = {}
        substitution = unify(args_for_clause1, args_for_clause2, substitution)
        if substitution != 'failure':
            for s in substitution:
                if s[0] not in theta:
                    theta[s[0]] = []
                theta[s[0]] = s[1]
        
            ###print theta
        
            for key_clause1, value_clause1 in unification_clause1.items():
                for j in range(len(unification_clause1[key_clause1])):
                    for k in range(len(value_clause1[j][1])):
                        if value_clause1[j][1][k] in theta:
                            value_clause1[j][1][k] = theta[value_clause1[j][1][k]]
        
            ###print "\tAfter Performing Unification - "
            ###print "\tClauses - After - "
            ###print "\t\tClause 1 - ", unification_clause1
            for key_clause2, value_clause2 in unification_clause2.items():
                for j in range(len(unification_clause2[key_clause2])):
                    for k in range(len(value_clause2[j][1])):
                        if value_clause2[j][1][k] in theta:
                            value_clause2[j][1][k] = theta[value_clause2[j][1][k]]
        
            
            ###print "\t\tClause 2 - ", unification_clause2
            ###print "\tUnification Complete..."
            
            '''
                Delete the Complementary clauses
            '''
            if len(unification_clause2[predicate_key])==1:
                '''
                    Contains single clause
                '''
                del unification_clause2[predicate_key]
            else:
                for key_clause2, value_clause2 in unification_clause2.items():
                    if key_clause2 == predicate_key:
                        for j in range(len(unification_clause2[key_clause2])):
                            if value_clause2[j][2] == predicate_location[1]:
                                if len(unification_clause2[key_clause2])==1:
                                    del unification_clause2[key_clause2]
                                else:
                                    unification_clause2[key_clause2].pop(j)
                                break
            if len(unification_clause1[predicate_key])==1:
                '''
                    Contains single clause
                '''
                del unification_clause1[predicate_key]
            else:
                for key_clause1, value_clause1 in unification_clause1.items():
                    if key_clause1 == predicate_key:
                        for j in range(len(unification_clause1[key_clause1])):
                            if value_clause1[j][2] == predicate_location[0]:
                                if len(unification_clause1[key_clause1])==1:
                                    del unification_clause1[key_clause1]
                                else:
                                    unification_clause1[key_clause1].pop(j)
                                break
 
            ###print "\tClauses - After Deleting Complementary Clauses - "
            ###print "\t\tClause 1 - ", unification_clause1
            ###print "\t\tClause 2 - ", unification_clause2
            
            '''
                Note*** - Try removing duplicates during appending itself
            '''
            '''
                Appending the two Clauses to form a new one
            '''
            
            for predicate_key_clause2, predicate_value_clause2 in unification_clause2.items():
                if predicate_key_clause2 not in unification_clause1:
                    unification_clause1[predicate_key_clause2] = unification_clause2.pop(predicate_key_clause2)
                else:
                    unification_clause1[predicate_key_clause2] += unification_clause2.pop(predicate_key_clause2)
            
            ###print "\tClauses - After forming a new clause - "
            ###print "\t\tClause 1 - ", unification_clause1
            ###print "\t\tClause 2 - ", unification_clause2  
            
            '''
                Replace Arguments
            ''' 
            unification_clause2 = standardizeArguments(unification_clause1)
            ###print "\tAfter Standardizing Arguments - ",unification_clause2
            res.append(unification_clause2)
        #else:
         #   res.append({})  
    return res  
def getComplements(ci, cj):
    keys = []
    location = []
    for key_ci, value_ci in ci.items():
        ####print key_ci
        if key_ci in cj  :
            ####print str(ci[key_ci][0])+" "+str(cj[key_ci][0])
            for i in range(len(ci[key_ci])):
                for j in range(len(cj[key_ci])):
                    ####print ci[key_ci][i], cj[key_ci][j]
                    
                    if (ci[key_ci][i][0] == (not cj[key_ci][j][0])):
                        '''###print "Complements - ",
                        ####print len(ci[key_ci])
                        ###print ci[key_ci], cj[key_ci]
                        '''
                        keys.append(key_ci)
                        location.append((ci[key_ci][i][2], cj[key_ci][j][2]))
                    
                    #Complements found
    return keys, location
   
def folResolve(ci, cj):
    key, location = getComplements(ci, cj)
    
    if key != []:
        ###print ""
        ###print "Query Clauses - "
        ###print "Clause 1 - Before Unification - ",
        ###print ci
        ###print "Clause 2 - Before Unification - ",
        ###print cj
        return unification(ci, cj, key, location)

def mapArgument(clause):
    ####print "\t\tIn Map Argument - "#, clause
    temp_mapping = {}
    for predicate in clause:
        for i in range(len(clause[predicate])):
            ####print (predicate, i)
            for j in range(len(clause[predicate][i][1])):
                ####print clause[predicate][i][1][j]
                if clause[predicate][i][1][j] not in temp_mapping:
                    temp_mapping[clause[predicate][i][1][j]] = []
                    temp_mapping[clause[predicate][i][1][j]].append((clause[predicate][i][0], predicate, i, j))
                else:
                    temp_mapping[clause[predicate][i][1][j]].append((clause[predicate][i][0], predicate, i, j))  
                
                
    return temp_mapping
    
def isSubset(new, new_KB):
    matched_args = []
    result = True
    new = sorted(new)
    new_KB = sorted(new_KB)
    ######print "In isSubset() - "
    for predicate_newKB in new_KB:
        ####print "\nKB - ", len(predicate_newKB), predicate_newKB
        for predicate_new in new:
            ####print "\t", len(predicate_new), predicate_new
            if len(predicate_newKB) == len(predicate_new):
                flag = True
                for predicate_key_new, predicate_key_newKB in itertools.izip(predicate_new, predicate_newKB):
                    
                    if (predicate_key_new != predicate_key_newKB) or (len(predicate_new[predicate_key_new]) != len(predicate_newKB[predicate_key_newKB])):
                        flag = False
                        break
                    
                        
                if flag:
                    #print "\t\t", timer_list[0] - (time.time() - start_time)
                    if 29 - (time.time() - start_time) < 0.0:
                        return False 
                    
                    possibility = True
                    argument_list_newKB = mapArgument(predicate_newKB)
                    argument_list_new = mapArgument(predicate_new)
                    ######print "\tSame predicates - "
                    ######print "\t\t\tArgs new KB -  ", argument_list_newKB, argument_list_newKB.keys()
                    ######print "\t\t\tArgs new -  ", argument_list_new, argument_list_new.keys()
                    
                    for i in argument_list_newKB:
                        for j in argument_list_new:
                            ####print argument_list_newKB[i], argument_list_new[j]
                            if j not in matched_args:
                                if i[0] == j[0] and i[0].isupper():
                                    '''
                                        Both are same constants
                                    '''
                                    if argument_list_newKB[i] == argument_list_new[j]:
                                        matched_args.append(j)
                                        break
                                elif i[0].islower() and j[0].islower():
                                    '''
                                        Both are args
                                    '''
                                    if argument_list_newKB[i] == argument_list_new[j]:
                                        matched_args.append(j)
                                        break
                                
                    ####print matched_args
                    if len(matched_args) == len(argument_list_new):
                        #result = False
                        return True
    ####print result                   
    #return result  
    return False                         
        

def resolution(query, new_KB):
    global count, start_time
    ###print query
    ###print ""
    ###print new_KB
    ###print ''
    ###print 'In Resolution Function'
    ###print ''
    
    d = 0
    x = 0
    while True:
        d += 1
        new = []
        n = len(new_KB)
        for i in range(n):
            for j in range(i + 1, n):
                ci = new_KB[i]
                cj = new_KB[j]
                
                resolvents = folResolve(ci, cj)
                ####print "Resolvents - ", resolvents
                
                if resolvents != None and {} in resolvents:
                    return True
                '''
                    Try to resolve further
                '''
                if resolvents != None:
                    new += resolvents
                if 29 - (time.time() - start_time) < 0.0:
                    return False 
                ####print isSubset(new, new_KB)
        ###print "\n\n\n"
        ####print new_KB
        
        flag = False 
        for s in new:
            if 29 < (time.time() - start_time):
                return False 
            elif not isSubset([s], new_KB):
                flag = True
                break
        if not flag:
            return False
        '''       
        if isSubset(new, new_KB):
            return False
        '''
        for c in new:
            ####print c
            if 29 < (time.time() - start_time):
                return False 
            if not isSubset([c], new_KB):
                new_KB += [c]
        
        ####print timer_list, (time.time() - start_time) 
        
        
def standardizeVariablesInKB(current_str):   
    global argument_count
    new_str = deepcopy(current_str)
    current_predicates = new_str.split('|')
    argument_dict = dict()
    for each_current_predicate in current_predicates:
        args = findArguments(each_current_predicate)
        for i in args:
            if len(i) == 1 and (i[0] < 'A' or i[0] > 'Z') :
                if i[0] not in argument_dict:
                    argument_dict[i] = "arg"+str(argument_count)
                    argument_count += 1
                for j in range(len(new_str)):
                    if new_str[j] == i and (new_str[j-1] == '(' or new_str[j-1] == ','):
                        new_str = new_str[:j]+argument_dict[i]+new_str[j+1:]
    return new_str

number_of_queries = 0
queries_dict = dict()
sentences_dict = dict()
preprocessed_sentence_dict = dict()
predicates_dict = dict()
Kb_sentenes_list = list()
KnowledgeBase = list()
KB = list()
predicate_count = 0
argument_count = 0
global_count = 0
preprocessed_sentence_counter = 0

readInput()
for each_sentence in sentences_dict:
    s = preprocessInput(sentences_dict[each_sentence])
    if s not in preprocessed_sentence_dict:
        preprocessed_sentence_dict[preprocessed_sentence_counter] = s
        ###print "Preprocessed Sentence - "+s
        cnf = flatten(convertToCNF(performInfixToPrefix(reverse(s))))
        getSentences(cnf)
        ###print "CNF - " + cnf
        ###print "Kb_sentences_list - "+str(Kb_sentenes_list)
                
convertPreprocessedSentences(Kb_sentenes_list)

KB = tellKB(KnowledgeBase, KB)
result = []
###print ""
total_time = 100
#global number_of_queries
timer_list = [total_time/number_of_queries] * number_of_queries
###print timer_list
count = 0
timer_result = list()
for key, value in queries_dict.items():
    query = value

    s = preprocessInput(value)
    if s not in preprocessed_sentence_dict:
        preprocessed_sentence_dict[preprocessed_sentence_counter] = s
        ###print "Preprocessed Sentence - "+s
        cnf = flatten(convertToCNF(performInfixToPrefix(reverse(s))))
        ###print "CNF - " + cnf
        
        for key, value in predicates_dict.items():
            if value == query:
                query = query.replace(value, key)
                
    if query[0] == '~':
        query = query[1:]
    else:
        query = '~'+query
    ###print "Q - ",query
    convertPreprocessedSentences(Kb_sentenes_list) 
    
    new_KB = deepcopy(KB)  
    query = standardizeVariablesInKB(query)
    current_predicates = query.split('|')
    temp = dict()
    for each_current_predicates in current_predicates:
        predicate = findPredicate(each_current_predicates)
        if predicate[0] == '~':
            predicate = predicate.replace('~', '')
            neg = True
        else:
            neg = False 
        if predicate not in temp:
            temp[predicate]=[]
        lst = list()
        lst.append(neg)
        lst.append(findArguments(each_current_predicates))
        lst.append(global_count)
        global_count += 1
        temp[predicate].append(lst)
        ####print lst
    if temp not in new_KB:
        new_KB.append(temp)
    ###print "---------------------------------------------------------------------------------"
    ###print "Current Query - ",
    ###print query
    ###print ""
    ###print "Final Knowledge Base"
    
    
    timer_result.append(timer_list)
    ####print timer_list
    n = len(new_KB) 
    start_time = time.time()   
    result.append(resolution(query, new_KB))
    '''
    end_time = time.time() - start_time
    total_time = total_time - end_time
    count += 1
    if count != number_of_queries:
        timer_list = [total_time / (number_of_queries - count)] * (number_of_queries - count)
    '''
    
###print result
###print timer_result
output = open("output.txt", "w+")
for res in result:
    print res
    output.write(str(res).upper()+"\n") 
    