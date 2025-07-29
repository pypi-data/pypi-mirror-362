import json
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

from tools.cert_key_parser import parse_certificates
from tools.cert_utils import download_cert, gen_key_pair
from tools.http_utils import HttpUtils

# Create an MCP server
mcp = FastMCP("yop-mcp")


@mcp.tool()
def yeepay_yop_overview() -> str:
    """
    通过此工具，可以了解易宝支付开放平台(YOP)的平台规范，接入流程，网站地图，内容中包含链接时可以调用工具yeepay_yop_link_detail进一步获取其详细内容

    Returns:
        str: 易宝支付开放平台(YOP)的概览信息(markdown格式)
    """

    return HttpUtils.download_content("https://open.yeepay.com/docs-v3/llms.txt")


@mcp.tool()
def yeepay_yop_product_overview() -> str:
    """
    通过此工具，获取易宝支付开放平台(YOP)的产品能力概览，内容中包含链接时可以调用工具yeepay_yop_link_detail进一步获取其详细内容

    Returns:
        str: 易宝支付开放平台(YOP)的产品能力概览(markdown格式)
    """

    return HttpUtils.download_content(
        "https://open.yeepay.com/docs-v3/product/llms.txt"
    )


@mcp.tool()
def yeepay_yop_product_detail_and_associated_apis(product_code: str) -> str:
    """
    通过此工具，获取易宝支付开放平台(YOP)指定产品的产品介绍，使用说明、相关的API接口列表，内容中包含链接时可以调用工具yeepay_yop_link_detail进一步获取其详细内容

    Args:
        product_code: str - 产品编码(产品的唯一标识)

    Returns:
        str: 易宝支付开放平台(YOP)指定产品的产品介绍，使用说明、相关的API接口列表(markdown格式)
    """

    product_code = product_code.strip()
    # https://open.yeepay.com/docs-v3/product/user-scan/llms.txt
    response = HttpUtils.download_content(
        "https://open.yeepay.com/docs-v3/product/" + product_code + "/llms.txt"
    )
    # 如果返回错误，则调用备用地址
    if response.startswith("HTTP请求失败"):
        return HttpUtils.download_content(
            "https://open.yeepay.com/docs-v3/product/llms.txt"
        )
    return response


@mcp.tool()
def yeepay_yop_api_detail(api_uri: str) -> str:
    """
    通过此工具，获取易宝支付开放平台(YOP)的API接口的详细定义，包含基本信息、请求参数、请求示例、
    响应参数、响应示例、错误码、回调、示例代码等信息，内容中包含链接时可以调用工具yeepay_yop_link_detail进一步获取其详细内容

    Args:
        api_uri: str - API的URI路径， 例如：/rest/v1.0/aggpay/pre-pay,
            https://open.yeepay.com/docs-v3/api/post_rest_v1.0_aggpay_pre-pay.md,
            https://open.yeepay.com/docs-v2/apis/user-scan/post__rest__v1.0__aggpay__pre-pay/index.html

    Returns:
        str: 易宝支付开放平台(YOP)的API接口的详细定义，包含基本信息、请求参数、请求示例、
            响应参数、响应示例、错误码、回调、示例代码等信息(markdown格式)

    """

    api_uri = api_uri.strip()
    response = "HTTP请求失败"

    if api_uri.startswith("http"):
        if api_uri.endswith(".md"):
            response = HttpUtils.download_content(api_uri)
        elif (
            api_uri.endswith(".html")
            or "/docs/apis/" in api_uri
            or "/docs-v2/apis/" in api_uri
        ):
            url_parts = api_uri.split("/")
            for part in url_parts:
                if (
                    part.startswith("post__")
                    or part.startswith("get__")
                    or part.startswith("options__")
                ):
                    api_id = part.replace("__", "_")
                    response = HttpUtils.download_content(
                        "https://open.yeepay.com/docs-v3/api/" + api_id + ".md"
                    )
                    break

    if response.startswith("HTTP请求失败") and "_" in api_uri:
        response = HttpUtils.download_content(
            "https://open.yeepay.com/docs-v3/api/" + api_uri + ".md"
        )

    formatted_api_uri = api_uri.replace("/", "_")
    if response.startswith("HTTP请求失败"):
        response = HttpUtils.download_content(
            "https://open.yeepay.com/docs-v3/api/" + formatted_api_uri + ".md"
        )
    if response.startswith("HTTP请求失败"):
        response = HttpUtils.download_content(
            "https://open.yeepay.com/docs-v3/api/post" + formatted_api_uri + ".md"
        )
    if response.startswith("HTTP请求失败"):
        response = HttpUtils.download_content(
            "https://open.yeepay.com/docs-v3/api/get" + formatted_api_uri + ".md"
        )
    if response.startswith("HTTP请求失败"):
        response = HttpUtils.download_content(
            "https://open.yeepay.com/docs-v3/api/options" + formatted_api_uri + ".md"
        )

    return response


