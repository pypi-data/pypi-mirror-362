"""
证书密钥解析工具
功能：根据证书文件（私钥证书（.pfx）、公钥证书（.cer））解析出Base64编码后的公钥或私钥字符串
"""

import base64
import os
from typing import Any, Dict, Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509 import load_der_x509_certificate, load_pem_x509_certificate


def parse_certificates(
    algorithm: str = "RSA",
    pfx_cert: Optional[str] = None,
    pub_cert: Optional[str] = None,
    pwd: Optional[str] = None,
) -> Dict[str, Any]:
    result = {"message": "解析成功", "privateKey": None, "publicKey": None}

    # 验证算法类型
    if algorithm not in ["RSA", "SM2"]:
        result["message"] = f"不支持的算法类型: {algorithm}，仅支持 RSA 和 SM2"
        return result

    # 如果两个证书文件都没有提供
    if not pfx_cert and not pub_cert:
        result["message"] = "请至少提供一个证书文件（pfx_cert 或 pub_cert）"
        return result

    try:
        # 处理私钥证书
        if pfx_cert and os.path.exists(pfx_cert):
            pfx_result = parse_key_from_certificate(pfx_cert, pwd)
            if pfx_result["private_key"]:
                result["privateKey"] = pfx_result["private_key"]
            if pfx_result["public_key"] and not result.get("publicKey"):
                result["publicKey"] = pfx_result["public_key"]

            # 检查算法类型是否匹配
            if pfx_result["key_type"] != algorithm:
                result["message"] = (
                    f"警告：PFX证书中检测到的算法类型({pfx_result['key_type']})与指定的算法类型({algorithm})不匹配"
                )
        elif pfx_cert:
            result["message"] = f"私钥证书文件不存在: {pfx_cert}"
            return result

        # 处理公钥证书
        if pub_cert and os.path.exists(pub_cert):
            pub_result = parse_key_from_certificate(pub_cert)
            if pub_result["public_key"]:
                result["publicKey"] = pub_result["public_key"]

            # 检查算法类型是否匹配
            if pub_result["key_type"] != algorithm:
                current_message = result["message"]
                if current_message and "warning" in current_message:
                    result["message"] = (
                        current_message
                        + f"，CER证书中检测到的算法类型({pub_result['key_type']})与指定的算法类型({algorithm})不匹配"
                    )
                else:
                    result["message"] = (
                        f"警告：CER证书中检测到的算法类型({pub_result['key_type']})与指定的算法类型({algorithm})不匹配"
                    )
        elif pub_cert:
            current_message = result["message"]
            if (current_message and "warning" in current_message) or (
                pfx_cert and os.path.exists(pfx_cert)
            ):
                result["message"] = (
                    current_message or ""
                ) + f"，公钥证书文件不存在: {pub_cert}"
            else:
                result["message"] = f"公钥证书文件不存在: {pub_cert}"
                return result

        # 检查是否至少解析出了一个密钥
        if not result["privateKey"] and not result["publicKey"]:
            result["message"] = "未能从证书中解析出任何密钥"

        return result
    except (ValueError, OSError, IOError) as e:
        result["message"] = f"解析证书失败: {str(e)}"
        return result


