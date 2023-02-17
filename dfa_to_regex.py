from typing import Tuple, Set, Union
class Automaton:
    def __init__(self) -> None:
        self.transition_function: Dict[str, Dict[str, str]] = {}
        self.start_state: Optional[str] = None
        self.end_states: Set[str] = set()
        self.alphabet: Set[str] = set()

def assignment(n: int) -> Tuple[bool, str]:
    automaton = Automaton()
    automaton.start_state = "z"
    automaton.alphabet = {"1", "0"}
    automaton.end_states = {"q0"}
    
    if n == 1:
        reg = r'^[01]+$'
        return False, reg
    
    if n == 1:
        automaton.transition_function = {"z": {"0": "q0", "1": "q0"}}
    elif n != 1:
        automaton.transition_function = {"z": {"0": "q0", "1": "q1"}}
    
    # Generates DFA transitions for every binary number divisible by "n"
    for state in range(n):
        state_name = 'q' + str(state)
        automaton.transition_function[state_name] = {}
        for digit in [0, 1]:
            next_state = (2 * state + digit) % n
            next_state_name = 'q' + str(next_state)
            automaton.transition_function[state_name][str(digit)] = next_state_name    
    
    # The first step is that you create a new initial state from which an epsilon step leads 
    # to all previous initial states, and a new accepting state that epsilon steps from each 
    # previously accepting state lead to.
    new_start_state = "I"
    new_accept_state = "F"

    automaton.transition_function[new_start_state] = {'': automaton.start_state}

    for accept_state in automaton.end_states:
        automaton.transition_function[accept_state][''] = new_accept_state

    # Create a list for every intermediate state we want to remove
    states = []
    states.append(new_start_state)
    for i in automaton.transition_function:
        if i != new_start_state:
            states.append(i)

    # The next step of the algorithm will be repeated in a loop. We repeat these steps until our automaton has only 2 states,
    # namely the 2 new ones we added. Our regex will be the word through which we pass from the initial state to our new accepting state.
    while len(states) > 2:
        
        for state in states[::-1]:
            current_state = state
            in_states = []
            out_states = []
            loop = ''

            # Appending different values for each state.
            for i in states:
                if i == current_state:
                    for key, value in automaton.transition_function[i].items():
                        if value == current_state:
                            loop = f"({key})*"
                            continue
                        out_states.append(key)
                        out_states.append(value)
                for key in automaton.transition_function[i]:
                    if i == current_state:
                        continue
                    if automaton.transition_function[i][key] == current_state:
                        in_states.append(key)
                        in_states.append(i)

            whole_in_states = in_states[:]
            whole_out_states = out_states[:]
            # Repeat until there is not a single state coming to our state.
            while len(in_states) != 0:

                # We choose a state that we reduce by saying that for all combinations X, Y, where X is a transition from some state (different from ours), 
                # we name it A through the word p to our chosen state and Y is a transition from our chosen state to another state (different from ours), 
                # continue B through word q, create a new transition from state A to state B through word pq (p concatenated with q), and remove our chosen state, 
                # along with all transitions to and from it. If our selected state had a transition into itself through some word x, then instead of pq, 
                # all transitions are in the form px*q (p, concatenated with any number of x, concatenated with q).
                for state in in_states[1::2]:
                    
                    try:
                        if flag:
                            state = go_again
                            flag = False
                    except:
                        pass

                    if state in out_states:
                        
                        in_index = in_states.index(state)
                        out_index = out_states.index(state)
                        reg = f"({in_states[in_index-1]}{loop}{out_states[out_index-1]})"
                        
                        keys_values = []
                        
                        for key, value in automaton.transition_function[in_states[in_index]].items():
                            keys_values.append(key)
                            keys_values.append(value)
                        if state in keys_values:
                            index = keys_values.index(state)
                            together = keys_values[index-1]
                            del automaton.transition_function[state][together]
                            automaton.transition_function[in_states[in_index]][f"(({together}|{reg})*)"] = state
                        else:
                            automaton.transition_function[in_states[in_index]][f"{reg}*"] = state

                        if len(in_states[1::2]) == 1:
                            out_states.remove(out_states[out_index])
                            out_states.remove(out_states[out_index-1])
                        elif ((state in out_states) and (len(out_states[1::2]) != 1)):
                            go_again = state
                            out_states.remove(out_states[out_index])
                            out_states.remove(out_states[out_index-1])
                            flag = True
                            break
                        else:
                            in_states.remove(in_states[in_index])
                            in_states.remove(in_states[in_index-1])

                    if state not in out_states:

                        in_index = in_states.index(state)

                        for out_state in out_states[1::2]:
                            out_index = out_states.index(out_state)

                            reg = f"({in_states[in_index-1]}{loop}{out_states[out_index-1]})"
                            
                            keys_values = []
                            for key, value in automaton.transition_function[in_states[in_index]].items():
                                keys_values.append(key)
                                keys_values.append(value)

                            if out_states[out_index] in keys_values:
                                index = keys_values.index(out_state)
                                together = keys_values[index-1]
                                del automaton.transition_function[in_states[in_index]][together]
                                automaton.transition_function[in_states[in_index]][f"({together}|{reg})"] = out_states[out_index]
                            else:
                                automaton.transition_function[in_states[in_index]][reg] = out_state
                        
                        in_states.remove(in_states[in_index])
                        in_states.remove(in_states[in_index-1])

                            
             # Finally, we delete this state from our transitions, since we no longer need it.
             # We no longer have this state in our whole transitions.
            del automaton.transition_function[current_state]
            states.remove(current_state)
            
            # Also deleting every previous transition to our state, since we created new one
            for state in automaton.transition_function:
                for key, value in list(automaton.transition_function[state].items()):
                    if value == current_state:
                        del automaton.transition_function[state][key]
            
            #To see how this code works you can print it and take your time

            # print(f"\nState: {current_state}")
            # print(f"IN: {whole_in_states}")
            # print(f"OUT: {whole_out_states}")
            # print(f"LOOP: {loop}")
            # print(f"New transitions: {automaton.transition_function}\n")

    reg = out_states[0]
    regex = f"^{reg}$"

    return regex

reg = assignment(3)
print(reg)
