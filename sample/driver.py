import sys
import math
import queue
import copy
import time
import resource
import numpy as np
import heapq
from collections import deque


class Board:

	def __init__(self, boardstate):
		boardstate = list(map(int, boardstate)) #to int
		self.state = tuple(boardstate)
		self.dim = math.sqrt(len(boardstate))
		self.prev = None
		self.prev_dir = None
		self.depth = 0

	def add_prev(self, previous):
		self.prev = previous
		self.depth = self.prev.depth + 1

	def add_prev_dir(self, direction):
		self.prev_dir = direction

	def __eq__(self, other):
		return self.state == other.state

	def __hash__(self):
		return hash(str(self))

class astarBoard:

	def __init__(self, b):
		boardstate = list(map(int, b.state)) #to int
		self.state = tuple(b.state)
		self.dim = math.sqrt(len(b.state))
		self.prev = None
		self.prev_dir = None
		self.depth = 0
		self.dist = manhattanDist(self)
		#self.pathCost = len(trackPath(self))
		self.cost = self.depth + self.dist

	def add_prev(self, previous):
		self.prev = previous
		self.depth = self.prev.depth + 1

	def add_prev_dir(self, direction):
		self.prev_dir = direction

	def boardEquals(self, other):
		return self.state == other.state

	def updatePathCost(self, val):
		if val < self.depth:
			self.depth = val

	def updateCost(self):
		self.cost = self.depth + self.dist

	def __eq__(self, other):
		return self.dist == other.dist

	def __lt__(self, other):
		return self.dist < other.dist

	def __gt__(self, other):
		return self.dist > other.dist

	def __hash__(self):
		return hash(str(self))


def main():

	#read array from arguments
	#run using python driver.py bfs 0,8,7,6,5,4,3,2,1
	searchtype = sys.argv[1]
	arr = sys.argv[2].split(',')
	b = Board(arr)
	
	if searchtype == "bfs":
		bfs(b, goalTest)
	if searchtype == "dfs":
		dfs(b, goalTest)
	if searchtype == "ast":
		astar(b, goalTest)
	if searchtype == "ida":
		limit = astarBoard(b).dist
		while not (ida(b, goalTest, limit)):
			limit+=1



def goalTest(board):

	state = board.state
	s = copy.deepcopy(state)
	s = tuple(sorted(s))
	#print(state)
	#print(s)
	if state == s:
		return 1
	return 0


def trackPath(board):
	path_list = []
	while board.prev is not None:
		path_list.append(board.prev_dir)
		board = board.prev
	path_list.reverse()
	return path_list


