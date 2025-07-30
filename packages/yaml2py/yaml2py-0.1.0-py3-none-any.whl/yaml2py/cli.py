import os
import re
from pathlib import Path
from typing import Any, Dict, List, Type, Union

import click  # 使用 Click 來建立漂亮的 CLI
import yaml


def snake_to_camel(snake_str: str) -> str:
    """將 snake_case 轉換為 CamelCase"""
    components = snake_str.split("_")
    return "".join(x.title() for x in components)


def to_snake_case(camel_str: str) -> str:
    """將 CamelCase 轉換為 snake_case"""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_str)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def infer_yaml_type(value: Any) -> str:
    """推斷 YAML 值的 Python 型態"""
    if value is None:
        return "Optional[Any]"
    elif isinstance(value, bool):
        # 注意：bool 必須在 int 之前檢查
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "str"
    elif isinstance(value, list):
        if not value:
            return "List[Any]"
        # 分析列表元素型態
        element_types = set()
        for item in value:
            element_types.add(infer_yaml_type(item))
        if len(element_types) == 1:
            return f"List[{element_types.pop()}]"
        return f"List[Union[{', '.join(sorted(element_types))}]]"
    elif isinstance(value, dict):
        return "Dict[str, Any]"
    else:
        return "Any"


def is_sensitive_field(field_name: str) -> bool:
    """檢查是否為敏感欄位"""
    sensitive_keywords = ["password", "secret", "token", "key", "api_key", "private"]
    return any(keyword in field_name.lower() for keyword in sensitive_keywords)


class YamlSchemaGenerator:
    """YAML Schema 生成器"""

    def __init__(self):
        self.nested_classes = []
        self.generated_classes = set()  # 避免重複生成相同的類別

    def generate_class_definition(
        self, name: str, data: Dict[str, Any], level: int = 0
    ) -> str:
        """生成類別定義（包含巢狀類別）"""
        class_name = snake_to_camel(name) + "Schema"

        # 避免重複生成
        if class_name in self.generated_classes:
            return ""
        self.generated_classes.add(class_name)

        # 先處理巢狀類別
        nested_definitions = []
        properties = []

        for key, value in data.items():
            prop_name = to_snake_case(key)

            if isinstance(value, dict):
                # 巢狀物件
                nested_class_name = snake_to_camel(key) + "Schema"
                nested_def = self.generate_class_definition(key, value, level + 1)
                if nested_def:
                    nested_definitions.append(nested_def)
                properties.append((prop_name, nested_class_name, value))

            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # 物件列表
                item_class_name = snake_to_camel(key.rstrip("s")) + "Schema"
                if value:  # 使用第一個元素作為範本
                    nested_def = self.generate_class_definition(
                        key.rstrip("s"), value[0], level + 1
                    )
                    if nested_def:
                        nested_definitions.append(nested_def)
                properties.append((prop_name, f"List[{item_class_name}]", value))
            else:
                # 簡單型態
                type_hint = infer_yaml_type(value)
                properties.append((prop_name, type_hint, value))

        # 組合完整的類別定義
        lines = []

        # 先加入巢狀類別
        for nested in nested_definitions:
            lines.extend(nested.split("\n"))
            lines.append("")

        # 主類別定義
        lines.append(f"class {class_name}(ConfigSchema):")
        lines.append(f'    """[{name}] configuration"""')
        lines.append("    ")
        lines.append("    def __init__(self, data: Dict[str, Any]) -> None:")
        lines.append("        self._data = data")
        lines.append("")

        # 生成屬性
        for prop_name, type_hint, original_value in properties:
            lines.append("    @property")
            lines.append(f"    def {prop_name}(self) -> {type_hint}:")

            # 根據型態生成不同的存取邏輯
            if "Schema" in type_hint and "List[" not in type_hint:
                # 巢狀物件
                lines.append(f'        """Get {prop_name} configuration"""')
                lines.append(
                    f"        return {type_hint}(self._data.get('{prop_name}', {{}}))"
                )
            elif "List[" in type_hint and "Schema" in type_hint:
                # 物件列表
                schema_class = type_hint.replace("List[", "").replace("]", "")
                lines.append(f'        """Get {prop_name} list"""')
                lines.append(f"        items = self._data.get('{prop_name}', [])")
                lines.append(f"        return [{schema_class}(item) for item in items]")
            else:
                # 簡單型態
                lines.append(f'        """Get {prop_name} value"""')
                if isinstance(original_value, list):
                    lines.append(f"        return self._data.get('{prop_name}', [])")
                elif isinstance(original_value, dict):
                    lines.append(f"        return self._data.get('{prop_name}', {{}})")
                elif original_value is None:
                    lines.append(f"        return self._data.get('{prop_name}')")
                else:
                    lines.append(
                        f"        return self._data.get('{prop_name}', {repr(original_value)})"
                    )
            lines.append("")

        return "\n".join(lines)


