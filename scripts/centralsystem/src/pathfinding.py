from databaseconnector import DatabaseConnector
import math
import itertools
import methods

class PathFinding():
    '''Object to wrap all the different lists and methods needed to find paths'''

    def __init__(self, databaseconnector):
        self.databaseconnector = databaseconnector 
        
        temp_node_tuple = self.databaseconnector.get_query('SELECT id FROM nodes')
        node_list = []
        for item in temp_node_tuple:
            node_list.append(item[0])
        self.node_tuple = tuple(node_list)
        self.edge_tuple = self.databaseconnector.get_query('SELECT edge_id, weight FROM edges')
        self.edgeconnections_tuple = self.databaseconnector.get_query('SELECT edge_one_id, edge_two_id, direction FROM edgeconnections')

    def dijkstra(self, start_node):
        #creates empty lists for the vertives, a dict for mapping vertex to distance and a dict for mapping which node was used to reach the node
        vertex_list = []
        distance_list = {}
        previous_node_list = {}

        #sets up the lists
        for vertex in self.node_tuple:
            vertex_list.append(vertex)
            distance_list[vertex] = -1
            previous_node_list[vertex] = -1

            distance_list[start_node] = 0
        
        #takes the element with the shortest distance and uses that point to calculate next points
        while len(vertex_list) != 0:
            #print(distance_list)
            current_vertex = (-1, -1) # represents the nodeID and the distance to it #TODO check for better, cleaner way to do this
            for vertex in vertex_list:
                if current_vertex[1] < 0 or (current_vertex[1] > distance_list[vertex] and distance_list[vertex] >= 0):
                    current_vertex = (vertex, distance_list[vertex])

            #removes the vertex with the lowest distance from the vertex list
            #print(current_vertex)
            #print(vertex_list)
            vertex_list.remove(current_vertex[0])

            neighbour_graph = []
            for item in self.edge_tuple:
                vertices = methods.elegant_unpair(item[0])
                if  vertices[0] == current_vertex[0] and vertices[1] in vertex_list:
                    neighbour_graph.append((vertices, item[1]))
                if vertices[1] == current_vertex[0] and vertices[0] in vertex_list:
                    neighbour_graph.append(((vertices[1], vertices[0]), item[1]))    

            for neighbour in neighbour_graph:
                alternative_route = current_vertex[1] + neighbour[1]
                #print('alt route len:', alternative_route)
                if distance_list[neighbour[0][1]] < 0 or alternative_route < distance_list[neighbour[0][1]]:
                    #print(distance_list[neighbour[0][1]])
                    distance_list[neighbour[0][1]] = alternative_route
                    previous_node_list[neighbour[0][1]] = current_vertex[0]
        #print(previous_node_list)
        #print(distance_list)
        return previous_node_list, distance_list

    def dijkstra_to_directions(self, target, previous_node_list):
        edge_list_vertex = []
        while previous_node_list[target] != -1:
            edge_list_vertex.append((target, previous_node_list[target]))
            target = previous_node_list[target]

        edge_list_vertex = list(reversed(edge_list_vertex))
        if len(edge_list_vertex) == 1:
            return [(methods.elegant_unpair(methods.elegant_pair(edge_list_vertex[0])))] #easiest way to make sure the tuple is from lowest number to highest number since these are just some simple calculations where as since its a tuple this would take alot of processing to do any other way

        edge_list_paired = []
        for i in range(1, len(edge_list_vertex)):
            edge_list_paired.append((methods.elegant_pair(edge_list_vertex[i-1]), methods.elegant_pair(edge_list_vertex[i])))

        edge_list_orientated = []
        for item in edge_list_paired:
            for orientated_item in self.edgeconnections_tuple:
                if item == (orientated_item[0], orientated_item[1]):
                    edge_list_orientated.append(((methods.elegant_unpair(item[0]), methods.elegant_unpair(item[1])), orientated_item[2]))
                    break
                elif item == (orientated_item[1], orientated_item[0]):
                    edge_list_orientated.append(((methods.elegant_unpair(item[0]), methods.elegant_unpair(item[1])), orientated_item[2] * -1))
                    break
            else:
                edge_list_orientated.append(((methods.elegant_unpair(item[0]), methods.elegant_unpair(item[1])), 0))

        return edge_list_orientated

    def shortest_way_multiple_points(self, node_list):
        permutations = list(itertools.permutations(node_list))
        length = 0
        shortest_permutation = 0
        for permutation in permutations:
            permutation += (0, )  
            #print('permutation: ', permutation)
            direction_dicts_list = []
            last_node = 0
            temp_length = 0
            for node_id in permutation:
                curr_dict, distance_list = self.dijkstra(last_node)
                direction_dicts_list.append((node_id, curr_dict))
                last_node = node_id
                temp_length += distance_list[node_id]

            #print('length: ', length, 'temp_length: ', temp_length)
            if temp_length < length or shortest_permutation == 0:
                shortest_permutation = direction_dicts_list
                length = temp_length

        dir_list = []
        for item in shortest_permutation:
            #print('items:', item)
            dir_list.append(self.dijkstra_to_directions(item[0], item[1]))
        
        methods.print_list('dir_list: ', dir_list)
        for i in range(0, len(dir_list)): #add the initial move command to each of the movement directions array
            if i == 0: #the first element always starts at 0 and thus needs to add a forward direction to get to 1 from where on the dijkstra will tel the directions
                dir_list[i] = [(((0, 0), (0, 1)), 0)] + dir_list[i]
            index = len(dir_list[i - 1]) - 1
            if type(dir_list[i][0][0]) is int: #check if the robot needs to only move 1 node, the method dijkstra_to_directions will give only a single tuple back in this case instead of the (((), ()), num), this means that the first element is a int instead of another tuple
                if dir_list[i - 1][index][0][1] == dir_list[i][0]: #checks if the robot needs to turn 180 degrees or just drive forward
                    dir_list[i] = [((dir_list[i - 1][index][0][1], dir_list[i][0]), 180)]
                else:
                    dir_list[i] = [((dir_list[i - 1][index][0][1], dir_list[i][0]), 0)]
            elif i == 0 and type(dir_list[i][1][0]) is int: #same as previous if statement but filters out if its the first element which would mean that the first if statment has added an item to the list even though the single tuple still needs replacing
                if dir_list[i - 1][index][0][1] == dir_list[i][0]: #checks if the robot needs to turn 180 degrees or just drive forward
                    dir_list[i] = [((dir_list[i - 1][index][0][1], dir_list[i][1]), 180)]
                else:
                    dir_list[i] = [((dir_list[i - 1][index][0][1], dir_list[i][1]), 0)]
            elif not i ==  0: # cant make this an else statement since i need to check both if statements and both if statements also need to be false to be able to do this statement
                if dir_list[i - 1][index][0][1] == dir_list[i][0][0][0]: #checks if the robot needs to turn 180 degrees or just drive forward
                    dir_list[i] = [((dir_list[i - 1][index][0][1], dir_list[i][0][0][0]), 180)] + dir_list[i]
                else:
                    dir_list[i] = [((dir_list[i - 1][index][0][1], dir_list[i][0][0][0]), 0)] + dir_list[i]

            if i == len(dir_list) - 1: #turn the robot around when arriving back at the starting point
                dir_list[i].append((((0, 0), (0, 0)), 180)) 
        
        return shortest_permutation, dir_list

    def robot_directions(self, node_list):
        return_list = []
        #print('node list:', node_list)
        shortest_permutation, dir_list = self.shortest_way_multiple_points(node_list)
        for dir_list in dir_list:
            temp_list = []
            for item in dir_list:
                temp_list.append(item[1])
            return_list.append(temp_list)
        return shortest_permutation, return_list

if __name__ == '__main__':
    finder = PathFinding(DatabaseConnector())
    methods.print_list('path for 19, 20 and 7 is', finder.robot_directions([19, 20, 7]))
