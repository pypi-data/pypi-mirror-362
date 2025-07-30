from ..pipelines import Tokenizer
from ..score_functions import ScoringFactory


class Topics:
    """
    Topic modeling using community detection.
    """

    def __init__(self, config):
        """
        Creates a new Topics instance.

        Args:
            config: topic configuration
        """

        self.config = config if config else {}
        self.tokenizer = Tokenizer(stopwords=True)

        self.stopwords = set()
        if "stopwords" in self.config:
            self.stopwords.update(self.config["stopwords"])

    def __call__(self, graph):
        """
        Runs topic modeling for input graph.

        Args:
            graph: Graph instance

        Returns:
            dictionary of {topic name: [ids]}
        """

        communities = graph.communities(self.config)

        communities = sorted(communities, key=len, reverse=True)

        centrality = graph.centrality()

        topics = [self.score(graph, x, community, centrality) for x, community in enumerate(communities)]

        return self.merge(topics)

    def score(self, graph, index, community, centrality):
        """
        Scores a community of nodes and generates the topn terms in the community.

        Args:
            graph: Graph instance
            index: community index
            community: community of nodes
            centrality: node centrality scores

        Returns:
            (topn topic terms, topic ids sorted by score descending)
        """

        scoring = ScoringFactory.create({"method": self.config.get("labels", "bm25"), "terms": True})
        scoring.index((node, self.tokenize(graph, node), None) for node in community)

        if scoring.idf:
            idf = sorted(scoring.idf, key=scoring.idf.get)

            topn = self.config.get("terms", 4)

            terms = self.topn(idf, topn)

            community = [uid for uid, _ in scoring.search(terms, len(community))]
        else:
            terms = ["topic", str(index)]

            community = sorted(community, key=lambda x: centrality[x], reverse=True)

        return (terms, community)

    def tokenize(self, graph, node):
        """
        Tokenizes node text.

        Args:
            graph: Graph instance
            node: node id

        Returns:
            list of node tokens
        """

        text = graph.attribute(node, "text")
        return self.tokenizer(text) if text else []

    def topn(self, terms, n):
        """
        Gets topn terms.

        Args:
            terms: list of terms
            n: topn

        Returns:
            topn terms
        """

        topn = []

        for term in terms:
            if self.tokenizer(term) and term not in self.stopwords:
                topn.append(term)

            if len(topn) == n:
                break

        return topn

    def merge(self, topics):
        """
        Merges duplicate topics

        Args:
            topics: list of (topn terms, topic ids)

        Returns:
            dictionary of {topic name:[ids]}
        """

        merge, termslist = {}, {}

        for terms, uids in topics:
            key = frozenset(terms)

            if key not in merge:
                merge[key], termslist[key] = [], terms

            merge[key].extend(uids)

        results = {}
        for k, v in sorted(merge.items(), key=lambda x: len(x[1]), reverse=True):
            results["_".join(termslist[k])] = v

        return results
