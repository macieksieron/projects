import sys
from lexer import tokens
import ply.yacc as yacc
import re

#-----------------------------------------------------------------------------------------------------------------------------------#

class Variable:
	def __init__(self,name,memory):
		self.name = name
		self.memory = memory 
		self.inicialized = False
		
class Procedure:
	def __init__(self,name,begin,variables,internal,commands):
		self.name = name
		self.begin = begin
		self.variables = variables 
		self.internal = internal
		self.commands = commands
		self.save = []

#-----------------------------------------------------------------------------------------------------------------------------------#

k = 132

def m_get(i):
	global k
	k+=1
	return 'GET ' + str(i) + '\n'

def m_put(i):
	global k
	k+=1
	return 'PUT ' + str(i) + '\n' 

def m_load(i):
	global k
	k+=1
	return 'LOAD ' + str(i) + '\n'

def m_store(i):
	global k
	k+=1
	return 'STORE ' + str(i) + '\n'

def m_storeI(i):
	global k
	k+=1
	return 'STOREI ' + str(i) + '\n'
	
def m_loadI(i):
	global k
	k+=1
	return 'LOADI ' + str(i) + '\n'

def m_add(i):
	global k
	k+=1
	return 'ADD ' + str(i) + '\n'

def m_sub(i):
	global k
	k+=1
	return 'SUB ' + str(i) + '\n'

def m_addI(i):
	global k
	k+=1
	return 'ADDI ' + str(i) + '\n'

def m_subI(i):
	global k
	k+=1
	return 'SUBI ' + str(i) + '\n'

def m_set(x):
	global k
	k+=1
	return 'SET ' + str(x) + '\n'

def m_half():
	global k
	k+=1
	return 'HALF ' + '\n'

def m_jump(j):
	global k
	k+=1
	return 'JUMP ' + str(j) + '\n'

def m_jump(j):
	global k
	k+=1
	return 'JUMP ' + str(j) + '\n'

def m_jpos(j):
	global k
	k+=1
	return 'JPOS ' + str(j) + '\n'

def m_jzero(j):
	global k
	k+=1
	return 'JZERO ' + str(j) + '\n'	

def m_jumpI(i):
	global k
	k+=1
	return 'JUMPI ' + str(i) + '\n'

#-----------------------------------------------------------------------------------------------------------------------------------#

memory_size = 25
variables = []
procedures = []
begin = 133
temp = []
temp2 = []
#to_inicialize = []

modulo = """LOADI 1
STORE 4
LOADI 2
STORE 5
SET 0
STOREI 3
SET 0
STORE 6
SUB 5
JPOS 15
LOAD 5
SUB 6
JPOS 15
JUMP 39
LOAD 4
SUB 5
JPOS 22
LOAD 5
SUB 4
JZERO 22
JUMP 37
LOAD 5
ADD 5
STORE 5
LOAD 5
SUB 4
JZERO 36
LOAD 5
HALF 
STORE 5
LOAD 4
SUB 5
STORE 4
LOADI 2
STORE 5
JUMP 15
LOAD 4
STOREI 3
JUMPI 7 
"""

multiply = """LOADI 8
STORE 11
LOADI 9
STORE 12
SET 0
STOREI 10
SET 0
STORE 16
LOAD 12
SUB 16
JZERO 79
SET 12
STORE 1
SET 2
STORE 14
SET 14
STORE 2
SET 13
STORE 3
SET 62 
STORE 7 
JUMP 1 
SET 1
STORE 15
SUB 13
JPOS 72
LOAD 13
SUB 15
JPOS 72
LOADI 10
ADD 11
STOREI 10
LOAD 11
ADD 11
STORE 11
LOAD 12
HALF 
STORE 12
JUMP 46
JUMPI 17 
"""

divide = """LOADI 18
STORE 21
LOADI 19
STORE 22
SET 0
STORE 24
SUB 22
JPOS 92
LOAD 22
SUB 24
JPOS 92
JUMP 130
SET 0
STOREI 20
SET 1
STORE 23
LOAD 21
SUB 22
JPOS 103
LOAD 22
SUB 21
JZERO 103
JUMP 129
LOAD 22
ADD 22
STORE 22
LOAD 23
ADD 23
STORE 23
LOAD 22
SUB 21
JZERO 128
LOAD 23
HALF 
STORE 23
LOAD 22
HALF 
STORE 22
LOAD 21
SUB 22
STORE 21
LOADI 20
ADD 23
STOREI 20
LOADI 19
STORE 22
SET 1
STORE 23
JUMP 96
JUMP 132
SET 0
STOREI 20
JUMPI 25 [KONIEC WBUDOWANYCH PROCEDUR]
"""

#-----------------------------------------------------------------------------------------------------------------------------------#

def p_program_all(p):
	'program_all : procedures main'
	global begin
	p[0] = m_jump(begin) + modulo + multiply + divide + delete_labels(p[1]) + delete_labels(p[2])

def p_main(p):
	'''main : PROGRAM IS VAR declarations BEGIN commands END
			| PROGRAM IS BEGIN commands END
	'''
	if len(p)==8:
		p[0] = p[6] + "HALT"
	else:
		p[0] = p[4] + "HALT"

def add_I(commands):
	updated = commands.split("\n")
	for i in range(len(updated)-1): 
		if "HALF" not in updated[i]:
			x = int(re.search(r'\d+', updated[i]).group())
			for variable in temp:
				if variable.memory == x:
					if "LOAD" in updated[i] and "#NOTI" not in updated[i]:
						updated[i] = updated[i].replace("LOAD","LOADI")
					if "STORE" in updated[i] and "#NOTI" not in updated[i]:
						updated[i] = updated[i].replace("STORE","STOREI")
						#to_inicialize.append(x)
					if "ADD" in updated[i] and "#NOTI" not in updated[i]:
						updated[i] = updated[i].replace("ADD","ADDI")
					if "SUB" in updated[i] and "#NOTI" not in updated[i]:
						updated[i] = updated[i].replace("SUB","SUBI")
	return '\n'.join(updated)


def p_procedures_with_var_single(p):
	'procedures : PROCEDURE proc_head IS VAR internal_declarations BEGIN commands END'
	global begin,procedures,temp,memory_size,temp2
	memory_size+=1
	temp.append(Variable("!",memory_size))
	p[7] = p[7] + (m_jumpI(memory_size)) 
	p[7] = add_I(p[7])
	procedures.append(Procedure(p[2],begin,temp,temp2,p[7]))
	temp = []
	temp2 = []
	begin += p[7].count('\n')
	if len(p) == 1:
		p[0] = ""
	if len(p) == 9:
		p[0] = p[7]

def p_procedures_with_var_multiple(p):
	'procedures : procedures PROCEDURE proc_head IS VAR internal_declarations BEGIN commands END'
	global begin,procedures,temp,memory_size,temp2
	memory_size+=1
	temp.append(Variable("!",memory_size))
	p[8] = p[8] + (m_jumpI(memory_size)) 
	p[8] = add_I(p[8])
	procedures.append(Procedure(p[3],begin,temp,temp2,p[8]))
	temp = []
	temp2 = []
	begin += p[8].count('\n')
	if len(p) == 1:
		p[0] = ""
	if len(p) == 10:
		p[0] = p[1] + p[8]

