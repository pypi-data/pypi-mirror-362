import re
import string
import typing

import regex

from ..base import Pipeline


class Tokenizer(Pipeline):
    """
    Tokenizes text into tokens using one of the following methods.

      1. Backwards compatible tokenization that only accepts alphanumeric tokens from the Latin alphabet.

      2. Split using word boundary rules from the Unicode Text Segmentation algorithm (see Unicode Standard Annex
         This is similar to the standard tokenizer in Apache Lucene and works well for most languages.
    """

    STOP_WORDS: typing.ClassVar = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "but",
        "by",
        "for",
        "if",
        "in",
        "into",
        "is",
        "it",
        "no",
        "not",
        "of",
        "on",
        "or",
        "such",
        "that",
        "the",
        "their",
        "then",
        "there",
        "these",
        "they",
        "this",
        "to",
        "was",
        "will",
        "with",
    }

    @staticmethod
    def tokenize(text, lowercase=True, emoji=True, alphanum=True, stopwords=True):
        """
        Tokenizes text into a list of tokens. The default backwards compatible parameters filter out English stop
        words and only accept alphanumeric tokens.

        Args:
            text: input text
            lowercase: lower cases all tokens if True, defaults to True
            emoji: tokenize emoji in text if True, defaults to True
            alphanum: requires 2+ character alphanumeric tokens if True, defaults to True
            stopwords: removes provided stop words if a list, removes default English stop words if True

        Returns:
            list of tokens
        """

        return Tokenizer(lowercase, emoji, alphanum, stopwords)(text)

    def __init__(self, lowercase=True, emoji=True, alphanum=False, stopwords=False):
        """
        Creates a new tokenizer. The default parameters segment text per Unicode Standard Annex

        Args:
            lowercase: lower cases all tokens if True, defaults to True
            emoji: tokenize emoji in text if True, defaults to True
            alphanum: requires 2+ character alphanumeric tokens if True, defaults to False
            stopwords: removes provided stop words if a list, removes default English stop words if True
        """

        self.lowercase = lowercase

        self.alphanum, self.segment = None, None
        if alphanum:
            # Note: The standard Python re module is much faster than regex for this expression
            self.alphanum = re.compile(r"^\d*[a-z][\-.0-9:_a-z]{1,}$")
        else:
            pattern = r"\w\p{Extended_Pictographic}\p{WB:RegionalIndicator}" if emoji else r"\w"
            self.segment = regex.compile(rf"[{pattern}](?:\B\S)*", flags=regex.WORD)

        self.stopwords = stopwords if isinstance(stopwords, list) else Tokenizer.STOP_WORDS if stopwords else False

    def __call__(self, text):
        """
        Tokenizes text into a list of tokens.

        Args:
            text: input text

        Returns:
            list of tokens
        """

        if text is None:
            return None

        text = text.lower() if self.lowercase else text

        if self.alphanum:
            tokens = [token.strip(string.punctuation) for token in text.split()]

            tokens = [token for token in tokens if re.match(self.alphanum, token)]
        else:
            tokens = regex.findall(self.segment, text)

        if self.stopwords:
            tokens = [token for token in tokens if token not in self.stopwords]

        return tokens
