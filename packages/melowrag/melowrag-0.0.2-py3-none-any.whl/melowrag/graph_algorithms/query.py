# Copyright 2025 The MelowRAG Author @erfanzar (Erfan Zare Chavoshi).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import re

try:
    from grandcypher import GrandCypher  # type:ignore

    GRANDCYPHER = True
except ImportError:
    GRANDCYPHER = False

logger = logging.getLogger(__name__)


class Query:
    """
    Runs openCypher graph queries using the GrandCypher library. This class also supports search functions.
    """

    SIMILAR = "__SIMILAR__"

    def __init__(self):
        """
        Create a new graph query instance.
        """

        if not GRANDCYPHER:
            raise ImportError('GrandCypher is not available - install "graph" extra to enable')

    def __call__(self, graph, query, limit):
        """
        Runs a graph query.

        Args:
            graph: graph instance
            query: graph query, can be a full query string or a parsed query dictionary
            limit: number of results

        Returns:
            results
        """

        attributes, uids = None, None

        if isinstance(query, dict):
            query, attributes, uids = self.build(query)

        if uids:
            graph = self.filter(graph, attributes, uids)

        logger.debug(query)

        return GrandCypher(graph.backend, limit if limit else 3).run(query)

    def isquery(self, queries):
        """
        Checks a list of queries to see if all queries are openCypher queries.

        Args:
            queries: list of queries to check

        Returns:
            True if all queries are openCypher queries
        """

        return all(query and query.strip().startswith("MATCH ") and "RETURN " in query for query in queries)

    def parse(self, query):
        """
        Parses a graph query. This method supports parsing search functions and replacing them with placeholders.

        Args:
            query: graph query

        Returns:
            parsed query as a dictionary
        """

        where, limit, nodes, similar = None, None, [], []

        match = re.search(r"where(.+?)return", query, flags=re.DOTALL | re.IGNORECASE)
        if match:
            where = match.group(1).strip()

        match = re.search(r"limit\s+(\d+)", query, flags=re.DOTALL | re.IGNORECASE)
        if match:
            limit = match.group(1)

        for x, match in enumerate(re.finditer(r"similar\((.+?)\)", query, flags=re.DOTALL | re.IGNORECASE)):
            query = query.replace(match.group(0), f"{Query.SIMILAR}{x}")

            params = [param.strip().replace("'", "").replace('"', "") for param in match.group(1).split(",")]
            nodes.append(params[0])
            similar.append(params[1:])

        return {
            "query": query,
            "where": where,
            "limit": limit,
            "nodes": nodes,
            "similar": similar,
        }

    def build(self, parse):
        """
        Constructs a full query from a parsed query. This method supports substituting placeholders with search results.

        Args:
            parse: parsed query

        Returns:
            graph query
        """

        query, attributes, uids = parse["query"], {}, {}

        if "results" in parse:
            for x, result in enumerate(parse["results"]):
                node = parse["nodes"][x]

                attribute = f"match_{x}"
                clause = f"{node}.{attribute} > 0"

                query = query.replace(f"{Query.SIMILAR}{x}", f"{clause}")

                for uid, score in result:
                    if uid not in uids:
                        uids[uid] = score

                attributes[attribute] = result

        return query, attributes, uids.items()

    def filter(self, graph, attributes, uids):
        """
        Filters the input graph by uids. This method also adds similar match attributes.

        Args:
            graph: graph instance
            attributes: results by attribute matched
            uids: single list with all matching ids

        Returns:
            filtered graph
        """

        graph = graph.filter(uids)

        for attribute, result in attributes.items():
            for uid, score in result:
                graph.addattribute(uid, attribute, score)

        return graph
