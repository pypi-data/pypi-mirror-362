#!/usr/bin/env python3
"""
测试 Crewler 修复的简单脚本
"""
import asyncio
import tempfile
import os
from hero.util.crewler import Crewler

async def test_crewler():
    """测试 Crewler 的基本功能"""
    try:
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"使用临时目录: {temp_dir}")
            
            # 创建 Crewler 实例
            crewler = Crewler(temp_dir)
            print("Crewler 实例创建成功")
            
            # 测试初始化
            await crewler.initialize()
            print("Crewler 初始化成功")
            
            # 测试关闭
            await crewler.close()
            print("Crewler 关闭成功")
            
            print("✅ 所有测试通过！")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_crewler()) 