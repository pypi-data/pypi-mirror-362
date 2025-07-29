class UMNetDBError(Exception):
    """
    Generic umnetdb error
    """

    pass


class UMnetDBModelError(Exception):
    """
    Error related to data models
    """

    pass


class UMnetDBLookupError(Exception):
    """ "
    Error related to queries
    """

    def __init__(self, query, table):
        super().__init__(f"Could not find {query} in {table.__name__} table")
