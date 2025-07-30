class TemplateError(Exception):
    """Base exception for template errors."""
    pass

class TemplateValidationError(TemplateError):
    """Raised when template validation fails."""
    pass

class TemplateNotFoundError(TemplateError, FileNotFoundError):
    """Raised when template file doesn't exist."""
    pass