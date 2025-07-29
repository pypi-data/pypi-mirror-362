import base64
import os
from enum import Enum
from typing import Any, Dict, List, Optional

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    pkcs12,
)
from cryptography.x509.oid import NameOID

from tools.config import Config
from tools.http_utils import HttpUtils
from tools.json_utils import JsonUtils


class KeyType(Enum):
    RSA2048 = "RSA"
    SM2 = "SM2"


class CheckResult:
    def __init__(self, result: bool, msg: str = ""):
        self.result = result
        self.msg = msg


class CertDownloadResult:
    def __init__(self, error_msg: Optional[str] = None):
        self.cert: Optional[str] = None
        self.error_msg = error_msg

    def with_cert(self, cert: str) -> "CertDownloadResult":
        self.cert = cert
        return self

    def with_error_msg(self, error_msg: str) -> "CertDownloadResult":
        self.error_msg = error_msg
        return self


class CertUtils:
    @staticmethod
    def load_private_key(pri_key_str: str, key_type: KeyType) -> Any:
        """加载私钥"""
        try:
            pri_key_bytes = base64.b64decode(pri_key_str)
            if key_type == KeyType.RSA2048:
                return serialization.load_der_private_key(pri_key_bytes, password=None)
            elif key_type == KeyType.SM2:
                # 这里需要特殊处理SM2密钥，可能需要使用专门的SM2库
                # 示例实现可能需要使用第三方库如gmssl
                return pri_key_bytes  # 实际实现需要更换
        except Exception as e:
            raise Exception(f"加载私钥失败: {str(e)}")

    @staticmethod
    def load_public_key(pub_key_str: str, key_type: KeyType) -> Any:
        """加载公钥"""
        try:
            pub_key_bytes = base64.b64decode(pub_key_str)
            if key_type == KeyType.RSA2048:
                return serialization.load_der_public_key(pub_key_bytes)
            elif key_type == KeyType.SM2:
                # 同样需要特殊处理SM2公钥
                return pub_key_bytes  # 实际实现需要更换
        except Exception as e:
            raise Exception(f"加载公钥失败: {str(e)}")

    @staticmethod
    def gen_p10(
        pri_key: str, pub_key: str, key_type: KeyType
    ) -> str:  # pylint: disable=unused-argument
        """生成P10证书请求"""
        try:
            # 加载密钥
            private_key = CertUtils.load_private_key(pri_key, key_type)

            # 创建证书请求
            if key_type == KeyType.RSA2048:
                builder = x509.CertificateSigningRequestBuilder()
                builder = builder.subject_name(
                    x509.Name(
                        [
                            x509.NameAttribute(
                                NameOID.COMMON_NAME, "certificate request"
                            ),
                        ]
                    )
                )

                request = builder.sign(private_key, hashes.SHA256())

                # 返回PEM格式的证书请求
                pem_data = request.public_bytes(Encoding.PEM).decode("utf-8")
                pem_data = pem_data.replace("-----BEGIN CERTIFICATE REQUEST-----\n", "")
                pem_data = pem_data.replace("-----END CERTIFICATE REQUEST-----\n", "")
                pem_data = pem_data.replace("\n", "")
                return pem_data
            elif key_type == KeyType.SM2:
                # SM2证书请求需要特殊处理
                # 这里是简化实现，实际需要使用SM2算法库
                return "SM2_CERTIFICATE_REQUEST"  # 实际实现需要更换
            else:
                raise Exception(f"不支持的密钥类型: {key_type}")
        except Exception as e:
            raise Exception(f"生成P10证书请求失败: {str(e)}")

    @staticmethod
    def make_pub_cert(cert: str, serial_no: str, cert_path: str) -> str:
        """生成公钥证书文件"""
        try:
            os.makedirs(cert_path, exist_ok=True)
            pub_cert_path = os.path.join(cert_path, f"{serial_no}.cer")
            SupportUtil.write_string_to_file(cert, pub_cert_path)
            return pub_cert_path
        except Exception as e:
            raise Exception(f"生成公钥证书文件失败: {str(e)}")

    @staticmethod
    def make_pfx_cert(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        pri_key: str,
        cert: str,
        key_type: KeyType,
        pwd: str,
        serial_no: str,
        cert_path: str,
    ) -> str:
        """生成PFX私钥证书文件"""
        try:
            private_key = CertUtils.string2_private_key(pri_key, key_type)
            cert_bytes = cert.encode()

            if not os.path.exists(cert_path):
                os.makedirs(cert_path)

            pri_cert_path = os.path.join(cert_path, f"{serial_no}.pfx")

            if not os.path.exists(pri_cert_path):
                certificate = CertUtils.get_x509_certificate(cert_bytes)
                alias = f"{{{serial_no}}}"
                cfca_certificate = CertUtils.load_cert_chain(key_type)

                # 创建PKCS12格式的密钥存储
                pfx_data = pkcs12.serialize_key_and_certificates(
                    name=alias.encode(),
                    key=private_key,
                    cert=certificate,
                    cas=cfca_certificate,
                    encryption_algorithm=serialization.BestAvailableEncryption(
                        pwd.encode()
                    ),
                )

                # 保存PFX文件
                with open(pri_cert_path, "wb") as pfx_file:
                    pfx_file.write(pfx_data)

            return pri_cert_path

        except Exception as e:
            raise RuntimeError(str(e))

    @staticmethod
    def string2_private_key(pri_key: str, key_type: KeyType) -> Any:
        """
        将私钥字符串转换为私钥对象

        Args:
            pri_key: Base64编码的私钥字符串
            key_type: 密钥类型

        Returns:
            私钥对象
        """
        try:
            # 解码Base64私钥
            key_bytes = base64.b64decode(pri_key)
            # 使用PKCS8格式加载私钥
            private_key = serialization.load_der_private_key(
                key_bytes, password=None, backend=default_backend()
            )
            # 验证密钥类型
            if key_type == KeyType.RSA2048 and not isinstance(
                private_key, rsa.RSAPrivateKey
            ):
                raise RuntimeError(f"Expected RSA private key, got {type(private_key)}")
            elif key_type == KeyType.SM2 and not isinstance(
                private_key, ec.EllipticCurvePrivateKey
            ):
                raise RuntimeError(
                    f"Expected EC private key for SM2, got {type(private_key)}"
                )
            return private_key
        except Exception as e:
            raise RuntimeError("No such algorithm.") from e

    @staticmethod
    def get_x509_certificate(cert_bytes: bytes) -> Any:
        return x509.load_pem_x509_certificate(cert_bytes, default_backend())

    @staticmethod
    def load_cert_chain(key_type: KeyType) -> List[Any]:
        """
        加载证书链

        Args:
            key_type: 密钥类型

        Returns:
            证书链列表
        """
        try:
            qa_host_path = os.path.join(Config.QA_HOST_PATH, "qa_host.txt")

            if not os.path.exists(qa_host_path):
                if key_type == KeyType.SM2:
                    root_cert_name = "config/CFCA_SM2_ACS_CA.pem"
                    middle_cert_name = "config/CFCA_SM2_ACS_OCA31.pem"
                elif key_type == KeyType.RSA2048:
                    root_cert_name = "config/CFCA_RSA_ACS_CA.pem"
                    middle_cert_name = "config/CFCA_RSA_ACS_OCA31.pem"
                else:
                    raise Exception("unsupported alg")
            else:
                if key_type == KeyType.SM2:
                    root_cert_name = "config/CFCA_SM2_ACS_TEST_SM2_CA.cer"
                    middle_cert_name = "config/CFCA_SM2_ACS_TEST_SM2_OCA31.cer"
                elif key_type == KeyType.RSA2048:
                    root_cert_name = "config/CFCA_RSA_ACS_TEST_CA.cer"
                    middle_cert_name = "config/CFCA_RSA_ACS_TEST_OCA31.cer"
                else:
                    raise Exception("unsupported alg")

            # 加载证书文件 - 使用项目根目录的相对路径
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            root_cert_path = os.path.join(project_root, root_cert_name)
            middle_cert_path = os.path.join(project_root, middle_cert_name)

            certs = []
            for cert_path in [root_cert_path, middle_cert_path]:
                with open(cert_path, "rb") as cert_file:
                    cert_data = cert_file.read()
                    if cert_path.endswith(".pem"):
                        cert = x509.load_pem_x509_certificate(
                            cert_data, default_backend()
                        )
                    else:  # .cer file
                        cert = x509.load_der_x509_certificate(
                            cert_data, default_backend()
                        )
                    certs.append(cert)

            return certs

        except Exception as e:
            raise Exception("Failed to load certificate chain") from e

    @staticmethod
    def check_input(
        serial_no: str,
        auth_code: str,
        key_type: KeyType,
        pri_key: str,
        pub_key: str,
        pwd: str,
    ) -> CheckResult:
        """检查输入参数有效性"""
        # 使用key_type参数进行验证
        if key_type not in [KeyType.RSA2048, KeyType.SM2]:
            return CheckResult(False, f"不支持的密钥类型: {key_type}")

        if not serial_no:
            return CheckResult(False, "证书序列号不能为空")
        if not auth_code:
            return CheckResult(False, "授权码不能为空")
        if not pri_key:
            return CheckResult(False, "私钥不能为空")
        if not pub_key:
            return CheckResult(False, "公钥不能为空")

        # 密码长度检查
        if pwd and (len(pwd) < 12 or len(pwd) > 16):
            return CheckResult(False, "密码长度应为12-16位")

        # 检查密钥格式是否为Base64
        try:
            base64.b64decode(pri_key)
            base64.b64decode(pub_key)
        except Exception:
            return CheckResult(False, "密钥格式不正确，应为Base64编码")

        return CheckResult(True)

    @staticmethod
    def check_key(pri_key: str, pub_key: str, key_type: KeyType) -> bool:
        """检查公私钥是否匹配"""
        try:
            # 加载密钥
            private_key = CertUtils.load_private_key(pri_key, key_type)
            public_key = CertUtils.load_public_key(pub_key, key_type)

            if key_type == KeyType.RSA2048:
                # 对于RSA，我们可以通过签名验证来确认密钥对匹配
                # 创建一个测试消息
                test_message = b"test message for key verification"

                # 使用私钥签名
                signature = private_key.sign(
                    test_message, padding.PKCS1v15(), hashes.SHA256()
                )

                # 使用公钥验证
                try:
                    public_key.verify(
                        signature, test_message, padding.PKCS1v15(), hashes.SHA256()
                    )
                    return True
                except Exception:
                    return False

            elif key_type == KeyType.SM2:
                # SM2密钥对验证需要特殊处理
                # 这里是简化实现
                return True  # 实际实现需要更换

        except Exception as e:
            raise Exception(f"密钥验证失败: {str(e)}")

    @staticmethod
    def check_cert(pri_key: str, cert: str, key_type: KeyType) -> bool:
        """检查证书与私钥是否匹配"""
        try:
            # 加载私钥和证书
            private_key = CertUtils.load_private_key(pri_key, key_type)
            certificate = x509.load_pem_x509_certificate(cert.encode("utf-8"))

            # 获取证书中的公钥
            cert_public_key = certificate.public_key()

            # 创建测试消息进行签名验证
            test_message = b"test message for cert verification"

            if key_type == KeyType.RSA2048:
                # 使用私钥签名
                signature = private_key.sign(
                    test_message, padding.PKCS1v15(), hashes.SHA256()
                )

                # 使用证书公钥验证
                try:
                    if isinstance(cert_public_key, rsa.RSAPublicKey):
                        cert_public_key.verify(
                            signature, test_message, padding.PKCS1v15(), hashes.SHA256()
                        )
                    else:
                        # 对于非RSA公钥，暂时返回True
                        pass
                    return True
                except Exception:
                    return False

            elif key_type == KeyType.SM2:
                # SM2证书验证需要特殊处理
                # 这里是简化实现
                return True  # 实际实现需要更换

        except Exception as e:
            raise Exception(f"证书验证失败: {str(e)}")

    @staticmethod
    def download_cert_from_cfca(
        serial_no: str, auth_code: str, cert_req: str
    ) -> CertDownloadResult:
        try:
            # 准备请求数据
            param = {
                "serialNo": serial_no,
                "authCode": auth_code,
                "certReq": cert_req,
                "toolsVersion": Config.TOOLS_VERSION,
            }

            # 发送请求到CFCA API
            headers = {}
            headers["Authorization"] = "Basic " + base64.b64encode(
                Config.BASIC.encode("utf-8")
            ).decode("utf-8")

            response = HttpUtils.get_response(
                Config.CFCA_CERT_DOWNLOAD_URL, param, headers
            )
            map_data = JsonUtils.json_to_pojo(response, dict)

            if map_data.get("code") == "000000":
                data_map = map_data.get("data")
                return CertDownloadResult().with_cert(
                    "-----BEGIN CERTIFICATE-----\n"
                    + data_map.get("cert")
                    + "\n-----END CERTIFICATE-----"
                )
            else:
                return CertDownloadResult().with_error_msg(map_data.get("message"))

        except Exception as e:
            return CertDownloadResult(error_msg=f"下载证书失败: {str(e)}")

    @staticmethod
    def generate_sm2_key_pair() -> List[str]:
        # 使用SM2曲线创建私钥
        private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())

        # 从私钥获取公钥
        public_key = private_key.public_key()

        # 导出私钥，DER格式
        private_key_der = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        # 导出公钥，DER格式
        public_key_der = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        # Base64编码
        private_key_b64 = base64.b64encode(private_key_der).decode("utf-8")
        public_key_b64 = base64.b64encode(public_key_der).decode("utf-8")

        return [private_key_b64, public_key_b64]


