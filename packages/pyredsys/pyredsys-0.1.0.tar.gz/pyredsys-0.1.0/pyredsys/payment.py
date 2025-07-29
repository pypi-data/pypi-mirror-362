import base64

from pyredsys.constants import SIGNATURE_VERSION
from pyredsys.types import MerchantParameters, SignedMerchantParameters
from pyredsys.utils import generate_diversified_key, sign_hmac_sha512


def request_payment(
    secret_key: str,
    params: MerchantParameters,
):
    # Documentation
    # https://pagosonline.redsys.es/desarrolladores-inicio/documentacion-operativa/autorizacion/#redireccion
    ds_merchant_parameters = params.model_dump_json(exclude_unset=True)
    ds_merchant_parameters_b64 = base64.urlsafe_b64encode(
        ds_merchant_parameters.encode()
    )
    diversified_key = generate_diversified_key(secret_key, params.DS_MERCHANT_ORDER)
    ds_signature_b64 = sign_hmac_sha512(diversified_key, ds_merchant_parameters_b64)
    signed_params = SignedMerchantParameters(
        Ds_MerchantParameters=ds_merchant_parameters_b64.decode(),
        Ds_Signature=ds_signature_b64.decode(),
        Ds_SignatureVersion=SIGNATURE_VERSION,
    )
    return signed_params
