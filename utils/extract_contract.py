import json
import networkx as nx
import matplotlib.pyplot as plt
from datasets import load_dataset
import random

def build_ast_graph(node, graph, parent_id=None):
    if not isinstance(node, dict):
        return
        
    node_id = node.get('id', id(node))
    node_name = node.get('name', 'Unknown')
    
    if node_name == 'ContractDefinition':
        node_name = 'ContractDef'
    elif node_name == 'FunctionDefinition':
        node_name = 'FunctionDef'
    elif node_name == 'VariableDeclaration':
        node_name = 'VariableDecl'
    elif node_name == 'ElementaryTypeName':
        node_name = 'ElemTypeName'
    elif node_name == 'ExpressionStatement':
        node_name = 'ExprStatement'
    
    graph.add_node(node_id, label=node_name)
    
    if parent_id is not None:
        graph.add_edge(parent_id, node_id)
        
    for child in node.get('children', []):
        build_ast_graph(child, graph, node_id)

def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        parsed.append(root)
        neighbors = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            neighbors.remove(parent)
            
        if len(neighbors) != 0:
            dx = width / len(neighbors)
            nextx = xcenter - width/2 - dx/2
            for neighbor in neighbors:
                nextx += dx
                pos = _hierarchy_pos(G, neighbor, width=dx, vert_gap=vert_gap, 
                                     vert_loc=vert_loc-vert_gap, xcenter=nextx,
                                     pos=pos, parent=root, parsed=parsed)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

ds = load_dataset("JakeClark/soliaudit-dasp-ast-graph", split="train")
target_address = "0xa82749c94ab7f921725624fb90e7600216169597"

for item in ds:
    if target_address in item.get('address', ''):
        ast_str = item.get('AST', '')
        try:
            ast_dict = json.loads(ast_str)
            
            G = nx.DiGraph()
            build_ast_graph(ast_dict, G)
            
            plt.figure(figsize=(8, 10))
            
            # Find root (node with in-degree 0)
            root = [n for n, d in G.in_degree() if d == 0][0]
            pos = hierarchy_pos(G, root)
            
            labels = nx.get_node_attributes(G, 'label')
            
            nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, arrowstyle='->', edge_color='#bdc3c7', width=2.0)
            
            bbox_props = dict(boxstyle="round,pad=0.5", fc="#3498db", ec="none")
            nx.draw_networkx_labels(G, pos, labels=labels, font_size=9, font_weight='bold', font_color='white', bbox=bbox_props)
            
            # Disable axes
            plt.axis('off')
            plt.title("Abstract Syntax Tree", fontsize=16, pad=20)
            
            # Add some padding around the graph so boxes don't get cut off
            x_values, y_values = zip(*pos.values())
            x_min, x_max = min(x_values), max(x_values)
            y_min, y_max = min(y_values), max(y_values)
            plt.xlim(x_min - 0.2, x_max + 0.2)
            plt.ylim(y_min - 0.1, y_max + 0.1)

            out_path = '/home/jc/code_projects/smart_contract_detection_xAI/results/images/ast_example.png'
            plt.savefig(out_path, dpi=300, bbox_inches='tight')
            print(f"Graph saved to {out_path}")
        except Exception as e:
            print("Error:", e)
        break
