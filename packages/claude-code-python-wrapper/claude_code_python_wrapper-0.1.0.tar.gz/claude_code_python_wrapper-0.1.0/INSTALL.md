# 安装和使用指南

## 前置要求

1. Python 3.10 或更高版本
2. 本地已安装 `claudee` 命令并可在 PATH 中访问

## 安装方法

### 方法 1：直接从 GitHub 安装（推荐）

最简单的方式是直接使用 pip 从 GitHub 安装：

```bash
# 使用 HTTPS
pip install git+https://github.com/jancee/claude-code-python-wrapper.git

# 或使用 SSH（需要配置 GitHub SSH 密钥）
pip install git+ssh://git@github.com/jancee/claude-code-python-wrapper.git
```

### 方法 2：克隆后本地安装

如果你想要修改代码或贡献项目：

```bash
# 1. 克隆仓库
git clone https://github.com/jancee/claude-code-python-wrapper.git
cd claude-code-python-wrapper

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 3. 安装包
pip install .  # 普通安装

# 或开发模式安装（代码修改后无需重新安装）
pip install -e .

# 4. 安装开发依赖（可选）
pip install -e ".[dev]"
```

### 方法 3：下载发布包安装

```bash
# 下载最新版本
wget https://github.com/jancee/claude-code-python-wrapper/archive/main.zip
unzip main.zip
cd claude-code-python-wrapper-main

# 安装
pip install .
```

## 验证安装

安装完成后，在 Python 中验证：

```python
# 验证导入
from claude_cli import ClaudeCLI, AsyncClaudeCLI, ClaudeOptions

# 创建实例测试
claude = ClaudeCLI(command="claudee")
print("安装成功！")
```

## 快速使用示例

### 1. 基础查询

```python
from claude_cli import ClaudeCLI

# 初始化
claude = ClaudeCLI(command="claudee")

# 执行查询
response = claude.query("Hello, Claude!")
print(response.output)
```

### 2. 异步使用

```python
import asyncio
from claude_cli import AsyncClaudeCLI

async def main():
    claude = AsyncClaudeCLI(command="claudee")
    response = await claude.query("What is Python?")
    print(response.output)

asyncio.run(main())
```

### 3. 中英文翻译

```python
from claude_cli import ClaudeCLI

claude = ClaudeCLI(command="claudee")

# 中译英
chinese_text = "人工智能正在改变世界"
response = claude.query(f"请将以下中文翻译成英文：{chinese_text}")
print(response.output)

# 英译中
english_text = "AI is changing the world"
response = claude.query(f"请将以下英文翻译成中文：{english_text}")
print(response.output)
```

### 4. 批量处理

```python
import asyncio
from claude_cli import AsyncClaudeCLI

async def batch_translate(texts):
    claude = AsyncClaudeCLI(command="claudee")
    
    # 创建翻译任务
    tasks = []
    for text in texts:
        prompt = f"翻译成英文：{text}"
        tasks.append(claude.query(prompt))
    
    # 并发执行
    results = await asyncio.gather(*tasks)
    
    # 输出结果
    for text, result in zip(texts, results):
        print(f"原文: {text}")
        print(f"译文: {result.output}\n")

# 使用示例
texts = ["今天天气很好", "欢迎使用Claude", "人工智能的未来"]
asyncio.run(batch_translate(texts))
```

## 配置选项

使用 `ClaudeOptions` 自定义行为：

```python
from claude_cli import ClaudeCLI, ClaudeOptions

options = ClaudeOptions(
    max_turns=3,           # 最大对话轮数
    model="claude-3",      # 模型选择
    max_tokens=1000,       # 最大输出长度
    cwd="/path/to/dir"     # 工作目录
)

claude = ClaudeCLI(command="claudee", default_options=options)
```

## 常见问题

### 1. "Claude CLI 'claudee' not found"

确保 `claudee` 已安装并在 PATH 中：

```bash
# 检查是否安装
which claudee  # Linux/Mac
where claudee  # Windows

# 如果未找到，请先安装 Claude CLI
```

### 2. 导入错误

确保正确安装了包：

```bash
# 重新安装
pip uninstall claude-code-python-wrapper
pip install git+https://github.com/jancee/claude-code-python-wrapper.git
```

### 3. 权限问题

某些系统可能需要使用 `--user` 标志：

```bash
pip install --user git+https://github.com/jancee/claude-code-python-wrapper.git
```

## 更多示例

查看 `examples/` 目录获取更多使用示例：

- `basic_usage.py` - 基础用法
- `async_usage.py` - 异步操作
- `translator.py` - 翻译器实现
- `advanced_usage.py` - 高级功能

## 获取帮助

- 查看 [README](README.md) 了解完整功能
- 提交 [Issue](https://github.com/jancee/claude-code-python-wrapper/issues) 报告问题
- 查看 [示例代码](https://github.com/jancee/claude-code-python-wrapper/tree/main/examples)