import random
import math
import Eat.print
import turtle as tt


NUMBER_OF_LAYERS = 2
NUMBER_OF_NODES = 18

MUTATION_CONNECTION_CHANCE = .01
MUTATION_CONNECTION_STRENGTH = .5
visible = 1
input_nodes = (visible *2+1)*(visible *2+1)
# input_nodes = 1
class AI:

    """
    a computer brain
    """

    def __init__(self, player=False):
        """
        creates a brain
        :param player: either a previous player or not
        """
        if not player:
            self.input = range(input_nodes)
            self.layers = Layers()

            # self.output = Layer(-2, 5)
            self.output = Layer(-2, 5)
            connect(self.output, self.layers.layers[len(self.layers.layers) - 1])
        else:
            self.input = range(input_nodes)
            self.layers = Layers(player.layers)
            self.output = Layer(None,None,player.output)

        # to see the player:

        # tt.reset()
        # Eat.print.print_player(self)
        # tt.update()
        # input()
    def choice(self, inpt):
        """
        gets the final answer based on information
        :param position: the input
        :return:
        """
        # fix input
        self.input = []
        for x in range(len(inpt)):
            for y in range(len(inpt)):
                square = inpt[x][y]
                if square is None:
                    self.input.append(0)
                else:
                    self.input.append(square.moss)
        answers = []
        for i in range(len(self.output.nodes)):
            answers.append(self.output.nodes[i].get_answer(self))

        highest = 0
        highest_value = answers[0]
        for i in range(1, len(answers)):
            if answers[i] > highest_value:
                highest = i
                highest_value = answers[i]
        if highest == 0:
            return 'w'
        elif highest == 1:
            return 'a'
        elif highest == 2:
            return 's'
        elif highest == 3:
            return 'd'
        else:
            return 'x'

    def see_choice(self,inpt):
        """
        gets the final answer based on information
        :param position: the input
        :return:
        """
        # fix input
        self.input = []
        for x in range(len(inpt)):
            for y in range(len(inpt)):
                square = inpt[x][y]
                if square is None:
                    self.input.append(0)
                else:
                    self.input.append(square.moss)
        answers = []
        for i in range(len(self.output.nodes)):
            answers.append(self.output.nodes[i].see_answer(self))

        highest = 0
        highest_value = answers[0]
        for i in range(1, len(answers)):
            if answers[i] > highest_value:
                highest = i
                highest_value = answers[i]
        if highest == 0:
            return 'w'
        elif highest == 1:
            return 'a'
        elif highest == 2:
            return 's'
        elif highest == 3:
            return 'd'
        else:
            return 'x'


class Layers:
    """
    the layers of nodes of connections to compute an answer
    """

    def __init__(self, layers=False):
        """
        creates a default set of layers
        """
        if not layers:
            self.layers = []

            for i in range(NUMBER_OF_LAYERS):
                self.layers.append(Layer(i))
                if i > 0:
                    connect(self.layers[i], self.layers[i - 1])
            connect_to_input(self.layers[0])
        else:
            self.layers = []
            for i in range(len(layers.layers)):
                self.layers.append(Layer(False, False, layers.layers[i]))


def connect_to_input(connect_from):
    for node_from in range(len(connect_from.nodes)):
        for node_to in range(input_nodes):
            connect_from.nodes[node_from].connections.append(Connection(-1, node_to, random.random()*2 - 1))


def connect(connect_from, connect_to):
    """
    creates nodes in connect from to addresses of connect_to
    :param connect_from: where the nodes are being created
    :param connect_to: what the nodes are connecting to
    :param connect_to_name: the name of the layer: connect_to
    """
    connect_to_name = connect_to.layer_name
    for node_from in range(len(connect_from.nodes)):
        for node_to in range(len(connect_to.nodes)):
            connect_from.nodes[node_from].connections.append(Connection(connect_to_name, node_to, random.random()*2 - 1))


class Layer:
    """
    a layer in a set of layers of computation
    contains nodes of connections to compute an answer
    """

    def __init__(self, layer_name, num_of_nodes=NUMBER_OF_NODES, layer=False):
        """
        creates a default layer
        :param layer_name: name of this layer
        :param num_of_nodes: the number of nodes this layer should have
        """
        if not layer:
            self.layer_name = layer_name
            self.nodes = []
            for i in range(num_of_nodes):
                self.nodes.append(Node(i))
        else:
            self.nodes = []
            for i in range(len(layer.nodes)):
                self.nodes.append(Node(False, layer.nodes[i]))


class Node:
    """
    a node in a layer in a set of layers of computation
    contains connections to compute an answer
    """

    def __init__(self, node_name, node=False):
        """
        creates a default Node
        :param node_name: the name of this node
        """
        self.color = None
        if isinstance(node, bool):
            self.node_name = node_name
            self.connections = []
        else:
            self.connections = []
            for i in range(len(node.connections)):
                self.connections.append(Connection(False, False, False, node.connections[i]))

    def get_answer(self, brain):
        answer = 0.0
        for connection in self.connections:
            if connection.layer_name == -1:
                answer += brain.input[connection.node_name] * connection.weight
            else:
                answer += brain.layers.layers[connection.layer_name].nodes[connection.node_name].get_answer(
                    brain) * connection.weight
        return answer/NUMBER_OF_NODES

    def see_answer(self, brain):
        answer = 0.0
        for connection in self.connections:
            if connection.layer_name == -1:
                answer += brain.input[connection.node_name] * connection.weight
            else:
                answer += brain.layers.layers[connection.layer_name].nodes[connection.node_name].see_answer(
                    brain) * connection.weight
        self.color = answer
        return answer/NUMBER_OF_NODES


class Connection:
    """
    a connection in a set of nodes in a layer in a set of layers of computation
    contains a layer_name,node_name,and weight
    """

    def __init__(self, layer_name, node_name, weight=1, connection=None):
        if connection is None:
            self.layer_name = layer_name
            self.node_name = node_name
            self.weight = weight
        else:
            self.layer_name = connection.layer_name
            self.node_name = connection.node_name
            self.weight = connection.weight
            if random.random() < MUTATION_CONNECTION_CHANCE:
                self.weight += (random.random()-1) * MUTATION_CONNECTION_STRENGTH