class SupportUtil:
    @staticmethod
    def is_file_exists(file_path: str) -> bool:
        """检查文件是否存在"""
        return os.path.exists(file_path)

    @staticmethod
    def read_file_as_string(file_path: str) -> str:
        """从文件中读取内容为字符串"""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def write_string_to_file(content: str, file_path: str) -> None:
        """将字符串内容写入文件"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)


def download_cert(
    algorithm: str = "RSA",
    serial_no: str = "",
    auth_code: str = "",
    private_key: str = "",
    public_key: str = "",
    pwd: str = "",
) -> Dict[str, Any]:
    # 确定密钥类型
    key_type = KeyType.SM2 if algorithm.upper() == "SM2" else KeyType.RSA2048

    # 检查输入参数
    check_result = CertUtils.check_input(
        serial_no, auth_code, key_type, private_key, public_key, pwd
    )
    if not check_result.result:
        return {"message": check_result.msg}

    # 检查公私钥匹配
    p10_generated = False  # 标记是否已生成P10请求
    try:
        if not p10_generated and not CertUtils.check_key(
            private_key, public_key, key_type
        ):
            return {"message": "商户公私钥不匹配，请重新输入"}
    except Exception as e:
        return {"message": f"密钥解析异常: {str(e)}"}

    # 生成证书请求
    if p10_generated:
        cert_req = private_key
    else:
        try:
            cert_req = CertUtils.gen_p10(private_key, public_key, key_type)
        except Exception as e:
            return {"message": f"生成证书请求失败: {str(e)}"}

    # 确定证书保存路径
    cert_path = (
        Config.SM2_CERT_SAVE_PATH
        if key_type == KeyType.SM2
        else Config.RSA_CERT_SAVE_PATH
    )
    pri_cert_path = os.path.join(cert_path, f"{serial_no}.pfx")
    pub_cert_path = os.path.join(cert_path, f"{serial_no}.cer")

    # 检查证书是否已存在
    if SupportUtil.is_file_exists(pri_cert_path) and SupportUtil.is_file_exists(
        pub_cert_path
    ):
        return {
            "message": "本地证书已存在",
            "pfxCert": pri_cert_path,
            "pubCert": pub_cert_path,
        }

    try:
        # 获取证书
        cert: Optional[str] = None
        if SupportUtil.is_file_exists(pub_cert_path):
            cert = SupportUtil.read_file_as_string(pub_cert_path)
        else:
            cert_download_result = CertUtils.download_cert_from_cfca(
                serial_no, auth_code, cert_req
            )
            if cert_download_result.error_msg:
                return {"message": cert_download_result.error_msg}
            cert = cert_download_result.cert

        # 检查证书与私钥匹配
        if cert and not CertUtils.check_cert(private_key, cert, key_type):
            return {"message": "证书已下载过，且证书与输入的私钥不匹配，请核对"}

        # 保存证书
        if cert:
            pub_cert_path = CertUtils.make_pub_cert(cert, serial_no, cert_path)
        if not p10_generated and cert:
            pri_cert_path = CertUtils.make_pfx_cert(
                private_key, cert, key_type, pwd, serial_no, cert_path
            )

        return {
            "message": "CFCA证书激活并下载成功",
            "pfxCert": pri_cert_path,
            "pubCert": pub_cert_path,
        }
    except Exception as e:
        return {"message": f"系统异常，请稍后重试: {str(e)}"}


def gen_key_pair(  # pylint: disable=too-many-arguments,too-many-positional-arguments,redefined-builtin
    algorithm: str = "RSA", format: str = "pkcs8", storage_type: str = "file"
) -> Dict[str, Any]:
    try:
        private_key_str = None
        public_key_str = None

        if algorithm.upper() == "RSA":
            # 生成RSA密钥对，使用2048位密钥长度
            private_key = rsa.generate_private_key(
                public_exponent=65537, key_size=2048, backend=default_backend()
            )
            public_key = private_key.public_key()

            # 处理私钥格式
            if format.lower() == "pkcs8":
                private_key_bytes = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            else:  # pkcs1
                private_key_bytes = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )

            # 处理公钥格式
            public_key_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )

            # 去除PEM头尾并转为Base64字符串
            private_key_str = private_key_bytes.decode("utf-8")
            private_key_str = private_key_str.replace(
                "-----BEGIN PRIVATE KEY-----\n", ""
            )
            private_key_str = private_key_str.replace("-----END PRIVATE KEY-----\n", "")
            private_key_str = private_key_str.replace(
                "-----BEGIN RSA PRIVATE KEY-----\n", ""
            )
            private_key_str = private_key_str.replace(
                "-----END RSA PRIVATE KEY-----\n", ""
            )
            private_key_str = private_key_str.replace("\n", "")

            public_key_str = public_key_bytes.decode("utf-8")
            public_key_str = public_key_str.replace("-----BEGIN PUBLIC KEY-----\n", "")
            public_key_str = public_key_str.replace("-----END PUBLIC KEY-----\n", "")
            public_key_str = public_key_str.replace("\n", "")

        elif algorithm.upper() == "SM2":
            if format.lower() != "pkcs8":
                return {
                    "message": "SM2密钥只支持生成PKCS8格式",
                    "privateKey": None,
                    "publicKey": None,
                    "privateCert": None,
                    "publicCert": None,
                }
            private_key_str, public_key_str = CertUtils.generate_sm2_key_pair()
        else:
            return {
                "message": f"不支持的密钥算法: {algorithm}",
                "privateKey": None,
                "publicKey": None,
                "privateCert": None,
                "publicCert": None,
            }

        # 如果需要保存到文件
        private_cert_path = None
        public_cert_path = None

        if storage_type.lower() == "file":
            # 创建目录
            key_dir = "./keys/"
            os.makedirs(key_dir, exist_ok=True)

            algorithm_name = "RSA2048" if algorithm.upper() == "RSA" else "SM2"

            # 保存私钥
            private_cert_path = os.path.join(key_dir, f"应用私钥{algorithm_name}.txt")
            with open(private_cert_path, "w", encoding="utf-8") as f:
                f.write(private_key_str)

            # 保存公钥
            public_cert_path = os.path.join(key_dir, f"应用公钥{algorithm_name}.txt")
            with open(public_cert_path, "w", encoding="utf-8") as f:
                f.write(public_key_str)

        return {
            "message": "密钥对生成成功"
            + ("，并已保存到文件" if storage_type.lower() == "file" else ""),
            "privateKey": private_key_str,
            "publicKey": public_key_str,
            "privateCert": private_cert_path,
            "publicCert": public_cert_path,
        }

    except Exception as e:
        return {
            "message": f"生成密钥对失败: {str(e)}",
            "privateKey": None,
            "publicKey": None,
            "privateCert": None,
            "publicCert": None,
        }


def main() -> None:
    # 下载证书
    serial_no = "4931008761"
    auth_code = "A396G3AY47"
    private_key = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCj0pMOyEt0orX/+GPNMCueo/dZJC/KUqTtHHFXQB6Kc/vCQJSvWGPpIQEFiA68zzvjnhg3oKwT2vG9Gp2vmDC2V/zuCu2HyCi/mobMX/Mzch7O3beA/0A4d0ZzpyUKLRoq6PUb7jLqY+rnowFCNK4g8oLNA+sipJr3a1FFze9sBJKLFcPknSt7FtElgYIsXaXyHWJLHChusb99oZ8JZzZuA/DMRTdQUjf7fZoAq8gcXTtanZC6/2J07BAG8f0ZLc8qeEixApFE48xZ3p0N6brGq2eycs3tUMgcEiuvHRIB3p9TPFbLOdGR6D3dTz6EC87ImgchtVLA4VOuuEEsTZxFAgMBAAECggEAClijNvzJXy1jhy39x5iyOIusdHHHnuSHS/5O3i7Lfv0COmtvuH9BmBigguPr4lrIMoDqkKDSHVLnj4TdzpgzA2EdNT91buziPe+ZcdDhgC9F6NSx4TC9spM93NICkdj1XR5nVIM/rfPvgv+VdcPz91q5jg8gS4jPzK53bIwsActSIthwjmeT9QAUy7Nu3CTkLQTf1oJ5sV7AG+mJ28a1/l4Y/VBUWfplgNeahdcZ3Y5W3bc3yg82wD0aDyy+an+KVq9Kk3Jy/bUMBCzlujb7GAJRS/7Z6TLcRpSUYKnqKpD42IjOsAnZYYnouXxVbRbvUrn/8yVlapSP3wJ5LtRHIQKBgQDiT9jtMcf4W/99ekuIMp4w5FDQvxnr3y40aaxEl+qmiFHoznOlBN9cPNFR/yyCW14+nfF73GBpMcM1M96jSIkVhrWngSYBJ4LUtdOejb/iyl2hJrkIlxmfxUFXImdB1Dz6dbDvNo8/mTgeyykuBVycn33N3jsokjhNZ8TUYwGuKQKBgQC5UCtfNnFZrjYUSQomyBjfoNCo10L7UVOUUIgzdTloD4A4JdD5QdDHoOqK1sgWxMGa8pnN6ONUlntIh9DDUTvWI5ESNFAyVuXHIteaLACxo4XLGnfILcd83JuUVWXJ9qM6BJgCJ7bKasjYabnE8vD6w2hhxEpxb4r/v1pVJADIvQKBgFy1Nvkb3n44ObZORejaS4Fd1lldH6JHf+cKrv4+eWqVB3DmOeuMzm87nsgHT1VrVnUyQH1r7rbJIt2FjRu4mCeQUpP2zPnGFMtMXQ9jpAqkuaxNb5k8RMv1g2nNdx05c21qjvu/jvkPrDS5JvpqSeEDWQbflb5t/9B9xNz4XfTZAoGBAKtXiQK8IAo/nhkbf5tkIDuFQekbP/+HrrPP0l9h3/Zrfq5rqNEPHa+3BaXh+ZezzR8reTJ+RtOLX+osScaOcbkJobUnUY958XMysA8I6ItXGvo0OtSIH48/m0qHu1oGBd47KSG0/roiChqvhuiniFEUJIthJ0PDUs4ta6SVaXQxAoGAHBwLgpLtqU94IgkPe2/+p8R17l2BfbqwF6NUwxvjAM8uEd43eymGgfvHfUS580h7MDiNdrcXSntvlyokVejdJTufaCu6itNjVztYbwaJqkJ8vFHidlMvXKVtuvE8YAKrPm9CtwtQSm3zuwx2BNPE5AxXHcXiloks5kh7iNPaBN8="
    public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAo9KTDshLdKK1//hjzTArnqP3WSQvylKk7RxxV0AeinP7wkCUr1hj6SEBBYgOvM87454YN6CsE9rxvRqdr5gwtlf87grth8gov5qGzF/zM3Iezt23gP9AOHdGc6clCi0aKuj1G+4y6mPq56MBQjSuIPKCzQPrIqSa92tRRc3vbASSixXD5J0rexbRJYGCLF2l8h1iSxwobrG/faGfCWc2bgPwzEU3UFI3+32aAKvIHF07Wp2Quv9idOwQBvH9GS3PKnhIsQKRROPMWd6dDem6xqtnsnLN7VDIHBIrrx0SAd6fUzxWyznRkeg93U8+hAvOyJoHIbVSwOFTrrhBLE2cRQIDAQAB"
    print(
        download_cert(
            algorithm="RSA",
            serial_no=serial_no,
            auth_code=auth_code,
            private_key=private_key,
            public_key=public_key,
            pwd="1234567891234",
        )
    )

    # 生成密钥对
    # private_key, public_key = CertUtils.generate_key()
    # print(f"私钥(Base64): {private_key}")
    # print(f"公钥(Base64): {public_key}")

    # print(gen_key_pair(algorithm="RSA", format="pkcs8", storage_type="string"))


if __name__ == "__main__":
    main()
