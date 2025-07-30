#!/usr/bin/env python3
"""
PatentAgent 系统状态测试
测试系统各个组件的状态和可用性
"""

import os
import sys
import json
from datetime import datetime


def test_directory_structure():
    """测试目录结构"""
    print("📁 测试目录结构...")
    
    required_dirs = [
        "patentagents",
        "patentagents/agents",
        "patentagents/agents/utils",
        "patentagents/agents/analysts",
        "patentagents/agents/writers",
        "patentagents/cli",
        "patentagents/dataflows",
        "patentagents/graph",
        "tests"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"❌ 缺少目录: {missing_dirs}")
        return False
    else:
        print("✅ 目录结构完整")
        return True


def test_core_files():
    """测试核心文件"""
    print("\n📄 测试核心文件...")
    
    required_files = [
        "patentagents/__init__.py",
        "patentagents/agents/__init__.py",
        "patentagents/agents/utils/__init__.py",
        "patentagents/agents/utils/patent_states.py",
        "patentagents/agents/utils/patent_utils.py",
        "patentagents/agents/analysts/__init__.py",
        "patentagents/agents/analysts/technology_analyst.py",
        "patentagents/agents/analysts/innovation_discovery.py",
        "patentagents/agents/analysts/prior_art_researcher.py",
        "patentagents/agents/writers/__init__.py",
        "patentagents/agents/writers/patent_writer.py",
        "patentagents/cli/__init__.py",
        "patentagents/cli/main.py",
        "patentagents/dataflows/google_patents_utils.py",
        "patentagents/dataflows/zhihuiya_utils.py",
        "patentagents/graph/patent_graph.py",
        "target.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺少文件: {missing_files}")
        return False
    else:
        print("✅ 核心文件完整")
        return True


def test_file_sizes():
    """测试文件大小"""
    print("\n📏 测试文件大小...")
    
    file_size_requirements = {
        "patentagents/agents/utils/patent_states.py": 1000,  # 至少1KB
        "patentagents/agents/utils/patent_utils.py": 10000,  # 至少10KB
        "patentagents/agents/analysts/technology_analyst.py": 5000,  # 至少5KB
        "patentagents/agents/analysts/innovation_discovery.py": 5000,
        "patentagents/agents/analysts/prior_art_researcher.py": 8000,
        "patentagents/agents/writers/patent_writer.py": 8000,
        "patentagents/cli/main.py": 5000,
        "patentagents/dataflows/google_patents_utils.py": 8000,
        "patentagents/dataflows/zhihuiya_utils.py": 8000,
        "patentagents/graph/patent_graph.py": 5000,
        "target.md": 10000
    }
    
    size_issues = []
    for file_path, min_size in file_size_requirements.items():
        if os.path.exists(file_path):
            actual_size = os.path.getsize(file_path)
            if actual_size < min_size:
                size_issues.append(f"{file_path}: {actual_size}B < {min_size}B")
        else:
            size_issues.append(f"{file_path}: 文件不存在")
    
    if size_issues:
        print(f"⚠️ 文件大小问题: {size_issues}")
        return False
    else:
        print("✅ 文件大小符合要求")
        return True


def test_function_definitions():
    """测试函数定义"""
    print("\n🔧 测试函数定义...")
    
    function_checks = []
    
    # 检查各个文件中的关键函数
    files_to_check = [
        ("patentagents/agents/utils/patent_states.py", [
            "class PatentState",
            "def create_initial_patent_state",
            "def validate_patent_state"
        ]),
        ("patentagents/agents/utils/patent_utils.py", [
            "class PatentToolkit",
            "def search_google_patents",
            "def search_zhihuiya_patents"
        ]),
        ("patentagents/agents/analysts/technology_analyst.py", [
            "def create_technology_analyst",
            "def validate_technology_analysis"
        ]),
        ("patentagents/agents/analysts/innovation_discovery.py", [
            "def create_innovation_discovery_analyst",
            "def validate_innovation_opportunities"
        ]),
        ("patentagents/agents/analysts/prior_art_researcher.py", [
            "def create_prior_art_researcher",
            "def validate_prior_art_research"
        ]),
        ("patentagents/agents/writers/patent_writer.py", [
            "def create_patent_writer",
            "def validate_patent_draft"
        ]),
        ("patentagents/cli/main.py", [
            "class PatentAgentCLI",
            "def run_analysis",
            "def check_system_status"
        ]),
        ("patentagents/graph/patent_graph.py", [
            "class PatentAgentsGraph",
            "def create_patent_agents_graph"
        ])
    ]
    
    for file_path, functions in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for func_name in functions:
                    if func_name not in content:
                        function_checks.append(f"{file_path}: 缺少 {func_name}")
            except Exception as e:
                function_checks.append(f"{file_path}: 读取失败 - {e}")
        else:
            function_checks.append(f"{file_path}: 文件不存在")
    
    if function_checks:
        print(f"❌ 函数定义问题: {function_checks}")
        return False
    else:
        print("✅ 关键函数定义完整")
        return True