# --------------------------
#     新的輔助探測函數
# --------------------------


def find_default_config_path():
    """從當前目錄向上尋找 YAML 配置檔案"""
    path = "."
    for _ in range(5):  # 向上查找最多5層
        abs_path = os.path.abspath(path)

        # 檢查幾種常見的路徑模式
        check_patterns = [
            "config.yaml",
            "config.yml",
            "config/*.yaml",
            "config/*.yml",
            "settings.yaml",
            "settings.yml",
            "app.yaml",
            "app.yml",
        ]

        for pattern in check_patterns:
            full_pattern = os.path.join(abs_path, pattern)
            # 使用 glob 來處理萬用字元
            from glob import glob

            matches = glob(full_pattern)
            if matches:
                return matches[0]

        # 如果找不到，就到上一層目錄
        if os.path.dirname(abs_path) == abs_path:
            break
        path = os.path.join(path, "..")

    return None


def find_default_output_dir():
    """在當前目錄下尋找常見的源碼目錄結構，並推薦一個輸出路徑"""
    cwd = os.getcwd()
    # 優先推薦 src/config
    if os.path.isdir(os.path.join(cwd, "src")):
        return os.path.join(cwd, "src", "config")

    # 其次是 app/config
    if os.path.isdir(os.path.join(cwd, "app")):
        return os.path.join(cwd, "app", "config")

    # 如果都沒有，就推薦在當前目錄下創建一個 config/
    return os.path.join(cwd, "src", "config")


# --------------------------
#     核心 CLI 邏輯
# --------------------------

