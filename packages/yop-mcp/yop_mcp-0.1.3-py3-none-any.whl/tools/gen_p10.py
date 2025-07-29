import base64
from enum import Enum
from typing import Any

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization


class KeyType(Enum):
    RSA2048 = "RSA"
    SM2 = "SM2"


def get_signature_alg(key_type: KeyType) -> str:
    if key_type == KeyType.RSA2048:
        return "SHA256withRSA"
    if key_type == KeyType.SM2:
        return "SM3withSM2"
    raise RuntimeError("不支持的算法")


def string2_public_key(pub_key: str, key_type: KeyType) -> Any:
    try:
        decoded_key = base64.b64decode(pub_key)
        if key_type == KeyType.RSA2048:
            return serialization.load_der_public_key(decoded_key)
        if key_type == KeyType.SM2:
            # 对于SM2，使用EC算法和BouncyCastle
            # sm2_obj = sm2.CryptSM2(
            #     public_key=binascii.hexlify(decoded_key).decode(),
            #     private_key=None
            # )
            # return sm2_obj
            return serialization.load_der_public_key(decoded_key)
        raise RuntimeError("不支持的算法")
    except Exception as e:
        raise RuntimeError(f"没有此类算法: {e}") from e


def string2_private_key(pri_key: str, key_type: KeyType) -> Any:
    try:
        decoded_key = base64.b64decode(pri_key)
        if key_type == KeyType.RSA2048:
            return serialization.load_der_private_key(decoded_key, password=None)
        if key_type == KeyType.SM2:
            # 对于SM2，使用EC算法
            # sm2_obj = sm2.CryptSM2(
            #     public_key=None,
            #     private_key=binascii.hexlify(decoded_key).decode()
            # )
            # return sm2_obj
            return serialization.load_der_private_key(decoded_key, password=None)
        raise RuntimeError("不支持的算法")
    except Exception as e:
        raise RuntimeError(f"没有此类算法: {e}") from e


def gen_p10(pri_key: str, pub_key: str, key_type: KeyType) -> str:
    # 第一步：根据算法将公钥字符串转换为公钥对象
    # public_key = string2_public_key(pub_key, key_type)  # 暂时不使用
    _ = pub_key  # 避免未使用变量警告

    # 第二步：根据算法将私钥字符串转换为私钥对象
    private_key = string2_private_key(pri_key, key_type)

    try:
        # 第三步：生成X500Principal对象并创建签名
        x500_name = x509.Name([])  # 空的X500Principal

        # 第四步：创建PKCS10CertificationRequestBuilder
        builder = x509.CertificateSigningRequestBuilder()
        builder = builder.subject_name(x500_name)

        # 第五步：根据签名算法决定签名方式
        if key_type == KeyType.RSA2048:
            sign_algorithm = hashes.SHA256()
            # signature_algorithm = x509.RSASignatureWithSHA256()
        elif key_type == KeyType.SM2:
            sign_algorithm = hashes.SHA256()  # SM2使用SHA256作为替代
        else:
            raise RuntimeError("不支持的算法")

        # 第六步：构建CSR请求并进行签名
        csr = builder.sign(private_key, sign_algorithm)

        # 获取DER格式的CSR并进行base64编码
        csr_der = csr.public_bytes(serialization.Encoding.DER)
        return base64.b64encode(csr_der).decode("utf-8")

    except Exception as e:
        raise RuntimeError(f"生成P10请求失败: {e}") from e


