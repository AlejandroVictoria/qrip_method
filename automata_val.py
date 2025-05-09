import numpy as np
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import graphviz


class tabAutomata:
    def __init__(self, selection):
        self.initial_state = 1
        self.final_state = ""
        self.transition_function = {}
        self.states = {}
        self.len_symbols = ""
        self.alphabet = []
        self.selection = selection
        self.path = {
            1: "table_automata1.txt",
            2: "table_automata2.txt",
            3: "table_automata3.txt",
            4: "table_automata4.txt",
            5: "table_automata5.txt"
        }

        self.graph_repr = nx.DiGraph()
        self.labels = defaultdict()
        self.qrip_transition = None
        self.qrip_start = 0
        self.qrip_final = 0
        self.regex_list = {}

        if selection == 1:
            self.final_state = 7
        elif selection == 2:
            self.final_state = 14
        elif selection == 3:
            self.final_state = 3
        elif selection == 4:
            self.final_state = 3
        elif selection == 5:
            self.final_state = 4
        self.loading_automata()


    def read_transition(self):
        path = self.path[self.selection]

        with open(path, "r") as file:
            data = file.readlines()
            count_charray = data[0].split(",")                                  #Crea un array con los elementos de la cadena cortando las comas en ella.
            len_alphabet = len(count_charray) - 1                               #Del array creado siempre habrá dos elementos extras, el espacio en blanco dejado a propósito y el salto de línea al final.
            array_data = np.empty((0, len_alphabet))

            for line in data:
                i = 0
                array_row = np.array([[]])
                line = line.split(",")

                while i < len(line) - 1:
                    array_row = np.append(array_row, [line[i]])
                    i += 1

                array_data = np.append(array_data, [array_row], axis=0)
        
        self.error_state = len(data) - 1
        return array_data
    
    def creating_graph(self):
        m,n = np.shape(self.transition_function)

        for q_state in range(m):
            for q_transition in range(n):
                if q_state > 0 and q_transition > 0:
                    # Adding nodes and edges to graph
                    t_state = int(self.transition_function[q_state, q_transition])
                    self.graph_repr.add_edge(q_state, t_state)

                    alphabet = self.transition_function[0, q_transition]
                    
                    if (q_state, t_state) in self.labels.keys():
                        self.labels[(q_state, t_state)] = self.labels[(q_state, t_state)] + alphabet
                    else:
                        self.labels[(q_state, t_state)] = alphabet

        # print(self.labels)

        return None

    def plotting_graph(self):
        pos = nx.spring_layout(self.graph_repr)
        fig, ax = plt.subplots(figsize=(1,1))

        nx.draw(
            self.graph_repr, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in self.graph_repr.nodes()}
            )
        
        nx.draw_networkx_edge_labels(
            self.graph_repr, pos,
            edge_labels= self.labels,
            font_color='red'
        )

        plt.axis('off')
        plt.show()
        return None
    
    def visualize_graph(self, transition_matrix, viz = '0'):
        m,n = np.shape(transition_matrix)
        print("Transition matrix:\n", self.qrip_transition)
        # print(m,n)
        graph = graphviz.Digraph(comment="DFA")
        labels = {}
        regex_list = self.regex_list.copy()

        for i in range(m):
            if i > 0:
                q_state = int(transition_matrix[i,0])
                for j in range(n):
                    if j > 0:
                        # Creating adjacency list with alphabet values
                        t_state = int(transition_matrix[i,j])
                        # self.graph_repr.add_edge(q_state, t_state)
                        alphabet = transition_matrix[0, j]

                        
                        if t_state != 5:
                            labels[(q_state, t_state)] = alphabet

                # Adding nodes to graph vis
                node = "q" + str(t_state)
                if t_state != 5:
                    graph.node(node, node)

                # Marking the final state
                if transition_matrix[i,j] == str(self.final_state):
                    graph.node(node, node, shape='doublecircle')


        #print(labels)
        # Adding edges to graph
        for source,destiny in labels.keys():
            # if self.regex_list != {}:
                
            if (str(source),str(destiny)) in regex_list.keys():
                graph.edge("q{}".format(source),"q{}".format(destiny), regex_list[(str(source),str(destiny))])
                regex_list.pop((str(source),str(destiny)))
            else:
                graph.edge("q{}".format(source),"q{}".format(destiny), labels[(source,destiny)])

        for keys in regex_list.keys():
            graph.edge("q{}".format(keys[0]),"q{}".format(keys[1]), regex_list[keys])
        # Rendering graph
        graph.render("DFA" + viz, view=True)
        return None

    def qrip_method(self):
        # Step 1: Adding new start and final states.
        m,n = np.shape(self.transition_function)
        new_start, new_final = np.array([m - 1 for i in range(n)]), np.array([m - 1 for i in range(n)])
        
        for i in range(n):
            # print(self.transition_function[0,i])
            if i == 0:
                new_start[i] = m
                new_final[i] = m + 1
            if self.transition_function[0,i] == "":
                new_start[i] = self.initial_state

        self.qrip_start = m
        self.qrip_final = m + 1
        self.qrip_transition = self.transition_function
        self.qrip_transition = np.append(self.qrip_transition, [new_start], axis=0)
        self.qrip_transition = np.append(self.qrip_transition, [new_final], axis=0)
        # Adding new final state on new transtion matrix
        self.qrip_transition[self.final_state,-1] = new_final[0]
        self.final_state = new_final[0]
        self.visualize_graph(self.qrip_transition)
        
        # Step 2: Ripping states
        m,n = np.shape(self.qrip_transition)

        # Listing all in and out states
        while True:
            qrip = self.qrip_transition[1,0]
            
            if int(qrip) == self.error_state:
                break

            in_states,out_states = {},{}
            # in_states,out_states = [],[]
            m,n = np.shape(self.qrip_transition)
            
            # Defining the next node to be ripped
            for i in range(m):
                for j in range(n):
                    if i > 0 and j > 0:
                        if self.qrip_transition[i,j] == qrip:
                            # if self.re_gex == "" and self.qrip_transition[i,0] != str(self.qrip_start):
                            # if self.re_gex == "":
                            in_states[(self.qrip_transition[i,0], qrip)] = self.qrip_transition[0,j]
                            # else:
                            #     in_states[(self.qrip_transition[i,0], qrip)] = self.re_gex

                            self.qrip_transition[i,j] = self.error_state

                        elif self.qrip_transition[i,0] == qrip and self.qrip_transition[i,j] != str(self.error_state):
                            out_states[(qrip, self.qrip_transition[i,j])] = self.qrip_transition[0,j]

            j = 1

            for k in out_states.keys():
                if k[1] != str(self.error_state):
                    self.qrip_transition[-2,j] = k[1]
                    j += 1

            # print("Qrip:", qrip)
            # # print("Entrada:", in_statess['2'][0])

            # Applying REGEX operators:
            for keys in self.regex_list.keys():
                in_states[keys] = self.regex_list[keys]

            self.regex_list = self.qrip_oper(qrip, in_states, out_states)
            # print("self.regex_list:", self.regex_list)
            # Modifying qrip_transition
            self.qrip_transition = np.delete(self.qrip_transition, (1), axis=0)
            # # print("Transition matrix:\n", self.qrip_transition)
            self.visualize_graph(self.qrip_transition, viz=str(qrip))
            # input()

        return None
    

    def qrip_oper(self, qrip, in_states, out_states):
        in_regex, out_regex = {},[]
        in_regex_str, out_regex_str = "",""
        break_statement = False

        if qrip == str(self.error_state):
            in_regex = self.regex_list
        else:
            for key_in in in_states.keys():
                for key_out in out_states.keys():
                    #Kleen Closure:
                    # print(key_in, key_out)
                    if (key_in[0], key_out[1]) in in_states.keys():
                        in_regex_u = in_states[key_in[0], key_out[1]]
                        for key_val in in_states.keys():
                            if key_val[0] == key_val[1]:
                                in_regex_kleen = "({})*".format(in_states[key_val])
                            if (key_in[0], key_out[1]) != key_val:
                                out_regex.append(in_states[key_val])
                        in_regex[(key_in[0], key_out[1])] = in_regex_u + "U" + out_regex[0] + in_regex_kleen + out_regex[1]
                        break_statement = True
                        break
                    else:
                        if key_in[0] == key_in[1]:
                            in_regex_str = "({})*".format(in_states[key_in])
                        else:
                        #Concatenation:
                            if in_regex_str != "":
                                in_regex[(key_in[0], key_out[1])] = in_states[key_in] + in_regex_str + out_states[key_out]
                            else:
                                in_regex[(key_in[0], key_out[1])] = in_states[key_in] + out_states[key_out]
                    print("Qrip State:", qrip)
                    print("in_regex:", in_regex)
                #Concatenation
                if break_statement:
                    break_statement = False
                    break
        
        # print(in_regex)
        # print(in_states)
        # print(out_states)
        # input("regex")
        return in_regex
    

    def loading_automata(self):
        self.transition_function = self.read_transition()
        # self.transition_function = np.array([
            # [ "", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "e", "+", "-"],
            # ["1", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "8", "8", "8", "8"],
            # ["2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "3", "5", "8", "8"],
            # ["3", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "8", "8", "8", "8"],
            # ["4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "8", "5", "8", "8"],
            # ["5", "7", "7", "7", "7", "7", "7", "7", "7", "7", "7", "7", "8", "8", "6", "6"],
            # ["6", "7", "7", "7", "7", "7", "7", "7", "7", "7", "7", "7", "8", "8", "8", "8"],
            # ["7", "7", "7", "7", "7", "7", "7", "7", "7", "7", "7", "7", "8", "8", "8", "8"],
            # ["8", "8", "8", "8", "8", "8", "8", "8", "8", "8", "8", "8", "8", "8", "8", "8"],
        # ], dtype=str)

        m,n = np.shape(self.transition_function)
        self.states = np.array([element for element in range(1,m)])
        self.len_symbols = n

        return None
    
    def automata_compute(self, input_string):
        transition_states = []
        
        i = int(self.initial_state)
                
        for element in input_string:
            j = 1
            while j < self.len_symbols:
                symbol = self.transition_function[0,j]
                if element == symbol:
                    i = int(self.transition_function[i,j])
                    break
                j += 1
            
            print("Simbolo analizado: {}\nNuevo estado asignado: Q{}.\n".format(symbol,i))
            
            if i == self.error_state:
                print("Se encontró un error. Estado final Q8")
                break

        if i == self.final_state:
            print("Se completó correctamente. Estado final Q7")
        else:
            print("Se generó un error")

    def print_properties(self):
        print(self.transition_function)
        return None

if __name__ == "__main__":
    obj1 = tabAutomata(5)
    obj1.creating_graph()
    #obj1.visualize_graph()
    #obj1.print_properties()
    obj1.qrip_method()
