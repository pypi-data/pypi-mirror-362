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

from .token import Token


class Expression:
    """
    Parses expression statements and runs a set of substitution/formatting rules.
    """

    def __init__(self, resolver, tolist):
        """
        Creates a new expression parser.

        Args:
            resolver: function to call to resolve query column names with database column names
            tolist: outputs expression lists if True, text if False
        """

        self.resolver = resolver
        self.tolist = tolist

    def __call__(self, tokens, alias=False, aliases=None, similar=None):
        """
        Parses and formats a list of tokens as follows:
            - Replaces query column names with database column names
            - Adds similar query placeholders and extracts similar function parameters
            - Rewrites expression and returns

        Args:
            tokens: input expression
            alias: if True, column aliases should be generated and added to aliases dict
            aliases: dict of generated aliases, if present these tokens should NOT be resolved
            similar: list of similar queries, if present new similar queries are appended to this list

        Returns:
            rewritten clause
        """

        transformed = self.process(list(tokens), alias, aliases, similar)

        if alias and not self.tolist:
            return self.buildalias(transformed, tokens, aliases)

        return self.buildlist(transformed) if self.tolist is True else self.buildtext(transformed)

    def process(self, tokens, alias, aliases, similar):
        """
        Replaces query column names with database column names, adds similar query placeholders and
        extracts similar function parameters.

        Args:
            tokens: input expression
            alias: if True, column aliases should be generated and added to aliases dict
            aliases: dict of generated aliases, if present these tokens should NOT be resolved
            similar: list of similar queries, if present new similar queries are appended to this list

        Returns:
            transformed tokens
        """

        index, iterator = 0, ((x, token) for x, token in enumerate(tokens) if not Token.isdistinct(token))
        for x, token in iterator:
            if Token.isseparator(token):
                index += 1

            elif Token.isbracket(token):
                self.bracket(iterator, tokens, x)

            elif Token.issimilar(tokens, x, similar):
                self.similar(iterator, tokens, x, similar)

            elif Token.isfunction(tokens, x):
                self.function(iterator, tokens, token, aliases, similar)

            elif Token.isalias(tokens, x, alias):
                self.alias(iterator, tokens, x, aliases, index)

            elif Token.isattribute(tokens, x):
                self.attribute(tokens, x, aliases)

            elif Token.iscompound(tokens, x):
                self.compound(iterator, tokens, x, aliases, similar)

        return [token for token in tokens if token]

    def buildtext(self, tokens):
        """
        Builds a new expression from tokens. This method applies a set of rules to generate whitespace between tokens.

        Args:
            tokens: input expression

        Returns:
            expression text
        """

        text = ""
        for token in tokens:
            text += Token.wrapspace(text, token)

        return text.strip()

    def buildlist(self, tokens):
        """
        Builds a new expression from tokens. This method returns a list of expression components.
        These components can be joined together on commas to form a text expression.

        Args:
            tokens: input expression

        Returns:
            expression list
        """

        parts, current, parens, brackets = [], [], 0, 0

        for token in tokens:
            if token == "," and not parens and not brackets:
                parts.append(self.buildtext(current))
                current = []
            else:
                if token == "(":
                    parens += 1
                elif token == ")":
                    parens -= 1
                elif token == "[":
                    brackets += 1
                elif token == "]":
                    brackets -= 1
                elif Token.issortorder(token):
                    token = f" {token}"
                current.append(token)

        if current:
            parts.append(self.buildtext(current))

        return parts

    def buildalias(self, transformed, tokens, aliases):
        """
        Builds new alias text expression from transformed and input tokens.

        Args:
            transformed: transformed tokens
            tokens: original input tokens
            aliases: dict of column aliases

        Returns:
            alias text expression
        """

        transformed = self.buildlist(transformed)
        tokens = self.buildlist(tokens)

        expression = []
        for x, token in enumerate(transformed):
            if x not in aliases.values():
                alias = tokens[x]

                if not any(Token.isoperator(t) for t in alias) and alias[0] in ("[", "(") and alias[-1] in ("]", ")"):
                    alias = alias[1:-1]

                values = alias.split()
                if len(values) > 0 and Token.isdistinct(values[0]):
                    alias = " ".join(values[1:])

                token = self.resolver(token, alias)

            expression.append(token)

        return ", ".join(expression)

    def bracket(self, iterator, tokens, x):
        """
        Consumes a [bracket] expression.

        Args:
            iterator: tokens iterator
            tokens: input tokens
            x: current position
        """

        params = []

        token = tokens[x]
        tokens[x] = None

        brackets = 1

        while token and (token != "]" or brackets > 0):
            x, token = next(iterator, (None, None))

            if token == "[":
                brackets += 1
            elif token == "]":
                brackets -= 1

            if token != "]" or brackets > 0:
                params.append(token)

            tokens[x] = None

        tokens[x] = self.resolve(self.buildtext(params), None)

    def similar(self, iterator, tokens, x, similar):
        """
        Substitutes a similar() function call with a placeholder that can later be used to add
        embeddings query results as a filter.

        Args:
            iterator: tokens iterator
            tokens: input tokens
            x: current position
            similar: list where similar function call parameters are stored
        """

        params = []

        token = tokens[x]
        tokens[x] = None

        while token and token != ")":
            x, token = next(iterator, (None, None))
            if token and token not in ["(", ",", ")"]:
                params.append(token.replace("'", "").replace('"', ""))

            tokens[x] = None

        tokens[x] = f"{Token.SIMILAR_TOKEN}{len(similar)}"

        similar.append(params)

    def function(self, iterator, tokens, token, aliases, similar):
        """
        Resolves column names within the function's parameters.

        Args:
            iterator: tokens iterator
            tokens: input tokens
            token: current token
            aliases: dict of generated aliases, if present these tokens should NOT be resolved
            similar: list where similar function call parameters are stored
        """

        while token and token != ")":
            x, token = next(iterator, (None, None))

            if Token.isbracket(token):
                self.bracket(iterator, tokens, x)

            elif Token.issimilar(tokens, x, similar):
                self.similar(iterator, tokens, x, similar)

            elif Token.isfunction(tokens, x):
                self.function(iterator, tokens, token, aliases, similar)

            elif Token.isattribute(tokens, x):
                self.attribute(tokens, x, aliases)

            elif Token.iscompound(tokens, x):
                self.compound(iterator, tokens, x, aliases, similar)

    def alias(self, iterator, tokens, x, aliases, index):
        """
        Reads an alias clause and stores it in aliases.

        Args:
            iterator: tokens iterator
            tokens: input tokens
            x: current position
            aliases: dict where aliases are stored - stores {alias: clause index}
            index: clause index, used to match aliases with columns
        """

        token = tokens[x]

        if token in Token.ALIAS:
            x, token = next(iterator, (None, None))

        while x + 1 < len(tokens) and not Token.isseparator(Token.get(tokens, x + 1)):
            x, token = next(iterator, (None, None))

        aliases[Token.normalize(token)] = index

    def attribute(self, tokens, x, aliases):
        """
        Resolves an attribute column name.

        Args:
            tokens: input tokens
            x: current token position
            aliases: dict of generated aliases, if present these tokens should NOT be resolved
        """

        tokens[x] = self.resolve(tokens[x], aliases)

    def compound(self, iterator, tokens, x, aliases, similar):
        """
        Resolves column names in a compound expression (left side <operator(s)> right side).

        Args:
            iterator: tokens iterator
            tokens: input tokens
            x: current token position
            aliases: dict of generated aliases, if present these tokens should NOT be resolved
            similar: list where similar function call parameters are stored
        """

        if Token.iscolumn(tokens[x - 1]):
            tokens[x - 1] = self.resolve(tokens[x - 1], aliases)

        token = tokens[x]
        while token and Token.isoperator(token):
            x, token = next(iterator, (None, None))

        if token and Token.iscolumn(token):
            if Token.isfunction(tokens, x):
                self.function(iterator, tokens, token, aliases, similar)
            else:
                tokens[x] = self.resolve(token, aliases)

    def resolve(self, token, aliases):
        """
        Resolves this token's value if it is not an alias or a bind parameter.

        Args:
            token: token to resolve
            aliases: dict of generated aliases, if present these tokens should NOT be resolved

        Returns:
            resolved token value
        """

        if (aliases and Token.normalize(token) in aliases) or (token.startswith(":")):
            return token

        return self.resolver(token)
