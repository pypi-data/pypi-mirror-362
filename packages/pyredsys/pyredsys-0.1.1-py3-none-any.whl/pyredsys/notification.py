import base64
import json

from pyredsys.constants import SIGNATURE_VERSION
from pyredsys.exceptions import (
    SignatureVerificationError,
    SignatureVersionMismatchError,
)
from pyredsys.types import NotificationParameters
from pyredsys.utils import generate_diversified_key, sign_hmac_sha512


def validate_notification(
    secret_key: str,
    params_b64: str,
    signature: str,
    signature_version: str,
):
    # Documentation
    # https://pagosonline.redsys.es/desarrolladores-inicio/documentacion-operativa/autorizacion/#notificacion
    if signature_version != SIGNATURE_VERSION:
        raise SignatureVersionMismatchError(SIGNATURE_VERSION, signature_version)
    params = json.loads(base64.urlsafe_b64decode(params_b64).decode())
    params = NotificationParameters.model_validate(params)
    diversified_key = generate_diversified_key(secret_key, params.Ds_Order)
    calculated_signature = sign_hmac_sha512(diversified_key, params_b64.encode())
    expected_signature = signature.encode()
    if calculated_signature != expected_signature:
        raise SignatureVerificationError(expected_signature, calculated_signature)
    return params
