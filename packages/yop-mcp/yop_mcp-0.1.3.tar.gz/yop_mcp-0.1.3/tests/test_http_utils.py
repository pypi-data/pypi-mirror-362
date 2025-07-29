"""
测试HTTP工具模块
"""

import os
import sys
from unittest.mock import MagicMock, patch

import httpx
import pytest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.http_utils import HttpUtils


class TestHttpUtils:
    """测试HTTP工具类"""

    @patch("httpx.Client")
    def test_download_content_success(self, mock_client):
        """测试成功下载内容"""
        # 设置mock
        mock_response = MagicMock()
        mock_response.text = "Test content"
        mock_response.raise_for_status.return_value = None

        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance

        # 执行测试
        result = HttpUtils.download_content("https://example.com/test")

        # 验证结果
        assert result == "Test content"
        mock_client_instance.get.assert_called_once_with("https://example.com/test")

    @patch("httpx.Client")
    def test_download_content_http_error(self, mock_client):
        """测试HTTP错误情况"""
        # 设置mock
        mock_response = MagicMock()
        mock_response.status_code = 404

        mock_client_instance = MagicMock()
        mock_client_instance.get.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=MagicMock(), response=mock_response
        )
        mock_client.return_value.__enter__.return_value = mock_client_instance

        # 执行测试
        result = HttpUtils.download_content("https://example.com/notfound")

        # 验证结果
        assert result.startswith("HTTP请求失败: HTTP 404")

    @patch("httpx.Client")
    def test_download_content_general_error(self, mock_client):
        """测试一般错误情况"""
        # 设置mock
        mock_client_instance = MagicMock()
        mock_client_instance.get.side_effect = Exception("Connection error")
        mock_client.return_value.__enter__.return_value = mock_client_instance

        # 执行测试
        result = HttpUtils.download_content("https://example.com/error")

        # 验证结果
        assert result.startswith("HTTP请求失败: Connection error")

    @patch("httpx.Client")
    @patch("builtins.open", create=True)
    @patch("pathlib.Path.mkdir")
    def test_download_file_success(self, mock_mkdir, mock_open, mock_client):
        """测试成功下载文件"""
        # 设置mock
        mock_response = MagicMock()
        mock_response.content = b"Test file content"
        mock_response.raise_for_status.return_value = None

        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # 执行测试
        result = HttpUtils.download_file("https://example.com/file", "/path/to/save")

        # 验证结果
        assert result == "/path/to/save"
        mock_file.write.assert_called_once_with(b"Test file content")

    @patch("httpx.Client")
    def test_post_json_success(self, mock_client):
        """测试成功POST JSON"""
        # 设置mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.raise_for_status.return_value = None

        mock_client_instance = MagicMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance

        # 执行测试
        data = {"key": "value"}
        result = HttpUtils.post_json("https://example.com/api", data)

        # 验证结果
        assert result == {"status": "success"}
        mock_client_instance.post.assert_called_once()

    @patch("httpx.Client")
    def test_post_json_text_response(self, mock_client):
        """测试POST JSON返回文本"""
        # 设置mock
        mock_response = MagicMock()
        mock_response.json.side_effect = Exception("Not JSON")
        mock_response.text = "Plain text response"
        mock_response.raise_for_status.return_value = None

        mock_client_instance = MagicMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance

        # 执行测试
        data = {"key": "value"}
        result = HttpUtils.post_json("https://example.com/api", data)

        # 验证结果
        assert result == "Plain text response"

    @patch("httpx.Client")
    def test_get_json_success(self, mock_client):
        """测试成功GET JSON"""
        # 设置mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status.return_value = None

        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance

        # 执行测试
        result = HttpUtils.get_json("https://example.com/api")

        # 验证结果
        assert result == {"data": "test"}
        mock_client_instance.get.assert_called_once_with(
            "https://example.com/api", params=None, headers=None
        )

    @patch("httpx.Client")
    def test_get_response_success(self, mock_client):
        """测试get_response方法成功"""
        # 设置mock
        mock_response = MagicMock()
        mock_response.text = '{"result": "success"}'
        mock_response.raise_for_status.return_value = None

        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance

        # 执行测试
        params = {"param1": "value1", "param2": "value2"}
        headers = {"Authorization": "Bearer token"}
        result = HttpUtils.get_response("https://example.com/api", params, headers)

        # 验证结果
        assert result == '{"result": "success"}'
        mock_client_instance.get.assert_called_once_with(
            "https://example.com/api",
            params={"param1": "value1", "param2": "value2"},
            headers=headers,
        )


if __name__ == "__main__":
    pytest.main([__file__])