def possibleMoves(board, bfsdfs):
	#returns list of Boards boardsList

	state = board.state
	state = list(state)
	length = len(state)
	dim = int(math.sqrt(length))
	boardsList = []
	pos = state.index(0)
	#print("'0' in position", pos)


	if pos >= length - dim: # 6,7,8
		#bottom row
		newstate = copy.deepcopy(state)
		newstate[pos], newstate[pos-dim] = newstate[pos-dim], newstate[pos]
		temp = Board((tuple(newstate)))
		if bfsdfs == "astar" or bfsdfs == "ida":
			temp = astarBoard(temp)
		temp.add_prev_dir("Up")
		boardsList.append(temp)

	if pos >= dim and pos < length - dim: # 3,4,5
		#middle row
		newstate = copy.deepcopy(state)
		newstate[pos], newstate[pos-dim] = newstate[pos-dim], newstate[pos]
		temp = Board((tuple(newstate)))
		if bfsdfs == "astar" or bfsdfs == "ida":
			temp = astarBoard(temp)
		temp.add_prev_dir("Up")
		boardsList.append(temp)

		newstate = copy.deepcopy(state)
		newstate[pos], newstate[pos+dim] = newstate[pos+dim], newstate[pos]
		temp = Board((tuple(newstate)))
		if bfsdfs == "astar" or bfsdfs == "ida":
			temp = astarBoard(temp)
		temp.add_prev_dir("Down")
		boardsList.append(temp)

	if pos < dim: # 0,1,2
		#top row
		newstate = copy.deepcopy(state)
		newstate[pos], newstate[pos+dim] = newstate[pos+dim], newstate[pos]
		temp = Board((tuple(newstate)))
		if bfsdfs == "astar" or bfsdfs == "ida":
			temp = astarBoard(temp)
		temp.add_prev_dir("Down")
		boardsList.append(temp)

	if (pos % dim) == (dim - 1):
		#right col
		newstate = copy.deepcopy(state)
		newstate[pos], newstate[pos-1] = newstate[pos-1], newstate[pos]
		temp = Board((tuple(newstate)))
		if bfsdfs == "astar" or bfsdfs == "ida":
			temp = astarBoard(temp)
		temp.add_prev_dir("Left")
		boardsList.append(temp)
	
	if ((pos % dim) != (dim - 1)) and ((pos % dim) != 0):
		#middle col
		newstate = copy.deepcopy(state)
		newstate[pos], newstate[pos-1] = newstate[pos-1], newstate[pos]
		temp = Board((tuple(newstate)))
		if bfsdfs == "astar" or bfsdfs == "ida":
			temp = astarBoard(temp)
		temp.add_prev_dir("Left")
		boardsList.append(temp)

		newstate = copy.deepcopy(state)
		newstate[pos], newstate[pos+1] = newstate[pos+1], newstate[pos]
		temp = Board((tuple(newstate)))
		if bfsdfs == "astar" or bfsdfs == "ida":
			temp = astarBoard(temp)
		temp.add_prev_dir("Right")
		boardsList.append(temp)

	if (pos % dim) == 0:
		#left col
		newstate = copy.deepcopy(state) #copy curr state getting checked
		newstate[pos], newstate[pos+1] = newstate[pos+1], newstate[pos] #switch
		temp = Board((tuple(newstate))) #new board
		if bfsdfs == "astar" or bfsdfs == "ida":
			temp = astarBoard(temp)
		temp.add_prev_dir("Right") #add prev dir
		boardsList.append(temp) #add to boardslist
		
	if bfsdfs == "dfs" or bfsdfs == "ida":
		boardsList.reverse()

	"""
	for elem in list(boardsList):
		print("Boardslist: ", elem.state)
	"""
	return boardsList


def manhattanDist(board):
	dim = math.sqrt(len(board.state))
	state = np.array(board.state)
	sorted_state = copy.deepcopy(state)
	sorted_state = sorted(sorted_state)

	state2 = np.reshape(state, (dim, dim))
	sorted_state2 = np.reshape(sorted_state, (dim, dim))

	dist = 0
	for arr in state2:
		for num in arr:
			idx = np.argwhere(state2 == num)
			sidx = np.argwhere(sorted_state2 == num)
			dist += abs(idx[0][0] - sidx[0][0])
			dist += abs(idx[0][1] - sidx[0][1])
	
	return dist		


