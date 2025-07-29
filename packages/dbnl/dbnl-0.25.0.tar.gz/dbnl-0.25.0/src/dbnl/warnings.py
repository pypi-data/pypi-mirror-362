class DBNLWarning(Warning):
    pass


class DBNLAPIIncompatibilityWarning(DBNLWarning):
    """A warning that occurs when the DBNL SDK could not validate the API version compatibility
    or is incompatible with the current API version."""
