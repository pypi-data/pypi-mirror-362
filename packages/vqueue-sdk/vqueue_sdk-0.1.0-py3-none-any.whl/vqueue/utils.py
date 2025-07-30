from uuid import UUID


def validate_uuidv4(uuid: str) -> UUID:
    """Validate a string is a valid UUIDv4

    Args:
        uuid: The string to be validated.

    Returns:
        The valid UUID.

    Raises:
        ValueError: If the string is not a valid UUIDv4
    """
    try:
        validated_uuid = UUID(uuid)
        if validated_uuid.version != 4:
            raise ValueError("Token must be a UUIDv4.")
        return validated_uuid
    except ValueError as e:
        raise ValueError("Invalid UUID format.") from e
