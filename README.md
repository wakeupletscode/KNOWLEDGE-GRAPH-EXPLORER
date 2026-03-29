# 🕸️ Knowledge Graph Builder

Automatically construct, analyze, and visualize knowledge graphs from any Wikipedia topic using NLP and graph theory.

---

## 📌 Overview

This tool takes a Wikipedia topic as input, extracts entities and relationships from the article text using spaCy dependency parsing, and builds a directed knowledge graph. It then runs graph analytics to surface the most important entities and renders two types of visualizations — a static matplotlib graph and an interactive PyVis network.

---

## ✨ Features

- 🔍 **Entity Extraction** — Extracts subject-object pairs from sentences using spaCy NLP
- 📊 **Graph Analytics** — Computes PageRank and Degree Centrality to rank entities
- 🖼️ **Static Visualization** — Matplotlib graph with centrality-based node sizing
- 🌐 **Interactive Visualization** — Dark-themed PyVis network (filtered to top 60 nodes by PageRank), saved as HTML
- 🔎 **CLI Query Engine** — Explore any entity's incoming and outgoing connections interactively

---
# User Input : "Paracetamol"

## 📸 Screenshots

### Static Graph (Matplotlib)
<img width="1105" height="812" alt="image" src="https://github.com/user-attachments/assets/72712a19-622d-40bb-b485-05021a46ecde" />


### Interactive Graph (PyVis)
<img width="1112" height="748" alt="image" src="https://github.com/user-attachments/assets/ea301da8-9caf-4c1a-a555-9e32c14a00ab" />


---
## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `spaCy` | NLP / dependency parsing |
| `NetworkX` | Graph construction & analytics |
| `PyVis` | Interactive graph visualization |
| `Matplotlib` | Static graph visualization |
| `Wikipedia API` | Article text retrieval |
| `Pandas` | Entity pair storage & deduplication |

---

## ⚙️ Setup

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/knowledge-graph-builder.git
cd knowledge-graph-builder
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Download the spaCy language model**
```bash
python -m spacy download en_core_web_sm
```

> ⚠️ This step is required and is not handled by `requirements.txt`.

---

## 🚀 Usage

```bash
python main.py
```

You'll be prompted to enter a Wikipedia topic:

```
Enter Wikipedia topic: Artificial Intelligence
```

The script will:
1. Fetch and clean the Wikipedia article
2. Extract entity pairs and build the graph
3. Print top 5 entities by Degree Centrality and PageRank
4. Display the matplotlib graph
5. Save an interactive HTML graph as `knowledge_graph_dark.html`
6. Launch the CLI query engine

### CLI Query Engine

```
--- Knowledge Graph Query Engine ---
Enter entity: intelligence

Connections for 'intelligence':

→ Outgoing Relations:
    intelligence → tasks
    intelligence → systems

← Incoming Relations:
    AI → intelligence
```

Type `list` to see available entities, `exit` to quit.

---

## 📂 Project Structure

```
knowledge-graph-builder/
│
├── main.py                     # Main script
├── requirements.txt            # Python dependencies
├── knowledge_graph_dark.html   # Generated interactive graph (after running)
├── screenshots/
│   ├── matplotlib_graph.png    # Static graph screenshot
│   └── pyvis_graph.png         # Interactive graph screenshot
└── README.md
```

---

## 📝 Notes

- Wikipedia articles with disambiguation pages may throw an error — try a more specific topic name
- Very short articles may produce sparse graphs with few entity pairs
- The interactive HTML file can be opened in any browser — no server needed

---

## 📄 License

MIT License
