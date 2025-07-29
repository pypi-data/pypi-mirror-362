class RedSysError(Exception):
    pass


class RedSysNotificationValidationError(RedSysError):
    pass


class SignatureVersionMismatchError(RedSysNotificationValidationError):
    def __init__(self, expected_version: str, received_version: str):
        self.expected_version = expected_version
        self.received_version = received_version
        super().__init__(
            f"Expected: {expected_version}, Calculated: {received_version}"
        )


class SignatureVerificationError(RedSysNotificationValidationError):
    def __init__(self, expected_signature: bytes, calculated_signature: bytes):
        self.expected_signature = expected_signature
        self.calculated_signature = calculated_signature
        super().__init__(
            f"Expected: {expected_signature}, Calculated: {calculated_signature}"
        )