def test_imports():
    """测试导入语句"""
    print("\n📦 测试导入语句...")
    
    import_issues = []
    
    # 检查各个文件的导入语句
    files_to_check = [
        ("patentagents/agents/utils/patent_states.py", [
            "from typing import",
            "from datetime import"
        ]),
        ("patentagents/agents/utils/patent_utils.py", [
            "import requests",
            "from typing import"
        ]),
        ("patentagents/agents/analysts/technology_analyst.py", [
            "from typing import",
            "import logging"
        ]),
        ("patentagents/cli/main.py", [
            "import os",
            "from typing import"
        ])
    ]
    
    for file_path, imports in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for import_stmt in imports:
                    if import_stmt not in content:
                        import_issues.append(f"{file_path}: 缺少 {import_stmt}")
            except Exception as e:
                import_issues.append(f"{file_path}: 读取失败 - {e}")
        else:
            import_issues.append(f"{file_path}: 文件不存在")
    
    if import_issues:
        print(f"⚠️ 导入语句问题: {import_issues}")
        return False
    else:
        print("✅ 导入语句完整")
        return True


def test_documentation():
    """测试文档"""
    print("\n📚 测试文档...")
    
    doc_issues = []
    
    # 检查文档字符串
    files_to_check = [
        "patentagents/agents/utils/patent_states.py",
        "patentagents/agents/utils/patent_utils.py",
        "patentagents/agents/analysts/technology_analyst.py",
        "patentagents/agents/analysts/innovation_discovery.py",
        "patentagents/agents/analysts/prior_art_researcher.py",
        "patentagents/agents/writers/patent_writer.py",
        "patentagents/cli/main.py",
        "patentagents/graph/patent_graph.py"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 检查是否有文档字符串
                if '"""' not in content and "'''" not in content:
                    doc_issues.append(f"{file_path}: 缺少文档字符串")
                    
                # 检查是否有函数文档
                if 'def ' in content and 'Args:' not in content and 'Returns:' not in content:
                    doc_issues.append(f"{file_path}: 函数缺少详细文档")
                    
            except Exception as e:
                doc_issues.append(f"{file_path}: 读取失败 - {e}")
        else:
            doc_issues.append(f"{file_path}: 文件不存在")
    
    if doc_issues:
        print(f"⚠️ 文档问题: {doc_issues}")
        return False
    else:
        print("✅ 文档完整")
        return True


def generate_test_report():
    """生成测试报告"""
    print("\n" + "="*60)
    print("🎯 PatentAgent 系统状态测试报告")
    print("="*60)
    
    test_results = []
    
    # 运行所有测试
    test_functions = [
        ("目录结构", test_directory_structure),
        ("核心文件", test_core_files),
        ("文件大小", test_file_sizes),
        ("函数定义", test_function_definitions),
        ("导入语句", test_imports),
        ("文档完整性", test_documentation)
    ]
    
    passed_tests = 0
    total_tests = len(test_functions)
    
    for test_name, test_func in test_functions:
        try:
            result = test_func()
            test_results.append((test_name, result))
            if result:
                passed_tests += 1
        except Exception as e:
            print(f"💥 {test_name}测试出错: {e}")
            test_results.append((test_name, False))
    
    # 输出测试结果
    print(f"\n📊 测试结果总结:")
    print(f"✅ 通过: {passed_tests}")
    print(f"❌ 失败: {total_tests - passed_tests}")
    print(f"📊 总计: {total_tests}")
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f"🎉 测试通过率: {success_rate:.1f}%")
    
    # 评估系统状态
    if success_rate >= 80:
        print("🌟 系统状态：优秀")
        status = "excellent"
    elif success_rate >= 60:
        print("👍 系统状态：良好")
        status = "good"
    elif success_rate >= 40:
        print("⚠️ 系统状态：一般")
        status = "fair"
    else:
        print("❌ 系统状态：需要改进")
        status = "poor"
    
    # 生成JSON报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "test_results": dict(test_results),
        "summary": {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": success_rate,
            "status": status
        }
    }
    
    with open("tests/system_status_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 详细报告已保存到: tests/system_status_report.json")
    
    return success_rate >= 60


if __name__ == "__main__":
    print("🧪 开始PatentAgent系统状态测试...")
    success = generate_test_report()
    sys.exit(0 if success else 1) 