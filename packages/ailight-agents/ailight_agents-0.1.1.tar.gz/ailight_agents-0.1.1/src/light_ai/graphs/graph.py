from typing import Any, Dict, Callable, List, Optional

class GraphState(dict):
    """
    Un dizionario specializzato per mantenere lo stato del grafo.
    Permette di accedere agli elementi sia come attributi che come chiavi.
    Esempio: state.messages è equivalente a state['messages']
    """
    def __getattr__(self, key: str) -> Any:
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'GraphState' object has no attribute '{key}'")

    def __setattr__(self, key: str, value: Any):
        self[key] = value
        

# Un "Nodo" è semplicemente una funzione o un oggetto chiamabile
# che accetta uno stato e restituisce uno stato aggiornato.
NodeCallable = Callable[[GraphState], Dict[str, Any]]

# Un "Arco Condizionale" è una funzione che accetta lo stato
# e restituisce il nome del prossimo nodo da eseguire.
ConditionalEdge = Callable[[GraphState], str]

class Graph:
    def __init__(self):
        self.nodes: Dict[str, NodeCallable] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, ConditionalEdge] = {}
        self.entry_point: Optional[str] = None
        self.end_points: List[str] = []

    def add_node(self, name: str, action: NodeCallable):
        """Aggiunge un nodo (un agente o un tool) al grafo."""
        self.nodes[name] = action

    def add_edge(self, start_node: str, end_node: str):
        """Aggiunge un arco normale tra due nodi."""
        self.edges[start_node] = end_node

    def add_conditional_edge(self, start_node: str, logic: ConditionalEdge):
        """Aggiunge un arco la cui destinazione è decisa da una funzione logica."""
        self.conditional_edges[start_node] = logic
        
    def set_entry_point(self, node_name: str):
        """Imposta il nodo di partenza."""
        self.entry_point = node_name

    def set_end_point(self, node_name: str):
        """Definisce un nodo come punto di terminazione."""
        self.end_points.append(node_name)

    def run(self, initial_input: Dict[str, Any]) -> GraphState:
        """Esegue il grafo a partire da un input iniziale."""
        if not self.entry_point:
            raise ValueError("Il punto di ingresso (entry point) non è stato impostato.")

        state = GraphState(initial_input)
        current_node_name = self.entry_point

        while current_node_name not in self.end_points:
            print(f"--- Esecuzione Nodo: {current_node_name} ---")
            
            node_action = self.nodes.get(current_node_name)
            if not node_action:
                raise ValueError(f"Nodo '{current_node_name}' non trovato.")

            # Esegui l'azione del nodo e aggiorna lo stato
            updates = node_action(state)
            state.update(updates)

            # Decide il prossimo passo
            if current_node_name in self.conditional_edges:
                next_node_name = self.conditional_edges[current_node_name](state)
            elif current_node_name in self.edges:
                next_node_name = self.edges[current_node_name]
            else:
                # Se non ci sono archi definiti, il grafo termina
                break
            
            current_node_name = next_node_name

        print("--- Grafo Terminato ---")
        return state