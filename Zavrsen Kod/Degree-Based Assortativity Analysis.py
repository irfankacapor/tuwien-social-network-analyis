import networkx as nx
import pandas as pd

# First step was to load the dataset containing directed edge data between users.
# This dataset was chosen because it includes detailed information about user interactions:
# - Source and target user IDs define directed relationships,
# - Weight values represent the strength of these relationships.
directed_edge_list_path = "../shared/194.050-2024W/Data/Group_Project/df_edge_list_directed_users_combined_postings_replies_and_votes_to_postings_net.parquet"
directed_edges = pd.read_parquet(directed_edge_list_path)

# Next step was to make sure that the dataset has been loaded correctly, by displaying first few rows and the shape of the dataset
directed_edges.head(), directed_edges.shape

# Afterwards the idea was to create a directed graph using the NetworkX library. 
# Directed graphs are used here because the direction of interactions (e.g., who initiated vs. received) is useful for the analysis.
G_directed = nx.DiGraph()

# Then edges were added to the graph based on the loaded dataset, with 
# interaction direction (from source to target) and weights included (to represent the strength of relationships).
for _, row in directed_edges.iterrows():
    G_directed.add_edge(
        row["ID_CommunityIdentity_Source"],
        row["ID_CommunityIdentity_Target"],
        weight=row["weight_total"]
    )

# Afterwards the degrees for each node in the graph were calculated. This helps quantify user activity:
# - In-degree indicates how many interactions a user receives and their popularity.
# - Out-degree reflects how many interactions a user initiates and their activity level.
# - Total degree captures overall engagement in the network.
in_degrees = dict(G_directed.in_degree(weight='weight'))
out_degrees = dict(G_directed.out_degree(weight='weight'))
total_degrees = {node: in_degrees[node] + out_degrees[node] for node in G_directed.nodes()}

# Lastly the assortativity coefficients for the graph were calculated.
# Assortativity measures whether nodes with similar properties (e.g., degree) tend to connect.
# In-degree assortavity measures whether users who receive many interactions tend to receive interactions from similarly popular users.
# Out-degree assortavity measures whether highly active users (initiating many interactions) tend to connect with other highly active users.
# Calculated values: In-degree assortativity: -0.04514232732989388, Out-degree assortativity: -0.08632228318843047
in_degree_assortativity = nx.degree_assortativity_coefficient(G_directed, x='in', y='in', weight='weight')
out_degree_assortativity = nx.degree_assortativity_coefficient(G_directed, x='out', y='out', weight='weight')

in_degree_assortativity, out_degree_assortativity