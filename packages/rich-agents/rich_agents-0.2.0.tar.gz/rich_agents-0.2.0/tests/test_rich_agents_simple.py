#!/usr/bin/env python3
"""
Rich-Agents 简单功能测试
不依赖pytest，直接运行测试验证核心功能
"""

import os
import sys
import tempfile
import traceback
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """测试基础导入功能"""
    print("测试基础导入...")
    
    try:
        from shared.config.rich_agents_config_manager import RichAgentsConfigManager
        print("✅ RichAgentsConfigManager 导入成功")
    except Exception as e:
        print(f"❌ RichAgentsConfigManager 导入失败: {str(e)}")
        return False
    
    try:
        from shared.llm_adapters.unified_llm_adapter import UnifiedLLMAdapter
        print("✅ UnifiedLLMAdapter 导入成功")
    except Exception as e:
        print(f"❌ UnifiedLLMAdapter 导入失败: {str(e)}")
        return False
    
    return True


def test_config_manager():
    """测试配置管理器"""
    print("\n测试配置管理器...")
    
    try:
        from shared.config.rich_agents_config_manager import RichAgentsConfigManager
        
        # 创建临时目录测试
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = RichAgentsConfigManager(temp_dir)
            print("✅ 配置管理器初始化成功")
            
            # 测试获取配置
            trading_config = config_manager.get_trading_config()
            assert trading_config["agent_type"] == "trading"
            print(f"✅ TradingAgent配置: {len(trading_config)} 项")
            
            patent_config = config_manager.get_patent_config()
            assert patent_config["agent_type"] == "patent"
            print(f"✅ PatentAgent配置: {len(patent_config)} 项")
            
            # 测试LLM提供商
            providers = config_manager.get_available_llm_providers()
            assert len(providers) > 0
            print(f"✅ 可用LLM提供商: {', '.join(providers)}")
            
            # 测试系统状态
            status = config_manager.get_system_status()
            assert status["config_loaded"] is True
            print(f"✅ 系统状态: {len(status)} 项状态信息")
            
            # 测试配置验证
            validation = config_manager.validate_config("trading")
            assert "valid" in validation
            print("✅ 配置验证功能正常")
            
            return True
            
    except Exception as e:
        print(f"❌ 配置管理器测试失败: {str(e)}")
        traceback.print_exc()
        return False


def test_llm_adapter():
    """测试LLM适配器"""
    print("\n测试LLM适配器...")
    
    try:
        from shared.llm_adapters.unified_llm_adapter import UnifiedLLMAdapter, LLMAdapterFactory
        
        # 测试支持的提供商
        providers = UnifiedLLMAdapter.get_supported_providers()
        assert len(providers) > 0
        assert "openai" in providers
        assert "dashscope" in providers
        print(f"✅ 支持的LLM提供商: {', '.join(providers)}")
        
        # 测试配置验证
        valid_config = {"model": "gpt-4", "api_key": "test_key"}
        result = UnifiedLLMAdapter.validate_provider_config("openai", valid_config)
        assert result["valid"] is True
        print("✅ 有效配置验证通过")
        
        invalid_config = {}
        result = UnifiedLLMAdapter.validate_provider_config("openai", invalid_config)
        assert result["valid"] is False
        print("✅ 无效配置验证通过")
        
        # 测试不支持的提供商
        result = UnifiedLLMAdapter.validate_provider_config("invalid", valid_config)
        assert result["valid"] is False
        print("✅ 不支持提供商验证通过")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM适配器测试失败: {str(e)}")
        traceback.print_exc()
        return False


def test_cli_imports():
    """测试CLI模块导入"""
    print("\n测试CLI模块导入...")
    
    try:
        from cli.trading_cli import TradingAgentCLI
        print("✅ TradingAgentCLI 导入成功")
    except Exception as e:
        print(f"⚠️ TradingAgentCLI 导入失败: {str(e)}")
    
    try:
        from cli.patent_cli import PatentAgentCLI
        print("✅ PatentAgentCLI 导入成功")
    except Exception as e:
        print(f"⚠️ PatentAgentCLI 导入失败: {str(e)}")
    
    try:
        from cli.rich_agents_main import RichAgentsCLI
        print("✅ RichAgentsCLI 导入成功")
        return True
    except Exception as e:
        print(f"❌ RichAgentsCLI 导入失败: {str(e)}")
        traceback.print_exc()
        return False


def test_config_files_creation():
    """测试配置文件创建"""
    print("\n测试配置文件创建...")
    
    try:
        from shared.config.rich_agents_config_manager import RichAgentsConfigManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = RichAgentsConfigManager(temp_dir)
            
            # 检查配置文件是否被创建
            assert config_manager.main_config_file.exists()
            print("✅ 主配置文件创建成功")
            
            assert config_manager.trading_config_file.exists()
            print("✅ TradingAgent配置文件创建成功")
            
            assert config_manager.patent_config_file.exists()
            print("✅ PatentAgent配置文件创建成功")
            
            return True
            
    except Exception as e:
        print(f"❌ 配置文件创建测试失败: {str(e)}")
        traceback.print_exc()
        return False


def test_shared_modules():
    """测试共享模块"""
    print("\n测试共享模块...")
    
    try:
        import shared
        print("✅ shared包导入成功")
        
        import shared.config
        print("✅ shared.config模块导入成功")
        
        import shared.llm_adapters
        print("✅ shared.llm_adapters模块导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 共享模块测试失败: {str(e)}")
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    print("🚀 开始运行Rich-Agents功能测试")
    print("=" * 50)
    
    tests = [
        ("基础导入", test_imports),
        ("共享模块", test_shared_modules),
        ("配置管理器", test_config_manager),
        ("LLM适配器", test_llm_adapter),
        ("CLI模块导入", test_cli_imports),
        ("配置文件创建", test_config_files_creation)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                failed += 1
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} 测试异常: {str(e)}")
    
    print("\n" + "=" * 50)
    print("📊 测试结果统计")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")
    print(f"📈 成功率: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 所有测试通过! Rich-Agents核心功能正常工作")
        return True
    else:
        print(f"\n⚠️ {failed} 个测试失败，请检查相关功能")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 