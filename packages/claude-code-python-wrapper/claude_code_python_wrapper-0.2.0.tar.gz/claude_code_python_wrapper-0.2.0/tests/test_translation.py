#!/usr/bin/env python3
"""测试中英文翻译功能"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_cli import ClaudeCLI, ClaudeOptions


# 测试文章
CHINESE_TEXT = """人工智能正在改变世界

近年来，人工智能技术的快速发展引起了全球的关注。从ChatGPT到自动驾驶汽车，AI正在各个领域展现其强大的能力。

机器学习算法使计算机能够从大量数据中学习模式，而深度学习则进一步推动了图像识别、语音处理等技术的突破。

然而，我们也需要认真思考AI带来的伦理问题，确保技术发展能够造福全人类。"""

ENGLISH_TEXT = """The Future of Work in the Digital Age

Remote work has become increasingly common, transforming how we think about offices and collaboration. Cloud computing and video conferencing have made it possible for teams to work effectively from anywhere.

This shift brings both opportunities and challenges. While flexibility has improved work-life balance for many, it also requires new skills in digital communication and self-management.

Companies are adapting by investing in digital tools and rethinking their organizational cultures."""


def translate(text: str, to_english: bool = True) -> str:
    """执行翻译"""
    claude = ClaudeCLI(command="claudee")
    
    direction = "将以下中文翻译成英文" if to_english else "将以下英文翻译成中文"
    prompt = f"{direction}，保持原文风格和结构：\n\n{text}"
    
    options = ClaudeOptions(
        temperature=0.3,
        system_prompt="你是专业翻译，请提供准确流畅的翻译。"
    )
    
    response = claude.query(prompt, options=options)
    return response.output if response.return_code == 0 else f"Error: {response.error}"


def main():
    print("=== 中英文翻译测试 ===\n")
    
    # 测试1：中译英
    print("【测试1：中文 → 英文】")
    print("原文：")
    print("-" * 50)
    print(CHINESE_TEXT)
    print("-" * 50)
    
    print("\n翻译中...")
    english_result = translate(CHINESE_TEXT, to_english=True)
    
    print("\n英文翻译：")
    print("-" * 50)
    print(english_result)
    print("-" * 50)
    
    # 测试2：英译中
    print("\n\n【测试2：英文 → 中文】")
    print("原文：")
    print("-" * 50)
    print(ENGLISH_TEXT)
    print("-" * 50)
    
    print("\n翻译中...")
    chinese_result = translate(ENGLISH_TEXT, to_english=False)
    
    print("\n中文翻译：")
    print("-" * 50)
    print(chinese_result)
    print("-" * 50)
    
    # 测试3：短句翻译
    print("\n\n【测试3：短句快速翻译】")
    test_phrases = [
        ("机器学习是人工智能的核心技术。", True),
        ("Python is widely used in data science.", False),
        ("深度神经网络可以处理复杂的模式识别任务。", True),
    ]
    
    for phrase, to_eng in test_phrases:
        direction = "中→英" if to_eng else "英→中"
        print(f"\n{direction}: {phrase}")
        result = translate(phrase, to_english=to_eng)
        print(f"翻译: {result}")
    
    print("\n\n翻译测试完成！")


if __name__ == "__main__":
    main()