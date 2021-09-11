from search import *
import math
import heapq
import itertools

class RoutingGraph(Graph):
    def __init__(self, map_str):
        map_str = map_str.splitlines()
        self.map_str = []
        for row in map_str:
            self.map_str.append(row.strip())

    def starting_nodes(self):
        starting_nodes = []
        for row in range(len(self.map_str)):
            for col in range(len(self.map_str[row])):
                if self.map_str[row][col] == 'S':
                    starting_nodes.append((row, col, math.inf))
                elif self.map_str[row][col] in [str(i) for i in range(10)]:
                    starting_nodes.append((row, col, int(self.map_str[row][col])))
        return starting_nodes

    def is_goal(self, node):
        row = node[0]
        col = node[1]
        if self.map_str[row][col] == 'G': 
            return True
        else:
            return False

    def outgoing_arcs(self, tail_node):
        arcs = []
        row = tail_node[0]
        col = tail_node[1]
        fuel = tail_node[2]
        move_options = [('N' , -1, 0), ('E' ,  0, 1), ('S' ,  1, 0), ('W' ,  0, -1)]
        if fuel > 0 :
            for i in range(len(move_options)):
                if self.map_str[row + move_options[i][1]][col + move_options[i][2]] not in ['X', '|', '-', '+']:
                    head = (row + move_options[i][1], col + move_options[i][2], fuel - 1)
                    arcs.append(Arc(tail_node, head, move_options[i][0], 5))
        if self.map_str[row][col] == 'F' and fuel < 9:
            head = (row, col, 9)
            arcs.append(Arc(tail_node, head, 'Fuel up', 15))
        return arcs
    
    def estimated_cost_to_goal(self, node):
        nodeRow = node[0]
        nodeCol = node[1]
        
        goalDistances = []
        
        for row in range(len(self.map_str)):
            for col in range(len(self.map_str[row])):
                if self.map_str[row][col] == 'G':
                    xDist = abs(nodeCol - col)
                    yDist = abs(nodeRow - row)
                    goalDistances.append((xDist + yDist) * 5)
        
        return min(goalDistances)
        
    
    
class AStarFrontier(Frontier):
    def __init__(self, map_graph):
        self.map_graph = map_graph
        self.pq = []
        self.expanded = set()
        self.counter = itertools.count()
        
    def add(self, path):
        cost = sum(arc.cost for arc in path)
        heuristic = self.map_graph.estimated_cost_to_goal(path[-1].head)
        priority = cost + heuristic
        count = next(self.counter)
        entry = [priority, count, path]
        heapq.heappush(self.pq, entry)
    
    def __iter__(self):
        return self

    def __next__(self):
        if len (self.pq) > 0:
            while self.pq:
                priority, count, path = heapq.heappop(self.pq)
                head = path[-1].head
                if head not in self.expanded:
                    self.expanded.add(head)
                    return path
            raise StopIteration
        else:
            raise StopIteration    
        
        
        
  
def print_map(map_graph, frontier, solution):
    map_str = ''
    map_list = []
    expanded_nodes = set()
    solution_nodes = set()
    for row in map_graph.map_str:
        map_list.append([i for i in row])
    if solution != None:
        for arc in solution:
            solution_node = (arc.head[0], arc.head[1])
            solution_nodes.add((arc.head[0], arc.head[1]))
    for node in frontier.expanded:
        expanded_node = (node[0], node[1])
        if expanded_node not in solution_nodes:
            expanded_nodes.add(expanded_node)
    for row in range(len(map_list)):
        for col in range(len(map_list[row])):
            if map_list[row][col] not in ['S', 'G']:
                if (row, col) in solution_nodes:
                    map_list[row][col] = '*'
                elif (row, col) in expanded_nodes:
                    map_list[row][col] = '.'
    for row in range(len(map_list)):
        for col in range(len(map_list[row])):
            map_str += map_list[row][col]
        map_str += '\n'
    print(map_str)
      
def main():
    map_str = """\
    +-------------+
    |    XG       |
    |    XXXXX  X |
    |S        X   |
    +-------------+
    """
    
    map_graph = RoutingGraph(map_str)
    frontier = AStarFrontier(map_graph)
    solution = next(generic_search(map_graph, frontier), None)
    print(solution)
    print_map(map_graph, frontier, solution)
  
    
if __name__ == "__main__":
    main()