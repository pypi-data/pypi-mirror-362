import json
from typing import Any, List, Optional


class JsonUtils:
    @staticmethod
    def object_to_json(data: Any) -> Optional[str]:
        try:
            return json.dumps(data)
        except (TypeError, ValueError) as e:
            print(e)
            return None

    @staticmethod
    def json_to_pojo(json_str: str, cls: Optional[type] = None) -> Any:
        """将JSON字符串转换为Python对象"""
        # cls参数保留用于未来扩展
        _ = cls  # 避免pylint警告
        return json.loads(json_str)

    @staticmethod
    def json_to_list(
        json_data: str, bean_type: Optional[type] = None
    ) -> Optional[List[Any]]:
        try:
            # bean_type参数保留用于未来扩展
            _ = bean_type  # 避免pylint警告
            result = json.loads(json_data)
            if isinstance(result, list):
                return result
            return None
        except (TypeError, ValueError) as e:
            print(e)
            return None