def p_procedures_single(p):
	'procedures : PROCEDURE proc_head IS BEGIN commands END'
	global begin,procedures,temp,memory_size,temp2
	memory_size+=1
	temp.append(Variable("!",memory_size))
	p[5] = p[5] + (m_jumpI(memory_size)) 
	p[5] = add_I(p[5])
	procedures.append(Procedure(p[2],begin,temp,temp2,p[5]))
	temp = []
	temp2 = []
	begin += p[5].count('\n')
	if len(p) == 1:
		p[0] = ""
	if len(p) == 7:
		p[0] = p[5]

def p_procedures_multiple(p):
	'procedures : procedures PROCEDURE proc_head IS BEGIN commands END'
	global begin,procedures,temp,memory_size,temp2
	memory_size+=1
	temp.append(Variable("!",memory_size))
	p[6] = p[6] + (m_jumpI(memory_size))
	p[6] = add_I(p[6])
	procedures.append(Procedure(p[3],begin,temp,temp2,p[6]))
	temp = []
	temp2 = []
	begin += p[6].count('\n')
	if len(p) == 1:
		p[0] = ""
	if len(p) == 8:
		p[0] = p[1] + p[6]

def p_procedures_empty(p):
	'procedures : '
	p[0] = ""

def p_proc_head(p):
	'proc_head : ID LBR proc_declarations RBR'
	p[0] = p[1]

def p_proc_declarations_single(p):
	'proc_declarations : ID'
	global memory_size,temp
	for variable in temp+temp2:
		if variable.name == p[3]:
			raise Exception("Error: Second declaration of variable " + p[1] + ". (line " + str(p.lineno(1)) + ")")
	memory_size += 1
	var = Variable(p[1],memory_size)
	var.inicialized = True
	temp.append(var)
	p[0] = p[1]

def p_proc_declarations_multiple(p):
	'proc_declarations : proc_declarations COMMA ID'
	global memory_size,temp
	for variable in temp+temp2:
		if variable.name == p[3]:
			raise Exception("Error: Second declaration of variable " + p[3] + ". (line " + str(p.lineno(1)) + ")")
	memory_size += 1
	var = Variable(p[3],memory_size)
	var.inicialized = True
	temp.append(var)
	p[0] = p[1] 

def p_internal_declarations_single(p):
	'internal_declarations : ID'
	global memory_size,temp2
	for variable in temp+temp2:
		if variable.name == p[1]:
			raise Exception("Error: Second declaration of variable " + p[1] + ". (line " + str(p.lineno(1)) + ")")
	memory_size += 1
	var = Variable(p[1],memory_size)
	temp2.append(var)
	p[0] = p[1]

def p_internal_declarations_multiple(p):
	'internal_declarations : internal_declarations COMMA ID'
	global memory_size,temp2
	for variable in temp2+temp:
		if variable.name == p[3]:
			raise Exception("Error: Second declaration of variable " + p[3] + ". (line " + str(p.lineno(1)) + ")")
	memory_size += 1
	var = Variable(p[3],memory_size)
	temp2.append(var)
	p[0] = p[1] 

def p_command_proc(p):
	'command : ID LBR variables RBR SEMICOLON'
	global procedures,k,variables
	i = 0
	was_declared = False
	p[3] = p[3].split(" ")
	p[0] = ""
	for procedure in procedures:
		if procedure.name == p[1]:
			if len(p[3])!=len(procedure.variables)-1:
				raise Exception("Error: Wrong number of arguments for procedure \"" + procedure.name + "\" (line " + str(p.lineno(1)) + ")")			 	
			for variable in procedure.variables:
				if i<=len(procedure.variables)-2:
					for variable1 in temp+temp2+variables:
						if variable1.name == p[3][i] and variable1 in variables+temp2:
							was_declared = True	 	
							variable1.inicialized = True
							p[0] += m_set(variable1.memory) +\
						   			m_store(str(variable.memory) + " #NOTI")
							#for x in to_inicialize:
								#if variable.memory == x:
									#variable1.inicialized = True
						if variable1.name == p[3][i] and variable1 in temp:
							was_declared = True
							p[0] += m_load(str(variable1.memory) + " #NOTI") +\
						   			m_store(str(variable.memory) + " #NOTI")
					if was_declared == False:
						raise Exception("Error: Variable " + p[3][i] + " was not declared. (line " + str(p.lineno(1)) + ")")			 	
					else:
						was_declared = False
					i+=1
				else:
					p[0] += m_set(str(k+4) + " #CHANGE") +\
							m_store(str(variable.memory) + " #NOTI") +\
							m_jump(str(procedure.begin) + " #PROC") 
			return
	raise Exception("Error: Procedure " + p[1] + " doesn't exist. (line " + str(p.lineno(1)) + ")")			 	

def p_variables_single(p):
	'variables : ID'
	p[0] = p[1]
	
def p_variables_multiple(p):
	'variables : variables COMMA ID'
	p[0] = p[1] + " " + p[3]

def p_declarations_single(p):
	'declarations : ID'
	global memory_size
	memory_size += 1
	variables.append(Variable(p[1],memory_size))
	p[0] = p[1]

def p_declarations_multiple(p):
	'declarations : declarations COMMA ID'
	for variable in variables:
		if variable.name == p[3]:
			raise Exception("Error: Second declaration of variable " + p[3] + ". (line " + str(p.lineno(1)) + ")")
	global memory_size
	memory_size += 1
	variables.append(Variable(p[3],memory_size))
	p[0] = p[1] 

def p_commands_single(p):
	'commands : command'
	p[0] = p[1]

def p_commands_multiple(p):
	'commands : commands command'
	p[0] = p[1] + p[2]

def p_value_NUM(p):
	'value : NUM'
	p[0] = ("NUM", p[1])

def p_value_ID(p):
	'value : ID'
	p[0] = ("ID", p[1])

#-----------------------------------------------------------------------------------------------------------------------------------#

