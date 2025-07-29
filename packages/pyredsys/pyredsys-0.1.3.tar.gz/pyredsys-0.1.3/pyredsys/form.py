from pyredsys.types import SignedMerchantParameters

html_template = """
<form name="from"
      action="https://sis-t.redsys.es:25443/sis/realizarPago"
      method="post">
       <input type="hidden" name="Ds_SignatureVersion" value="{Ds_SignatureVersion}" />
       <input type="hidden"
              name="Ds_MerchantParameters"
              value="{Ds_MerchantParameters}" />
       <input type="hidden"
              name="Ds_Signature"
              value="{Ds_Signature}" />
       <input type="submit" />
</form>
"""


def render_form(params: SignedMerchantParameters):
    return html_template.format(
        Ds_SignatureVersion=params.Ds_SignatureVersion,
        Ds_MerchantParameters=params.Ds_MerchantParameters,
        Ds_Signature=params.Ds_Signature,
    )