if __name__ == "__main__":
    # 示例RSA密钥（注释掉的长行）
    # pri_key = "MIIEpAIBAAKCAQEAw/21Fbt4/qq924888iha86Qvz9R65UWVj+9JU+gyaE/YUo//eyW37Jg/3jXfL4yPaWcPb7sz6PlhWsxRCSqN4eaEYyCL9/CqGC7S4+r/HeeAusTZBKjRh8nnWUSaRWk0EugzMb0DpMN+HD86HcF40/+bDYzgajcmns+JFbVXNuTvUmjZlPlKmG1i3rTCEZWEzOiIUIGZULIp5lTNDOYUQ5yBhkY1xy9cK8k1kZaBVDZb/b8FXqJ3yE41HITKyUFIEOUPVZlmzO5k6QBM/1ysbATF6hwWIirf9yUti9U8i6GVSv4wZHtLDDVQTC5XcvVtUhbLTOToLl+jAKddMBNYrQIDAQABAoIBABx9SDHpBv0J58A/MY5H1HS/JJ4S1mx2cXezQlb6lT05ggn6WZpWkMZJGVudPBym03/wVbuZnEGc4ox2z77D20z/m7XnGMGJT8hlIg20brIzoTBFBgDZ419YN5Nv1/cIBGRNMYfk4F82daH4hOOnaH90k97j4AlAjBIgu94Wdp+JZVAaAWopvuWOTvIpPCK17YGMCvOTsZ7EoqFdQMVQkz6cuQDY7s7CcxlaxJ/LV1o+UBcF43Z1qBZDwk6d0WpPhUZi0KHxJk6CASDzHUCZS9wbLnpwW3PJxjnkpknF0oihENQDvWCjKbSS+TbIjAIGNKRUk+ebL842J/kHQhIC5zECgYEA+LTHKzK9zm78aZGKc3y8hFEp8I5a5pTTj5keaAA70iQqzvwuaeR4BAqFMhVtijmamQFFAZW+zzN97nfBzjjhhSHjgS7boYcDiU6SBjt7G5ctm90Uh1M/HY4lVZ0xBfBQ7DPal2oD2S86GzfCe+dBtKD1QyYjIcGQiUNq7ASch1kCgYEAyb0oZGLRuh8d5dHbOhe6X/0UgQH4H3zOe2X6gYTbJqrprfuQPAFsp/yPwQqSP1Wu2HYyHjfC+vzXP1ZwTKB47Nf5WGLcWD9dmW5hX0s/45ZtnuAd4NiJAL/oeRn/QyFrTj79L7WCygZ0O6E2WMhcWtNcS6SqRw10CdbW3JkyxXUCgYEAy5mazwdsERoUswu9jwuXfK7BKbgwPEGr7AuKs9M1JbQMA4S5LmElyxEdt0GJejXsFMPQTRrcqN1bg6QwWXWBUa7Lg07r6BESWQ6kRkvdXVnmsYlMK/h/W9+pOqxDnLv+U0+j7H6ShfK+m9eK9En+JTP7dKw86H6Ap440cuDXj4kCgYANeGvyCAco/lrotZKF1n/DWQq9cnw23gaLhsurSku30UG5NEr1NsMilGKk6SfKwtXh7kJ6cg6645cby5HEDBMG/YTQugkse06sqAooasXhVHINYbmdAdhkDGxhabL5sImRt/L/9Ia/Jp8sPB983iQMjIBlLKGSDPvqjEXchP424QKBgQCdupR37xfxdjP4Va1NxrjaxsWg2hgM1j7zLs6mvFtjatFqA9d8UWFQkkBnegaObnMrgYrm7oX/ntVORvfVPoJQ//U91L+Ysr+xvqTzgx36KHqLQXqCxPk2e3Dco6KjDeUYhr1ko5ogBgQZGElTYZTJbKXOCJS30GpjtaZzmtuo6w=="  # noqa: E501
    # pub_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw/21Fbt4/qq924888iha86Qvz9R65UWVj+9JU+gyaE/YUo//eyW37Jg/3jXfL4yPaWcPb7sz6PlhWsxRCSqN4eaEYyCL9/CqGC7S4+r/HeeAusTZBKjRh8nnWUSaRWk0EugzMb0DpMN+HD86HcF40/+bDYzgajcmns+JFbVXNuTvUmjZlPlKmG1i3rTCEZWEzOiIUIGZULIp5lTNDOYUQ5yBhkY1xy9cK8k1kZaBVDZb/b8FXqJ3yE41HITKyUFIEOUPVZlmzO5k6QBM/1ysbATF6hwWIirf9yUti9U8i6GVSv4wZHtLDDVQTC5XcvVtUhbLTOToLl+jAKddMBNYrQIDAQAB"  # noqa: E501
    # key_type = KeyType.RSA2048

    # SM2密钥示例
    PRI_KEY = (
        "MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgDQKlS7bO/Kk5ki6EX2jc7fwpBZdQSfLLkydhhpfNJp+h"
        "RANCAASvzBZG6h3rpDOLy9Fx5yW3Pa6Od3CngeFK5f8uUlPHrtxLmNl0CHBserrsk/fFJanzIKpEEIisR7AOykJ2wqgr"
    )
    PUB_KEY = (
        "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEr8wWRuod66Qzi8vRcecltz2ujndwp4HhSuX/LlJTx67cS5jZdAhwbHq67JP3"
        "xSWp8yCqRBCIrEewDspCdsKoKw=="
    )
    KEY_TYPE = KeyType.SM2
    print(gen_p10(pri_key=PRI_KEY, pub_key=PUB_KEY, key_type=KEY_TYPE))
