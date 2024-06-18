# Author: Vaclav Chadim
# at FIT BUT 

# Implementace 1. ukolu do IPP


import sys
import re
from xml.dom import minidom  

#pomocny "slovnik" instrukci
inst_dict = {
    'MOVE': ['Var', 'Symb'],
    'CREATEFRAME': [],
    'PUSHFRAME': [],
    'POPFRAME': [],
    'DEFVAR': ['Var'],
    'CALL': ['Label'],
    'RETURN': [],
    'PUSHS': ['Symb'],
    'POPS': ['Var'],
    'ADD': ['Var', 'Symb', 'Symb'],
    'SUB': ['Var', 'Symb', 'Symb'],
    'MUL': ['Var', 'Symb', 'Symb'],
    'IDIV': ['Var', 'Symb','Symb'],
    'LT': ['Var', 'Symb', 'Symb'],
    'GT': ['Var', 'Symb', 'Symb'],
    'EQ': ['Var', 'Symb', 'Symb'],
    'AND': ['Var', 'Symb', 'Symb'],
    'OR': ['Var', 'Symb', 'Symb'],
    'NOT': ['Var', 'Symb'],
    'INT2CHAR': ['Var', 'Symb'],
    'STRI2INT': ['Var', 'Symb', 'Symb'],
    'READ': ['Var', 'Type'],
    'WRITE': ['Symb'],
    'CONCAT': ['Var', 'Symb', 'Symb'],
    'STRLEN': ['Var', 'Symb'],
    'GETCHAR': ['Var', 'Symb', 'Symb'],
    'SETCHAR': ['Var', 'Symb', 'Symb'],
    'TYPE': ['Var', 'Symb'],
    'LABEL': ['Label'],
    'JUMP': ['Label'],
    'JUMPIFEQ': ['Label', 'Symb', 'Symb'],
    'JUMPIFNEQ': ['Label', 'Symb', 'Symb'],
    'EXIT': ['Symb'],
    'DPRINT': ['Symb'],
    'BREAK': [],
}

#Kontrola Hlavicky        
class Prep:
    @classmethod
    def prepstr(cls, listy): 
        
        setter = False      
        for line in listy:
            line = line.strip()    
            
            if line.upper() == ".IPPCODE24"   and   setter == False:
                
                setter = True
                
            elif   line.upper() == ".IPPCODE24"  and  setter == True:
                print("Chybná nebo chybějící hlavička ve zdrojovém kódu!(23)\n", file=sys.stderr)
                sys.exit(23)           

            if setter == False:
                print("Chybná nebo chybějící hlavička ve zdrojovém kódu!(21)\n", file=sys.stderr)
                sys.exit(21)
        listy.remove(".IPPcode24")
        
        listy = list(filter(None,listy))
       
        