def p_command_read(p):
	'command : READ ID SEMICOLON'
	for variable in variables+temp+temp2:
		if variable.name == p[2]:
			variable.inicialized = True
			if variable not in temp:
				p[0] = m_get(variable.memory)
				return
			else:
				p[0] = m_get(0) +\
					   m_store(variable.memory)
				return
	raise Exception("Error: Variable " + p[2] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_write(p):
	'command : WRITE value SEMICOLON'
	if p[2][0]=="NUM":
		p[0] = m_set(int(p[2][1])) +\
			   m_put(0)
	else:
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == False:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				else:
					if variable not in temp:
						p[0] = m_put(variable.memory)
						return
					else:
						p[0] = m_load(variable.memory) +\
							   m_put(0)
						return

		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

#-----------------------------------------------------------------------------------------------------------------------------------#

def p_command_assign_value(p):
	'command : ID ASSIGN value SEMICOLON'
	if p[3][0] == "NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[1]:
				variable.inicialized = True
				p[0] = m_set(p[3][1]) +\
					   m_store(str(variable.memory))
				return	   
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	else:
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[3][1]:
						if variable2.inicialized==True:
							variable1.inicialized = True
							p[0] = m_load(variable2.memory) +\
								m_store(variable1.memory)
							return	
						else: 
							raise Exception("Error: Variable " + p[3][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[3][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_assign_sum(p):
	'command : ID ASSIGN value PLUS value SEMICOLON'
	if p[3][0] == "NUM" and p[5][0] == "NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[1]:
				variable.inicialized = True
				p[0] = m_set(int(p[3][1])+int(p[5][1])) +\
			   		   m_store(variable.memory)
				return	   
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	if p[3][0] == "ID" and p[5][0] == "NUM":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[3][1]:
						if variable2.inicialized==True:
							variable1.inicialized = True
							p[0] = m_set(p[5][1]) +\
								   m_add(variable2.memory) +\
								   m_store(variable1.memory)
							return	
						else: 
							raise Exception("Error: Variable " + p[3][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[3][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	if p[3][0] == "NUM" and p[5][0] == "ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[5][1]:
						if variable2.inicialized==True:
							variable1.inicialized = True
							p[0] = m_set(p[3][1]) +\
								   m_add(variable2.memory) +\
								   m_store(variable1.memory)
							return	
						else: 
							raise Exception("Error: Variable " + p[5][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[5][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "ID" and p[5][0] == "ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[3][1]:
						for variable3 in variables+temp+temp2:
							if variable3.name == p[5][1]:
								if variable2.inicialized==True:
									if variable3.inicialized==True:
										variable1.inicialized = True
										p[0] = m_load(variable2.memory) +\
												m_add(variable3.memory) +\
												m_store(variable1.memory)
										return	
									else: 
										raise Exception("Error: Variable " + p[5][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
								else:
									raise Exception("Error: Variable " + p[3][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						raise Exception("Error: Variable " + p[5][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[3][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_assign_divide(p):
	'command : ID ASSIGN value DIVIDE value SEMICOLON'
	global memory_size
	if p[3][0] == "NUM" and p[5][1] == 2:
		for variable in variables+temp+temp2:
			if variable.name == p[1]:
				variable.inicialized = True
				p[0] = m_set(int(int(p[3][1])/2)) +\
			   		   m_store(variable.memory)
				return	   
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "ID" and p[5][1] == 2:
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[3][1]:
						if variable2.inicialized==True:
							variable1.inicialized = True
							p[0] = m_load(variable2.memory) +\
								   m_half() +\
								   m_store(variable1.memory)
							return	
						else: 
							raise Exception("Error: Variable " + p[3][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[3][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "NUM" and p[5][0] == "NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[1]:
				variable.inicialized = True
				p[0] = m_set(int(p[3][1])/int(p[5][1])) +\
			   		   m_store(variable.memory)
				return	   
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "ID" and p[5][0] == "NUM":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[3][1]:
						if variable2.inicialized==True:
							variable1.inicialized = True
							memory_size+=1
							if variable2 in temp:
								first = m_load(str(variable2.memory) + " #NOTI") +\
										m_store("18" + " #NOTI") 
							else:
								first = m_set(variable2.memory) +\
										m_store("18") 
							if variable1 in temp:
								third = m_load(str(variable1.memory) + " #NOTI") +\
											m_store("20" + " #NOTI") 
							else:
								third = m_set(variable1.memory) +\
											m_store("20") 
							p[0] = first +\
								   m_set(p[5][1]) +\
								   m_store(memory_size) +\
								   m_set(memory_size) +\
								   m_store(19) +\
								   third +\
								   m_set(str(k+4) + " #CHANGE") +\
								   m_store("25" + " #NOTI") +\
								   m_jump("80" + " #PROC") 
							return	
						else: 
							raise Exception("Error: Variable " + p[3][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[3][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "NUM" and p[5][0] == "ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[5][1]:
						if variable2.inicialized==True:
							variable1.inicialized = True
							memory_size+=1
							if variable2 in temp:
								second = m_load(str(variable2.memory) + " #NOTI") +\
										m_store("19" + " #NOTI") 
							else:
								second = m_set(variable2.memory) +\
										m_store("19") 
							if variable1 in temp:
								third = m_load(str(variable1.memory) + " #NOTI") +\
											m_store("20" + " #NOTI") 
							else:
								third = m_set(variable1.memory) +\
											m_store("20") 
							p[0] = m_set(p[3][1]) +\
								   m_store(memory_size) +\
								   m_set(memory_size) +\
								   m_store(18) +\
								   second +\
								   third +\
								   m_set(str(k+4) + " #CHANGE") +\
								   m_store("25" + " #NOTI") +\
								   m_jump("80" + " #PROC") 
							return	
						else: 
							raise Exception("Error: Variable " + p[5][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[5][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "ID" and p[5][0] == "ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[3][1]:
						for variable3 in variables+temp+temp2:
							if variable3.name == p[5][1]:
								if variable2.inicialized==True:
									if variable3.inicialized==True:
										variable1.inicialized = True
										if variable2 in temp:
											first = m_load(str(variable2.memory) + " #NOTI") +\
								   					m_store("18" + " #NOTI") 
										else:
											first = m_set(variable2.memory) +\
								   					m_store("18") 
										if variable3 in temp:
											second = m_load(str(variable3.memory) + " #NOTI") +\
								   					 m_store("19" + " #NOTI") 
										else:
											second = m_set(variable3.memory) +\
								   					 m_store("19") 
										if variable1 in temp:
											third =	m_load(str(variable1.memory) + " #NOTI") +\
								   					m_store("20" + " #NOTI") 
										else:
											third =	m_set(variable1.memory) +\
								   					m_store("20") 
										p[0] =  first +\
												second +\
												third +\
												m_set(str(k+4) + " #CHANGE") +\
												m_store("25" + " #NOTI") +\
												m_jump("80" + " #PROC") 
										return	
									else: 
										raise Exception("Error: Variable " + p[5][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
								else:
									raise Exception("Error: Variable " + p[3][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						raise Exception("Error: Variable " + p[5][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[3][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_assign_diff(p):
	'command : ID ASSIGN value MINUS value SEMICOLON'
	global memory_size
	if p[3][0] == "NUM" and p[5][0] == "NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[1]:
				variable.inicialized = True
				p[0] = m_set(int(p[3][1])-int(p[5][1])) +\
			   		   m_store(variable.memory)
				return	   
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	if p[3][0] == "ID" and p[5][0] == "NUM":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[3][1]:
						if variable2.inicialized==True:
							variable1.inicialized = True
							memory_size += 1
							p[0] = m_set(p[5][1]) +\
								   m_store(memory_size) +\
								   m_load(variable2.memory) +\
								   m_sub(memory_size) +\
								   m_store(variable1.memory)
							return	
						else: 
							raise Exception("Error: Variable " + p[3][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[3][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	if p[3][0] == "NUM" and p[5][0] == "ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[5][1]:
						if variable2.inicialized==True:
							variable1.inicialized = True
							p[0] = m_set(p[3][1]) +\
								   m_sub(variable2.memory) +\
								   m_store(variable1.memory)
							return	
						else: 
							raise Exception("Error: Variable " + p[5][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[5][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "ID" and p[5][0] == "ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[3][1]:
						for variable3 in variables+temp+temp2:
							if variable3.name == p[5][1]:
								if variable2.inicialized==True:
									if variable3.inicialized==True:
										variable1.inicialized = True
										p[0] = m_load(variable2.memory) +\
											m_sub(variable3.memory) +\
											m_store(variable1.memory)
										return	
									else: 
										raise Exception("Error: Variable " + p[5][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
								else:
									raise Exception("Error: Variable " + p[3][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						raise Exception("Error: Variable " + p[5][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[3][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_assign_modulo(p):
	'command : ID ASSIGN value MODULO value SEMICOLON'
	global memory_size
	if p[3][0] == "NUM" and p[5][0] == "NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[1]:
				variable.inicialized = True
				p[0] = m_set(int(p[3][1])%int(p[5][1])) +\
			   		   m_store(variable.memory)
				return	   
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "ID" and p[5][0] == "NUM":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[3][1]:
						if variable2.inicialized==True:
							variable1.inicialized = True
							memory_size+=1
							if variable2 in temp:
								first = m_load(str(variable2.memory) + " #NOTI") +\
										m_store("1" + " #NOTI") 
							else:
								first = m_set(variable2.memory) +\
										m_store("1") 
							if variable1 in temp:
								third = m_load(str(variable1.memory) + " #NOTI") +\
											m_store("3" + " #NOTI") 
							else:
								third = m_set(variable1.memory) +\
											m_store("3") 
							p[0] = first +\
								   m_set(p[5][1]) +\
								   m_store(memory_size) +\
								   m_set(memory_size) +\
								   m_store(2) +\
								   third +\
								   m_set(str(k+4) + " #CHANGE") +\
								   m_store("7" + " #NOTI") +\
								   m_jump("1" + " #PROC") 
							return	
						else: 
							raise Exception("Error: Variable " + p[3][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[3][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "NUM" and p[5][0] == "ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[5][1]:
						if variable2.inicialized==True:
							variable1.inicialized = True
							memory_size+=1
							if variable2 in temp:
								second = m_load(str(variable2.memory) + " #NOTI") +\
										m_store("2" + " #NOTI") 
							else:
								second = m_set(variable2.memory) +\
										m_store("2") 
							if variable1 in temp:
								third = m_load(str(variable1.memory) + " #NOTI") +\
											m_store("3" + " #NOTI") 
							else:
								third = m_set(variable1.memory) +\
											m_store("3") 
							p[0] = m_set(p[3][1]) +\
								   m_store(memory_size) +\
								   m_set(memory_size) +\
								   m_store(1) +\
								   second +\
								   third +\
								   m_set(str(k+4) + " #CHANGE") +\
								   m_store("7" + " #NOTI") +\
								   m_jump("1" + " #PROC") 
							return	
						else: 
							raise Exception("Error: Variable " + p[5][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[5][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "ID" and p[5][0] == "ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[3][1]:
						for variable3 in variables+temp+temp2:
							if variable3.name == p[5][1]:
								if variable2.inicialized==True:
									if variable3.inicialized==True:
										variable1.inicialized = True
										if variable2 in temp:
											first = m_load(str(variable2.memory) + " #NOTI") +\
								   					m_store("1" + " #NOTI") 
										else:
											first = m_set(variable2.memory) +\
								   					m_store("1") 
										if variable3 in temp:
											second = m_load(str(variable3.memory) + " #NOTI") +\
								   					 m_store("2" + " #NOTI") 
										else:
											second = m_set(variable3.memory) +\
								   					 m_store("2") 
										if variable1 in temp:
											third =	m_load(str(variable1.memory) + " #NOTI") +\
								   					m_store("3" + " #NOTI") 
										else:
											third =	m_set(variable1.memory) +\
								   					m_store("3") 
										p[0] =  first +\
												second +\
												third +\
												m_set(str(k+4) + " #CHANGE") +\
												m_store("7" + " #NOTI") +\
												m_jump("1" + " #PROC") 
										return	
									else: 
										raise Exception("Error: Variable " + p[5][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
								else:
									raise Exception("Error: Variable " + p[3][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						raise Exception("Error: Variable " + p[5][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[3][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_assign_multiply(p):
	'command : ID ASSIGN value MULTIPLY value SEMICOLON'
	global memory_size
	if p[3][0] == "NUM" and p[5][0] == "NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[1]:
				variable.inicialized = True
				p[0] = m_set(int(p[3][1])*int(p[5][1])) +\
			   		   m_store(variable.memory)
				return	   
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "ID" and p[5][0] == "NUM":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[3][1]:
						if variable2.inicialized==True:
							variable1.inicialized = True
							memory_size+=1
							if variable2 in temp:
								first = m_load(str(variable2.memory) + " #NOTI") +\
										m_store("8" + " #NOTI") 
							else:
								first = m_set(variable2.memory) +\
										m_store("8") 
							if variable1 in temp:
								third = m_load(str(variable1.memory) + " #NOTI") +\
											m_store("10" + " #NOTI") 
							else:
								third = m_set(variable1.memory) +\
											m_store("10") 
							p[0] = first +\
								   m_set(p[5][1]) +\
								   m_store(memory_size) +\
								   m_set(memory_size) +\
								   m_store(9) +\
								   third +\
								   m_set(str(k+4) + " #CHANGE") +\
								   m_store("17" + " #NOTI") +\
								   m_jump("40" + " #PROC") 
							return	
						else: 
							raise Exception("Error: Variable " + p[3][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[3][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "NUM" and p[5][0] == "ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[5][1]:
						if variable2.inicialized==True:
							variable1.inicialized = True
							memory_size+=1
							if variable2 in temp:
								second = m_load(str(variable2.memory) + " #NOTI") +\
										m_store("9" + " #NOTI") 
							else:
								second = m_set(variable2.memory) +\
										m_store("9") 
							if variable1 in temp:
								third = m_load(str(variable1.memory) + " #NOTI") +\
											m_store("10" + " #NOTI") 
							else:
								third = m_set(variable1.memory) +\
											m_store("10") 
							p[0] = m_set(p[3][1]) +\
								   m_store(memory_size) +\
								   m_set(memory_size) +\
								   m_store(8) +\
								   second +\
								   third +\
								   m_set(str(k+4) + " #CHANGE") +\
								   m_store("17" + " #NOTI") +\
								   m_jump("40" + " #PROC") 
							return	
						else: 
							raise Exception("Error: Variable " + p[5][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[5][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[3][0] == "ID" and p[5][0] == "ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[3][1]:
						for variable3 in variables+temp+temp2:
							if variable3.name == p[5][1]:
								if variable2.inicialized==True:
									if variable3.inicialized==True:
										variable1.inicialized = True
										if variable2 in temp:
											first = m_load(str(variable2.memory) + " #NOTI") +\
								   					m_store("8" + " #NOTI") 
										else:
											first = m_set(variable2.memory) +\
								   					m_store("8") 
										if variable3 in temp:
											second = m_load(str(variable3.memory) + " #NOTI") +\
								   					 m_store("9" + " #NOTI") 
										else:
											second = m_set(variable3.memory) +\
								   					 m_store("9") 
										if variable1 in temp:
											third =	m_load(str(variable1.memory) + " #NOTI") +\
								   					m_store("10" + " #NOTI") 
										else:
											third =	m_set(variable1.memory) +\
								   					m_store("10") 
										p[0] =  first +\
												second +\
												third +\
												m_set(str(k+4) + " #CHANGE") +\
												m_store("17" + " #NOTI") +\
												m_jump("40" + " #PROC") 
										return	
									else: 
										raise Exception("Error: Variable " + p[5][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
								else:
									raise Exception("Error: Variable " + p[3][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						raise Exception("Error: Variable " + p[5][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[3][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[1] + " was not declared. (line " + str(p.lineno(1)) + ")")

#-----------------------------------------------------------------------------------------------------------------------------------#

def p_command_if_eq(p):
	'command : IF value EQ value THEN commands ENDIF'
	global memory_size, k
	if p[2][0] == "NUM" and p[4][0] == "NUM":
		if int(p[2][1])==int(p[4][1]):
			p[0] = p[6]
		else:
			p[0] = ""
	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					p[6]=update_jumps(p[6],7)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+5) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+2)  +\
							p[6]
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		
	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					p[6] =  update_jumps(p[6],7)
					p[0] =  m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+5) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+2)  +\
							p[6]
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		
	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								p[6] =  update_jumps(p[6],6)
								p[0] =  m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(k+5) +\
										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(k+2)  +\
										p[6]
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	
def p_command_if_neq(p):
	'command : IF value NEQ value THEN commands ENDIF'
	global memory_size, k
	if p[2][0] == "NUM" and p[4][0] == "NUM":
		if int(p[2][1])!=int(p[4][1]):
			p[0] = p[6]
		else:
			p[0] = ""

	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n')
					p[6] = update_jumps(p[6],8)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+3)  +\
							m_jump(k+2+p[6].count('\n')) +\
							p[6]
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
					
	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n')
					p[6] = update_jumps(p[6],8)
					p[0] =  m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+3)  +\
							m_jump(k+2+p[6].count('\n')) +\
							p[6]
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")	

	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True: 
								k -= p[6].count('\n')
								p[6] = update_jumps(p[6],7)
								p[0] =  m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(k+6) +\
										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(k+3)  +\
										m_jump(k+2+p[6].count('\n')) +\
										p[6]
								k += p[6].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_if_geq(p):
	'command : IF value GEQ value THEN commands ENDIF'
	global memory_size, k
	if p[2][0] == "NUM" and p[4][0] == "NUM":
		if int(p[2][1])!=int(p[4][1]):
			p[0] = p[6]
		else:
			p[0] = ""

	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n')
					p[6] = update_jumps(p[6],8)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+3)  +\
							m_jump(k+2+p[6].count('\n')) +\
							p[6]
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
					
	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n')
					p[6] = update_jumps(p[6],9)
					p[0] =  m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+6) +\
							m_load(memory_size) +\
							m_sub(variable.memory) +\
							m_jzero(k+3)  +\
							m_jump(k+2+p[6].count('\n')) +\
							p[6]
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")	

	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True: 
								k -= p[6].count('\n')
								p[6] = update_jumps(p[6],7)
								p[0] =  m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(k+6) +\
										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jzero(k+3)  +\
										m_jump(k+2+p[6].count('\n')) +\
										p[6]
								k += p[6].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_if_leq(p):
	'command : IF value LEQ value THEN commands ENDIF'
	global memory_size, k
	if p[2][0] == "NUM" and p[4][0] == "NUM":
		if int(p[2][1])!=int(p[4][1]):
			p[0] = p[6]
		else:
			p[0] = ""

	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n')
					p[6] = update_jumps(p[6],9)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+6) +\
							m_load(memory_size) +\
							m_sub(variable.memory) +\
							m_jzero(k+3)  +\
							m_jump(k+2+p[6].count('\n')) +\
							p[6]
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
					
	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n')
					p[6] = update_jumps(p[6],8)
					p[0] =  m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+3)  +\
							m_jump(k+2+p[6].count('\n')) +\
							p[6]
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")	

	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True: 
								k -= p[6].count('\n')
								p[6] = update_jumps(p[6],7)
								p[0] =  m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(k+6) +\
										m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jzero(k+3)  +\
										m_jump(k+2+p[6].count('\n')) +\
										p[6]
								k += p[6].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_if_gt(p):
	'command : IF value GT value THEN commands ENDIF'
	global memory_size, k
	if p[2][0] == "NUM" and p[4][0] == "NUM":
		if int(p[2][1])>int(p[4][1]):
			p[0] = p[6]
		else:
			p[0] = ""

	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					k -= p[6].count('\n')
					p[6] =  update_jumps(p[6],3)
					p[0] =  m_set(p[2][1]) +\
							m_sub(variable.memory) +\
							m_jzero(k+2+p[6].count('\n')) +\
							p[6]
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					k -= p[6].count('\n')
					memory_size += 1
					p[6] =  update_jumps(p[6],5)
					p[0] =  m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+2+p[6].count('\n')) +\
							p[6]
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								k -= p[6].count('\n')
								p[6] =  update_jumps(p[6],3)
								p[0] =  m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jzero(k+2+p[6].count('\n')) +\
										p[6]
								k += p[6].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_if_lt(p):
	'command : IF value LT value THEN commands ENDIF'
	global memory_size, k
	if p[2][0] == "NUM" and p[4][0] == "NUM":
		if int(p[2][1])>int(p[4][1]):
			p[0] = p[6]
		else:
			p[0] = ""

	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n')
					p[6] =  update_jumps(p[6],5)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+2+p[6].count('\n')) +\
							p[6]
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					k -= p[6].count('\n')
					memory_size += 1
					p[6] =  update_jumps(p[6],3)
					p[0] =  m_set(p[4][1]) +\
							m_sub(variable.memory) +\
							m_jzero(k+2+p[6].count('\n')) +\
							p[6]
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								k -= p[6].count('\n')
								p[6] =  update_jumps(p[6],3)
								p[0] =  m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jzero(k+2+p[6].count('\n')) +\
										p[6]
								k += p[6].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

#-----------------------------------------------------------------------------------------------------------------------------------#

def p_command_ifelse_eq(p):
	'command : IF value EQ value THEN commands ELSE commands ENDIF'
	global memory_size, k
	if p[2][0] == "NUM" and p[4][0] == "NUM":
		if int(p[2][1])==int(p[4][1]):
			p[0] = p[6]
		else:
			p[0] = p[8]
	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					p[6]=update_jumps(p[6],7)
					p[8]=update_jumps(p[8],8)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+5-p[8].count('\n')+1) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+2-p[8].count('\n')+1)  +\
							p[6] +\
							m_jump(k+2) +\
							p[8] 
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		
	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					p[6] =  update_jumps(p[6],7)
					p[8]=update_jumps(p[8],8)
					p[0] =  m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+5-p[8].count('\n')+1) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+2-p[8].count('\n')+1)  +\
							p[6] +\
							m_jump(k+2) +\
							p[8] 
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		
	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								p[6] =  update_jumps(p[6],6)
								p[8]=update_jumps(p[8],7)
								p[0] =  m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(k+5-p[8].count('\n')+1) +\
										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(k+2-p[8].count('\n')+1)  +\
										p[6] +\
										m_jump(k+2) +\
										p[8] 
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_ifelse_neq(p):
	'command : IF value NEQ value THEN commands ELSE commands ENDIF'
	global memory_size, k
	if p[2][0] == "NUM" and p[4][0] == "NUM":
		if int(p[2][1])!=int(p[4][1]):
			p[0] = p[6]
		else:
			p[0] = p[8]
	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n') + p[8].count('\n')
					p[6]=update_jumps(p[6],8)
					p[8]=update_jumps(p[8],9)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+3)  +\
							m_jump(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(k+2+p[6].count('\n')+p[8].count('\n')) +\
							p[8] 
					k += p[6].count('\n') + p[8].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n') + p[8].count('\n')
					p[6]=update_jumps(p[6],8)
					p[8]=update_jumps(p[8],9)
					p[0] = 	m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+3)  +\
							m_jump(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(k+2+p[6].count('\n')+p[8].count('\n')) +\
							p[8] 
					k += p[6].count('\n') + p[8].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		
	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								memory_size += 1
								k -= p[6].count('\n') + p[8].count('\n')
								p[6]=update_jumps(p[6],7)
								p[8]=update_jumps(p[8],8)
								p[0] =  m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(k+6) +\
										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(k+3)  +\
										m_jump(k+2+p[6].count('\n')+1) +\
										p[6] +\
										m_jump(k+2+p[6].count('\n') + p[8].count('\n')) +\
										p[8] 
								k += p[6].count('\n') + p[8].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_ifelse_geq(p):
	'command : IF value GEQ value THEN commands ELSE commands ENDIF'
	global memory_size, k
	if p[2][0] == "NUM" and p[4][0] == "NUM":
		if int(p[2][1])>=int(p[4][1]):
			p[0] = p[6]
		else:
			p[0] = p[8]
	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n') + p[8].count('\n')
					p[6]=update_jumps(p[6],8)
					p[8]=update_jumps(p[8],9)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+3)  +\
							m_jump(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(k+2+p[6].count('\n')+p[8].count('\n')) +\
							p[8] 
					k += p[6].count('\n') + p[8].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n') + p[8].count('\n')
					p[6]=update_jumps(p[6],9)
					p[8]=update_jumps(p[8],10)
					p[0] = 	m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+6) +\
							m_load(memory_size) +\
							m_sub(variable.memory) +\
							m_jzero(k+3)  +\
							m_jump(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(k+2+p[6].count('\n')+p[8].count('\n')) +\
							p[8] 
					k += p[6].count('\n') + p[8].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		
	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								memory_size += 1
								k -= p[6].count('\n') + p[8].count('\n')
								p[6]=update_jumps(p[6],7)
								p[8]=update_jumps(p[8],8)
								p[0] =  m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(k+6) +\
										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jzero(k+3)  +\
										m_jump(k+2+p[6].count('\n')+1) +\
										p[6] +\
										m_jump(k+2+p[6].count('\n') + p[8].count('\n')) +\
										p[8] 
								k += p[6].count('\n') + p[8].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_ifelse_leq(p):
	'command : IF value LEQ value THEN commands ELSE commands ENDIF'
	global memory_size, k
	if p[2][0] == "NUM" and p[4][0] == "NUM":
		if int(p[2][1])<=int(p[4][1]):
			p[0] = p[6]
		else:
			p[0] = p[8]
	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n') + p[8].count('\n')
					p[6]=update_jumps(p[6],9)
					p[8]=update_jumps(p[8],10)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+6) +\
							m_load(memory_size) +\
							m_sub(variable.memory) +\
							m_jzero(k+3)  +\
							m_jump(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(k+2+p[6].count('\n')+p[8].count('\n')) +\
							p[8] 
					k += p[6].count('\n') + p[8].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n') + p[8].count('\n')
					p[6]=update_jumps(p[6],8)
					p[8]=update_jumps(p[8],9)
					p[0] = 	m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+3)  +\
							m_jump(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(k+2+p[6].count('\n')+p[8].count('\n')) +\
							p[8] 
					k += p[6].count('\n') + p[8].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		
	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								memory_size += 1
								k -= p[6].count('\n') + p[8].count('\n')
								p[6]=update_jumps(p[6],7)
								p[8]=update_jumps(p[8],8)
								p[0] =  m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(k+6) +\
										m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jzero(k+3)  +\
										m_jump(k+2+p[6].count('\n')+1) +\
										p[6] +\
										m_jump(k+2+p[6].count('\n') + p[8].count('\n')) +\
										p[8] 
								k += p[6].count('\n') + p[8].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_ifelse_gt(p):
	'command : IF value GT value THEN commands ELSE commands ENDIF'
	global memory_size, k
	if p[2][0] == "NUM" and p[4][0] == "NUM":
		if int(p[2][1])>int(p[4][1]):
			p[0] = p[6]
		else:
			p[0] = p[8]
	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n') + p[8].count('\n')
					p[6]=update_jumps(p[6],3)
					p[8]=update_jumps(p[8],4)
					p[0] =  m_set(p[2][1]) +\
							m_sub(variable.memory) +\
							m_jzero(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(k+2+p[6].count('\n')+p[8].count('\n')) +\
							p[8] 
					k += p[6].count('\n') + p[8].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n') + p[8].count('\n')
					p[6]=update_jumps(p[6],5)
					p[8]=update_jumps(p[8],6)
					p[0] = 	m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(k+2+p[6].count('\n')+p[8].count('\n')) +\
							p[8] 
					k += p[6].count('\n') + p[8].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		
	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								memory_size += 1
								k -= p[6].count('\n') + p[8].count('\n')
								p[6]=update_jumps(p[6],3)
								p[8]=update_jumps(p[8],4)
								p[0] =  m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jzero(k+2+p[6].count('\n')+1) +\
										p[6] +\
										m_jump(k+2+p[6].count('\n') + p[8].count('\n')) +\
										p[8] 
								k += p[6].count('\n') + p[8].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_ifelse_lt(p):
	'command : IF value LT value THEN commands ELSE commands ENDIF'
	global memory_size, k
	if p[2][0] == "NUM" and p[4][0] == "NUM":
		if int(p[2][1])<int(p[4][1]):
			p[0] = p[6]
		else:
			p[0] = p[8]
	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n') + p[8].count('\n')
					p[6]=update_jumps(p[6],5)
					p[8]=update_jumps(p[8],6)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(k+2+p[6].count('\n')+p[8].count('\n')) +\
							p[8] 
					k += p[6].count('\n') + p[8].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					k -= p[6].count('\n') + p[8].count('\n')
					p[6]=update_jumps(p[6],3)
					p[8]=update_jumps(p[8],4)
					p[0] = 	m_set(p[4][1]) +\
							m_sub(variable.memory) +\
							m_jzero(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(k+2+p[6].count('\n')+p[8].count('\n')) +\
							p[8] 
					k += p[6].count('\n') + p[8].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		
	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								memory_size += 1
								k -= p[6].count('\n') + p[8].count('\n')
								p[6]=update_jumps(p[6],3)
								p[8]=update_jumps(p[8],4)
								p[0] =  m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jzero(k+2+p[6].count('\n')+1) +\
										p[6] +\
										m_jump(k+2+p[6].count('\n') + p[8].count('\n')) +\
										p[8] 
								k += p[6].count('\n') + p[8].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

#-----------------------------------------------------------------------------------------------------------------------------------#

def p_command_while_eq(p):
	'command : WHILE value EQ value DO commands ENDWHILE'
	global memory_size, k

	if p[2][0]=="NUM" and p[4][0]=="NUM":
		if p[2][1]==p[4][1]:
			x = k+1
			p[0] = p[6] +\
			       m_jump(x-p[6].count('\n'))
		else:
			p[0] = ""

	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[6] = update_jumps(p[6],7)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+3)  +\
							p[6] +\
							m_jump(x-p[6].count('\n'))
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[6] = update_jumps(p[6],7)
					p[0] =  m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+3)  +\
							p[6] +\
							m_jump(x-p[6].count('\n'))
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	
	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								x = k+1
								p[6] =  update_jumps(p[6],6)
								p[0] =  m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(k+6) +\
										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(k+3)  +\
										p[6] +\
										m_jump(x-p[6].count('\n'))
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_while_neq(p):
	'command : WHILE value NEQ value DO commands ENDWHILE'
	global memory_size, k

	if p[2][0]=="NUM" and p[4][0]=="NUM":
		if p[2][1]!=p[4][1]:
			x = k+1
			p[0] = p[6] +\
			       m_jump(x-p[6].count('\n'))
		else:
			p[0] = ""

	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					k -= p[6].count('\n')
					p[6] = update_jumps(p[6],8)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+3)  +\
							m_jump(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(x-p[6].count('\n'))
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
					
	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					k -= p[6].count('\n')
					p[6] = update_jumps(p[6],8)
					p[0] =  m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+3)  +\
							m_jump(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(x-p[6].count('\n'))
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")	

	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True: 
								x = k+1
								k -= p[6].count('\n')
								p[6] = update_jumps(p[6],7)
								p[0] =  m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(k+6) +\
										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(k+3)  +\
										m_jump(k+2+p[6].count('\n')+1) +\
										p[6] +\
										m_jump(x-p[6].count('\n'))
								k += p[6].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_while_geq(p):
	'command : WHILE value GEQ value DO commands ENDWHILE'
	global memory_size, k

	if p[2][0]=="NUM" and p[4][0]=="NUM":
		if p[2][1]>=p[4][1]:
			x = k+1
			p[0] = p[6] +\
			       m_jump(x-p[6].count('\n'))
		else:
			p[0] = ""

	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					k -= p[6].count('\n')
					p[6] = update_jumps(p[6],8)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+3)  +\
							m_jump(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(x-p[6].count('\n'))										
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
					
	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					k -= p[6].count('\n')
					p[6] = update_jumps(p[6],9)
					p[0] =  m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+6) +\
							m_load(memory_size) +\
							m_sub(variable.memory) +\
							m_jzero(k+3)  +\
							m_jump(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(x-p[6].count('\n'))
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")	

	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True: 
								x = k+1
								k -= p[6].count('\n')
								p[6] = update_jumps(p[6],7)
								p[0] =  m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(k+6) +\
										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jzero(k+3)  +\
										m_jump(k+2+p[6].count('\n')+1) +\
										p[6] +\
										m_jump(x-p[6].count('\n'))
								k += p[6].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_while_leq(p):
	'command : WHILE value LEQ value DO commands ENDWHILE'
	global memory_size, k

	if p[2][0]=="NUM" and p[4][0]=="NUM":
		if p[2][1]<=p[4][1]:
			x = k+1
			p[0] = p[6] +\
			       m_jump(x-p[6].count('\n'))
		else:
			p[0] = ""	

	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					k -= p[6].count('\n')
					p[6] = update_jumps(p[6],9)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+6) +\
							m_load(memory_size) +\
							m_sub(variable.memory) +\
							m_jzero(k+3)  +\
							m_jump(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(x-p[6].count('\n'))										
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
					
	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					k -= p[6].count('\n')
					p[6] = update_jumps(p[6],8)
					p[0] =  m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+3)  +\
							m_jump(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(x-p[6].count('\n'))
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")	

	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True: 
								x = k+1
								k -= p[6].count('\n')
								p[6] = update_jumps(p[6],7)
								p[0] =  m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(k+6) +\
										m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jzero(k+3)  +\
										m_jump(k+2+p[6].count('\n')+1) +\
										p[6] +\
										m_jump(x-p[6].count('\n'))
								k += p[6].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_while_lt(p):
	'command : WHILE value LT value DO commands ENDWHILE'
	global memory_size, k

	if p[2][0]=="NUM" and p[4][0]=="NUM":
		if p[2][1]<p[4][1]:
			x = k+1
			p[0] = p[6] +\
			       m_jump(x-p[6].count('\n'))
		else:
			p[0] = ""

	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					x = k+1
					k -= p[6].count('\n')
					p[6] =  update_jumps(p[6],5)
					p[0] =  m_set(p[2][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(x-p[6].count('\n'))
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					x = k+1								
					k -= p[6].count('\n')
					memory_size += 1
					p[6] =  update_jumps(p[6],3)
					p[0] =  m_set(p[4][1]) +\
							m_sub(variable.memory) +\
							m_jzero(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(x-p[6].count('\n'))
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								x = k+1
								k -= p[6].count('\n')
								p[6] =  update_jumps(p[6],3)
								p[0] =  m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jzero(k+2+p[6].count('\n')+1) +\
										p[6] +\
										m_jump(x-p[6].count('\n'))
								k += p[6].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_while_gt(p):
	'command : WHILE value GT value DO commands ENDWHILE'
	global memory_size, k

	if p[2][0]=="NUM" and p[4][0]=="NUM":
		if p[2][1]>p[4][1]:
			x = k+1
			p[0] = p[6] +\
			       m_jump(x-p[6].count('\n'))
		else:
			p[0] = ""

	if p[2][0]=="NUM" and p[4][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					x = k+1
					k -= p[6].count('\n')
					p[6] =  update_jumps(p[6],3)
					p[0] =  m_set(p[2][1]) +\
							m_sub(variable.memory) +\
							m_jzero(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(x-p[6].count('\n'))
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[2][1]:
				if variable.inicialized == True:
					x = k+1								
					k -= p[6].count('\n')
					memory_size += 1
					p[6] =  update_jumps(p[6],5)
					p[0] =  m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+2+p[6].count('\n')+1) +\
							p[6] +\
							m_jump(x-p[6].count('\n'))
					k += p[6].count('\n')
					return
				else:
					raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[2][0]=="ID" and p[4][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[2][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[4][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								x = k+1
								k -= p[6].count('\n')
								p[6] =  update_jumps(p[6],3)
								p[0] =  m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jzero(k+2+p[6].count('\n')+1) +\
										p[6] +\
										m_jump(x-p[6].count('\n'))
								k += p[6].count('\n')
								return
							else:
								raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[2][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[2][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

#-----------------------------------------------------------------------------------------------------------------------------------#

def p_command_repeat_eq(p):
	'command : REPEAT commands UNTIL value EQ value SEMICOLON'
	global memory_size, k

	if p[4][0]=="NUM" and p[6][0]=="NUM":
		if p[4][1]!=p[6][1]:
			x = k+1
			p[0] = p[2] +\
			       m_jump(x-p[2].count('\n'))
		else:
			p[0] = p[2]

	if p[4][0]=="NUM" and p[6][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[6][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[0] =  p[2] +\
							m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(x-p[2].count('\n')) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(x-p[2].count('\n'))  
					return
				else:
					raise Exception("Error: Variable " + p[6][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[6][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[4][0]=="ID" and p[6][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[0] =  p[2] +\
							m_set(p[6][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(x-p[2].count('\n')) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(x-p[2].count('\n'))  
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	
	if p[4][0]=="ID" and p[6][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[4][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[6][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								x = k+1
								p[0] = 	p[2] +\
 										m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(x-p[2].count('\n')) +\
										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(x-p[2].count('\n'))  
								return
							else:
								raise Exception("Error: Variable " + p[6][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[6][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_repeat_neq(p):
	'command : REPEAT commands UNTIL value NEQ value SEMICOLON'
	global memory_size, k

	if p[4][0]=="NUM" and p[6][0]=="NUM":
		if p[4][1]==p[6][1]:
			x = k+1
			p[0] = p[2] +\
			       m_jump(x-p[2].count('\n'))
		else:
			p[0] = p[2]

	if p[4][0]=="NUM" and p[6][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[6][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[0] =  p[2] +\
							m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+3)  +\
							m_jump(x-p[2].count('\n'))
					return
				else:
					raise Exception("Error: Variable " + p[6][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[6][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[4][0]=="ID" and p[6][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[0] =  p[2] +\
							m_set(p[6][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+3)  +\
							m_jump(x-p[2].count('\n'))
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	
	if p[4][0]=="ID" and p[6][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[4][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[6][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								x = k+1
								p[0] = 	p[2] +\
 										m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(k+6) +\
										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(k+3)  +\
										m_jump(x-p[2].count('\n'))
								return
							else:
								raise Exception("Error: Variable " + p[6][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[6][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_repeat_geq(p):
	'command : REPEAT commands UNTIL value GEQ value SEMICOLON'
	global memory_size, k
	
	if p[4][0]=="NUM" and p[6][0]=="NUM":
		if p[4][1]<p[6][1]:
			x = k+1
			p[0] = p[2] +\
			       m_jump(x-p[2].count('\n'))
		else:
			p[0] = p[2]

	if p[4][0]=="NUM" and p[6][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[6][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[0] =  p[2] +\
							m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+3)  +\
							m_jump(x-p[2].count('\n'))
					return
				else:
					raise Exception("Error: Variable " + p[6][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[6][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[4][0]=="ID" and p[6][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[0] =  p[2] +\
							m_set(p[6][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+6) +\
							m_load(memory_size) +\
							m_sub(variable.memory) +\
							m_jzero(k+3)  +\
							m_jump(x-p[2].count('\n'))
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	
	if p[4][0]=="ID" and p[6][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[4][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[6][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								x = k+1
								p[0] = 	p[2] +\
 										m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(k+6) +\
										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jzero(k+3)  +\
										m_jump(x-p[2].count('\n'))
								return
							else:
								raise Exception("Error: Variable " + p[6][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[6][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_repeat_leq(p):
	'command : REPEAT commands UNTIL value LEQ value SEMICOLON'
	global memory_size, k
	
	if p[4][0]=="NUM" and p[6][0]=="NUM":
		if p[4][1]>p[6][1]:
			x = k+1
			p[0] = p[2] +\
			       m_jump(x-p[2].count('\n'))
		else:
			p[0] = p[2]

	if p[4][0]=="NUM" and p[6][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[6][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[0] =  p[2] +\
							m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+6) +\
							m_load(memory_size) +\
							m_sub(variable.memory) +\
							m_jzero(k+3)  +\
							m_jump(x-p[2].count('\n'))
					return
				else:
					raise Exception("Error: Variable " + p[6][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[6][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[4][0]=="ID" and p[6][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[0] =  p[2] +\
							m_set(p[6][1]) +\
							m_store(memory_size) +\
							m_sub(variable.memory) +\
							m_jpos(k+6) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jzero(k+3)  +\
							m_jump(x-p[2].count('\n'))
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	
	if p[4][0]=="ID" and p[6][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[4][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[6][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								x = k+1
								p[0] = 	p[2] +\
 										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(k+6) +\
										m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jzero(k+3)  +\
										m_jump(x-p[2].count('\n'))
								return
							else:
								raise Exception("Error: Variable " + p[6][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[6][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_repeat_gt(p):
	'command : REPEAT commands UNTIL value GT value SEMICOLON'
	global memory_size, k
	
	if p[4][0]=="NUM" and p[6][0]=="NUM":
		if p[4][1]<=p[6][1]:
			x = k+1
			p[0] = p[2] +\
			       m_jump(x-p[2].count('\n'))
		else:
			p[0] = p[2]

	if p[4][0]=="NUM" and p[6][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[6][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[0] =  p[2] +\
							m_set(p[4][1]) +\
							m_sub(variable.memory) +\
							m_jpos(k+3)  +\
							m_jump(x-p[2].count('\n'))
					return
				else:
					raise Exception("Error: Variable " + p[6][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[6][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[4][0]=="ID" and p[6][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[0] =  p[2] +\
							m_set(p[6][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+3)  +\
							m_jump(x-p[2].count('\n')) 
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	
	if p[4][0]=="ID" and p[6][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[4][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[6][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								x = k+1
								p[0] = 	p[2] +\
 										m_load(variable1.memory) +\
										m_sub(variable2.memory) +\
										m_jpos(k+3)  +\
										m_jump(x-p[2].count('\n'))
								return
							else:
								raise Exception("Error: Variable " + p[6][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[6][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

def p_command_repeat_lt(p):
	'command : REPEAT commands UNTIL value LT value SEMICOLON'
	global memory_size, k
	
	if p[4][0]=="NUM" and p[6][0]=="NUM":
		if p[4][1]>=p[6][1]:
			x = k+1
			p[0] = p[2] +\
			       m_jump(x-p[2].count('\n'))
		else:
			p[0] = p[2]

	if p[4][0]=="NUM" and p[6][0]=="ID":
		for variable in variables+temp+temp2:
			if variable.name == p[6][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[0] =  p[2] +\
							m_set(p[4][1]) +\
							m_store(memory_size) +\
							m_load(variable.memory) +\
							m_sub(memory_size) +\
							m_jpos(k+3)  +\
							m_jump(x-p[2].count('\n'))
					return
				else:
					raise Exception("Error: Variable " + p[6][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[6][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

	if p[4][0]=="ID" and p[6][0]=="NUM":
		for variable in variables+temp+temp2:
			if variable.name == p[4][1]:
				if variable.inicialized == True:
					memory_size += 1
					x = k+1
					p[0] =  p[2] +\
							m_set(p[6][1]) +\
							m_sub(variable.memory) +\
							m_jpos(k+3) +\
							m_jump(x-p[2].count('\n'))
					return
				else:
					raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
	
	if p[4][0]=="ID" and p[6][0]=="ID":
		for variable1 in variables+temp+temp2:
			if variable1.name == p[4][1]:
				for variable2 in variables+temp+temp2:
					if variable2.name == p[6][1]:
						if variable1.inicialized == True:
							if variable2.inicialized == True:
								x = k+1
								p[0] = 	p[2] +\
 										m_load(variable2.memory) +\
										m_sub(variable1.memory) +\
										m_jpos(k+3) +\
										m_jump(x-p[2].count('\n'))
								return
							else:
								raise Exception("Error: Variable " + p[6][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
						else:
							raise Exception("Error: Variable " + p[4][1] + " was not inicialized. (line " + str(p.lineno(1)) + ")")
				raise Exception("Error: Variable " + p[6][1] + " was not declared. (line " + str(p.lineno(1)) + ")")
		raise Exception("Error: Variable " + p[4][1] + " was not declared. (line " + str(p.lineno(1)) + ")")

#-----------------------------------------------------------------------------------------------------------------------------------#

def update_jumps(commands,n):
	updated = commands.split("\n")
	for i in range(len(updated)-1): 
		if "JZERO" in updated[i]:
			x = int(re.search(r'\d+', updated[i]).group())+n
			updated[i] = "JZERO " + str(x)
		if "JPOS" in updated[i]:
			x = int(re.search(r'\d+', updated[i]).group())+n
			updated[i] = "JPOS " + str(x)
		if "JUMP" in updated[i] and "#PROC" not in updated[i]:
			x = int(re.search(r'\d+', updated[i]).group())+n
			updated[i] = "JUMP " + str(x)
		if "SET" in updated[i] and "#CHANGE" in updated[i]:
			x = int(re.search(r'\d+', updated[i]).group())+n
			updated[i] = "SET " + str(x) + " #CHANGE"
	return '\n'.join(updated)

def delete_labels(commands):
	updated = commands.split("\n")
	for i in range(len(updated)-1):
		updated[i] = updated[i].split("#", 1)[0]
	return '\n'.join(updated)

#-----------------------------------------------------------------------------------------------------------------------------------#

parser = yacc.yacc()
file = open(sys.argv[1], "r")

try:
	parsed = parser.parse(file.read(), tracking=True)
	try:
		file_write = open(sys.argv[2], "w")
		file_write.write(parsed)
	except Exception as e:
		exit()
except Exception as e:
	print(e)
	exit()

