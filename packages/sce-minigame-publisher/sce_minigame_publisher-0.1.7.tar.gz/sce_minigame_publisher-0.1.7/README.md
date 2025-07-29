# auto-publish

TapTap SCE小游戏自动发布工具，用于自动化发布和管理小游戏项目。

## 安装

```bash
# 确保您已安装 Python 和 pip
pip install sce-minigame-publisher
```

## 功能特点

- 自动化处理游戏资源（图片、文件夹等）
- 支持批量上传游戏文件
- 自动将图片转换为 base64 编码
- 支持自定义配置参数
- 提供详细的错误处理和日志输出
- 支持 `.sceignore` 文件忽略指定文件和目录
- 多种灵活的 Token 输入方式

## Token 配置 (重要)

认证 Token 不再通过 `minigame_config.json` 文件配置。您可以通过以下三种方式提供 Token，优先级从高到低：

1.  **命令行参数**: 通过 `-t` 或 `--token` 参数直接传入。
    ```bash
    sce-minigame-publisher --token YOUR_API_TOKEN
    ```
2.  **.env 文件**: 在项目根目录下（即您运行 `sce-minigame-publisher` 命令的目录）创建 `.env` 文件，并设置 `SCE_PUBLISH_TOKEN` 变量。
    ```.env
    SCE_PUBLISH_TOKEN="YOUR_API_TOKEN"
    ```
    工具会自动加载此文件。
3.  **手动输入**: 如果以上两种方式均未提供 Token，程序启动时会提示您在命令行中手动输入。

## 使用方法

1.  在您的项目目录下创建并配置 `minigame_config.json` 文件 (见下方说明)。
2.  将游戏资源文件放置在 `minigame_config.json` 中 `outDirectory` 指定的位置。
3.  准备好您的 API Token (通过上述任一方式)。
4.  运行主程序：
    ```bash
    sce-minigame-publisher
    ```

### 命令行参数

```bash
# 使用当前目录的默认配置文件 (minigame_config.json)
sce-minigame-publisher

# 指定配置文件
sce-minigame-publisher -c path/to/your/config.json

# 指定 Token
sce-minigame-publisher -t YOUR_API_TOKEN

# 显示详细日志
sce-minigame-publisher --verbose

# 自定义API URL
sce-minigame-publisher --url http://your-api-url.com

# 自定义内容类型
sce-minigame-publisher --content-type "application/json"

# 显示版本信息
sce-minigame-publisher -v
```

| 参数 | 描述 |
|------|------|
| `-c, --config` | 配置文件路径 (默认: ./minigame_config.json) |
| `-t, --token` | API Token (会覆盖 .env 文件和手动输入) |
| `-v, --version` | 显示版本信息 |
| `--verbose` | 显示详细日志 |
| `--url` | 自定义API URL (默认值已内置) |
| `--content-type` | 内容类型 (默认: application/json) |

## 配置文件说明 (`minigame_config.json`)

配置文件 `minigame_config.json` 现在采用扁平化结构，不再包含顶层的 `data` 字段。所有先前的 `data` 子字段现在都位于配置文件的顶层。示例如下：

```json
{
    "projectID": "your-project-id",
    "tapID": 123456,
    "title": "游戏标题",
    "outDirectory": "path/to/game/folder",
    "screenOrientation": "portrait or landscape",
    "description": "游戏描述",
    "tags": ["标签1", "标签2"],
    "versionName": "1.0.0",
    "banner": ["path/to/banner.png"],
    "icon": ["path/to/icon.png"],
    "screenshots": ["path/to/screenshot1.png", "path/to/screenshot2.png"]
}
```

**关键字段说明:**

*   `projectID`: (字符串) 您的项目 ID。
*   `tapID`: (整数) TapTap 平台的游戏 ID。
*   `title`: (字符串) 游戏标题。
*   `outDirectory`: (字符串) 包含游戏构建文件的目录路径，相对于此配置文件。
*   `screenOrientation`: (字符串) 屏幕方向，例如 "portrait" 或 "landscape"。
*   `description`: (字符串) 游戏描述。
*   `tags`: (字符串数组) 游戏的标签。
*   `versionName`: (字符串) 游戏版本号，例如 "1.0.0"。
*   `banner`: (字符串数组) Banner 图片的路径列表，相对于此配置文件。
*   `icon`: (字符串数组) 图标图片的路径列表，相对于此配置文件。
*   `screenshots`: (字符串数组) 游戏截图的路径列表，相对于此配置文件。

