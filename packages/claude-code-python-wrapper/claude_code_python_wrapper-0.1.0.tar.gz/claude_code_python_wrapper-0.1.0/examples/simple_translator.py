#!/usr/bin/env python3
"""简化版中英文翻译器"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_cli import ClaudeCLI


def translate_text(text: str, to_english: bool = True) -> str:
    """翻译文本"""
    claude = ClaudeCLI(command="claudee")
    
    if to_english:
        prompt = f"""请将以下中文翻译成英文。要求译文准确、流畅、自然：

{text}"""
    else:
        prompt = f"""请将以下英文翻译成中文。要求译文准确、流畅、符合中文表达习惯：

{text}"""
    
    response = claude.query(prompt)
    return response.output if response.return_code == 0 else f"翻译失败: {response.error}"


def main():
    print("=== 中英文翻译演示 ===\n")
    
    # 示例1：中文段落翻译
    chinese_paragraph = """
    人工智能的发展正在深刻改变我们的生活方式。从智能手机的语音助手到自动驾驶汽车，
    从医疗诊断到金融风控，AI技术已经渗透到社会的各个角落。这场技术革命不仅提高了
    生产效率，也为解决人类面临的诸多挑战提供了新的可能性。
    """
    
    print("【示例1：中文段落 → 英文】")
    print("原文:", chinese_paragraph.strip())
    print("\n翻译中...")
    
    english_translation = translate_text(chinese_paragraph, to_english=True)
    print("\n英文翻译:")
    print(english_translation)
    
    print("\n" + "="*60 + "\n")
    
    # 示例2：英文段落翻译
    english_paragraph = """
    The rapid advancement of artificial intelligence is fundamentally transforming how we live and work. 
    From voice assistants in smartphones to autonomous vehicles, from medical diagnostics to financial 
    risk management, AI technology has permeated every corner of society. This technological revolution 
    not only enhances productivity but also offers new possibilities for addressing many challenges 
    facing humanity.
    """
    
    print("【示例2：英文段落 → 中文】")
    print("原文:", english_paragraph.strip())
    print("\n翻译中...")
    
    chinese_translation = translate_text(english_paragraph, to_english=False)
    print("\n中文翻译:")
    print(chinese_translation)
    
    print("\n" + "="*60 + "\n")
    
    # 示例3：技术文档翻译
    technical_chinese = """
    机器学习模型的训练过程包括以下步骤：
    1. 数据预处理：清洗数据并进行特征工程
    2. 模型选择：根据任务特点选择合适的算法
    3. 参数调优：通过交叉验证找到最佳超参数
    4. 模型评估：使用测试集评估模型性能
    5. 部署上线：将训练好的模型集成到生产环境
    """
    
    print("【示例3：技术文档翻译】")
    print("原文:", technical_chinese.strip())
    print("\n翻译中...")
    
    technical_english = translate_text(technical_chinese, to_english=True)
    print("\n英文翻译:")
    print(technical_english)
    
    print("\n" + "="*60 + "\n")
    
    # 示例4：简短句子翻译
    print("【示例4：常用短句翻译】")
    
    short_sentences = [
        ("今天天气真好！", True),
        ("Welcome to Beijing!", False),
        ("请问洗手间在哪里？", True),
        ("Thank you for your help.", False),
        ("这个多少钱？", True),
    ]
    
    for sentence, to_eng in short_sentences:
        direction = "中→英" if to_eng else "英→中"
        print(f"\n{direction}: {sentence}")
        translation = translate_text(sentence, to_english=to_eng)
        print(f"翻译: {translation}")
    
    print("\n\n所有翻译示例完成！")


if __name__ == "__main__":
    main()