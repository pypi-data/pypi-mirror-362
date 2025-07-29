"""Utilize tiktoken to get token length.

Copyright (c) 2024 Neil Schneider
"""

import tiktoken

from slimcontext.utils.logger import setup_logger

logger = setup_logger(__name__)


class TokenCounter:
    """Counts the number of tokens in a given string using tiktoken.

    Attributes:
        model (str): The name of the model used for tokenization.
    """

    def __init__(self, model: str = 'gpt-4o') -> None:
        """Initialize the TokenCounter with a model.

        Args:
            model (str): The name of the model to use for tokenization. Defaults to 'gpt-4'.
        """
        self.model = model
        try:
            self.tokenizer = tiktoken.encoding_for_model(model)
            logger.debug('Using tokenizer for model: %s', model)
        except KeyError:
            logger.warning("Model '%s' not found. Using default encoding.", model)
            self.tokenizer = tiktoken.get_encoding('cl100k_base')

    def count_tokens(self, input_string: str) -> int:
        """Count the number of tokens in the input string.

        Args:
            input_string (str): The input string to tokenize.

        Returns:
            int: The number of tokens in the input string.
        """
        tokens = self.tokenizer.encode(input_string)
        token_count = len(tokens)
        logger.debug('Token count: %d', token_count)
        return token_count