def bfs(initialBoard, goalTest):

	frontier = deque()
	frontier.append(initialBoard)
	frontier_set = set()
	frontier_set.add(initialBoard.state)
	explored = set()
	max_fringe_size = 1 # =1

	while len(frontier) > 0:
		"""
		print("frontier:")
		for elem in list(frontier):
			print(elem.state)
		print("Explored:")
		for elem in list(explored):
			print(elem.state)	
		"""
		#max fringe size
		if len(frontier) > max_fringe_size:
			max_fringe_size = len(frontier)

		board = frontier.popleft()
		explored.add(board)

		if goalTest(board):

			#max search depth
			max_search_depth = 0
			for f in list(frontier):
				if f.depth > max_search_depth:
					max_search_depth = f.depth

			for e in list(explored):
				if e.depth > max_search_depth:
					max_search_depth = e.depth

			"""
			print("Final State:", board.state)
			print("path_to_goal:", trackPath(board))
			print("cost_of_path:", len(trackPath(board))) 
			print("nodes_expanded:", len(explored) - 1) #subtract initial node
			print("fringe_size:", len(frontier)) 
			print("max_fringe_size:", max_fringe_size)
			print("search_depth:", board.depth)
			print("max_search_depth:", max_search_depth)
			print("running_time:", time.time() - start_time)
			print("max_ram_usage:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000)
			"""
			with open("output.txt", "w") as text_file:
				print("path_to_goal:", trackPath(board), file=text_file)
				print("cost_of_path:", len(trackPath(board)), file=text_file) 
				print("nodes_expanded:", len(explored) - 1, file=text_file) #subtract initial node
				print("fringe_size:", len(frontier), file=text_file) 
				print("max_fringe_size:", max_fringe_size, file=text_file)
				print("search_depth:", len(trackPath(board)), file=text_file)
				print("max_search_depth:", max_search_depth, file=text_file)
				print("running_time:", time.time() - start_time, file=text_file)
				print("max_ram_usage:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000, file=text_file)
			
			return 1

		neighbors = possibleMoves(board, bfs)

		for neighbor in neighbors:
			if neighbor.state not in frontier_set:
				neighbor.add_prev(board)
				frontier.append(neighbor)
				frontier_set.add(neighbor.state)
		
	return 0


def dfs(initialBoard, goalTest):

	frontier = [] #stack
	frontier.append(initialBoard)
	frontier_set = set()
	frontier_set.add(initialBoard.state)
	explored = list(set())
	max_fringe_size = 1 # =1

	while len(frontier) > 0:
		"""
		print("frontier:")
		for elem in list(frontier):
			print(elem.state)
		
		print("Explored:")
		for elem in list(explored):
			print(elem.state)	
		"""
		#max fringe size
		if len(frontier) > max_fringe_size:
			max_fringe_size = len(frontier)

		board = frontier.pop()
		explored.append(board)

		if goalTest(board):

			
			
			#max search depth
			max_search_depth = 0
			for f in list(frontier):
				if f.depth > max_search_depth:
					max_search_depth = f.depth

			for e in list(explored):
				if e.depth > max_search_depth:
					max_search_depth = e.depth

			
			print("Final State:", board.state)
			print("path_to_goal:", trackPath(board))
			print("cost_of_path:", len(trackPath(board)))
			print("nodes_expanded:", len(explored) - 1)
			print("fringe_size:", len(frontier)) 
			print("max_fringe_size:", max_fringe_size)
			print("search_depth:", board.depth)
			print("max_search_depth:", max_search_depth)#
			print("running_time:", time.time() - start_time)
			print("max_ram_usage:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000)
			"""
			with open("output.txt", "w") as text_file:
				print("path_to_goal:", trackPath(board), file=text_file)
				print("cost_of_path:", len(trackPath(board)), file=text_file) 
				print("nodes_expanded:", len(explored) - 1, file=text_file) #subtract initial node
				print("fringe_size:", len(frontier), file=text_file) 
				print("max_fringe_size:", max_fringe_size, file=text_file)
				print("search_depth:", len(trackPath(board)), file=text_file)
				print("max_search_depth:", max_search_depth, file=text_file)
				print("running_time:", time.time() - start_time, file=text_file)
				print("max_ram_usage:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000, file=text_file)
			"""
			return 1

		neighbors = possibleMoves(board, "dfs")

		for neighbor in neighbors:
			if neighbor.state not in frontier_set:
				neighbor.add_prev(board)
				frontier.append(neighbor)
				frontier_set.add(neighbor.state)

	return 0


def astar(initialBoard, goalTest):

	initialBoard = astarBoard(initialBoard)
	frontier = []
	heapq.heappush(frontier, initialBoard)
	frontier_set = set()
	frontier_set.add(initialBoard.state)
	explored = list(set())
	max_fringe_size = 1

	while frontier:
		"""
		print("frontier:")
		for elem in list(frontier):
			print(elem.state)
		
		print("Explored:")
		for elem in list(explored):
			print(elem.state)	
		"""
		#max fringe size
		if len(frontier) > max_fringe_size:
			max_fringe_size = len(frontier)

		board = heapq.heappop(frontier)
		explored.append(board)

		if goalTest(board):
			
			max_search_depth = 0
			for f in list(frontier):
				if f.depth > max_search_depth:
					max_search_depth = f.depth

			for e in list(explored):
				if e.depth > max_search_depth:
					max_search_depth = e.depth

			"""
			print("Final State:", board.state)
			print("path_to_goal:", trackPath(board))
			print("cost_of_path:", len(trackPath(board))) 
			print("nodes_expanded:", len(explored) -1) #subtract initial state
			print("fringe_size:", len(frontier)) 
			print("max_fringe_size:", max_fringe_size)
			print("search_depth:", board.depth)
			print("max_search_depth:", max_search_depth)
			print("running_time:", time.time() - start_time)
			print("max_ram_usage:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000)
			"""
			with open("output.txt", "w") as text_file:
				print("path_to_goal:", trackPath(board), file=text_file)
				print("cost_of_path:", len(trackPath(board)), file=text_file) 
				print("nodes_expanded:", len(explored) - 1, file=text_file) #subtract initial node
				print("fringe_size:", len(frontier), file=text_file) 
				print("max_fringe_size:", max_fringe_size, file=text_file)
				print("search_depth:", len(trackPath(board)), file=text_file)
				print("max_search_depth:", max_search_depth, file=text_file)
				print("running_time:", time.time() - start_time, file=text_file)
				print("max_ram_usage:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000, file=text_file)
			
			return 1

		neighbors = possibleMoves(board, "astar")

		for neighbor in neighbors:


			if neighbor.state not in frontier_set:
				neighbor.add_prev(board)
				heapq.heappush(frontier, neighbor)
				frontier_set.add(neighbor.state)

			
	return 0


def ida(initialBoard, goalTest):

	initialBoard = astarBoard(initialBoard)
	frontier = [] #stack
	frontier.append(initialBoard)
	frontier_set = set()
	frontier_set.add(initialBoard.state)
	explored = list(set())
	max_fringe_size = 1

	while frontier:
		"""
		print("frontier:")
		for elem in list(frontier):
			print(elem.state)
		
		print("Explored:")
		for elem in list(explored):
			print(elem.state)	
		"""
		#max fringe size
		if len(frontier) > max_fringe_size:
			max_fringe_size = len(frontier)

		board = frontier.pop()
		while(board.depth > limit) and frontier:
			board = frontier.pop()
		explored.append(board)

		if goalTest(board):
	
			#max search depth
			max_search_depth = 0
			for f in list(frontier):
				if f.depth > max_search_depth:
					max_search_depth = f.depth

			for e in list(explored):
				if e.depth > max_search_depth:
					max_search_depth = e.depth
			"""
			print("Final State:", board.state)
			print("path_to_goal:", trackPath(board))
			print("cost_of_path:", len(trackPath(board)))
			print("nodes_expanded:", len(explored) - 1)
			print("fringe_size:", len(frontier)) 
			print("max_fringe_size:", max_fringe_size)
			print("search_depth:", board.depth)
			print("max_search_depth:", max_search_depth)
			print("running_time:", time.time() - start_time)
			print("max_ram_usage:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000)
			"""
			with open("output.txt", "w") as text_file:
				print("path_to_goal:", trackPath(board), file=text_file)
				print("cost_of_path:", len(trackPath(board)), file=text_file) 
				print("nodes_expanded:", len(explored) - 1, file=text_file) #subtract initial node
				print("fringe_size:", len(frontier), file=text_file) 
				print("max_fringe_size:", max_fringe_size, file=text_file)
				print("search_depth:", len(trackPath(board)), file=text_file)
				print("max_search_depth:", max_search_depth, file=text_file)
				print("running_time:", time.time() - start_time, file=text_file)
				print("max_ram_usage:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000, file=text_file)
			
			return 1

		neighbors = possibleMoves(board, "astar")
		for neighbor in neighbors:
			if neighbor.state not in frontier_set:
				if (neighbor.depth + neighbor.dist) < limit:
					#print("neighbor cost: ", neighbor.cost)
					#print("board cost: ", board.cost)
					neighbor.add_prev(board)
					neighbor.updatePathCost(board.depth + 1)
					neighbor.updateCost() 
					frontier.append(neighbor)
					frontier_set.add(neighbor.state)



	return 0


start_time = time.time()
main()
