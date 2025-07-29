import requests
import json
import os
import base64
import argparse
import sys
from pathlib import Path
import threading
import time
import fnmatch
from dotenv import load_dotenv, find_dotenv

# 定义颜色常量
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

__version__ = "0.1.7"

# 硬编码API配置
DEFAULT_API_URL = "http://pd-adminapi.spark.xd.com:8082/api/v1/update-minigame"
DEFAULT_CONTENT_TYPE = "application/json"

def load_config(config_path):
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # 移除 data 字段的特殊处理
            return config
    except FileNotFoundError:
        print(f"{RED}配置文件不存在: {config_path}{RESET}")
        raise
    except json.JSONDecodeError:
        print(f"{RED}配置文件格式错误: {config_path}{RESET}")
        raise

def load_sceignore(ignore_file_path):
    """Load ignore patterns from .sceignore file."""
    patterns = []
    if os.path.exists(ignore_file_path):
        try:
            with open(ignore_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Ignore comments and empty lines
                    if line and not line.startswith('#'):
                        patterns.append(line)
        except Exception as e:
            print(f"{YELLOW}Warning: Could not read {ignore_file_path}: {e}{RESET}")
    return patterns

def _should_ignore(relative_path, ignore_patterns):
    """Check if a relative path should be ignored based on patterns."""
    # Normalize path separators for consistency
    normalized_path = relative_path.replace('\\', '/')
    # Check against each pattern
    for pattern in ignore_patterns:
        # Check if the path itself matches
        if fnmatch.fnmatch(normalized_path, pattern):
            return True
        # Check if any parent directory matches (for directory patterns)
        # If pattern ends with '/', it's a directory pattern
        if pattern.endswith('/'):
            # Check if the path starts with the directory pattern
            if normalized_path.startswith(pattern):
                 return True
            # Also check if a parent directory exactly matches the pattern without the trailing '/'
            # e.g., ignore pattern 'build/' should ignore path 'build/subdir/file'
            # and also ignore the directory 'build' itself if walked
            pattern_dir = pattern.rstrip('/')
            path_parts = Path(normalized_path).parts
            if pattern_dir in path_parts:
                 # Check if one of the parent directories matches exactly
                 current_path = ""
                 for part in path_parts:
                     current_path = os.path.join(current_path, part).replace('\\','/') if current_path else part
                     if current_path == pattern_dir:
                         return True

        # Check if path is inside an ignored directory (pattern doesn't necessarily end with /)
        # This handles cases like ignoring a 'node_modules' folder entirely
        # Split pattern and path into parts
        pattern_parts = Path(pattern.strip('/')).parts
        path_parts = Path(normalized_path).parts

        # If pattern has more parts than path, it cannot match
        if len(pattern_parts) > len(path_parts):
            continue

        # Check if the beginning of the path matches the pattern parts
        match = True
        for i in range(len(pattern_parts)):
             # Use fnmatch for each part to support wildcards within directory names
             if not fnmatch.fnmatch(path_parts[i], pattern_parts[i]):
                 match = False
                 break
        if match:
             return True

    return False

def image_to_base64(image_path):
    """将图片转换为base64编码"""
    try:
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"图片文件不存在: {image_path}")
        print(f"{RED}请填写正确的文件路径或者删除该属性{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"处理图片时发生错误: {e}")
        sys.exit(1)

def process_folder(folder_path, ignore_patterns, verbose_logging):
    """处理文件夹中的所有文件，忽略指定的文件和目录."""
    try:
        if not os.path.exists(folder_path):
            print(f"{RED}文件夹不存在: {folder_path}{RESET}")
            print(f"{RED}请在配置文件中提供正确的 'outDirectory' 路径。{RESET}")
            return None
            
        folder_content = {}
        print(f"开始处理目录: {folder_path}")
        # 使用 topdown=True 以便修改 dirs 列表来跳过目录
        for root, dirs, files in os.walk(folder_path, topdown=True):
            # --- 忽略目录 --- 
            # 从 dirs 列表中原地移除要忽略的目录
            # 需要复制 dirs 列表进行迭代，因为我们要修改它
            original_dirs = dirs[:]
            dirs[:] = [] # 清空 dirs，只添加不被忽略的
            for d in original_dirs:
                dir_path = os.path.join(root, d)
                relative_dir_path = os.path.relpath(dir_path, folder_path)
                if _should_ignore(relative_dir_path, ignore_patterns):
                    if verbose_logging:
                        print(f"  忽略目录: {relative_dir_path}")
                else:
                    dirs.append(d) # 只保留不被忽略的目录
            # --- 忽略目录结束 --- 
            
            # --- 处理文件 --- 
            for file in files:
                file_path = os.path.join(root, file)
                relative_file_path = os.path.relpath(file_path, folder_path)
                
                # 忽略 .sceignore 文件本身
                if relative_file_path == '.sceignore':
                    continue

                # 检查是否忽略此文件
                if _should_ignore(relative_file_path, ignore_patterns):
                    if verbose_logging:
                        print(f"  忽略文件: {relative_file_path}")
                    continue
                    
                # 处理并添加未被忽略的文件
                try:
                    if verbose_logging:
                         print(f"  添加文件: {relative_file_path}")
                    # 将文件转换为base64
                    with open(file_path, 'rb') as f:
                        file_content = base64.b64encode(f.read()).decode('utf-8')
                    folder_content[relative_file_path.replace('\\', '/')] = file_content # 统一路径分隔符
                except Exception as e:
                    print(f"{YELLOW}处理文件 {file_path} 时发生错误: {e}{RESET}")
                    # 可选择继续或中止
                    continue 
            # --- 处理文件结束 --- 
                
        print(f"目录处理完成: {folder_path}")
        return folder_content
    except Exception as e:
        print(f"{RED}处理文件夹 {folder_path} 时发生严重错误: {e}{RESET}")
        sys.exit(1)

def process_images(config, config_dir, verbose_logging):
    """处理配置文件中的图片和文件夹，并处理忽略规则."""
    try:
        # --- 加载 .sceignore --- 
        ignore_patterns = []
        # (修改) .sceignore 文件路径现在基于 config_dir
        ignore_file_path = os.path.join(config_dir, '.sceignore') 
        if os.path.exists(ignore_file_path):
            print(f"加载忽略规则: {ignore_file_path}")
            ignore_patterns = load_sceignore(ignore_file_path)
            if verbose_logging:
                print(f"  忽略规则: {ignore_patterns}")
        elif verbose_logging:
            # (修改) 提示信息也更新为 config_dir
            print(f"未找到 .sceignore 文件于: {config_dir}") 
        # --- 加载 .sceignore 结束 --- 
        
        # 处理banner数组 - 直接从 config 获取
        if 'banner' in config and isinstance(config['banner'], list):
            banner_base64 = []
            for banner_path in config['banner']:
                full_path = os.path.join(config_dir, banner_path)
                banner_base64.append(image_to_base64(full_path))
            config['banner'] = banner_base64
            
        # 处理icon数组 - 直接从 config 获取
        if 'icon' in config and isinstance(config['icon'], list):
            icon_base64 = []
            for icon_path in config['icon']:
                full_path = os.path.join(config_dir, icon_path)
                icon_base64.append(image_to_base64(full_path))
            config['icon'] = icon_base64
            
        # 处理screenshots数组 - 直接从 config 获取
        if 'screenshots' in config and isinstance(config['screenshots'], list):
            screenshots_base64 = []
            for screenshot_path in config['screenshots']:
                full_path = os.path.join(config_dir, screenshot_path)
                screenshots_base64.append(image_to_base64(full_path))
            config['screenshots'] = screenshots_base64
            
        # 处理文件夹 (传递 ignore_patterns 和 verbose_logging) - 直接从 config 获取
        if 'outDirectory' in config and config['outDirectory']:
            folder_path = os.path.join(config_dir, config['outDirectory'])
            # 将 ignore_patterns 和 verbose_logging 传递给 process_folder
            folder_content = process_folder(folder_path, ignore_patterns, verbose_logging)
            if folder_content is not None: # 检查 process_folder 是否成功返回
                config['folder_content'] = folder_content
            else:
                 # 如果文件夹处理失败 (例如目录不存在)，可以选择退出或继续
                 print(f"{YELLOW}警告: 未能处理文件夹 {folder_path}。继续处理其他内容。{RESET}")
                 # 或者: sys.exit(1) 如果这是关键错误
            
        return config
    except Exception as e:
        print(f"处理图片和文件夹时发生错误: {e}")
        print(f"{RED}请填写正确的文件路径或者删除该属性{RESET}")
        sys.exit(1)

def send_request(config, api_url, content_type, token):
    """发送请求并显示进度模拟"""
    
    # --- 进度条模拟相关 --- 
    result_container = {"response": None, "error": None}
    stop_spinner = False

    def _make_request():
        nonlocal stop_spinner
        try:
            headers = {
                "Content-Type": content_type,
                "Authorization": token
            }
            # data = config['data'] # 旧逻辑
            # 现在 config 对象本身就是 payload（经过处理，不含 token 等外部参数）
            # 但要注意，API 可能期望的是一个名为 'data' 的键，其值为我们的 config 内容
            # 或者 API 直接接受扁平化的 config 内容。这里假设 API 直接接受扁平化的 config
            # 如果 API 仍然期望 { "data": { ... } } 结构，需要调整为: data_payload = {"data": config}
            data_payload = config 
            # verify=False 用于忽略SSL证书验证，仅在信任目标服务器时使用
            response = requests.post(api_url, headers=headers, json=data_payload, verify=False) 
            result_container["response"] = response
        except requests.exceptions.RequestException as e:
            result_container["error"] = e
        finally:
            stop_spinner = True
            
    request_thread = threading.Thread(target=_make_request)
    request_thread.start()
    
    spinner_chars = "|/-\\"
    idx = 0
    print(f"正在发送请求到: {api_url}") 
    while request_thread.is_alive():
        # 使用 \r 将光标移回行首，实现原地旋转效果
        print(f"  发送中 {spinner_chars[idx % len(spinner_chars)]}", end="\r") 
        idx += 1
        time.sleep(0.1)
    
    # 清除旋转光标并在同一行打印完成信息
    print("  发送完成       ", end="\n") 
    
    request_thread.join() # 确保线程完全结束
    # --- 进度条模拟结束 ---

    if result_container["error"]:
        print(f"{RED}请求发生错误: {result_container['error']}{RESET}")
        sys.exit(1)
    
    response = result_container["response"]
    
    # 打印响应信息
    print(f"状态码: {response.status_code}")
    
    # 尝试解析JSON响应
    try:
        response_json = response.json()
        
        # 检查响应中的result字段
        if 'data' in response_json and isinstance(response_json['data'], dict) and 'result' in response_json['data'] and response_json['data']['result'] is False:
            # 只输出msg和url
            if 'msg' in response_json['data']:
                print(f"{RED}错误: {response_json['data']['msg']}{RESET}")
            if 'url' in response_json['data']:
                print(f"链接: {response_json['data']['url']}")
        else:
            # 输出完整的响应JSON
            print(f"响应JSON: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
    except json.JSONDecodeError:
        print(f"{RED}响应内容: {response.text}{RESET}")
        
    return response

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='TapTap SCE小游戏自动发布工具')
    parser.add_argument('-c', '--config', 
                        default='minigame_config.json',
                        help='配置文件路径 (默认: minigame_config.json)')
    parser.add_argument('-v', '--version', 
                        action='version', 
                        version=f'sce-minigame-publisher {__version__}')
    parser.add_argument('--verbose', 
                        action='store_true', 
                        help='显示详细日志')
    
    # Add API related parameters
    parser.add_argument('--url', 
                        default=DEFAULT_API_URL,
                        help=f'API URL (default: {DEFAULT_API_URL})')
    parser.add_argument('--content-type', 
                        default=DEFAULT_CONTENT_TYPE,
                        help=f'Content type (default: {DEFAULT_CONTENT_TYPE})')
    parser.add_argument('-t', '--token',
                        help='API token. Overrides .env file and interactive input.')
    
    return parser.parse_args()

def is_latin1_compatible(text):
    """检查文本是否兼容Latin-1编码"""
    try:
        text.encode('latin-1')
        return True
    except UnicodeEncodeError:
        return False

def main():
    """主函数"""
    try:
        # 解析命令行参数
        args = parse_args()
        
        # 获取配置文件绝对路径
        if os.path.isabs(args.config):
            config_path = args.config
        else:
            config_path = os.path.abspath(args.config)
        
        config_dir = os.path.dirname(config_path)
        
        # 加载配置
        print("正在加载配置文件...")
        if args.verbose:
            print(f"配置文件路径: {config_path}")
            
        config = load_config(config_path)
        
        # --- 获取 Token ---
        token = None
        # 1. 尝试从命令行参数获取
        if args.token:
            token = args.token
            if args.verbose:
                print("使用命令行参数提供的 token。")
        
        # 2. 如果命令行没有，尝试从 .env 文件获取
        if not token:
            if args.verbose:
                print(f"{YELLOW}--- Info: Attempting to load .env from CWD ---{RESET}")
            
            # 明确从当前工作目录查找 .env 文件
            dotenv_path = find_dotenv(usecwd=True)
            if args.verbose:
                print(f"{YELLOW}--- Info: find_dotenv(usecwd=True) result: '{dotenv_path if dotenv_path else "Not found"}'{RESET}")
            
            # 加载 .env 文件。
            # override=True 确保 .env 文件中的值优先于任何已存在的环境变量。
            # verbose=args.verbose 允许在用户请求详细输出时显示 dotenv 的加载信息。
            load_success = load_dotenv(dotenv_path=dotenv_path if dotenv_path else None, 
                                      verbose=args.verbose, 
                                      override=True)
            
            if args.verbose:
                print(f"{YELLOW}--- Info: load_dotenv() success: {load_success}{RESET}")

            env_token = os.getenv('SCE_PUBLISH_TOKEN')
            if env_token:
                token = env_token
                # 不再在此处打印 "使用 .env 文件中的 SCE_PUBLISH_TOKEN。" 
                # 因为 load_dotenv(verbose=True) 已经可能打印了相关信息
                # 并且下面的成功获取token的日志会更通用
            
            if token and args.verbose:
                print(f"{GREEN}--- Info: Token successfully loaded via .env file.{RESET}")
            elif not env_token and args.verbose: # 仅在 verbose 且 env_token 确实未取到时提示
                print(f"{YELLOW}--- Info: SCE_PUBLISH_TOKEN not found in environment after attempting .env load.{RESET}")

        # 3. 如果都没有，提示用户输入
        if not token:
            print(f"{YELLOW}未通过命令行参数或 .env 文件 (SCE_PUBLISH_TOKEN) 提供 token。{RESET}")
            while not token:
                try:
                    token = input("请输入 API token: ").strip()
                    if not token:
                        print(f"{RED}Token 不能为空，请重新输入。{RESET}")
                except KeyboardInterrupt:
                    print(f"\n{RED}用户取消输入。{RESET}")
                    return False # 或 sys.exit(1)
        
        # 检查token是否包含非Latin-1字符
        if not is_latin1_compatible(token):
            print(f"{RED}错误: token包含非Latin-1字符，请使用ASCII字符（如英文字母、数字和符号）组成的token。{RESET}")
            print(f"{YELLOW}提示: HTTP请求头只能包含Latin-1字符集中的字符。{RESET}")
            return False
            
        # === 添加配置数据校验 开始 ===
        # config_data = config.get('data', {}) # 旧逻辑
        # 现在直接在 config 对象上校验
        
        # 校验 tapID 必须是数字
        tap_id = config.get('tapID') # 直接从 config 获取
        if tap_id is None:
            print(f"{RED}错误: 配置文件中缺少 tapID 字段。{RESET}") # 更新错误信息
            return False
        # 检查 tapID 是否为整数或浮点数
        if not isinstance(tap_id, int):
            print(f"{RED}错误: 配置文件中的 tapID ('{tap_id}') 必须是整数。{RESET}") # 更新错误信息
            return False
            
        # 校验其他必须为字符串的字段
        string_fields_to_check = ['projectID', 'title', 'outDirectory', 'screenOrientation', 'description', 'versionName']
        for field in string_fields_to_check:
            # 检查字段是否存在于 config 中
            if field in config:
                value = config[field] # 直接从 config 获取
                # 如果值不是字符串，则打印错误并返回 False
                if not isinstance(value, str):
                    print(f"{RED}错误: 配置文件中的 {field} ('{value}') 必须是字符串。{RESET}") # 更新错误信息
                    return False
        # === 添加配置数据校验 结束 ===
        
        # 处理图片
        print("正在处理图片...")
        config = process_images(config, config_dir, args.verbose)
        
        # 发送请求
        response = send_request(config, args.url, args.content_type, token)
        
        return response.status_code == 200

    except Exception as e:
        print(f"{RED}程序执行出错: {e}{RESET}")
        import traceback
        print(traceback.format_exc())  # 打印完整的错误堆栈
        return False

def cli_main():
    """CLI入口点"""
    success = main()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    cli_main() 