# 找到模板文件的絕對路徑
_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def run_generator(config_path: str, output_dir: str):
    click.echo(f"Reading YAML configuration from: {config_path}")

    if not os.path.exists(config_path):
        click.secho(f"Error: Configuration file not found at '{config_path}'", fg="red")
        return

    # 讀取 YAML 檔案
    with open(config_path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            click.secho(f"Error parsing YAML file: {e}", fg="red")
            return

    if not isinstance(data, dict):
        click.secho(
            "Error: YAML file must contain a dictionary at the root level", fg="red"
        )
        return

    # --- Generate schema.py ---
    click.echo("Generating schema.py...")

    generator = YamlSchemaGenerator()
    all_class_definitions = []

    # 生成所有頂層類別
    for key, value in data.items():
        if isinstance(value, dict):
            class_def = generator.generate_class_definition(key, value)
            if class_def:
                all_class_definitions.append(class_def)
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            # 為列表中的物件生成類別
            # 使用第一個元素作為範本
            item_name = key.rstrip("s")  # 移除複數 s
            class_def = generator.generate_class_definition(item_name, value[0])
            if class_def:
                all_class_definitions.append(class_def)

    # 讀取模板
    with open(os.path.join(_TEMPLATE_DIR, "schema.py.tpl"), "r", encoding="utf-8") as f:
        schema_template = f.read()

    # 更新模板內容以支援 YAML
    schema_template = schema_template.replace(
        "from configparser import SectionProxy",
        "from typing import Any, Dict, List, Union, Optional",
    )

    schema_content = schema_template.replace(
        "{{CLASS_DEFINITIONS}}", "\n\n".join(all_class_definitions)
    )

    # 建立輸出目錄
    os.makedirs(output_dir, exist_ok=True)

    # 寫入 schema.py
    with open(os.path.join(output_dir, "schema.py"), "w", encoding="utf-8") as f:
        f.write(schema_content)

    click.secho(
        f"Successfully generated {os.path.join(output_dir, 'schema.py')}", fg="green"
    )

    # --- Generate manager.py ---
    click.echo("Generating manager.py...")

    # 收集所有頂層類別名稱
    schema_imports = []
    manager_properties = []

    for key, value in data.items():
        prop_name = to_snake_case(key)

        if isinstance(value, dict):
            # 字典型態
            class_name = snake_to_camel(key) + "Schema"
            schema_imports.append(f"    {class_name},")

            property_code = f'''
    @property
    def {prop_name}(self) -> {class_name}:
        """Get {key} configuration"""
        if not hasattr(self, '_{prop_name}_cache'):
            self._{prop_name}_cache = {class_name}(self._data.get('{key}', {{}}))
        return self._{prop_name}_cache'''

            manager_properties.append(property_code)

        elif isinstance(value, list) and value and isinstance(value[0], dict):
            # 物件列表型態
            item_class_name = snake_to_camel(key.rstrip("s")) + "Schema"
            schema_imports.append(f"    {item_class_name},")

            property_code = f'''
    @property
    def {prop_name}(self) -> List[{item_class_name}]:
        """Get {key} list"""
        if not hasattr(self, '_{prop_name}_cache'):
            items = self._data.get('{key}', [])
            self._{prop_name}_cache = [{item_class_name}(item) for item in items]
        return self._{prop_name}_cache'''

            manager_properties.append(property_code)

    # 讀取管理器模板
    with open(
        os.path.join(_TEMPLATE_DIR, "manager.py.tpl"), "r", encoding="utf-8"
    ) as f:
        manager_template = f.read()

    # 替換模板內容
    manager_content = manager_template.replace(
        "{{SCHEMA_IMPORTS}}", "\n".join(schema_imports)
    )
    manager_content = manager_content.replace(
        "{{MANAGER_PROPERTIES}}", "\n".join(manager_properties)
    )

    # 寫入 manager.py
    with open(os.path.join(output_dir, "manager.py"), "w", encoding="utf-8") as f:
        f.write(manager_content)

    click.secho(
        f"Successfully generated {os.path.join(output_dir, 'manager.py')}", fg="green"
    )

    # 建立 __init__.py
    init_content = """\"\"\"Auto-generated YAML configuration module\"\"\"

from .manager import ConfigManager
from .schema import *

__all__ = ['ConfigManager']
"""

    with open(os.path.join(output_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(init_content)

    click.secho("\nYAML configuration generation complete!", bold=True)


@click.command()
@click.option(
    "--config",
    "-c",
    help="The path to the input YAML file.",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
)
@click.option(
    "--output",
    "-o",
    help="The directory to save the generated schema.py and manager.py.",
    type=click.Path(file_okay=False, resolve_path=True),
)
def main(config, output):
    """
    A CLI tool to generate type-hinted Python config classes from YAML files.
    """
    # 如果使用者沒有通過命令行參數提供路徑，我們才進行探測和詢問
    if not config:
        default_config = find_default_config_path()
        config = click.prompt(
            "Path to your YAML configuration file",
            type=click.Path(exists=True, dir_okay=False, resolve_path=True),
            default=default_config,
        )

    if not output:
        default_output = find_default_output_dir()
        output = click.prompt(
            "Path to the output directory for generated files",
            type=click.Path(file_okay=False, resolve_path=True),
            default=default_output,
        )

    run_generator(config, output)


if __name__ == "__main__":
    main()