if __name__ == "__main__":

    #Kontrola dalsich parametru
    if len( sys.argv ) > 1:
        if len( sys.argv ) > 2:
            print("Chybějící parametr skriptu (je-li třeba) nebo použití zakázané kombinace parametrů!(10)\n", file=sys.stderr)
            sys.exit(10)
        #napoveda k pouziti
        if (sys.argv[1] == '--help') or (sys.argv[1] == '-h') :
            print("parse.py [--help] <infile >outfile",file=sys.stdout)
            print("Použití:",file=sys.stdout)
            print("Skript typu filtr (parse.py v jazyce Python 3.10)",file=sys.stdout)
            print("načte ze standardního vstupu zdrojový kód v IPPcode24, ",file=sys.stdout)
            print("zkontroluje lexikální a syntaktickou správnost kóduu",file=sys.stdout)            
            print("a vypíše na standardní výstup XML reprezentaci programu\n",file=sys.stdout)                
            print("--help",file=sys.stdout)
            print("Přepínač pro vypsání nápovědy",file=sys.stdout)
            sys.exit(0)
        else:
            print("Chybějící parametr skriptu (je-li třeba) nebo použití zakázané kombinace parametrů!(10)\n", file=sys.stderr)
            sys.exit(10)
    
        
    #maly file check
    lines = sys.stdin.readlines()
    if len(lines) == 0:
        print("Chybná nebo chybějící hlavička ve zdrojovém kódu!(21)\n", file=sys.stderr)
        sys.exit(21)

    #odstraneni komentaru
    for idx, ele in enumerate(lines):
        lines[idx] = lines[idx].split("#")[0]
        lines[idx] = lines[idx].replace("\n", '')
        lines[idx] = lines[idx].strip()
    
    lines = list(filter(None,lines))
    

    #volani kontroly hlavicky
    Prep.prepstr(lines)
    
    #odstraneni prazdnych radku pokud vznikly
    lines = list(filter(None,lines))
    
    #syntax a lexi kontrola
    for line in lines:
        
        if line.split(" ")[0].upper() in inst_dict:

            #slova z radku dam do listu
            parse_line = line.split(" ")
            
            #prvni je vzdy instrukce
            inst = parse_line[0].upper()
            
            parse_line = parse_line [1:]
            
            parse_line = list(filter(None,parse_line))
            
            
            if len(parse_line) != len(inst_dict[inst]):
                print("Jiná lexikální nebo syntaktická chyba!(23)", file=sys.stderr)
                sys.exit(23)
            
            
            
            
            for idx, ele in enumerate(parse_line):
                
                #VARIABLE 
                if inst_dict[inst][idx] == 'Var':
                    found = re.search("^(GF|TF|LF)@([_]|[-]|[$]|[&]|[%]|[!]|[?]|[*]|[a-zA-Z])([_]|[-]|[$]|[&]|[%]|[!]|[?]|[*]|[0-9a-zA-Z])*$", parse_line[idx])
                    
                    if not found:
                        print("Jiná lexikální nebo syntaktická chyba!(23)", file=sys.stderr)
                        sys.exit(23)
                        
                #LABEL        
                if inst_dict[inst][idx] == 'Label':
                    found = re.search("^([_]|[-]|[$]|[&]|[%]|[!]|[?]|[*]|[a-zA-Z])([_]|[-]|[$]|[&]|[%]|[!]|[?]|[*]|[0-9a-zA-Z])*$", parse_line[idx])
                    
                    if not found:
                        print("Jiná lexikální nebo syntaktická chyba!(23)", file=sys.stderr)
                        sys.exit(23)
                
                #SYMB - opravdu dlouhy a neprehledny
                if inst_dict[inst][idx] == 'Symb':
                    
                    found = re.search("(^(GF|TF|LF)@([_]|[-]|[$]|[&]|[%]|[!]|[?]|[*]|[a-zA-Z])([_]|[-]|[$]|[&]|[%]|[!]|[?]|[*]|[0-9a-zA-Z])*$)|(((^int@([+-]?[0-9]+|[+-]?0[Xx][0-9A-Fa-f]+|[+-]?0[Oo][0-7]+)$)|(^string@)|(^bool@true|false$)|(^nil@nil$)))", parse_line[idx])
                    
                    if not found:
                        print("Jiná lexikální nebo syntaktická chyba!(23)", file=sys.stderr)
                        sys.exit(23) 
                    
                    #Uprimne jsem se v tomto regexu na <symb> nechal trochu unest
                    
                    #kotrola esc seq ve stringu
                    string_found = parse_line[idx].split("@",1)[1]
                    if parse_line[idx].split("@")[0] == "string":
                        string_found_split = string_found.split("\\")
                        
                        string_found_split = string_found_split[1:]
                        
                        for string in string_found_split:
                            checking_start = re.search("^([0-9][0-9][0-9])",string)
                            if not checking_start:
                                print("Jiná lexikální nebo syntaktická chyba!(23)", file=sys.stderr)
                                sys.exit(23)  
                    
                        
                #TYPE
                if inst_dict[inst][idx] == 'Type':
                    
                    found = re.search("^(int|string|bool)?$", parse_line[idx])
                    
                    if not found:
                        print("Jiná lexikální nebo syntaktická chyba!(23)", file=sys.stderr)
                        sys.exit(23)               
            
        #zadny match v inst_dict tedy chyba            
        else:
            inst_cor = re.search("^[0-9a-zA-Z]+$", line.split(" ")[0].upper())
            print(inst_cor)
            if not inst_cor:
                print("Jiná lexikální nebo syntaktická chyba!(23)", file=sys.stderr)
                sys.exit(23)
            else:
                print("Neznámý nebo chybný operační kód ve zdrojovém kódu zapsaném v IPPcode24!(22)\n", file=sys.stderr)
                sys.exit(22)
    
    
    

    
    #Generování výstupního XML
    
    #zakladni "hlavicka"
    root = minidom.Document()
    xml = root.createElement('program')
    xml.setAttribute('language', 'IPPcode24')  
    root.appendChild(xml) 
    
    #generovani jednotlivych intrukci
    order = 1
    for line in lines:
        
        parse_line = line.split(" ")
        
        inst = parse_line[0].upper()
        parse_line = parse_line [1:]

        parse_line = list(filter(None,parse_line))        
    
        productChild = root.createElement('instruction') 
        productChild.setAttribute('order', str(order)) 
        order += 1
        productChild.setAttribute('opcode', inst) 
        
        
        arg_num = 1
        for idx, ele in enumerate(parse_line):
            
                #VAR
            if inst_dict[inst][idx] == 'Var':
                arguments = root.createElement('arg'+ str(arg_num))
                arg_num += 1
                arguments.setAttribute('type', 'var')  
                arguments_text = root.createTextNode(parse_line[idx]) 
                arguments.appendChild(arguments_text) 
                productChild.appendChild(arguments)
                
                #LABEL        
            if inst_dict[inst][idx] == 'Label':
                arguments = root.createElement('arg'+ str(arg_num))
                arg_num += 1
                arguments.setAttribute('type', 'label') 
                arguments_text = root.createTextNode(parse_line[idx]) 
                arguments.appendChild(arguments_text) 
                productChild.appendChild(arguments)
                
                #SYMB
            if inst_dict[inst][idx] == 'Symb':
                arguments = root.createElement('arg'+ str(arg_num))
                arg_num += 1
                check_parse_line = parse_line[idx].split("@",1)
                
                if check_parse_line[0] == "GF":
                    arguments.setAttribute('type', 'var')  
                    arguments_text = root.createTextNode(parse_line[idx])  
                if check_parse_line[0] == "LF":
                    arguments.setAttribute('type', 'var') 
                    arguments_text = root.createTextNode(parse_line[idx])                   
                if check_parse_line[0] == "TF":
                    arguments.setAttribute('type', 'var')  
                    arguments_text = root.createTextNode(parse_line[idx]) 
                if check_parse_line[0] == "int":
                    arguments.setAttribute('type', 'int') 
                    arguments_text = root.createTextNode(check_parse_line[1]) 
                if check_parse_line[0] == "bool":
                    arguments.setAttribute('type', 'bool') 
                    arguments_text = root.createTextNode(check_parse_line[1]) 
                if check_parse_line[0] == "string":
                    arguments.setAttribute('type', 'string')  
                    arguments_text = root.createTextNode(check_parse_line[1])  
                if check_parse_line[0] == "nil":
                    arguments.setAttribute('type', 'nil') 
                    arguments_text = root.createTextNode(check_parse_line[1]) 
                arguments.appendChild(arguments_text)
                productChild.appendChild(arguments)
                
                #TYPE
            if inst_dict[inst][idx] == 'Type':
                arguments = root.createElement('arg'+ str(arg_num))
                arg_num += 1
                arguments.setAttribute('type', 'type')  
                arguments_text = root.createTextNode(parse_line[idx]) 
                arguments.appendChild(arguments_text)  
                productChild.appendChild(arguments)
        
        xml.appendChild(productChild) 
        

    #vypsani XML na stdout
    root.writexml(sys.stdout,  newl='\n', addindent='\t', encoding = 'UTF-8',) #indent='\t',
    sys.exit(0)