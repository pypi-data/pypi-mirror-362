"""
测试主模块功能
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from yop_mcp.main import (
    yeepay_yop_api_detail,
    yeepay_yop_download_cert,
    yeepay_yop_gen_key_pair,
    yeepay_yop_java_sdk_user_guide,
    yeepay_yop_link_detail,
    yeepay_yop_overview,
    yeepay_yop_parse_certificates,
    yeepay_yop_product_detail_and_associated_apis,
    yeepay_yop_product_overview,
    yeepay_yop_sdk_and_tools_guide,
)


class TestYOPMCPFunctions:
    """测试YOP MCP函数"""

    @patch("tools.http_utils.HttpUtils.download_content")
    def test_yeepay_yop_overview(self, mock_download):
        """测试获取YOP概览"""
        mock_download.return_value = "# YOP Platform Overview\nTest content"

        result = yeepay_yop_overview()

        assert result == "# YOP Platform Overview\nTest content"
        mock_download.assert_called_once_with(
            "https://open.yeepay.com/docs-v3/llms.txt"
        )

    @patch("tools.http_utils.HttpUtils.download_content")
    def test_yeepay_yop_product_overview(self, mock_download):
        """测试获取产品概览"""
        mock_download.return_value = "# Product Overview\nTest products"

        result = yeepay_yop_product_overview()

        assert result == "# Product Overview\nTest products"
        mock_download.assert_called_once_with(
            "https://open.yeepay.com/docs-v3/product/llms.txt"
        )

    @patch("tools.http_utils.HttpUtils.download_content")
    def test_yeepay_yop_product_detail_success(self, mock_download):
        """测试获取产品详情 - 成功情况"""
        mock_download.return_value = "# Product Detail\nTest product detail"

        result = yeepay_yop_product_detail_and_associated_apis("user-scan")

        assert result == "# Product Detail\nTest product detail"
        mock_download.assert_called_once_with(
            "https://open.yeepay.com/docs-v3/product/user-scan/llms.txt"
        )

    @patch("tools.http_utils.HttpUtils.download_content")
    def test_yeepay_yop_product_detail_fallback(self, mock_download):
        """测试获取产品详情 - 回退情况"""
        mock_download.side_effect = [
            "HTTP请求失败: 404",
            "# Fallback Product Detail\nFallback content",
        ]

        result = yeepay_yop_product_detail_and_associated_apis("invalid-product")

        assert result == "# Fallback Product Detail\nFallback content"
        assert mock_download.call_count == 2

    @patch("tools.http_utils.HttpUtils.download_content")
    def test_yeepay_yop_api_detail_uri_format(self, mock_download):
        """测试API详情获取 - URI格式"""
        mock_download.return_value = "# API Detail\nTest API detail"

        result = yeepay_yop_api_detail("/rest/v1.0/aggpay/pre-pay")

        assert result == "# API Detail\nTest API detail"
        # 应该尝试多种格式的URL
        assert mock_download.call_count >= 1

    @patch("tools.http_utils.HttpUtils.download_content")
    def test_yeepay_yop_java_sdk_user_guide(self, mock_download):
        """测试Java SDK用户指南"""
        mock_download.side_effect = [
            '{"data": {"docVersion": "v3.0"}}',
            "# Java SDK Guide\nTest guide",
        ]

        result = yeepay_yop_java_sdk_user_guide()

        assert result == "# Java SDK Guide\nTest guide"

    @patch("tools.http_utils.HttpUtils.download_content")
    def test_yeepay_yop_sdk_and_tools_guide(self, mock_download):
        """测试SDK和工具指南"""
        mock_download.return_value = "# SDK and Tools Guide\nTest guide"

        result = yeepay_yop_sdk_and_tools_guide()

        assert result == "# SDK and Tools Guide\nTest guide"
        mock_download.assert_called_once_with(
            "https://open.yeepay.com/docs-v3/platform/llms.txt"
        )

    @patch("tools.http_utils.HttpUtils.download_content")
    def test_yeepay_yop_link_detail_http_url(self, mock_download):
        """测试链接详情 - HTTP URL"""
        mock_download.return_value = "# Link Detail\nTest link content"

        result = yeepay_yop_link_detail(
            "https://open.yeepay.com/docs-v3/platform/201.md"
        )

        assert result == "# Link Detail\nTest link content"
        mock_download.assert_called_once_with(
            "https://open.yeepay.com/docs-v3/platform/201.md"
        )

    @patch("tools.http_utils.HttpUtils.download_content")
    def test_yeepay_yop_link_detail_relative_url(self, mock_download):
        """测试链接详情 - 相对URL"""
        mock_download.return_value = "# Link Detail\nTest link content"

        result = yeepay_yop_link_detail("docs-v3/platform/201.md")

        assert result == "# Link Detail\nTest link content"
        # 应该转换为完整URL
        mock_download.assert_called_once()

    @patch("yop_mcp.main.gen_key_pair")
    def test_yeepay_yop_gen_key_pair(self, mock_gen_key_pair):
        """测试生成密钥对"""
        mock_gen_key_pair.return_value = {
            "message": "密钥对生成成功",
            "private_key": "test_private_key",
            "public_key": "test_public_key",
        }

        result = yeepay_yop_gen_key_pair("RSA", "pkcs8", "file")

        assert result["message"] == "密钥对生成成功"
        mock_gen_key_pair.assert_called_once_with(
            algorithm="RSA", format="pkcs8", storage_type="file"
        )

    @patch("yop_mcp.main.download_cert")
    def test_yeepay_yop_download_cert(self, mock_download_cert):
        """测试下载证书"""
        mock_download_cert.return_value = {
            "message": "证书下载成功",
            "pfxCert": "/path/to/cert.pfx",
            "pubCert": "/path/to/cert.cer",
        }

        result = yeepay_yop_download_cert(
            algorithm="RSA",
            serial_no="123456",
            auth_code="AUTH123",
            private_key="test_private_key",
            public_key="test_public_key",
            pwd="password123456",  # 使用符合长度要求的密码
        )

        assert result["message"] == "证书下载成功"
        mock_download_cert.assert_called_once()

    @patch("yop_mcp.main.parse_certificates")
    def test_yeepay_yop_parse_certificates(self, mock_parse_certificates):
        """测试解析证书"""
        mock_parse_certificates.return_value = {
            "message": "证书解析成功",
            "privateKey": "parsed_private_key",
            "publicKey": "parsed_public_key",
        }

        result = yeepay_yop_parse_certificates(
            algorithm="RSA",
            pfx_cert="/path/to/cert.pfx",
            pub_cert="/path/to/cert.cer",
            pwd="password123",
        )

        assert result["message"] == "证书解析成功"
        mock_parse_certificates.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
