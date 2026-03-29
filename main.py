import spacy
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import wikipedia
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Get Wikipedia topic
topic = input("Enter Wikipedia topic: ")
wiki_page = wikipedia.page(topic)
text = wiki_page.content

# Clean text
text = re.sub(r'==.*?==+', '', text)
text = text.replace('\n', ' ')

# Extract entity pairs
def extract_entities(sentence):
    doc = nlp(sentence)
    subject = ""
    obj = ""
    for token in doc:
        if "subj" in token.dep_:
            subject = token.text
        if "obj" in token.dep_:
            obj = token.text
    return subject, obj

sentences = [sent.text for sent in nlp(text).sents]

data = []
for sentence in sentences:
    subj, obj = extract_entities(sentence)
    if subj and obj:
        data.append((subj, obj, sentence))

kg_df = pd.DataFrame(data, columns=["source", "target", "relation"])

# Clean graph
kg_df = kg_df.drop_duplicates()
kg_df = kg_df[kg_df["source"] != kg_df["target"]]

# Build graph
G = nx.from_pandas_edgelist(kg_df, "source", "target", create_using=nx.DiGraph())

# Graph Analytics
degree_centrality = nx.degree_centrality(G)
pagerank_scores = nx.pagerank(G)

print("\nTop 5 Entities by Degree Centrality:")
for node, score in sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(node, score)

print("\nTop 5 Entities by PageRank:")
for node, score in sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(node, score)

# Visualization
node_sizes = [degree_centrality[node] * 4000 for node in G.nodes()]

plt.figure(figsize=(12,8))
pos = nx.spring_layout(G)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=node_sizes,
    node_color="skyblue",
    edge_color="gray",
    font_size=8
)

plt.title("Knowledge Graph with Centrality-Based Scaling")
plt.show()

def visualize_pyvis(G, pagerank_scores, output_file="knowledge_graph_dark.html"):
    from pyvis.network import Network
    import os

    # Get top 60 nodes by PageRank for filtering
    top_nodes = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:60]
    important_set = set(node for node, _ in top_nodes)

    # Build filtered graph using only edges connected to important nodes
    edges_to_keep = [
        (u, v) for u, v in G.edges()
        if u in important_set or v in important_set
    ]
    G_filtered = nx.DiGraph()
    G_filtered.add_edges_from(edges_to_keep)

    # Create network with dark theme
    net = Network(
        height="750px",
        width="100%",
        bgcolor="#111111",
        font_color="white",
        directed=True
    )

    most_important = top_nodes[0][0]

    # Normalize PageRank for size scaling
    max_pr = max(pagerank_scores.values())
    min_pr = min(pagerank_scores.values())

    def scale_size(pr):
        return 12 + ((pr - min_pr) / (max_pr - min_pr)) * 25

    # Add nodes
    for node in G_filtered.nodes():
        size = scale_size(pagerank_scores[node]) if node in pagerank_scores else 12

        if node == most_important:
            net.add_node(node, label=node, size=45, color="#ff4d4d", font={"color": "white"})
        else:
            net.add_node(node, label=node, size=size, color="#1f77ff", font={"color": "white"})

    # Add edges
    for u, v in G_filtered.edges():
        if u == most_important or v == most_important:
            net.add_edge(u, v, width=4, color="#ffffff")
        else:
            net.add_edge(u, v, width=2, color="#888888")

    # Improve spacing
    net.barnes_hut(
        gravity=-8000,
        central_gravity=0.3,
        spring_length=150,
        spring_strength=0.05,
        damping=0.09
    )

    net.write_html(output_file)
    print("Graph saved at:", os.path.abspath(output_file))

visualize_pyvis(G, pagerank_scores)

def query_entity(G):
    if G.number_of_nodes() == 0:
        print("Graph is empty. No entities to query.")
        return

    print("\n--- Knowledge Graph Query Engine ---")
    print("Type an entity name to explore its connections.")
    print("Type 'list' to see some available entities.")
    print("Type 'exit' to quit.\n")

    # Create lowercase mapping for case-insensitive search
    node_map = {node.lower(): node for node in G.nodes()}

    while True:
        user_input = input("Enter entity: ").strip().lower()

        if user_input == "exit":
            print("Exiting query engine.")
            break

        if user_input == "list":
            print("\nSample Available Entities:")
            for node in list(G.nodes())[:20]:
                print("-", node)
            print()
            continue

        if user_input in node_map:
            actual_node = node_map[user_input]

            print(f"\nConnections for '{actual_node}':\n")

            # Outgoing edges
            outgoing = list(G.successors(actual_node))
            incoming = list(G.predecessors(actual_node))

            if outgoing:
                print("→ Outgoing Relations:")
                for neighbor in outgoing:
                    print("   ", actual_node, "→", neighbor)
            else:
                print("→ No outgoing relations.")

            if incoming:
                print("\n← Incoming Relations:")
                for neighbor in incoming:
                    print("   ", neighbor, "→", actual_node)
            else:
                print("\n← No incoming relations.")

            print()

        else:
            print("Entity not found. Type 'list' to see available entities.\n")
query_entity(G)
