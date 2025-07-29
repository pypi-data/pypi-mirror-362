import os


class Config:
    # 证书保存路径
    RSA_CERT_SAVE_PATH = "./certs/rsa/"
    SM2_CERT_SAVE_PATH = "./certs/sm2/"

    # API主机地址
    HOST = "https://mp.yeepay.com"

    # CFCA API相关配置
    CFCA_CERT_DOWNLOAD_URL = HOST + "/yop-developer-center/apis/cfca/cert/download"
    BASIC = "keytools:keytools"
    TOOLS_VERSION = "mcp"

    # QA环境配置
    QA_HOST_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")

    @classmethod
    def get_cert_path(cls, algorithm: str) -> str:
        """获取证书保存路径"""
        if algorithm.upper() == "RSA":
            return cls.RSA_CERT_SAVE_PATH
        if algorithm.upper() == "SM2":
            return cls.SM2_CERT_SAVE_PATH
        raise ValueError(f"不支持的算法: {algorithm}")

    @classmethod
    def is_supported_algorithm(cls, algorithm: str) -> bool:
        """检查是否支持指定算法"""
        return algorithm.upper() in ["RSA", "SM2"]
