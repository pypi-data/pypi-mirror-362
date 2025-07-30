# Claude Code Python Wrapper

一个功能完整的 Python 包装器，用于调用本地 Claude CLI (`claudee`) 命令。支持同步和异步操作，提供简洁的 API 接口。

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/claude-code-python-wrapper.svg)](https://badge.fury.io/py/claude-code-python-wrapper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 特性

- 🚀 **双模式支持**：同步 (`ClaudeCLI`) 和异步 (`AsyncClaudeCLI`) 接口
- 🔄 **流式响应**：支持实时流式输出（异步模式）
- 💬 **交互式会话**：保持上下文的多轮对话
- 📊 **JSON 解析**：自动解析 JSON 格式响应
- ⚙️ **灵活配置**：丰富的选项定制 Claude 行为
- 🛡️ **错误处理**：完善的错误处理和超时控制
- ⚡ **并发处理**：支持批量并发请求

## 安装

### 方法 1：从 PyPI 安装（推荐）

```bash
# 直接从 PyPI 安装
pip install claude-code-python-wrapper
```

### 方法 2：从 GitHub 安装

```bash
# 直接从 GitHub 安装最新版本
pip install git+https://github.com/jancee/claude-code-python-wrapper.git

# 或者使用 SSH
pip install git+ssh://git@github.com/jancee/claude-code-python-wrapper.git
```

### 方法 3：克隆后本地安装

```bash
# 克隆项目
git clone https://github.com/jancee/claude-code-python-wrapper.git
cd claude-code-python-wrapper

# 安装包
pip install .

# 或者开发模式安装（推荐开发者使用）
pip install -e .

# 安装开发依赖（可选）
pip install -e ".[dev]"
```

### 依赖要求

- Python >= 3.10
- `claudee` 命令已安装并可在 PATH 中访问

## 快速开始

### 基础用法

```python
from claude_cli import ClaudeCLI

# 初始化包装器
claude = ClaudeCLI(command="claudee")

# 简单查询
response = claude.query("什么是 Python？")
print(response.output)

# 检查执行状态
if response.return_code == 0:
    print("成功！")
else:
    print(f"错误：{response.error}")
```

### 带选项的查询

```python
from claude_cli import ClaudeCLI, ClaudeOptions

# 配置选项
options = ClaudeOptions(
    model="sonnet",  # 可选: "sonnet" 或 "opus"
    print_mode=True,  # 非交互式输出
    output_format="text",  # 输出格式: "text", "json", "stream-json"
    allowed_tools=["Bash", "Edit"]  # 允许的工具
)

# 执行查询
response = claude.query("编写一个快速排序算法", options=options)
```

### 异步操作

```python
import asyncio
from claude_cli import AsyncClaudeCLI

async def main():
    claude = AsyncClaudeCLI(command="claudee")
    
    # 单个异步查询
    response = await claude.query("解释 async/await")
    print(response.output)
    
    # 并发执行多个查询
    queries = ["什么是列表推导？", "什么是装饰器？", "什么是生成器？"]
    tasks = [claude.query(q) for q in queries]
    responses = await asyncio.gather(*tasks)
    
    for query, response in zip(queries, responses):
        print(f"Q: {query}")
        print(f"A: {response.output[:100]}...\n")

asyncio.run(main())
```

### 流式响应

```python
async def stream_example():
    claude = AsyncClaudeCLI(command="claudee")
    
    # 实时获取流式输出
    async for line in claude.stream_query("写一个关于编程的故事"):
        print(line, end='', flush=True)
```

### 交互式会话

```python
# 同步交互
claude = ClaudeCLI()
proc = claude.interactive(initial_prompt="我们来讨论 Python")

# 异步交互
async def interactive_chat():
    claude = AsyncClaudeCLI()
    
    async with await claude.interactive_session() as session:
        response = await session.send("什么是面向对象编程？")
        print(response)
        
        response = await session.send("给我一个例子")
        print(response)
```

## API 参考

### ClaudeOptions 配置项

| 参数 | 类型 | 描述 |
|------|------|------|
| `model` | `str` | 模型选择: "sonnet", "opus" 或完整模型名 |
| `fallback_model` | `str` | 备用模型 (仅--print模式) |
| `output_format` | `str` | 输出格式: "text", "json", "stream-json" |
| `input_format` | `str` | 输入格式: "text", "stream-json" |
| `allowed_tools` | `List[str]` | 允许使用的工具列表 |
| `disallowed_tools` | `List[str]` | 禁用的工具列表 |
| `continue_session` | `bool` | 继续最近的对话 |
| `resume_session` | `str` | 恢复指定会话ID |
| `add_dirs` | `List[str]` | 额外允许工具访问的目录 |
| `mcp_config` | `str` | MCP服务器配置文件 |
| `print_mode` | `bool` | 打印模式 (非交互式) |
| `debug` | `bool` | 启用调试模式 |
| `cwd` | `str` | 工作目录 |
| `extra_args` | `List[str]` | 额外的命令行参数 |

### ClaudeResponse 响应对象

| 属性 | 类型 | 描述 |
|------|------|------|
| `output` | `str` | Claude 的响应内容 |
| `return_code` | `int` | 命令返回码 (0 表示成功) |
| `error` | `str` | 错误信息（如果有） |
| `metadata` | `dict` | 额外的元数据信息 |

## 高级用法

### 批量处理与并发控制

```python
import asyncio
from claude_cli import AsyncClaudeCLI

async def batch_process_with_limit():
    claude = AsyncClaudeCLI()
    
    # 准备任务列表
    tasks = [
        {"id": 1, "prompt": "解释 Python 的 GIL"},
        {"id": 2, "prompt": "什么是元类？"},
        {"id": 3, "prompt": "解释描述符协议"},
        # ... 更多任务
    ]
    
    # 使用信号量限制并发数
    semaphore = asyncio.Semaphore(3)  # 最多 3 个并发请求
    
    async def process_with_limit(task):
        async with semaphore:
            response = await claude.query(task["prompt"])
            return {"id": task["id"], "result": response.output}
    
    # 并发处理所有任务
    results = await asyncio.gather(*[process_with_limit(t) for t in tasks])
    return results
```

### 错误处理与重试

```python
import asyncio
from claude_cli import AsyncClaudeCLI

async def query_with_retry(prompt, max_retries=3):
    claude = AsyncClaudeCLI()
    
    for attempt in range(max_retries):
        try:
            response = await claude.query(prompt, timeout=10.0)
            if response.return_code == 0:
                return response
            
            # 如果是临时错误，等待后重试
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避
                
        except Exception as e:
            print(f"尝试 {attempt + 1} 失败: {e}")
            if attempt == max_retries - 1:
                raise
    
    return None
```

### 自定义日志

```python
import logging
from claude_cli import ClaudeCLI

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建自定义 logger
logger = logging.getLogger("my_app")

# 使用自定义 logger
claude = ClaudeCLI(logger=logger)
```

## 实际应用示例

### 代码审查助手

```python
from claude_cli import ClaudeCLI

class CodeReviewer:
    def __init__(self):
        self.claude = ClaudeCLI()
    
    def review_code(self, code: str, language: str = "python"):
        prompt = f"""请审查以下 {language} 代码：
        
```{language}
{code}
```

提供：
1. 潜在的 bug 或问题
2. 性能优化建议
3. 代码风格改进
4. 安全性考虑
"""
        response = self.claude.query(prompt)
        return response.output if response.return_code == 0 else None

# 使用示例
reviewer = CodeReviewer()
code = """
def get_user(user_id):
    return db.query(f"SELECT * FROM users WHERE id = {user_id}")
"""
review = reviewer.review_code(code)
print(review)
```

### 文档生成器

```python
async def generate_docs(file_path: str):
    claude = AsyncClaudeCLI()
    
    with open(file_path, 'r') as f:
        code = f.read()
    
    prompt = f"""为以下代码生成详细的文档字符串：

{code}

要求：
- 使用 Google 风格的文档字符串
- 包含参数说明和返回值
- 添加使用示例
"""
    
    response = await claude.query(prompt)
    return response.output
```

## 运行示例

项目包含多个示例脚本：

```bash
# 基础示例
python examples/basic_usage.py

# 异步示例
python examples/async_usage.py

# 高级用法
python examples/advanced_usage.py

# 测试脚本
python test_basic.py
python test_async.py
python code_analyzer.py
```

## 故障排除

### 常见问题

1. **"Claude CLI 'claudee' not found in PATH"**
   - 确保 `claudee` 命令已正确安装
   - 检查 PATH 环境变量
   - 尝试使用完整路径初始化：`ClaudeCLI(command="/full/path/to/claudee")`

2. **超时错误**
   - 增加 timeout 参数：`claude.query(prompt, timeout=30.0)`
   - 检查网络连接
   - 考虑使用异步模式处理长时间运行的查询

3. **JSON 解析错误**
   - 确保 Claude 返回的是有效的 JSON 格式
   - 使用 try-except 处理解析错误

### 调试技巧

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 查看完整命令
response = claude.query("test")
print(response.metadata["command"])  # 显示实际执行的命令
```

## 项目结构

```
claude-cli-wrapper/
├── claude_cli/
│   ├── __init__.py        # 包导出
│   ├── wrapper.py         # 同步包装器实现
│   └── async_wrapper.py   # 异步包装器实现
├── examples/
│   ├── basic_usage.py     # 基础用法示例
│   ├── async_usage.py     # 异步操作示例
│   └── advanced_usage.py  # 高级功能示例
├── tests/                 # 测试目录
├── pyproject.toml         # 项目配置
├── README.md             # 本文档
├── test_basic.py         # 基础测试脚本
├── test_async.py         # 异步测试脚本
└── code_analyzer.py      # 代码分析器示例
```

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 开发要求

- 遵循 PEP 8 代码风格
- 添加适当的类型注解
- 编写单元测试
- 更新文档

### 发布到 PyPI 注意事项

在发布新版本到 PyPI 时，请注意以下 LICENSE 相关的配置问题：

**问题背景：** setuptools 在生成包元数据时可能会产生不兼容的 `license-file` 和 `license-expression` 字段，导致 twine upload 失败。

**解决方案：**
1. **pyproject.toml 配置**：不要在 `[project]` 中使用 `license` 字段
2. **LICENSE 文件**：确保项目根目录有 `LICENSE` 文件
3. **classifiers**：可选择性添加 `"License :: OSI Approved :: MIT License"` classifier
4. **构建流程**：如果上传失败，临时删除 LICENSE 文件重新构建

**发布步骤：**
```bash
# 1. 更新版本号
# 2. 清理构建文件
rm -rf dist/ build/ *.egg-info/

# 3. 构建包
python -m build

# 4. 如果上传失败，尝试临时删除 LICENSE 文件后重新构建
# rm LICENSE && python -m build

# 5. 上传到 PyPI
python -m twine upload dist/*

# 6. 恢复 LICENSE 文件（如果之前删除了）
# git checkout LICENSE
```

参考：[PyPI setuptools issue #4759](https://github.com/pypa/setuptools/issues/4759)

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 作者

- jancee (@jancee)

## 致谢

- 感谢 Anthropic 提供 Claude CLI 工具
- 感谢所有贡献者

---

如有问题或建议，请提交 [Issue](https://github.com/jancee/claude-code-python-wrapper/issues) 或 [Pull Request](https://github.com/jancee/claude-code-python-wrapper/pulls)。