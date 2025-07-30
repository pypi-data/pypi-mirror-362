from pydantic import BaseModel
from pydantic import Field


class ValidationResult(BaseModel):
    """Result of metrics validation."""

    is_valid: bool
    data: dict = Field(default_factory=dict)
    metrics_count: int = 0
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    validation_time: float = 0.0
    file_size: int = 0

    def add_error(self, error: str) -> None:
        """Add an error to the validation result."""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str) -> None:
        """Add a warning to the validation result."""
        self.warnings.append(warning)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)


class UploadResult(BaseModel):
    """Result of metrics upload."""

    validation_result: ValidationResult
    upload_successful: bool = False
    upload_error: str | None = None
    upload_url: str | None = None
    upload_time: float = 0.0
    bytes_uploaded: int = 0

    @property
    def is_successful(self) -> bool:
        return self.validation_result.is_valid and self.upload_successful
