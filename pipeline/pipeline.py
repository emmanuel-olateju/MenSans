"""
Custom Pipeline Module

This module provides a class for creating and executing data processing pipelines.

Classes:
    - Pipeline: A class representing a data processing pipeline.

"""

class Pipeline():
    """
    pipeline Class

    A class representing a data processing pipeline.

    Attributes:
        name (str): The name of the pipeline.
        methods (list): A list of methods in the pipeline.

    Methods:
        forward(raw): Perform forward pass through the pipeline.

    """
    def __init__(self,name,methods):
        """
        Initialize the Pipeline object.

        Args:
            name (str): The name of the pipeline.
            methods (list): A list of methods in the pipeline.

        Returns:
            None
        """
        self.name = name
        self.methods = methods

    def forward(self,raw):
        """
        Perform forward pass through the pipeline.

        Args:
            raw: The raw input data.

        Returns:
            The processed data after passing through the pipeline.
        """
        return raw
    