#!/usr/bin/env python3
"""
Rich-Agents 集成测试
测试简化版CLI的基本功能，避免复杂依赖
"""

import os
import sys
import tempfile
import traceback
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_basic_imports():
    """测试基础导入"""
    print("测试基础导入...")
    
    try:
        from shared.config.rich_agents_config_manager import RichAgentsConfigManager
        print("✅ RichAgentsConfigManager 导入成功")
        
        from shared.llm_adapters.unified_llm_adapter import UnifiedLLMAdapter
        print("✅ UnifiedLLMAdapter 导入成功")
        
        return True
    except Exception as e:
        print(f"❌ 基础导入失败: {str(e)}")
        traceback.print_exc()
        return False

def test_config_manager():
    """测试配置管理器"""
    print("\n测试配置管理器...")
    
    try:
        from shared.config.rich_agents_config_manager import RichAgentsConfigManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = RichAgentsConfigManager(temp_dir)
            print("✅ 配置管理器初始化成功")
            
            # 测试配置获取
            trading_config = config_manager.get_trading_config()
            print(f"✅ TradingAgent配置: {len(trading_config)} 项")
            
            patent_config = config_manager.get_patent_config()
            print(f"✅ PatentAgent配置: {len(patent_config)} 项")
            
            # 测试系统状态
            status = config_manager.get_system_status()
            print(f"✅ 系统状态: {status['config_loaded']}")
            
            return True
            
    except Exception as e:
        print(f"❌ 配置管理器测试失败: {str(e)}")
        traceback.print_exc()
        return False

def test_simple_cli_import():
    """测试简化CLI导入"""
    print("\n测试简化CLI导入...")
    
    try:
        # 测试简化CLI的基本导入
        from cli.rich_agents_simple import print_message
        print_message("测试消息", "success")
        print("✅ 简化CLI基础功能导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 简化CLI导入失败: {str(e)}")
        traceback.print_exc()
        return False

def test_patent_cli_basic():
    """测试PatentAgent CLI基础功能"""
    print("\n测试PatentAgent CLI基础功能...")
    
    try:
        from cli.patent_cli import PatentAgentCLI
        from shared.config.rich_agents_config_manager import RichAgentsConfigManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = RichAgentsConfigManager(temp_dir)
            patent_cli = PatentAgentCLI(config_manager)
            
            # 测试基础功能
            analysis_types = patent_cli.get_supported_analysis_types()
            print(f"✅ 支持的分析类型: {', '.join(analysis_types)}")
            
            agents = patent_cli.get_available_agents()
            print(f"✅ 可用智能体: {len(agents)} 个")
            
            return True
            
    except Exception as e:
        print(f"❌ PatentAgent CLI测试失败: {str(e)}")
        traceback.print_exc()
        return False

def test_main_entry():
    """测试主入口文件"""
    print("\n测试主入口文件...")
    
    try:
        # 测试main.py的基本导入
        import main
        print("✅ main.py 导入成功")
        
        # 测试函数定义
        assert hasattr(main, 'run_trading_agent_example')
        print("✅ run_trading_agent_example 函数存在")
        
        assert hasattr(main, 'run_rich_agents_cli')
        print("✅ run_rich_agents_cli 函数存在")
        
        return True
        
    except Exception as e:
        print(f"❌ 主入口测试失败: {str(e)}")
        traceback.print_exc()
        return False

def test_configuration_files():
    """测试配置文件生成"""
    print("\n测试配置文件生成...")
    
    try:
        from shared.config.rich_agents_config_manager import RichAgentsConfigManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = RichAgentsConfigManager(temp_dir)
            
            # 检查配置文件是否生成
            assert config_manager.main_config_file.exists()
            print("✅ 主配置文件生成成功")
            
            assert config_manager.trading_config_file.exists()
            print("✅ TradingAgent配置文件生成成功")
            
            assert config_manager.patent_config_file.exists()
            print("✅ PatentAgent配置文件生成成功")
            
            # 检查配置内容
            assert config_manager.main_config["name"] == "Rich-Agents"
            print("✅ 配置内容正确")
            
            return True
            
    except Exception as e:
        print(f"❌ 配置文件测试失败: {str(e)}")
        traceback.print_exc()
        return False

def test_api_key_management():
    """测试API密钥管理"""
    print("\n测试API密钥管理...")
    
    try:
        from shared.config.rich_agents_config_manager import RichAgentsConfigManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = RichAgentsConfigManager(temp_dir)
            
            # 测试API密钥检查
            api_status = config_manager.check_api_keys("trading")
            print(f"✅ TradingAgent API密钥状态: {len(api_status)} 项")
            
            api_status = config_manager.check_api_keys("patent")
            print(f"✅ PatentAgent API密钥状态: {len(api_status)} 项")
            
            # 测试LLM提供商
            providers = config_manager.get_available_llm_providers()
            print(f"✅ 可用LLM提供商: {', '.join(providers)}")
            
            return True
            
    except Exception as e:
        print(f"❌ API密钥管理测试失败: {str(e)}")
        traceback.print_exc()
        return False

def run_integration_tests():
    """运行集成测试"""
    print("🚀 开始运行Rich-Agents集成测试")
    print("=" * 50)
    
    tests = [
        ("基础导入", test_basic_imports),
        ("配置管理器", test_config_manager),
        ("简化CLI导入", test_simple_cli_import),
        ("PatentAgent CLI", test_patent_cli_basic),
        ("主入口文件", test_main_entry),
        ("配置文件生成", test_configuration_files),
        ("API密钥管理", test_api_key_management)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*15} {test_name} {'='*15}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 集成测试通过")
            else:
                failed += 1
                print(f"❌ {test_name} 集成测试失败")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} 集成测试异常: {str(e)}")
    
    print("\n" + "=" * 50)
    print("📊 集成测试结果统计")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")
    print(f"📈 成功率: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 所有集成测试通过! Rich-Agents系统集成正常")
        return True
    else:
        print(f"\n⚠️ {failed} 个集成测试失败，需要进一步检查")
        return False

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1) 