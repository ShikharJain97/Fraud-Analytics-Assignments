from pypragmatic import Vertex, Graph

class PageRankVertex(Vertex):
    def __init__(self, id, trust_score):
        super().__init__(id)
        self.trust_score = trust_score
        self.incoming_links = set()
        
    def compute(self, context):
        incoming_trusted_links = {v for v in self.incoming_links if v.trust_score > 0}
        trust_score = sum(v.trust_score for v in incoming_trusted_links)
        trust_score = (1 - damping_factor) + damping_factor * trust_score
        trust_score /= context.global_avg_trust_score
        
        if abs(trust_score - self.trust_score) > tolerance:
            self.trust_score = trust_score
            for v in self.out_neighbors:
                v.activate()

class PageRankGraph(Graph):
    def __init__(self, vertices):
        super().__init__(vertices)
        self.global_avg_trust_score = 0.0
        
    def compute(self, vertex):
        self.global_avg_trust_score += vertex.trust_score / len(self.vertices)
        
    def reduce(self):
        pass

# Initialize all pages with an equal trust score of 0
# Set the trust score of each page in seed_pages to 1
vertices = []
for page in all_pages:
    trust_score = 1 if page in seed_pages else 0
    vertices.append(PageRankVertex(page, trust_score))

# Create the graph and run the PageRank algorithm
graph = PageRankGraph(vertices)
graph.run()
trust_scores = {v.id: v.trust_score for v in graph.vertices}