def parse_key_from_certificate(
    cert_path: str, password: Optional[str] = None
) -> Dict[str, Any]:
    """
    从证书文件解析出Base64编码的密钥字符串

    Args:
        cert_path (str): 证书文件路径（.pfx 或 .cer 文件）
        password (str, optional): PFX证书的密码，默认为None

    Returns:
        dict: 包含解析结果的字典，格式如下:
            {
                'key_type': 'RSA'|'SM2'|'UNKNOWN',
                'public_key': Base64编码的公钥字符串,
                'private_key': Base64编码的私钥字符串 (仅当从PFX文件提取时)
            }

    Raises:
        ValueError: 当证书格式不支持或解析失败时
    """
    # 检查文件是否存在
    if not os.path.exists(cert_path):
        raise ValueError(f"证书文件不存在: {cert_path}")

    # 获取文件扩展名
    _, ext = os.path.splitext(cert_path)
    ext = ext.lower()

    result = {"key_type": "UNKNOWN", "public_key": None, "private_key": None}

    try:
        # 处理PFX/PKCS12文件 (包含私钥)
        if ext in (".pfx", ".p12"):
            # 读取证书文件
            with open(cert_path, "rb") as f:
                pfx_data = f.read()

            # 解析PFX
            password_bytes: Optional[bytes] = None
            if password:
                password_bytes = password.encode("utf-8")

            # 解析PFX/PKCS12文件
            private_key, certificate, _ = pkcs12.load_key_and_certificates(
                pfx_data, password_bytes, default_backend()
            )

            # 处理私钥
            if private_key:
                private_bytes = None
                # 判断密钥类型
                if isinstance(private_key, rsa.RSAPrivateKey):
                    result["key_type"] = "RSA"
                    # 获取PKCS8格式的私钥
                    private_bytes = private_key.private_bytes(
                        encoding=serialization.Encoding.DER,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                elif isinstance(private_key, ec.EllipticCurvePrivateKey):
                    # 检查是否为SM2
                    curve = private_key.curve
                    if hasattr(curve, "name") and "sm2" in curve.name.lower():
                        result["key_type"] = "SM2"
                    else:
                        result["key_type"] = "EC"

                    # 获取PKCS8格式的私钥
                    private_bytes = private_key.private_bytes(
                        encoding=serialization.Encoding.DER,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption(),
                    )

                # Base64编码
                if private_bytes:
                    result["private_key"] = base64.b64encode(private_bytes).decode(
                        "ascii"
                    )

            # 处理公钥证书
            if certificate:
                public_key = certificate.public_key()

                # 获取公钥的DER编码
                public_bytes = public_key.public_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )

                # Base64编码
                result["public_key"] = base64.b64encode(public_bytes).decode("ascii")

        # 处理证书文件 (通常只有公钥)
        elif ext in (".cer", ".pem"):
            # 读取证书文件
            with open(cert_path, "rb") as f:
                cert_data = f.read()

            # 尝试以PEM格式加载
            try:
                certificate = load_pem_x509_certificate(cert_data, default_backend())
            except ValueError:
                # 尝试以DER格式加载
                certificate = load_der_x509_certificate(cert_data, default_backend())

            # 提取公钥
            public_key = certificate.public_key()

            # 判断密钥类型
            if isinstance(public_key, rsa.RSAPublicKey):
                result["key_type"] = "RSA"
            elif isinstance(public_key, ec.EllipticCurvePublicKey):
                curve = public_key.curve
                if hasattr(curve, "name") and "sm2" in curve.name.lower():
                    result["key_type"] = "SM2"
                else:
                    result["key_type"] = "EC"

            # 获取公钥的DER编码
            public_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )

            # Base64编码
            result["public_key"] = base64.b64encode(public_bytes).decode("ascii")

        else:
            raise ValueError(f"不支持的证书格式: {ext}")

        return result

    except Exception as e:
        raise ValueError(f"解析证书失败: {str(e)}") from e


def main() -> None:
    try:
        # 注意替换为你实际的PFX文件路径和密码
        pfx_path = "./certs/rsa/4923287028.pfx"
        password = "qwertyuiop[]"

        print(f"解析证书: {pfx_path}")
        print(f"证书密码: {password}")
        print("指定算法: RSA")

        result = parse_certificates(algorithm="RSA", pfx_cert=pfx_path, pwd=password)

        print(f"\n消息: {result['message']}")

        if result["publicKey"]:
            print("\n公钥 (Base64):")
            print(result["publicKey"])

        if result["privateKey"]:
            print("\n私钥 (Base64):")
            print(result["privateKey"])

    except ValueError as e:
        print(f"错误: {str(e)}")


if __name__ == "__main__":
    main()
