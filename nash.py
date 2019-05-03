import sys
import shlex
from prettytable import PrettyTable
import numpy as np
from copy import deepcopy

def check_nash_equilibrium(start,game_matrix,no_of_players,dim):
	
	for i in range(no_of_players):
		s = deepcopy(start)
		s[i] = 0
		for j in range(dim[i]):
			start = tuple(start)
			s = tuple(s)
			if game_matrix[start+(i,)] < game_matrix[s+(i,)]:
				return
			start = list(start)
			s = list(s)
			s[i] += 1

	print(start)


def print_game_matrix(game_matrix):
	p = PrettyTable()
	for row in game_matrix:
		p.add_row(row)
	p.header = False
	p.border = True
	p.align = "r"
	print(p)

def n_player(payoffs,dimentions,players):
	no_of_players = len(dimentions)
	end = deepcopy(dimentions)
	dim = deepcopy(dimentions)
	dimentions.append(no_of_players)
	payoffs = [float(p) for p in payoffs]
	# print(payoffs)

	game_matrix = np.zeros(dimentions)
	# game_matrix = np.array(payoffs)
	# game_matrix = game_matrix.reshape(dimentions)
	# print(game_matrix[0,0,0,0])

	start = [0]*no_of_players
	product_dimentions = 1
	for d in dimentions:
		product_dimentions *= d

	k = 0
	while k<product_dimentions:
		# start = list(start)
		for x in range(no_of_players):
			temp = k%no_of_players
			start = tuple(start)
			game_matrix[start+(temp,)] = payoffs[k]
			start = list(start)
			k += 1
		for i in range(0,len(start)):
			if start[i]+1 >= dim[i]:
				start[i] = 0
			else:
				start[i] += 1
				break
	# print(start)
	start = [0]*no_of_players

	print("The payoffs matrix:")
	print(game_matrix)
	end = [e-1 for e in end]
	print("\nPure strategy nash equilibriums:")

	while start != end:
		check_nash_equilibrium(start,game_matrix,no_of_players,dim)
		for i in range(len(start)-1,-1,-1):
			if start[i]+1 >= dim[i]:
				start[i] = 0
			else:
				start[i] += 1
				break
	check_nash_equilibrium(start,game_matrix,no_of_players,dim)


def two_players(row_payoffs,col_payoffs,dimentions,players):
	m = dimentions[0]
	n = dimentions[1]
	row_game_matrix = []
	for i in range(m):
		temp = []
		for j in range(n):
			temp.append(float(row_payoffs[j*m+i]))
		row_game_matrix.append(temp)

	col_game_matrix = []
	for i in range(m):
		temp = []
		for j in range(n):
			temp.append(float(col_payoffs[j*m+i]))
		col_game_matrix.append(temp)

	print("The row player payoffs matrix:")
	print_game_matrix(row_game_matrix)
	print("The col player payoffs matrix:")
	print_game_matrix(col_game_matrix)

	print("\nPure strategy nash equilibriums:")

	row_game_matrix_trans = [*zip(*row_game_matrix)]
	# print_game_matrix(row_game_matrix_trans)

	for i in range(m):
		col_max = max(col_game_matrix[i])
		col_bests = []
		for j in range(n):
			if col_game_matrix[i][j] == col_max:
				col_bests.append(j)

		for col_best in col_bests:
			# row_best = row_game_matrix_trans[col_best].index(max(row_game_matrix_trans[col_best])) 
			row_max = max(row_game_matrix_trans[col_best])
			row_bests = []
			for k in range(m):
				if row_game_matrix_trans[col_best][k] == row_max:
					row_bests.append(k)
			for row_best in row_bests:
				if i == row_best:
					result = [row_best,col_best]
					print(result)
					# print("%s plays his strategy number %d and %s plays his strategy number %d" %(players[0],row_best,players[1],col_best))

def main():

	payoffs = []
	players = []
	dimentions = []
	sum_dimentions = 0
	product_dimentions = 1
	file = open(sys.argv[1], "r")
	for line in file:
		if line.find('{') != -1:
			line = line.replace('{', '')
			line = line.replace('}', '')
			l = shlex.split(line)
			players = [l[i] for i in range(int(len(l)/2))]
			print(players)
			dimentions = [int(l[i]) for i in range(int(len(l)/2),len(l))]
			print(dimentions)
				
			


		elif line[0].isdigit() or line[0] == '-':
			payoffs = line.split()
			if len(dimentions) == 2:
				row_payoffs = [float(payoffs[i]) for i in range(0,len(payoffs),2)]
				col_payoffs = [float(payoffs[i]) for i in range(1,len(payoffs),2)]

			for d in dimentions:
				product_dimentions *= d
				sum_dimentions += d


	# print(players)
	# print(payoffs)
	# print(dimentions)
	if players == [] or dimentions == [] or payoffs == []:
		print("Invalid strategies")
		exit(0)

	if len(dimentions) == 2:
		two_players(row_payoffs,col_payoffs,dimentions,players)

	elif len(dimentions) > 2:
		n_player(payoffs,dimentions,players)

	else:
		print("Invalid no of players")
		exit(0)

	

if __name__ == '__main__':
	main()