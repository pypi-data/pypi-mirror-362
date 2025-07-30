#!/usr/bin/env python3
"""简单的中英文文章翻译器"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_cli import ClaudeCLI, ClaudeOptions
from pathlib import Path


def translate_article(article_text: str, to_english: bool = True) -> str:
    """翻译文章"""
    # 初始化 Claude CLI
    claude = ClaudeCLI(command="claudee")
    
    # 设置翻译方向
    if to_english:
        direction = "请将以下中文文章翻译成英文"
    else:
        direction = "请将以下英文文章翻译成中文"
    
    # 构建提示词
    prompt = f"""{direction}。要求：
1. 保持原文的结构和段落划分
2. 使用流畅自然的目标语言
3. 准确传达原文含义
4. 保留专有名词

文章内容：

{article_text}"""
    
    # 配置选项
    options = ClaudeOptions(
        temperature=0.3,  # 降低随机性
        system_prompt="你是一位专业的翻译专家，精通中英文互译。"
    )
    
    # 执行翻译
    print("正在翻译中，请稍候...")
    response = claude.query(prompt, options=options)
    
    if response.return_code == 0:
        return response.output
    else:
        return f"翻译失败: {response.error}"


# 示例中文文章
CHINESE_ARTICLE = """探索人工智能的未来

在过去的十年里，人工智能技术取得了令人瞩目的进展。从简单的图像识别到复杂的自然语言处理，AI正在改变我们的生活方式。

深度学习的突破

深度学习作为AI的核心技术，通过模拟人脑神经网络的工作方式，使机器能够自主学习和决策。这种技术已经在医疗诊断、自动驾驶、语音识别等领域展现出巨大潜力。

面临的挑战

尽管AI发展迅速，但仍面临诸多挑战：
- 数据隐私和安全问题
- 算法偏见和公平性
- 能源消耗和环境影响
- 就业市场的变化

展望未来

随着技术的不断进步，我们有理由相信AI将为人类带来更多益处。关键在于如何确保AI的发展符合人类的价值观和道德标准，真正实现人机协作的美好愿景。"""


# 示例英文文章
ENGLISH_ARTICLE = """The Rise of Sustainable Technology

As climate change becomes an increasingly urgent global challenge, sustainable technology has emerged as a critical solution for our future.

Innovation in Clean Energy

Solar panels and wind turbines have become more efficient and affordable than ever before. Battery storage technology is advancing rapidly, making renewable energy more reliable and accessible to communities worldwide.

Green Transportation Revolution

Electric vehicles are no longer a niche market. Major automakers are committing to fully electric lineups, while cities invest in charging infrastructure and promote public transportation alternatives.

The Path Forward

Success in combating climate change requires continued innovation, policy support, and individual action. By embracing sustainable technology, we can create a cleaner, more prosperous future for generations to come."""


def main():
    print("=== Claude CLI 文章翻译器 ===\n")
    
    while True:
        print("请选择操作：")
        print("1. 翻译中文文章为英文")
        print("2. 翻译英文文章为中文")
        print("3. 翻译自定义文本")
        print("4. 翻译文件")
        print("5. 退出")
        
        choice = input("\n请输入选项 (1-5): ").strip()
        
        if choice == '1':
            print("\n【中译英示例】")
            print("原文：")
            print("-" * 60)
            print(CHINESE_ARTICLE)
            print("-" * 60)
            
            translation = translate_article(CHINESE_ARTICLE, to_english=True)
            print("\n英文翻译：")
            print("-" * 60)
            print(translation)
            print("-" * 60)
            
        elif choice == '2':
            print("\n【英译中示例】")
            print("原文：")
            print("-" * 60)
            print(ENGLISH_ARTICLE)
            print("-" * 60)
            
            translation = translate_article(ENGLISH_ARTICLE, to_english=False)
            print("\n中文翻译：")
            print("-" * 60)
            print(translation)
            print("-" * 60)
            
        elif choice == '3':
            print("\n【自定义翻译】")
            direction = input("选择翻译方向 (1:中→英, 2:英→中): ").strip()
            to_english = direction == '1'
            
            print(f"\n请输入要翻译的文本（输入END结束）：")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            
            text = '\n'.join(lines)
            if text:
                translation = translate_article(text, to_english=to_english)
                print("\n翻译结果：")
                print("-" * 60)
                print(translation)
                print("-" * 60)
            
        elif choice == '4':
            print("\n【文件翻译】")
            input_path = input("请输入要翻译的文件路径: ").strip()
            
            if not Path(input_path).exists():
                print("文件不存在！")
                continue
            
            direction = input("选择翻译方向 (1:中→英, 2:英→中): ").strip()
            to_english = direction == '1'
            
            # 读取文件
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 翻译
            translation = translate_article(content, to_english=to_english)
            
            # 保存结果
            output_path = input_path.rsplit('.', 1)[0] + '_translated.txt'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translation)
            
            print(f"\n翻译完成！结果已保存到: {output_path}")
            
        elif choice == '5':
            print("\n感谢使用！再见！")
            break
        
        else:
            print("\n无效选项，请重新选择。")
        
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()