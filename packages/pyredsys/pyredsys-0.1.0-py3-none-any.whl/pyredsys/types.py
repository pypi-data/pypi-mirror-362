from typing import Annotated, Any, Literal
from urllib.parse import unquote

from pydantic import BaseModel, Field, HttpUrl, field_serializer, field_validator


class MerchantParameters(BaseModel):
    DS_MERCHANT_ORDER: Annotated[str, Field(max_length=12)]
    DS_MERCHANT_MERCHANTCODE: int
    DS_MERCHANT_TERMINAL: int
    DS_MERCHANT_CURRENCY: int
    DS_MERCHANT_TRANSACTIONTYPE: int
    DS_MERCHANT_AMOUNT: int
    DS_MERCHANT_MERCHANTURL: HttpUrl
    DS_MERCHANT_URLOK: HttpUrl
    DS_MERCHANT_URLKO: HttpUrl

    # Optional fields, these are excluded, unless explicitly set

    # TODO: find what these languages map to, 2 is english
    DS_MERCHANT_CONSUMERLANGUAGE: Literal[0, 1, 2, 3, 7, 8, 9, 15, 17, 34, 37] = 0

    @field_serializer(
        "DS_MERCHANT_MERCHANTCODE",
        "DS_MERCHANT_TERMINAL",
        "DS_MERCHANT_CURRENCY",
        "DS_MERCHANT_TRANSACTIONTYPE",
        "DS_MERCHANT_AMOUNT",
    )
    def serialize_ints_as_strings(self, value: Any):
        # important to serialize these fields into int
        # because RedSys accepts these fields as str, not int
        return str(value)


class SignedMerchantParameters(BaseModel):
    Ds_MerchantParameters: str
    Ds_Signature: str
    Ds_SignatureVersion: str


class NotificationParameters(BaseModel):
    Ds_Date: str
    Ds_Hour: str
    Ds_SecurePayment: int
    Ds_Card_Country: int
    Ds_Amount: int
    Ds_Currency: int
    Ds_Order: str
    Ds_MerchantCode: int
    Ds_Terminal: int
    Ds_Response: int  # 0000 is success
    Ds_MerchantData: str
    Ds_TransactionType: int
    Ds_ConsumerLanguage: int
    Ds_AuthorisationCode: int
    Ds_Card_Brand: int
    Ds_Card_Typology: str
    Ds_Merchant_Cof_Txnid: int
    Ds_ProcessedPayMethod: int
    Ds_Control_1752472475397: int

    @field_validator("Ds_Date", "Ds_Hour", mode="before")
    @classmethod
    def decode_url(cls, v: Any):
        # Ds_Date and Ds_Hour is encoded as url-safe
        # For example: 14%2F07%2F2025, 07%3A54
        # This converts it to 14/07/2025, 07:54
        return unquote(v)
