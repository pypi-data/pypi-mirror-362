import configparser
import os

import click  # 使用 Click 來建立漂亮的 CLI


def snake_to_camel(snake_str: str) -> str:
    components = snake_str.split("_")
    return "".join(x.title() for x in components)


def infer_type(value: str) -> str:
    if value.lower() in ("true", "false"):
        return "boolean"
    try:
        int(value)
        return "int"
    except ValueError:
        try:
            float(value)
            return "float"
        except ValueError:
            return "str"


def generate_schema_class(section: str, options: configparser.SectionProxy) -> str:
    class_name = f"{snake_to_camel(section)}Schema"
    lines = [
        f"class {class_name}(ConfigSchema):",
        f'    """[{section}]"""',
        "    def __init__(self, config_section: SectionProxy) -> None:",
        "        super().__init__(config_section)\n",
    ]  # 使用 raw 訪問來避免插值問題
    config_dict = dict(options)
    for option, value in config_dict.items():
        option_type = infer_type(value)
        lines.append("    @property")
        lines.append(f"    def {option}(self):")
        if option_type == "int":
            lines.append(f"        return self._config_section.getint('{option}')")
        elif option_type == "float":
            lines.append(f"        return self._config_section.getfloat('{option}')")
        elif option_type == "boolean":
            lines.append(f"        return self._config_section.getboolean('{option}')")
        else:
            lines.append(f"        return self._config_section.get('{option}')")

    return "\n".join(lines)


# --------------------------
#     新的輔助探測函數
# --------------------------


def find_default_config_path():
    """從當前目錄向上尋找 config.ini，返回找到的路徑，否則返回 None。"""
    path = "."
    for _ in range(5):  # 向上查找最多5層
        abs_path = os.path.abspath(path)

        # 檢查幾種常見的路徑模式
        check_paths = [
            os.path.join(abs_path, "config.ini"),
            os.path.join(abs_path, "config", "config.ini"),
            os.path.join(abs_path, "con", "config.ini"),
        ]

        for p in check_paths:
            if os.path.isfile(p):
                return p

        # 如果找不到，就到上一層目錄
        if os.path.dirname(abs_path) == abs_path:
            break
        path = os.path.join(path, "..")

    return None


def find_default_output_dir():
    """在當前目錄下尋找常見的源碼目錄結構，並推薦一個輸出路徑。"""
    cwd = os.getcwd()
    # 優先推薦 src/config
    if os.path.isdir(os.path.join(cwd, "src")):
        return os.path.join(cwd, "src", "config")

    # 其次是 app/config
    if os.path.isdir(os.path.join(cwd, "app")):
        return os.path.join(cwd, "app", "config")
        # 如果都沒有，就推薦在當前目錄下創建一個 config/
    # return os.path.join(cwd, 'config_generated')
    # 使用一個更清晰的名字，避免與存放 ini 的 config/ 混淆
    return os.path.join(cwd, "src", "config")


# --------------------------
#     核心 CLI 邏輯
# --------------------------

# 找到模板文件的絕對路徑，這樣無論在哪裡執行 cli 都能找到它們
# 這很重要，因為當別人 pip install 後，模板文件會在 site-packages 裡
_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def run_generator(config_path: str, output_dir: str):
    click.echo(f"Reading configuration from: {config_path}")
    if not os.path.exists(config_path):
        click.secho(f"Error: Configuration file not found at '{config_path}'", fg="red")
        return

    # 修復：使用 RawConfigParser 來避免插值錯誤
    config = configparser.RawConfigParser()
    config.read(config_path, encoding="utf-8")  # --- Generate schema.py ---
    click.echo("Generating schema.py...")
    all_class_definitions = [
        generate_schema_class(s, config[s]) for s in config.sections()
    ]
    with open(os.path.join(_TEMPLATE_DIR, "schema.py.tpl"), "r", encoding="utf-8") as f:
        schema_template = f.read()
    schema_content = schema_template.replace(
        "{{CLASS_DEFINITIONS}}", "\n\n".join(all_class_definitions)
    )

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "schema.py"), "w", encoding="utf-8") as f:
        f.write(schema_content)

    click.secho(
        f"Successfully generated {os.path.join(output_dir, 'schema.py')}", fg="green"
    )

    # --- Generate manager.py ---
    click.echo("Generating manager.py...")
    schema_imports = [f"    {snake_to_camel(s)}Schema," for s in config.sections()]
    manager_properties = [
        f"        self.{s.lower()} = {snake_to_camel(s)}Schema(self._config['{s}'])"
        for s in config.sections()
    ]

    with open(
        os.path.join(_TEMPLATE_DIR, "manager.py.tpl"), "r", encoding="utf-8"
    ) as f:
        manager_template = f.read()

    content = manager_template.replace("{{SCHEMA_IMPORTS}}", "\n".join(schema_imports))
    manager_content = content.replace(
        "{{MANAGER_PROPERTIES}}", "\n".join(manager_properties)
    )

    with open(os.path.join(output_dir, "manager.py"), "w", encoding="utf-8") as f:
        f.write(manager_content)

    click.secho(
        f"Successfully generated {os.path.join(output_dir, 'manager.py')}", fg="green"
    )
    click.secho("\nConfiguration generation complete!", bold=True)


@click.command()
@click.option(
    "--config",
    "-c",
    help="The path to the input config.ini file.",
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
    A CLI tool to generate type-hinted Python config classes from .ini files.
    """
    # 如果使用者沒有通過命令行參數提供路徑，我們才進行探測和詢問
    if not config:
        default_config = find_default_config_path()
        config = click.prompt(
            "Path to your config.ini file",
            type=click.Path(exists=True, dir_okay=False, resolve_path=True),
            default=default_config,  # 關鍵：將探測到的路徑作為預設值
        )

    if not output:
        default_output = find_default_output_dir()
        output = click.prompt(
            "Path to the output directory for generated files",
            type=click.Path(file_okay=False, resolve_path=True),
            default=default_output,  # 關鍵：將推薦的路徑作為預設值
        )

    run_generator(config, output)


if __name__ == "__main__":
    main()
