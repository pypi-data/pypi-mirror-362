class SklikException(Exception):
    """
    Custom exception for Sklik API errors.

    Extends the base Exception class to include additional information about
    Sklik API errors, such as status codes and detailed error messages.

    Attributes:
        status_code: HTTP or API-specific status code indicating the error type.
        additional_information: Detailed error message or additional context from the API.
        message: Main error message (inherited from Exception).

    Example:
        >>> raise SklikException("API Error", 400, "Invalid campaign ID")
        SklikException: API Error
        # Access additional details:
        # exception.status_code -> 400
        # exception.additional_information -> "Invalid campaign ID"
    """

    def __init__(self, msg, status_code, additional_information):
        self.status_code = status_code
        self.additional_information = additional_information
        super().__init__(msg)
