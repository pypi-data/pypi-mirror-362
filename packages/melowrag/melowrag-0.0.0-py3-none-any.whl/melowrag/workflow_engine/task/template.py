"""
Template module
"""

from string import Formatter

from ...utilities import TemplateFormatter
from .file import Task


class TemplateTask(Task):
    """
    Task that generates text from a template and task inputs. Templates can be used to prepare data for a number of tasks
    including generating large language model (LLM) prompts.
    """

    def register(self, template=None, rules=None, strict=True):
        """
        Read template parameters.

        Args:
            template: prompt template
            rules: parameter rules
            strict: requires all task inputs to be consumed by template, defaults to True
        """

        # pylint: disable=W0201
        self.template = template if template else self.defaulttemplate()

        self.rules = rules if rules else self.defaultrules()

        self.formatter = TemplateFormatter() if strict else Formatter()

    def prepare(self, element):
        match = self.match(element)
        if match:
            return match

        if self.template:
            if isinstance(element, dict):
                return self.formatter.format(self.template, **element)

            if isinstance(element, tuple):
                return self.formatter.format(self.template, **{f"arg{i}": x for i, x in enumerate(element)})

            return self.formatter.format(self.template, text=element)

        return element

    def defaulttemplate(self):
        """
        Generates a default template for this task. Base method returns None.

        Returns:
            default template
        """

        return None

    def defaultrules(self):
        """
        Generates a default rules for this task. Base method returns an empty dictionary.

        Returns:
            default rules
        """

        return {}

    def match(self, element):
        """
        Check if element matches any processing rules.

        Args:
            element: input element

        Returns:
            matching value if found, None otherwise
        """

        if self.rules and isinstance(element, dict):
            for key, value in self.rules.items():
                if element[key] == value:
                    return element[key]

        return None


class RagTask(TemplateTask):
    """
    Template task that prepares input for a rag pipeline.
    """

    def prepare(self, element):
        if isinstance(element, dict):
            params = dict(element)
            params.pop("query", None)
            params["text"] = params.pop("question")

            element["question"] = super().prepare(params)
            return element

        return {"query": element, "question": super().prepare(element)}
