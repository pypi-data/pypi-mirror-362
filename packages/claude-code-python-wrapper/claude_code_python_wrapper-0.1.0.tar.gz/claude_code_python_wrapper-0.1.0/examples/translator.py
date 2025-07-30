#!/usr/bin/env python3
"""中英文翻译器 - 使用 Claude CLI 进行文本翻译"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from pathlib import Path
from typing import Optional, List
from claude_cli import ClaudeCLI, AsyncClaudeCLI, ClaudeOptions


class Translator:
    """中英文翻译器"""
    
    def __init__(self, command: str = "claudee"):
        self.claude = ClaudeCLI(command=command)
        self.async_claude = AsyncClaudeCLI(command=command)
        
        # 翻译专用的系统提示词
        self.system_prompt = """你是一位专业的中英文翻译专家。请遵循以下原则：
1. 保持原文的语气和风格
2. 使用地道的目标语言表达
3. 保留专有名词和技术术语的准确性
4. 必要时提供文化背景说明
5. 直接输出翻译结果，不要添加额外说明"""
    
    def translate_text(self, text: str, to_english: bool = True) -> str:
        """翻译单段文本"""
        direction = "中文翻译成英文" if to_english else "英文翻译成中文"
        prompt = f"请将以下文本从{direction}：\n\n{text}"
        
        options = ClaudeOptions(
            system_prompt=self.system_prompt,
            temperature=0.3  # 降低随机性，确保翻译一致性
        )
        
        response = self.claude.query(prompt, options=options)
        return response.output if response.return_code == 0 else f"翻译失败: {response.error}"
    
    async def translate_paragraphs(self, paragraphs: List[str], to_english: bool = True) -> List[str]:
        """批量翻译多个段落"""
        direction = "中文翻译成英文" if to_english else "英文翻译成中文"
        
        async def translate_paragraph(text: str) -> str:
            prompt = f"请将以下文本从{direction}：\n\n{text}"
            
            options = ClaudeOptions(
                system_prompt=self.system_prompt,
                temperature=0.3
            )
            
            response = await self.async_claude.query(prompt, options=options)
            return response.output if response.return_code == 0 else f"[翻译失败: {response.error}]"
        
        # 并发翻译所有段落
        tasks = [translate_paragraph(p) for p in paragraphs]
        return await asyncio.gather(*tasks)
    
    def translate_file(self, input_file: Path, output_file: Path, to_english: bool = True) -> None:
        """翻译整个文件"""
        if not input_file.exists():
            raise FileNotFoundError(f"输入文件不存在: {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 翻译内容
        translated = self.translate_text(content, to_english)
        
        # 保存翻译结果
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated)
        
        print(f"翻译完成！结果已保存到: {output_file}")
    
    async def translate_with_context(self, text: str, context: str, to_english: bool = True) -> str:
        """带上下文的翻译（用于专业文档）"""
        direction = "中文翻译成英文" if to_english else "英文翻译成中文"
        
        prompt = f"""上下文信息：{context}

请基于上述上下文，将以下文本从{direction}：

{text}"""
        
        options = ClaudeOptions(
            system_prompt=self.system_prompt + "\n6. 充分考虑提供的上下文信息",
            temperature=0.3
        )
        
        response = await self.async_claude.query(prompt, options=options)
        return response.output if response.return_code == 0 else f"翻译失败: {response.error}"


class InteractiveTranslator:
    """交互式翻译器"""
    
    def __init__(self, command: str = "claudee"):
        self.translator = Translator(command)
    
    async def start_session(self):
        """启动交互式翻译会话"""
        print("=== 交互式中英文翻译器 ===")
        print("输入 'quit' 退出，'switch' 切换翻译方向")
        print("默认：中文 → 英文\n")
        
        to_english = True
        
        while True:
            direction = "中→英" if to_english else "英→中"
            text = input(f"[{direction}] 请输入要翻译的文本: ").strip()
            
            if text.lower() == 'quit':
                print("感谢使用！")
                break
            elif text.lower() == 'switch':
                to_english = not to_english
                print(f"已切换到: {'中文→英文' if to_english else '英文→中文'}")
                continue
            elif not text:
                continue
            
            print("\n翻译中...")
            translated = self.translator.translate_text(text, to_english)
            print(f"\n翻译结果:\n{translated}\n")
            print("-" * 50)


# 示例文章
SAMPLE_ARTICLE = """人工智能的发展历程

