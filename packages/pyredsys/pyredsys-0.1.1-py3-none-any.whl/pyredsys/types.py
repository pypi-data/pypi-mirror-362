from typing import Annotated, Any
from urllib.parse import unquote

from pydantic import BaseModel, Field, HttpUrl, field_serializer, field_validator


class MerchantParameters(BaseModel):
    # Read https://pagosonline.redsys.es/desarrolladores-inicio/integrate-con-nosotros/parametros-de-entrada-y-salida/
    DS_MERCHANT_ORDER: Annotated[
        str, Field(max_length=12, min_length=4, pattern=r"^[0-9]{4}[0-9A-Za-z]{0,8}$")
    ]
    DS_MERCHANT_MERCHANTCODE: Annotated[int, Field(le=999999999)]  # 9 digits max
    DS_MERCHANT_TERMINAL: Annotated[int, Field(le=999)]  # 3 digits max
    DS_MERCHANT_CURRENCY: Annotated[int, Field(le=9999)]  # 4 digits max
    DS_MERCHANT_TRANSACTIONTYPE: Annotated[int, Field(le=9)]  # 1 digit max
    DS_MERCHANT_AMOUNT: Annotated[int, Field(le=999999999999)]  # 12 digits max
    DS_MERCHANT_MERCHANTURL: Annotated[HttpUrl, Field(max_length=250)]
    DS_MERCHANT_URLOK: Annotated[HttpUrl, Field(max_length=250)]
    DS_MERCHANT_URLKO: Annotated[HttpUrl, Field(max_length=250)]

    # Optional fields, these are excluded, unless explicitly set

    # TODO: find what these languages map to, 2 is english
    DS_MERCHANT_CONSUMERLANGUAGE: Annotated[int, Field(le=999)] = 2
    DS_MERCHANT_MERCHANTDATA: Annotated[str, Field(max_length=1024)] = ""
    DS_MERCHANT_PRODUCTDESCRIPTION: Annotated[str, Field(max_length=125)] = ""

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
