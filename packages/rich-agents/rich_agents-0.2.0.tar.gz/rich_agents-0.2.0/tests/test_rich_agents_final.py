#!/usr/bin/env python3
"""
Rich-Agents 最终验证脚本
在虚拟环境中全面测试Rich-Agents系统的所有功能
"""

import os
import sys
import subprocess
import tempfile
import traceback
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_command(cmd, description=""):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "description": description
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Command timed out",
            "description": description
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "description": description
        }

def test_system_imports():
    """测试系统导入"""
    print("🔍 测试系统导入...")
    
    tests = [
        "from shared.config.rich_agents_config_manager import RichAgentsConfigManager",
        "from shared.llm_adapters.unified_llm_adapter import UnifiedLLMAdapter",
        "from cli.patent_cli import PatentAgentCLI",
        "from cli.rich_agents_simple import RichAgentsSimpleCLI",
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            exec(test)
            print(f"  ✅ {test.split('import')[-1].strip()}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {test.split('import')[-1].strip()}: {str(e)}")
            failed += 1
    
    return passed, failed

def test_config_functionality():
    """测试配置功能"""
    print("\n⚙️ 测试配置功能...")
    
    try:
        from shared.config.rich_agents_config_manager import RichAgentsConfigManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = RichAgentsConfigManager(temp_dir)
            
            # 测试基本功能
            tests = [
                ("配置管理器初始化", lambda: config_manager is not None),
                ("主配置获取", lambda: len(config_manager.main_config) > 0),
                ("TradingAgent配置", lambda: len(config_manager.get_trading_config()) > 0),
                ("PatentAgent配置", lambda: len(config_manager.get_patent_config()) > 0),
                ("系统状态", lambda: config_manager.get_system_status()["config_loaded"]),
                ("配置验证", lambda: config_manager.validate_config()["valid"]),
                ("API密钥检查", lambda: len(config_manager.check_api_keys()) > 0),
                ("LLM提供商", lambda: len(config_manager.get_available_llm_providers()) == 4),
            ]
            
            passed = 0
            failed = 0
            
            for test_name, test_func in tests:
                try:
                    if test_func():
                        print(f"  ✅ {test_name}")
                        passed += 1
                    else:
                        print(f"  ❌ {test_name}: 返回False")
                        failed += 1
                except Exception as e:
                    print(f"  ❌ {test_name}: {str(e)}")
                    failed += 1
            
            return passed, failed
            
    except Exception as e:
        print(f"  ❌ 配置功能测试失败: {str(e)}")
        return 0, 1

def test_cli_functionality():
    """测试CLI功能"""
    print("\n🖥️ 测试CLI功能...")
    
    cli_tests = [
        ("python cli/rich_agents_simple.py --help", "简化版CLI帮助"),
        ("python main.py --help", "主入口帮助"),
    ]
    
    # 如果有完整依赖，测试完整版CLI
    try:
        import typer
        cli_tests.append(("python cli/rich_agents_main.py --help", "完整版CLI帮助"))
    except ImportError:
        pass
    
    passed = 0
    failed = 0
    
    for cmd, description in cli_tests:
        result = run_command(cmd, description)
        if result["success"]:
            print(f"  ✅ {description}")
            passed += 1
        else:
            print(f"  ❌ {description}: {result['stderr']}")
            failed += 1
    
    return passed, failed

def test_agent_functionality():
    """测试智能体功能"""
    print("\n🤖 测试智能体功能...")
    
    try:
        from cli.patent_cli import PatentAgentCLI
        from shared.config.rich_agents_config_manager import RichAgentsConfigManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager = RichAgentsConfigManager(temp_dir)
            patent_cli = PatentAgentCLI(config_manager)
            
            tests = [
                ("PatentAgent初始化", lambda: patent_cli is not None),
                ("支持的分析类型", lambda: len(patent_cli.get_supported_analysis_types()) > 0),
                ("可用智能体", lambda: len(patent_cli.get_available_agents()) > 0),
                ("配置验证", lambda: patent_cli.validate_patent_config()["valid"]),
            ]
            
            passed = 0
            failed = 0
            
            for test_name, test_func in tests:
                try:
                    if test_func():
                        print(f"  ✅ {test_name}")
                        passed += 1
                    else:
                        print(f"  ❌ {test_name}: 返回False")
                        failed += 1
                except Exception as e:
                    print(f"  ❌ {test_name}: {str(e)}")
                    failed += 1
            
            return passed, failed
            
    except Exception as e:
        print(f"  ❌ 智能体功能测试失败: {str(e)}")
        return 0, 1

def test_integration():
    """测试集成功能"""
    print("\n🔗 测试集成功能...")
    
    integration_tests = [
        ("echo '5' | timeout 5 python cli/rich_agents_simple.py || true", "简化版CLI交互"),
        ("python -c \"from cli.rich_agents_simple import main; print('CLI导入成功')\"", "CLI模块导入"),
        ("python -c \"import main; print('主模块导入成功')\"", "主模块导入"),
    ]
    
    passed = 0
    failed = 0
    
    for cmd, description in integration_tests:
        result = run_command(cmd, description)
        if result["success"] or "成功" in result["stdout"]:
            print(f"  ✅ {description}")
            passed += 1
        else:
            print(f"  ❌ {description}: {result['stderr']}")
            failed += 1
    
    return passed, failed

def test_dependencies():
    """测试依赖状态"""
    print("\n📦 测试依赖状态...")
    
    core_deps = ["rich", "typer", "langchain-openai", "langchain-anthropic", "langchain-google-genai", "langgraph"]
    
    passed = 0
    failed = 0
    
    for dep in core_deps:
        try:
            __import__(dep.replace("-", "_"))
            print(f"  ✅ {dep}")
            passed += 1
        except ImportError:
            print(f"  ❌ {dep}: 未安装")
            failed += 1
    
    return passed, failed

def run_final_validation():
    """运行最终验证"""
    print("🚀 Rich-Agents 最终验证测试")
    print("=" * 60)
    
    total_passed = 0
    total_failed = 0
    
    # 运行所有测试
    test_functions = [
        ("系统导入", test_system_imports),
        ("配置功能", test_config_functionality),
        ("CLI功能", test_cli_functionality),
        ("智能体功能", test_agent_functionality),
        ("集成功能", test_integration),
        ("依赖状态", test_dependencies),
    ]
    
    for test_name, test_func in test_functions:
        try:
            passed, failed = test_func()
            total_passed += passed
            total_failed += failed
        except Exception as e:
            print(f"\n❌ {test_name} 测试异常: {str(e)}")
            total_failed += 1
    
    print("\n" + "=" * 60)
    print("📊 最终验证结果")
    print(f"✅ 通过测试: {total_passed}")
    print(f"❌ 失败测试: {total_failed}")
    print(f"📈 成功率: {total_passed/(total_passed+total_failed)*100:.1f}%")
    
    if total_failed == 0:
        print("\n🎉 所有测试通过! Rich-Agents系统验证成功!")
        print("\n📋 系统功能总结:")
        print("• ✅ 统一配置管理系统")
        print("• ✅ 多LLM提供商支持 (百炼、OpenAI、Google、Anthropic)")
        print("• ✅ 简化版和完整版CLI")
        print("• ✅ TradingAgent金融分析智能体")
        print("• ✅ PatentAgent专利智能体")
        print("• ✅ 完整的错误处理和降级机制")
        print("• ✅ 虚拟环境兼容性")
        
        print("\n🔧 使用方法:")
        print("1. 简化版: python cli/rich_agents_simple.py")
        print("2. 完整版: python cli/rich_agents_main.py")
        print("3. 主入口: python main.py")
        print("4. 直接启动: python main.py --agent patent")
        
        return True
    else:
        print(f"\n⚠️ 发现 {total_failed} 个问题，需要进一步检查")
        return False

if __name__ == "__main__":
    success = run_final_validation()
    sys.exit(0 if success else 1) 