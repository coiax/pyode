# XODE Importer for PyODE
# Copyright (C) 2004 Timothy Stranex

"""
XODE Exceptions
@author: U{Timothy Stranex<mailto:timothy@stranex.com>}
"""

class InvalidError(Exception):
    """
    Raised when an XODE document is invalid.
    """

class ChildError(InvalidError):
    """
    Raised when an invalid child element is found.

    @ivar parent: The parent element.
    @type parent: str

    @ivar child: The invalid child element.
    @type child: str
    """

    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

    def __str__(self):
        return '<%s> is not a valid child of <%s>.' % (self.child, self.parent)

class MissingElementError(InvalidError):
    """
    Raised when a child element is missing.

    @ivar parent: The parent element.
    @type parent: str

    @ivar child: The missing child element.
    @type child: str
    """

    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

    def __str__(self):
        return 'Missing child <%s> of <%s>.' % (self.child, self.parent)