## 本地测试 (无需真实服务器)

如果您想在本地测试此工具（例如，如果您正在为此工具贡献代码或想了解其内部工作原理），可以按照以下步骤操作。普通用户通常不需要执行这些步骤。

项目包含一个简单的本地HTTP服务器 (`test_server.py`) 和测试配置文件 (`test_config.json`)，用于在本地验证工具的功能，特别是文件处理和忽略规则。请确保 `test_config.json` 也更新为扁平化结构。

### 准备测试环境 (针对开发者/贡献者)

1.  **克隆仓库**: 首先，您需要克隆包含 `test_server.py` 的代码仓库。
2.  **确保测试目录和文件存在**: 项目应包含 `test_outdir/` 目录，内有 `index.html`, `script.js`, `debug.log` 等文件。
3.  **创建忽略规则文件**: 在项目根目录（与 `test_config.json` 同级）创建 `.sceignore` 文件，例如：
    ```.sceignore
    # 忽略日志文件
    *.log
    
    # 忽略临时文件
    *.tmp
    
    # 忽略特定目录 (相对于 outDirectory)
    ignore_this_dir/
    ```
    *注意：`.sceignore` 文件中的模式是相对于 `test_config.json` 中 `outDirectory` 指定的目录 (`test_outdir/`) 来编写的。*

### 运行测试 (针对开发者/贡献者)

1.  **启动本地测试服务器**: 打开一个终端，在克隆的仓库的根目录下运行：
    ```bash
    python test_server.py
    ```
    服务器将在 `http://localhost:8000` 启动并等待请求。

2.  **运行发布脚本 (使用本地 Python 解释器)**: 打开**另一个**终端，在克隆的仓库的根目录下运行发布脚本，指定测试配置文件和本地服务器URL：
    ```bash
    # 使用测试配置，指向本地服务器，并开启详细日志
    python sce_minigame_publisher.py -c test_config.json --url http://localhost:8000/api/v1/update-minigame --verbose
    ```
    或者，如果您已经通过 `pip install -e .` 在本地可编辑模式下安装了此工具，您也可以使用：
    ```bash
    sce-minigame-publisher -c test_config.json --url http://localhost:8000/api/v1/update-minigame --verbose
    ```

### 验证结果

*   **在服务器终端**: 查看打印出的请求头和JSON内容。检查 `Folder Content Summary` 部分，确认 `.sceignore` 中指定的文件（如 `debug.log`）**没有**被包含在内。JSON 内容现在应该是扁平的，不含 `data` 外层。
*   **在发布脚本终端**: 查看脚本的输出，确认状态码为 `200`，并收到了来自测试服务器的成功响应。

完成后按 `Ctrl+C` 停止测试服务器。

## 注意事项

1. 确保所有图片文件都存在且格式正确
2. 游戏资源文件夹中的文件将被自动转换为 base64 编码
3. 请妥善保管 API token，不要泄露
4. API Token 必须通过命令行参数、.env 文件 (变量名为 `SCE_PUBLISH_TOKEN`) 或手动输入提供，并且只能包含ASCII字符
5. 建议在发布前先进行测试
6. 确保您的 `minigame_config.json` (和用于本地测试的 `test_config.json`) 已更新为新的扁平化结构。

## 常见问题解决

如果您在发布过程中遇到问题，请检查：
1. 配置文件 (`minigame_config.json`) 是否在当前目录或通过 `-c` 正确指定，是否是扁平结构，不包含 `token` 字段。
2. Token 是否已通过正确方式提供 (命令行、.env 文件中的 `SCE_PUBLISH_TOKEN` 或手动输入)，是否有效，是否只包含ASCII字符。
3. 图片路径是否正确 (相对于配置文件)。
4. `outDirectory` 指定的游戏文件夹是否存在 (相对于配置文件)。

## 依赖项

- Python 3.6+
- requests
- python-dotenv  # 用于从 .env 文件加载 Token

## 许可证

MIT 