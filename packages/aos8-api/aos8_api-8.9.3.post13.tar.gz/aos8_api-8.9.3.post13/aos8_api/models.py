from dataclasses import dataclass
from typing import Any, List, Optional, Union


@dataclass
class ApiResult:
    """
    Standard result object for API or command execution responses.

    Attributes:
        success (bool): Indicates whether the operation was successful.
        diag (int): Diagnostic or status code from the operation.
        error (Optional[Union[str, List[str]]]): Error message(s), if any.
        output (Optional[str]): Raw output from the operation, if applicable.
        data (Any): Parsed or structured result data.
    """
    success: bool
    diag: int
    error: Optional[Union[str, List[str]]] = None
    output: Optional[str] = None
    data: Any = None
