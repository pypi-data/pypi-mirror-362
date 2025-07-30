from gllm_agents.a2a.types import ArtifactType as ArtifactType, MimeType as MimeType, get_mime_type_from_filename as get_mime_type_from_filename
from typing import Any

class ArtifactHandler:
    """Handler class for creating and managing artifacts in agent tools.

    This class provides a clean, object-oriented interface for artifact creation
    with built-in validation, deduplication, and standardized formatting.
    """
    def __init__(self) -> None:
        """Initialize the ArtifactHandler."""
    def create_file_artifact(self, result: str, artifact_data: bytes | str, artifact_name: str, artifact_description: str = '', mime_type: str | None = None, enable_deduplication: bool = True) -> dict[str, Any]:
        """Create a file artifact response.

        Args:
            result: The message/result to show to the agent (clean, no file data).
            artifact_data: The binary data or base64 string for the artifact.
            artifact_name: The name for the artifact file.
            artifact_description: Description of the artifact.
            mime_type: MIME type of the artifact. If None, auto-detected from filename.
            enable_deduplication: Whether to check for duplicate artifacts.

        Returns:
            Dictionary with 'result' and 'artifact' keys following the standardized format.
        """
    def create_text_artifact(self, result: str, artifact_text: str, artifact_name: str, artifact_description: str = '', mime_type: str | None = None, enable_deduplication: bool = True) -> dict[str, Any]:
        """Create a text artifact response.

        Args:
            result: The message/result to show to the agent.
            artifact_text: The text content for the artifact.
            artifact_name: The name for the artifact file.
            artifact_description: Description of the artifact.
            mime_type: MIME type of the artifact. If None, auto-detected or defaults to text/plain.
            enable_deduplication: Whether to check for duplicate artifacts.

        Returns:
            Dictionary with 'result' and 'artifact' keys following the standardized format.
        """
    def create_error_response(self, error_message: str) -> str:
        """Create a standardized error response for tools.

        Args:
            error_message: The error message to return.

        Returns:
            String with error information.
        """
    def clear_cache(self) -> None:
        """Clear the artifact cache."""
    def get_cache_size(self) -> int:
        """Get the number of cached artifacts.

        Returns:
            Number of artifacts in cache.
        """
    @staticmethod
    def generate_artifact_hash(artifact_data: str, name: str, mime_type: str) -> str:
        """Generate a hash for artifact deduplication.

        Args:
            artifact_data: Base64 encoded artifact data.
            name: Artifact name.
            mime_type: MIME type.

        Returns:
            Hash string for deduplication.
        """

def create_artifact_response(result: str, artifact_data: bytes | str, artifact_name: str, artifact_description: str = '', mime_type: str | None = None) -> dict[str, Any]:
    '''Create a standardized artifact response for tools.

    This function creates a response that separates the agent-facing result
    from the user-facing artifact, following the established pattern for
    artifact generation in the agent system.

    Args:
        result: The message/result to show to the agent (clean, no file data).
        artifact_data: The binary data or base64 string for the artifact.
        artifact_name: The name for the artifact file.
        artifact_description: Description of the artifact. Defaults to "".
        mime_type: MIME type of the artifact. If None, will be auto-detected from filename.

    Returns:
        Dictionary with \'result\' and \'artifacts\' keys (artifacts is always a list).

    Example:
        >>> import io
        >>> csv_data = "Name,Age\\\\nAlice,30\\\\nBob,25"
        >>> response = create_artifact_response(
        ...     result="Generated a 2-row CSV table",
        ...     artifact_data=csv_data.encode(\'utf-8\'),
        ...     artifact_name="data.csv",
        ...     artifact_description="Sample data table",
        ...     mime_type="text/csv"
        ... )
        >>> assert "result" in response
        >>> assert "artifacts" in response
        >>> assert isinstance(response["artifacts"], list)
    '''
def create_text_artifact_response(result: str, artifact_text: str, artifact_name: str, artifact_description: str = '', mime_type: str | None = None) -> dict[str, Any]:
    '''Create a standardized text artifact response for tools.

    Convenience function for creating text-based artifacts (CSV, JSON, TXT, etc.).

    Args:
        result: The message/result to show to the agent.
        artifact_text: The text content for the artifact.
        artifact_name: The name for the artifact file.
        artifact_description: Description of the artifact. Defaults to "".
        mime_type: MIME type of the artifact. If None, will be auto-detected from filename or default to text/plain.

    Returns:
        Dictionary with \'result\' and \'artifacts\' keys (artifacts is always a list).

    Example:
        >>> response = create_text_artifact_response(
        ...     result="Created JSON data",
        ...     artifact_text=\'{"name": "Alice", "age": 30}\',
        ...     artifact_name="data.json",
        ...     mime_type="application/json"
        ... )
        >>> assert response["artifacts"][0]["mime_type"] == "application/json"
        >>> assert isinstance(response["artifacts"], list)
    '''
def create_multiple_artifacts_response(result: str, artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    """Create a standardized response for multiple artifacts.

    Args:
        result: The message/result to show to the agent.
        artifacts: List of artifact dictionaries.

    Returns:
        Dictionary with 'result' and 'artifacts' keys.
    """
def create_error_response(error_message: str) -> str:
    """Create a standardized error response for tools.

    For error cases, we return a simple string that will be passed directly
    to the agent without any artifact processing.

    Args:
        error_message: The error message to return.

    Returns:
        String with error information.
    """
def extract_artifacts_from_agent_response(result: Any) -> tuple[str, list[dict[str, Any]]]:
    """Extract artifacts from agent response for delegation tools.

    Args:
        result: The result returned by the delegated agent.

    Returns:
        Tuple of (text_response, artifacts_list) where:
        - text_response: The text content for the agent
        - artifacts_list: List of artifacts to be passed through
    """
def create_delegation_response_with_artifacts(result: str, artifacts: list[dict[str, Any]], agent_name: str = '') -> dict[str, Any] | str:
    """Create a delegation response that includes artifacts only when needed.

    Args:
        result: The text result from the delegated agent.
        artifacts: List of artifacts from the delegated agent (always a list).
        agent_name: Name of the agent for prefixing the result.

    Returns:
        Dictionary with 'result' and 'artifacts' keys if artifacts exist,
        otherwise just a string for backward compatibility and efficiency.
    """
