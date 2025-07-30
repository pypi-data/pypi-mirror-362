import typing
from io import StringIO
from shlex import shlex

from .expression import Expression


class SQL:
    """
    Translates melowrag SQL statements into database native queries.
    """

    CLAUSES: typing.ClassVar = ["select", "from", "where", "group", "having", "order", "limit", "offset"]

    def __init__(self, database=None, tolist=False):
        """
        Creates a new SQL query parser.

        Args:
            database: database instance that provides resolver callback, if any
            tolist: outputs expression lists if True, expression text otherwise, defaults to False
        """

        self.expression = Expression(database.resolve if database else self.defaultresolve, tolist)

    def __call__(self, query):
        """
        Parses an input SQL query and normalizes column names in the query clauses. This method will also embed
        similarity search placeholders into the query.

        Args:
            query: input query

        Returns:
            {clause name: clause text}
        """

        clauses = None
        if self.issql(query):
            query = query.split(";")[0]

            tokens, positions = self.tokenize(query)

            aliases, similar = {}, []

            clauses = {
                "select": self.parse(tokens, positions, "select", alias=True, aliases=aliases),
                "where": self.parse(tokens, positions, "where", aliases=aliases, similar=similar),
                "groupby": self.parse(tokens, positions, "group", offset=2, aliases=aliases),
                "having": self.parse(tokens, positions, "having", aliases=aliases),
                "orderby": self.parse(tokens, positions, "order", offset=2, aliases=aliases),
                "limit": self.parse(tokens, positions, "limit", aliases=aliases),
                "offset": self.parse(tokens, positions, "offset", aliases=aliases),
            }

            if similar:
                clauses["similar"] = similar

        return clauses if clauses else {"similar": [[query]]}

    # pylint: disable=W0613
    def defaultresolve(self, name, alias=None):
        """
        Default resolve function. Performs no processing, only returns name.

        Args:
            name: query column name
            alias: alias name, defaults to None

        Returns:
            name
        """

        return name

    def issql(self, query):
        """
        Detects if this is a SQL query.

        Args:
            query: input query

        Returns:
            True if this is a valid SQL query, False otherwise
        """

        if isinstance(query, str):
            query = query.lower().strip(";").replace("\n", " ").replace("\t", " ").strip()

            return query.startswith("select ") and (" from melowrag " in query or query.endswith(" from melowrag"))

        return False

    def snippet(self, text):
        """
        Parses a partial SQL snippet.

        Args:
            text: SQL snippet

        Returns:
            parsed snippet
        """

        tokens, _ = self.tokenize(text)
        return self.expression(tokens)

    def tokenize(self, query):
        """
        Tokenizes SQL query into tokens.

        Args:
            query: input query

        Returns:
            (tokenized query, token positions)
        """

        tokens = shlex(StringIO(query), punctuation_chars="=!<>+-*/%|")
        tokens.wordchars += ":@#"
        tokens.commenters = ""
        tokens = list(tokens)

        positions = {}

        for x, token in enumerate(tokens):
            t = token.lower()
            if (
                t not in positions
                and t in SQL.CLAUSES
                and (t not in ["group", "order"] or (x + 1 < len(tokens) and tokens[x + 1].lower() == "by"))
            ):
                positions[t] = x

        return (tokens, positions)

    def parse(self, tokens, positions, name, offset=1, alias=False, aliases=None, similar=None):
        """
        Runs query column name to database column name mappings for clauses. This method will also
        parse SIMILAR() function calls, extract parameters for those calls and leave a placeholder
        to be filled in with similarity results.

        Args:
            tokens: query tokens
            positions: token positions - used to locate the start of sql clauses
            name: current query clause name
            offset: how many tokens are in the clause name
            alias: True if terms in the clause should be aliased (i.e. column as alias)
            aliases: dict of generated aliases, if present these tokens should NOT be resolved
            similar: list where parsed similar clauses should be stored

        Returns:
            formatted clause
        """

        clause = None
        if name in positions:
            end = [positions.get(x, len(tokens)) for x in SQL.CLAUSES[SQL.CLAUSES.index(name) + 1 :]]
            end = min(end) if end else len(tokens)

            clause = tokens[positions[name] + offset : end]

            clause = self.expression(clause, alias, aliases, similar)

        return clause


class SQLError(Exception):
    """
    Raised for errors generated by user SQL queries
    """
