#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Any, Dict, Optional, Union

import httpx


class HttpUtils:
    """HTTP工具类，提供同步下载文件、获取内容等功能"""

    @staticmethod
    def download_content(url: str, timeout: Optional[int] = None) -> str:
        """
        同步下载文件（无进度显示）并返回文件内容

        Args:
            url: 下载地址
            timeout: 超时时间（秒）

        Returns:
            str: 下载的文本内容
        """
        try:
            with httpx.Client(http2=True, timeout=timeout) as client:  # 启用HTTP/2加速
                response = client.get(url)
                response.raise_for_status()  # 自动检测4xx/5xx错误
                content = response.text
            print(f"已获取内容，长度: {len(content)} 字符")
            return content
        except httpx.HTTPStatusError as e:
            print(f"HTTP错误 {e.response.status_code}")
            return f"HTTP请求失败: HTTP {e.response.status_code}"
        except Exception as e:  # 保持通用异常处理以支持测试
            print(f"请求失败：{str(e)}")
            return f"HTTP请求失败: {str(e)}"

    @staticmethod
    def download_file(url: str, save_path: str, timeout: Optional[int] = None) -> str:
        """
        同步下载文件（无进度显示）并保存到指定路径

        Args:
            url: 下载地址
            save_path: 保存路径
            timeout: 超时时间（秒）

        Returns:
            str: 保存的文件路径
        """
        try:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            with httpx.Client(http2=True, timeout=timeout) as client:  # 启用HTTP/2加速
                response = client.get(url)
                response.raise_for_status()  # 自动检测4xx/5xx错误
                with open(save_path, "wb") as f:
                    f.write(response.content)  # 适用于小文件
            print(f"文件已保存至 {save_path}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP错误 {e.response.status_code}")
        except IOError as e:
            print(f"文件写入失败：{str(e)}")
        return save_path

    @staticmethod
    def post_json(
        url: str,
        data: dict,
        headers: Optional[dict] = None,
        timeout: Optional[int] = None,
    ) -> Union[dict, str]:
        """
        发送POST请求，提交JSON数据

        Args:
            url: 请求地址
            data: 请求数据（字典格式，将自动转为JSON）
            headers: 请求头
            timeout: 超时时间（秒）

        Returns:
            Union[dict, str]: 响应内容，如果是JSON则返回解析后的字典，否则返回字符串
        """
        try:
            with httpx.Client(http2=True, timeout=timeout) as client:
                if headers is None:
                    headers = {"Content-Type": "application/json"}
                elif "Content-Type" not in headers:
                    headers["Content-Type"] = "application/json"

                response = client.post(url, json=data, headers=headers)
                response.raise_for_status()

                try:
                    json_response: Dict[Any, Any] = response.json()
                    return json_response
                except Exception:  # 保持通用异常处理以支持测试
                    return response.text
        except httpx.HTTPStatusError as e:
            print(f"HTTP错误 {e.response.status_code}")
            return f"HTTP请求失败: HTTP {e.response.status_code}"
        except Exception as e:  # 保持通用异常处理以支持测试
            print(f"请求失败：{str(e)}")
            return f"HTTP请求失败: {str(e)}"

    @staticmethod
    def get_json(
        url: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout: Optional[int] = None,
    ) -> Union[dict, str]:
        """
        发送GET请求，获取JSON数据

        Args:
            url: 请求地址
            params: 查询参数
            headers: 请求头
            timeout: 超时时间（秒）

        Returns:
            Union[dict, str]: 响应内容，如果是JSON则返回解析后的字典，否则返回字符串
        """
        try:
            with httpx.Client(http2=True, timeout=timeout) as client:
                response = client.get(url, params=params, headers=headers)
                response.raise_for_status()

                try:
                    json_response: Dict[Any, Any] = response.json()
                    return json_response
                except (ValueError, TypeError):
                    return response.text
        except httpx.HTTPStatusError as e:
            print(f"HTTP错误 {e.response.status_code}")
            return f"HTTP请求失败: HTTP {e.response.status_code}"
        except (httpx.RequestError, httpx.TimeoutException) as e:
            print(f"请求失败：{str(e)}")
            return f"HTTP请求失败: {str(e)}"

    @staticmethod
    def get_response(
        get_url: str, request_param: Dict[Any, Any], request_header: Dict[Any, Any]
    ) -> str:
        # 验证URL安全性，只允许HTTP和HTTPS协议
        if not get_url.startswith(("http://", "https://")):
            raise ValueError("只支持HTTP和HTTPS协议的URL")

        # 构建查询参数
        params = {}
        if request_param is not None:
            for key, value in request_param.items():
                params[str(key)] = str(value)

        # 使用httpx替代urllib，避免安全风险
        try:
            with httpx.Client(http2=True) as client:
                response = client.get(get_url, params=params, headers=request_header)
                response.raise_for_status()
                return response.text
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"HTTP请求失败: HTTP {e.response.status_code}")
        except Exception as e:
            raise RuntimeError(f"HTTP请求失败: {str(e)}")


# 为了兼容性，保留原始函数名称
def sync_download(url: str, timeout: Optional[int] = None) -> str:
    """同步下载文件（无进度显示）并返回文件内容"""
    return HttpUtils.download_content(url, timeout)


def sync_download_to_file(
    url: str, save_path: str, timeout: Optional[int] = None
) -> str:
    """同步下载文件（无进度显示）"""
    return HttpUtils.download_file(url, save_path, timeout)