@mcp.tool()
def yeepay_yop_sdk_and_tools_guide() -> str:
    """
    通过此工具，获取易宝支付开放平台(YOP)提供的各种SDK和工具的使用说明，内容中包含链接时可以调用工具yeepay_yop_link_detail进一步获取其详细内容

    Returns:
        str: 易宝支付开放平台(YOP)提供的各种SDK和工具的使用说明，以及对接最佳实践等(markdown格式)

    """
    try:
        return HttpUtils.download_content(
            "https://open.yeepay.com/docs-v3/platform/llms.txt"
        )
    except (ValueError, TypeError, ConnectionError):
        return "HTTP请求失败, url: https://open.yeepay.com/docs-v3/platform/llms.txt"


@mcp.tool()
def yeepay_yop_link_detail(url: str) -> str:
    """
    通过此工具，获取易宝支付开放平台(YOP)的各个子页面或者外部链接的详细内容，内容中包含链接时可以调用工具yeepay_yop_link_detail进一步获取其详细内容

    Args:
        url: str - 易宝支付开放平台(YOP)的子页面的URL地址

    Returns:
        str: 易宝支付开放平台(YOP)的各个子页面的详细内容

    """
    try:
        if url.startswith("http"):
            return HttpUtils.download_content(url)

        url = ("https://open.yeepay.com/" + url).replace("//", "/")
        return HttpUtils.download_content(url)
    except (ValueError, TypeError, ConnectionError):
        return "HTTP请求失败, url: " + url


@mcp.tool()
def yeepay_yop_java_sdk_user_guide() -> str:
    """
    通过此工具，获取易宝支付开放平台(YOP)的yop-java-sdk的使用说明，内容中包含链接时可以调用工具yeepay_yop_link_detail进一步获取其详细内容

    Returns:
        str: 易宝支付开放平台(YOP)的yop-java-sdk的使用说明(markdown格式)

    """
    try:
        platform_info = json.loads(
            HttpUtils.download_content(
                "https://open.yeepay.com/apis/commons/doc/platform/info"
            )
        )
        platform_version = platform_info.get("data").get("docVersion")
        return HttpUtils.download_content(
            "https://open.yeepay.com/apis/docs/platform/"
            + platform_version
            + "/sdk_guide/java-sdk-guide.html"
        )
    except (ValueError, TypeError, ConnectionError):
        return HttpUtils.download_content(
            "https://open.yeepay.com/docs-v3/platform/201.md"
        )


@mcp.tool()
def yeepay_yop_gen_key_pair(
    algorithm: str = "RSA", key_format: str = "pkcs8", storage_type: str = "file"
) -> Dict[str, Any]:
    """
    根据密钥算法生成非对称加密的密钥对（公钥和私钥），并保存到本地路径

    参数:
        algorithm: 密钥算法，可选值为 "RSA" 或 "SM2"，默认为 "RSA"
        key_format: 密钥格式，可选值为 "pkcs8"或"pkcs1"，默认为 "pkcs8"
        storage_type: 密钥存储类型，"file"或"string"，默认为 "file"
    """
    return gen_key_pair(
        algorithm=algorithm, format=key_format, storage_type=storage_type
    )


