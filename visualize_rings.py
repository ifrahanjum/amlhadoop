import re
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
edges_added = 0

with open('scored_fraud_report.txt', 'r') as f:
    for line in f:
        if "FRAUD RING DETECTED" in line:
            accounts = re.findall(r'ACC_[0-9]+', line)
            if len(accounts) == 4:
                # Add the circular edges
                G.add_edge(accounts[0], accounts[1])
                G.add_edge(accounts[1], accounts[2])
                G.add_edge(accounts[2], accounts[3])
                edges_added += 1
        # Limit to 30 rings to keep the graph readable
        if edges_added >= 30:
            break

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.6, iterations=60)

nx.draw_networkx_nodes(G, pos, node_color='#ff7f7f', node_size=600, edgecolors='darkred')
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=18, connectionstyle="arc3,rad=0.15")
nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif', font_weight='bold')

plt.title("Automated AML Detection: Critical Circular Smurfing Rings", fontsize=16, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig('aml_network_map.png', dpi=300)
print("[*] Successfully generated aml_network_map.png")