人工智能（AI）的概念最早可以追溯到1956年的达特茅斯会议。在这次历史性的会议上，约翰·麦卡锡首次提出了"人工智能"这一术语。此后的几十年里，AI经历了多次起伏，包括两次"AI寒冬"。

进入21世纪后，随着计算能力的提升和大数据的普及，深度学习技术取得了突破性进展。2016年，AlphaGo战胜围棋世界冠军李世石，标志着AI在复杂决策领域达到了新的高度。

如今，AI已经渗透到我们生活的方方面面：智能手机的语音助手、推荐系统、自动驾驶汽车等。ChatGPT等大语言模型的出现，更是让AI的应用前景变得无限广阔。

展望未来，AI将继续改变我们的世界。但同时，我们也需要关注AI带来的伦理和安全问题，确保技术发展造福人类。"""


async def demo_batch_translation():
    """演示批量翻译"""
    translator = Translator()
    
    # 将文章分段
    paragraphs = [p.strip() for p in SAMPLE_ARTICLE.split('\n\n') if p.strip()]
    
    print("=== 批量翻译示例 ===")
    print(f"原文共 {len(paragraphs)} 段\n")
    
    # 批量翻译
    print("正在翻译...")
    translated_paragraphs = await translator.translate_paragraphs(paragraphs, to_english=True)
    
    # 显示结果
    print("\n翻译结果：")
    print("=" * 60)
    for i, (original, translated) in enumerate(zip(paragraphs, translated_paragraphs)):
        print(f"\n【第 {i+1} 段】")
        print(f"原文：{original}")
        print(f"译文：{translated}")
        print("-" * 60)


def demo_file_translation():
    """演示文件翻译"""
    translator = Translator()
    
    # 创建示例文件
    input_file = Path("sample_chinese.txt")
    output_file = Path("sample_english.txt")
    
    # 写入示例内容
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(SAMPLE_ARTICLE)
    
    print("=== 文件翻译示例 ===")
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print("\n正在翻译...")
    
    # 翻译文件
    translator.translate_file(input_file, output_file, to_english=True)
    
    # 显示部分结果
    with open(output_file, 'r', encoding='utf-8') as f:
        result = f.read()
    
    print("\n翻译结果预览（前200字）：")
    print(result[:200] + "...")


async def demo_context_translation():
    """演示带上下文的翻译"""
    translator = Translator()
    
    context = "这是一篇关于深度学习在医疗诊断领域应用的学术论文"
    text = "卷积神经网络在医学影像识别中表现出色，特别是在肺部CT扫描的病变检测方面。"
    
    print("=== 带上下文的翻译示例 ===")
    print(f"上下文: {context}")
    print(f"待翻译: {text}")
    print("\n翻译中...")
    
    result = await translator.translate_with_context(text, context, to_english=True)
    print(f"\n翻译结果: {result}")


async def main():
    """运行所有演示"""
    print("Claude CLI 翻译器演示\n")
    
    # 1. 简单翻译
    print("1. 简单文本翻译")
    print("-" * 60)
    translator = Translator()
    
    chinese_text = "机器学习是人工智能的一个重要分支，它使计算机能够从数据中学习并改进性能。"
    english_translation = translator.translate_text(chinese_text, to_english=True)
    print(f"中文: {chinese_text}")
    print(f"英文: {english_translation}")
    
    english_text = "Python is a versatile programming language widely used in data science."
    chinese_translation = translator.translate_text(english_text, to_english=False)
    print(f"\n英文: {english_text}")
    print(f"中文: {chinese_translation}")
    
    # 2. 批量翻译
    print("\n\n2. 批量段落翻译")
    print("-" * 60)
    await demo_batch_translation()
    
    # 3. 文件翻译
    print("\n\n3. 文件翻译")
    print("-" * 60)
    demo_file_translation()
    
    # 4. 带上下文翻译
    print("\n\n4. 专业翻译（带上下文）")
    print("-" * 60)
    await demo_context_translation()
    
    # 5. 交互式翻译
    print("\n\n5. 交互式翻译")
    print("-" * 60)
    print("提示：这将启动交互式会话，输入 'quit' 退出")
    choice = input("是否启动交互式翻译？(y/n): ")
    if choice.lower() == 'y':
        session = InteractiveTranslator()
        await session.start_session()


if __name__ == "__main__":
    # 运行演示
    asyncio.run(main())