@mcp.tool()
def yeepay_yop_download_cert(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    algorithm: str = "RSA",
    serial_no: str = "",
    auth_code: str = "",
    private_key: str = "",
    public_key: str = "",
    pwd: str = "",
) -> Dict[str, Any]:
    """
    根据密钥算法、CFCA证书的序列号、授权码、非对称密钥对（公钥和私钥）、密码，下载该证书，并保存到本地路径

    Args:
        algorithm: 密钥算法，可选值为 "RSA" 或 "SM2"，默认为 "RSA"
        serial_no: cfca证书序列号
        auth_code: cfca证书授权码
        private_key: Base64 编码后的私钥字符串
        public_key: Base64 编码后的公钥字符串
        pwd: 密码，长度：12~16位

    Returns:
        Dict包含:
        - message: 响应信息
        - pfxCert: 私钥证书路径(.pfx)
        - pubCert: 公钥证书路径(.cer)
    """
    return download_cert(
        algorithm=algorithm,
        serial_no=serial_no,
        auth_code=auth_code,
        private_key=private_key,
        public_key=public_key,
        pwd=pwd,
    )


@mcp.tool()
def yeepay_yop_parse_certificates(
    algorithm: str = "RSA",
    pfx_cert: Optional[str] = None,
    pub_cert: Optional[str] = None,
    pwd: Optional[str] = None,
) -> Dict[str, Any]:
    """
    根据证书文件解析出Base64编码后的公钥或私钥字符串

    Args:
        algorithm (str): 密钥算法，可选值为 "RSA" 或 "SM2"，默认为 "RSA"
        pfx_cert (str): 私钥证书（.pfx）文件路径
        pub_cert (str): 公钥证书（.cer）文件路径
        pwd (str, optional): PFX证书的密码，默认为None

    Returns:
        dict: 包含解析结果的字典，格式如下:
            {
                'message': 响应信息,
                'privateKey': Base64编码后的私钥字符串,
                'publicKey': Base64编码后的公钥字符串
            }
    """
    return parse_certificates(
        algorithm=algorithm, pfx_cert=pfx_cert, pub_cert=pub_cert, pwd=pwd
    )


# -------------------------------------------------官方示例------------------------------------------
# Add an addition tool
# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """Add two numbers"""
#     return a + b

# Cursor 不支持资源、提示词
# Add a dynamic greeting resource
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}!"

# @mcp.prompt()
# def echo_prompt(message: str) -> str:
#     """Create an echo prompt"""
#     return f"Please process this message: {message}"


def main() -> None:
    """Main entry point for the YOP MCP Server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
    # 生成密钥对
    # print(yeepay_yop_gen_key_pair(algorithm="SM2", format="pkcs8", storage_type="file"))

    # 下载证书
    # serial_no = "4928999747"
    # auth_code = "64NPRSS6AR"
    # private_key = "MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgDQKlS7bO/Kk5ki6EX2jc7fwpBZdQSfLLkydhhpfNJp+h" \
    #               "RANCAASvzBZG6h3rpDOLy9Fx5yW3Pa6Od3CngeFK5f8uUlPHrtxLmNl0CHBserrsk/fFJanzIKpEEIisR7AOykJ2wqgr"
    # public_key = "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEr8wWRuod66Qzi8vRcecltz2ujndwp4HhSuX/LlJTx67cS5jZdAhwbHq67JP3" \
    #              "xSWp8yCqRBCIrEewDspCdsKoKw=="
    # print(yeepay_yop_download_cert(algorithm="SM2", serial_no=serial_no, auth_code=auth_code,
    #                                private_key=private_key, public_key=public_key, pwd="qwertyuiop[]"))
