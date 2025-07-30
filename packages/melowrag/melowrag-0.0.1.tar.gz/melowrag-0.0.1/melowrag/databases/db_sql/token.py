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

import typing


class Token:
    """
    Methods to check for token type.
    """

    SIMILAR_TOKEN = "__SIMILAR__"

    DISTINCT: typing.ClassVar = ["distinct"]

    ALIAS: typing.ClassVar = ["as"]

    OPERATORS: typing.ClassVar = [
        "=",
        "!=",
        "<>",
        ">",
        ">=",
        "<",
        "<=",
        "+",
        "-",
        "*",
        "/",
        "%",
        "||",
        "not",
        "between",
        "like",
        "is",
        "null",
    ]

    LOGIC_SEPARATORS: typing.ClassVar = ["and", "or"]
    SORT_ORDER: typing.ClassVar = ["asc", "desc"]

    @staticmethod
    def get(tokens, x):
        """
        Gets token at position x. This method will validate position is valid within tokens.

        Args:
            tokens: input tokens
            x: position to retrieve

        Returns:
            tokens[x] if x is a valid position, None otherwise
        """

        if 0 <= x < len(tokens):
            return tokens[x]

        return None

    @staticmethod
    def isalias(tokens, x, alias):
        """
        Checks if tokens[x] is an alias keyword.

        Args:
            tokens: input tokens
            x: current position
            alias: if column alias processing is enabled

        Returns:
            True if tokens[x] is an alias token, False otherwise
        """

        prior = Token.get(tokens, x - 1)
        token = tokens[x]

        return (
            alias
            and x > 0
            and not Token.isseparator(prior)
            and not Token.isgroupstart(prior)
            and not Token.isdistinct(prior)
            and (Token.iscolumn(token) or Token.isquoted(token))
        )

    @staticmethod
    def isattribute(tokens, x):
        """
        Checks if tokens[x] is an attribute.

        Args:
            tokens: input tokens
            x: current position

        Returns:
            True if tokens[x] is an attribute, False otherwise
        """

        return Token.iscolumn(tokens[x]) and not Token.isoperator(Token.get(tokens, x + 1))

    @staticmethod
    def isbracket(token):
        """
        Checks if token is an open bracket.

        Args:
            token: token to test

        Returns:
            True if token is an open bracket, False otherwise
        """

        return token == "["

    @staticmethod
    def iscolumn(token):
        """
        Checks if token is a column name.

        Args:
            token: token to test

        Returns:
            True if this token is a column name token, False otherwise
        """

        return (
            token
            and not Token.isoperator(token)
            and not Token.islogicseparator(token)
            and not Token.isliteral(token)
            and not Token.issortorder(token)
        )

    @staticmethod
    def iscompound(tokens, x):
        """
        Checks if tokens[x] is a compound expression.

        Args:
            tokens: input tokens
            x: current position

        Returns:
            True if tokens[x] is a compound expression, False otherwise
        """

        return Token.isoperator(tokens[x]) and (
            Token.iscolumn(Token.get(tokens, x - 1)) or Token.iscolumn(Token.get(tokens, x + 1))
        )

    @staticmethod
    def isdistinct(token):
        """
        Checks if token is the distinct keyword.

        Args:
            token: token to test

        Returns:
            True if this token is a distinct keyword, False otherwise
        """

        return token and token.lower() in Token.DISTINCT

    @staticmethod
    def isfunction(tokens, x):
        """
        Checks if tokens[x] is a function.

        Args:
            tokens: input tokens
            x: current position

        Returns:
            True if tokens[x] is a function, False otherwise
        """

        return Token.iscolumn(tokens[x]) and Token.get(tokens, x + 1) == "("

    @staticmethod
    def isgroupstart(token):
        """
        Checks if token is a group start token.

        Args:
            token: token to test

        Returns:
            True if token is a group start token, False otherwise
        """

        return token == "("

    @staticmethod
    def isliteral(token):
        """
        Checks if token is a literal.

        Args:
            token: token to test

        Returns:
            True if this token is a literal, False otherwise
        """

        return token and (token.startswith(("'", '"', ",", "(", ")", "*")) or token.replace(".", "", 1).isdigit())

    @staticmethod
    def islogicseparator(token):
        """
        Checks if token is a logic separator token.

        Args:
            token: token to test

        Returns:
            True if this token is a logic separator, False otherwise
        """

        return token and token.lower() in Token.LOGIC_SEPARATORS

    @staticmethod
    def isoperator(token):
        """
        Checks if token is an operator token.

        Args:
            token: token to test

        Returns:
            True if this token is an operator, False otherwise
        """

        return token and token.lower() in Token.OPERATORS

    @staticmethod
    def isquoted(token):
        """
        Checks if token is quoted.

        Args:
            token: token to test

        Returns:
            True if this token is quoted, False otherwise
        """

        return token.startswith(("'", '"')) and token.endswith(("'", '"'))

    @staticmethod
    def isseparator(token):
        """
        Checks if token is a separator token.

        Args:
            token to test

        Returns:
            True if this token is a separator, False otherwise
        """

        return token == ","

    @staticmethod
    def issimilar(tokens, x, similar):
        """
        Checks if tokens[x] is a similar() function.

        Args:
            tokens: input tokens: typing.ClassVar
            x: current position
            similar: list where similar function call parameters are stored,
                        can be None in which case similar processing is skipped

        Returns:
            True if tokens[x] is a similar clause
        """

        return similar is not None and tokens[x].lower() == "similar" and Token.get(tokens, x + 1) == "("

    @staticmethod
    def issortorder(token):
        """
        Checks if token is a sort order token.

        Args:
            token: token to test

        Returns:
            True if this token is a sort order operator, False otherwise
        """

        return token and token.lower() in Token.SORT_ORDER

    @staticmethod
    def normalize(token):
        """
        Applies a normalization algorithm to the input token as follows:
            - Strip single and double quotes
            - Make lowercase

        Args:
            token: input token

        Returns:
            normalized token
        """

        return token.lower().replace("'", "").replace('"', "")

    @staticmethod
    def wrapspace(text, token):
        """
        Applies whitespace wrapping rules to token.

        Args:
            text: current text buffer
            token: token to add

        Returns:
            token with whitespace rules applied
        """

        if token in ["*"] and (not text or text.endswith((" ", "("))):
            return token

        if Token.isoperator(token) or Token.islogicseparator(token) or token.lower() in ["in"]:
            return f" {token} " if not text.endswith(" ") else f"{token} "

        if Token.isseparator(token):
            return f"{token} "

        if not text or text.endswith((" ", "(", "[")) or token in ["(", "[", ")", "]"] or token.startswith("."):
            return token

        return f" {token}"
