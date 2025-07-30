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

"""
This module provides the Scan class for scanning indexes for query matches and the Clause class for parsing query clause parameters.
"""


class Scan:
    """
    Scans indexes for query matches and executes scans for lists of queries.

    Args:
        search (Callable): Index search function.
        limit (int): Maximum results.
        weights (Any): Default hybrid score weights.
        index (str): Default index name.
    """

    def __init__(self, search, limit, weights, index):
        """
        Creates a new scan instance.

        Args:
            search: index search function
            limit: maximum results
            weights: default hybrid score weights
            index: default index name
        """

        self.search = search

        self.limit = limit

        self.candidates = None

        self.weights = weights

        self.index = index

    def __call__(self, queries, parameters):
        """
        Executes a scan for a list of queries.

        Args:
            queries: list of queries to run
            parameters: list of dicts of named parameters to bind to placeholders

        Returns:
            list of (id, score) per query
        """

        results = {}

        default = None

        for index, iqueries in self.parse(queries, parameters).items():
            candidates = [query.candidates for query in iqueries if query.candidates]
            if not candidates and not default:
                default = self.default(queries)

            candidates = max(candidates) if candidates else default

            weights = [query.weights for query in iqueries if query.weights is not None]
            weights = max(weights) if weights else self.weights

            index = index if index else self.index

            for x, result in enumerate(self.search([query.text for query in iqueries], candidates, weights, index)):
                results[iqueries[x].uid] = (iqueries[x].qid, result)

        return [result for _, result in sorted(results.items())]

    def parse(self, queries, parameters):
        """
        Parse index query clauses from a list of parsed queries.

        Args:
            queries: list of parsed queries
            parameters: list of dicts of named parameters to bind to placeholders

        Returns:
            index query clauses grouped by index
        """

        results, uid = {}, 0
        for x, query in enumerate(queries):
            if "similar" in query:
                for params in query["similar"]:
                    if parameters and parameters[x]:
                        params = self.bind(params, parameters[x])

                    clause = Clause(uid, x, params)

                    if clause.index not in results:
                        results[clause.index] = []

                    results[clause.index].append(clause)
                    uid += 1

        return results

    def bind(self, similar, parameters):
        """
        Resolves bind parameters for a similar function call.

        Args:
            similar: similar function call arguments
            parameters: bind parameters

        Returns:
            similar function call arguments with resolved bind parameters
        """

        resolved = []
        for p in similar:
            if isinstance(p, str) and p.startswith(":") and p[1:] in parameters:
                resolved.append(parameters[p[1:]])
            else:
                resolved.append(p)

        return resolved

    def default(self, queries):
        """
        Derives the default number of candidates. The number of candidates are the number of results to bring back
        from index queries. This is an optional argument to similar() clauses.

        For a single query filter clause, the default is the query limit. With multiple filtering clauses, the default is
        10x the query limit. This ensures that limit results are still returned with additional filtering after an index.

        Args:
            queries: list of queries

        Returns:
            default candidate list size
        """

        multitoken = any(query.get("where") and len(query["where"].split()) > 1 for query in queries)
        return self.limit * 10 if multitoken else self.limit


class Clause:
    """
    Parses and stores query clause parameters for index scans.

    Args:
        uid (int): Query clause id.
        qid (int): Query id clause is a part of.
        params (Any): Query parameters to parse.
    """

    def __init__(self, uid, qid, params):
        """
        Creates a new query clause.

        Args:
            uid: query clause id
            qid: query id clause is a part of
            params: query parameters to parse
        """

        self.uid, self.qid = uid, qid
        self.text, self.index = params[0], None
        self.candidates, self.weights = None, None

        if len(params) > 1:
            self.parse(params[1:])

    def parse(self, params):
        """
        Parses clause parameters into this instance.

        Args:
            params: query clause parameters
        """

        for param in params:
            if (isinstance(param, str) and param.isdigit()) or isinstance(param, int):
                self.candidates = int(param)

            elif (isinstance(param, str) and param.replace(".", "").isdigit()) or isinstance(param, float):
                self.weights = float(param)

            else:
                self.index = param
