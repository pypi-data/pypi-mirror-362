"""Custom parser with table support for babbl."""

from marko import Parser

from babbl.elements import CodeReference, Table


class BabblParser(Parser):
    """Custom parser that includes table and code reference support."""

    def __init__(self):
        super().__init__()
        # Add table support
        self.add_element(Table)
        # Add code reference support
        self.add_element(CodeReference)

    def parse(self, text: str):
        """Parse text with table and code reference support."""
        return super().parse(text)
