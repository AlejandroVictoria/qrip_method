import numpy as np

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
            4: "table_automata4.txt"
        }

        if selection == 1:
            self.final_state = 7
        elif selection == 2:
            self.final_state = 14
        elif selection == 3:
            self.final_state = 3
        elif selection == 4:
            self.final_state = 3

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
    print("Automata que analiza cadenas de notación exponencial: 1.1e+10")
    obj1 = tabAutomata(1)
    print("\n-------------------------------------------------------------------------------------------------")
    print("--------------------------------------Ejemplo Correcto------------------------------------------")
    print("-------------------------------------------------------------------------------------------------")
    print("Cadena muestra: 3232.23234e+10")
    obj1.print_properties()