import inspect
import sys
import types

from ..utilities import Resolver
from .base import Pipeline


class PipelineFactory:
    """
    Pipeline factory. Creates new Pipeline instances.
    """

    @staticmethod
    def get(pipeline):
        """
        Gets a new instance of pipeline class.

        Args:
            pclass: Pipeline instance class

        Returns:
            Pipeline class
        """

        if "." not in pipeline:
            return PipelineFactory.list()[pipeline]

        return Resolver()(pipeline)

    @staticmethod
    def create(config, pipeline):
        """
        Creates a new Pipeline instance.

        Args:
            config: Pipeline configuration
            pipeline: Pipeline instance class

        Returns:
            Pipeline
        """

        pipeline = PipelineFactory.get(pipeline)

        return pipeline if isinstance(pipeline, types.FunctionType) else pipeline(**config)

    @staticmethod
    def list():
        """
        Lists callable pipelines.

        Returns:
            {short name: pipeline class}
        """

        pipelines = {}

        pipeline = sys.modules[".".join(__name__.split(".")[:-1])]

        for x in inspect.getmembers(pipeline, inspect.isclass):
            if issubclass(x[1], Pipeline) and [
                y for y, _ in inspect.getmembers(x[1], inspect.isfunction) if y == "__call__"
            ]:
                pipelines[x[0].lower()] = x[1]

        return pipelines
