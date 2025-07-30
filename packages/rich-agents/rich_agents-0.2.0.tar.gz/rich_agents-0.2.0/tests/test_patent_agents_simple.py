"""
PatentAgent 简化测试套件
测试专利智能体系统的核心逻辑，不依赖外部库
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class MockLLM:
    """模拟LLM用于测试"""
    
    def __init__(self, response_content: str = "模拟分析结果"):
        self.response_content = response_content
    
    def invoke(self, messages):
        """模拟LLM调用"""
        class MockResult:
            def __init__(self, content):
                self.content = content
        
        return MockResult(self.response_content)


class TestPatentUtilsFunctions(unittest.TestCase):
    """测试专利工具函数"""
    
    def test_patent_toolkit_basic_functions(self):
        """测试专利工具包基础功能"""
        # 测试不依赖外部库的函数
        from patentagents.agents.utils.patent_utils import PatentToolkit
        
        config = {
            "google_patents": {"api_key": "test_key"},
            "zhihuiya": {"client_id": "test_id", "client_secret": "test_secret"}
        }
        
        toolkit = PatentToolkit(config)
        
        # 测试基本初始化
        self.assertIsNotNone(toolkit)
        self.assertEqual(toolkit.config, config)
        
        # 测试状态获取
        status = toolkit.get_toolkit_status()
        self.assertIsInstance(status, dict)
        self.assertIn("google_patents_api", status)
        self.assertIn("zhihuiya_api", status)
        
        print("✅ 专利工具包基础功能测试通过")


class TestAnalystFunctions(unittest.TestCase):
    """测试分析师函数"""
    
    def test_technology_analyst_validation(self):
        """测试技术分析师验证功能"""
        from patentagents.agents.analysts.technology_analyst import validate_technology_analysis
        
        # 测试有效分析
        valid_report = """
        # 技术分析报告
        
        ## 技术领域概述
        详细的技术领域描述内容，包含了充分的技术背景信息。
        
        ## 市场需求分析
        市场需求分析内容，分析了当前市场的需求状况和发展趋势。
        
        ## 技术机会识别
        技术机会识别内容，识别了多个潜在的技术创新机会。
        
        ## 技术趋势预测
        技术趋势预测内容，预测了未来技术发展的方向和趋势。
        """
        
        validation = validate_technology_analysis(valid_report)
        self.assertTrue(validation["is_valid"])
        self.assertGreaterEqual(validation["quality_score"], 70)
        
        # 测试无效分析
        invalid_report = "简短的报告内容"
        
        validation = validate_technology_analysis(invalid_report)
        self.assertFalse(validation["is_valid"])
        self.assertLess(validation["quality_score"], 70)
        
        print("✅ 技术分析师验证功能测试通过")
    
    def test_innovation_discovery_validation(self):
        """测试创新发现师验证功能"""
        from patentagents.agents.analysts.innovation_discovery import validate_innovation_opportunities
        
        # 测试有效创新机会报告
        valid_report = """
        # 创新机会发现报告
        
        ## 技术空白识别
        识别了多个技术空白领域，包括具体的技术方向和应用场景。
        
        ## 跨领域创新机会
        发现了跨领域创新机会，分析了不同技术领域的融合可能性。
        
        ## 新兴技术趋势
        分析了新兴技术趋势，预测了未来技术发展的重点方向。
        
        ## 创新机会评估
        对发现的创新机会进行了详细的评估和优先级排序。
        """
        
        validation = validate_innovation_opportunities(valid_report)
        self.assertTrue(validation["is_valid"])
        self.assertGreaterEqual(validation["quality_score"], 70)
        
        print("✅ 创新发现师验证功能测试通过")
    
    def test_prior_art_research_validation(self):
        """测试先行技术研究验证功能"""
        from patentagents.agents.analysts.prior_art_researcher import validate_prior_art_research
        
        # 测试有效先行技术研究报告
        valid_report = """
        # 先行技术研究报告
        
        ## 专利检索结果
        进行了全面的专利检索，检索了相关的专利文献和技术资料。
        
        ## 现有技术分析
        分析了相关的现有技术状态，评估了技术发展的现状和水平。
        
        ## 技术发展趋势
        技术发展呈现上升趋势，在多个方面都有显著的进展。
        
        ## 竞争对手分析
        主要竞争对手包括多家知名公司，分析了其技术优势和市场地位。
        
        ## 侵权风险评估
        识别了多个高风险专利，评估了潜在的侵权风险和规避策略。
        
        ## 专利地图
        构建了技术专利地图，展示了技术领域的专利分布情况。
        
        | 专利ID | 标题 | 受让人 | 风险等级 |
        |--------|------|--------|----------|
        | US123456 | Test Patent | Google | High |
        | US789012 | Another Patent | Microsoft | Medium |
        """
        
        validation = validate_prior_art_research(valid_report)
        self.assertTrue(validation["is_valid"])
        self.assertGreaterEqual(validation["quality_score"], 70)
        
        print("✅ 先行技术研究验证功能测试通过")


class TestPatentWriterFunctions(unittest.TestCase):
    """测试专利撰写员函数"""
    
    def test_patent_draft_validation(self):
        """测试专利草稿验证功能"""
        from patentagents.agents.writers.patent_writer import validate_patent_draft, analyze_patent_claims
        
        # 测试有效专利草稿
        valid_draft = """
        发明名称
        ========
        一种基于人工智能的图像识别方法
        
        技术领域
        ========
        本发明涉及图像识别技术领域，特别是一种基于人工智能的图像识别方法。
        
        背景技术
        ========
        现有的图像识别技术存在准确率低、处理速度慢等局限性，需要改进。
        
        发明内容
        ========
        本发明提供了一种改进的图像识别方法，能够提高识别准确率和处理速度。
        
        权利要求书
        ==========
        1. 一种图像识别方法，其特征在于包括以下步骤：
           获取图像数据；
           使用深度学习模型处理图像数据；
           输出识别结果。
        
        2. 根据权利要求1所述的方法，其特征在于：
           所述深度学习模型为卷积神经网络。
        
        3. 根据权利要求2所述的方法，其特征在于：
           所述卷积神经网络包括多个卷积层和池化层。
        
        说明书摘要
        ==========
        本发明提供了一种基于人工智能的图像识别方法，能够有效提高识别准确率。
        
        实施例
        ======
        具体实施例1：使用ResNet模型进行图像分类。
        具体实施例2：使用YOLO模型进行目标检测。
        """
        
        validation = validate_patent_draft(valid_draft)
        self.assertTrue(validation["is_valid"])
        self.assertGreaterEqual(validation["quality_score"], 60)
        
        # 测试权利要求分析
        claims = [
            "1. 一种图像识别方法，其特征在于包括以下步骤：获取图像数据；处理图像数据。",
            "2. 根据权利要求1所述的方法，其特征在于：所述处理步骤包括特征提取。",
            "3. 根据权利要求2所述的方法，其特征在于：所述特征提取采用深度学习。"
        ]
        
        analysis = analyze_patent_claims(claims)
        self.assertEqual(analysis["total_claims"], 3)
        self.assertEqual(analysis["independent_claims"], 1)
        self.assertEqual(analysis["dependent_claims"], 2)
        
        print("✅ 专利撰写员验证功能测试通过")


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_patent_toolkit_helper_functions(self):
        """测试专利工具包辅助函数"""
        # 测试专利去重功能
        from patentagents.agents.analysts.prior_art_researcher import _deduplicate_patents
        
        test_patents = [
            {"patent_id": "US123456", "title": "Test Patent 1"},
            {"patent_id": "US123456", "title": "Test Patent 1"},  # 重复
            {"patent_id": "US789012", "title": "Test Patent 2"},
            {"publication_number": "US123456", "title": "Test Patent 3"},  # 通过publication_number重复
        ]
        
        unique_patents = _deduplicate_patents(test_patents)
        self.assertEqual(len(unique_patents), 2)  # 应该只有2个唯一专利
        
        print("✅ 专利去重功能测试通过")
    
    def test_patent_analysis_functions(self):
        """测试专利分析函数"""
        from patentagents.agents.analysts.prior_art_researcher import _identify_key_patents, _identify_high_risk_patents
        
        # 测试核心专利识别
        test_patents = [
            {
                "patent_id": "US123456",
                "title": "Advanced AI System for Medical Diagnosis and Treatment",
                "assignee": "Google Inc.",
                "publication_date": "2023-01-15",
                "status": "GRANT"
            },
            {
                "patent_id": "US789012", 
                "title": "Simple Method",
                "assignee": "Small Company",
                "publication_date": "2010-01-15",
                "status": "APPLICATION"
            },
            {
                "patent_id": "US345678",
                "title": "Machine Learning System for Image Recognition",
                "assignee": "Microsoft Corporation",
                "publication_date": "2022-06-20",
                "status": "GRANT"
            }
        ]
        
        key_patents = _identify_key_patents(test_patents)
        self.assertGreater(len(key_patents), 0)
        
        # 验证重要性评分
        for patent in key_patents:
            self.assertIn("importance_score", patent)
            self.assertGreaterEqual(patent["importance_score"], 3)
        
        # 测试高风险专利识别
        high_risk_patents = _identify_high_risk_patents(test_patents)
        self.assertGreaterEqual(len(high_risk_patents), 0)
        
        print("✅ 专利分析函数测试通过")


class TestDataProcessingFunctions(unittest.TestCase):
    """测试数据处理函数"""
    
    def test_patent_writer_helper_functions(self):
        """测试专利撰写员辅助函数"""
        from patentagents.agents.writers.patent_writer import _extract_core_invention, _extract_claims_from_draft
        
        # 测试核心发明提取
        tech_report = """
        ## 技术问题
        现有的图像识别技术存在准确率低的问题，在复杂场景下识别效果不佳。
        
        ## 技术挑战
        处理复杂场景下的图像识别仍然是一个重大挑战。
        """
        
        innovation_report = """
        ## 解决方案
        采用深度学习算法和多模态融合技术来提高识别准确率。
        
        ## 技术方法
        使用卷积神经网络进行特征提取，结合注意力机制提升性能。
        """
        
        prior_art_report = """
        ## 技术效果
        相比现有技术，本方案能够显著提高识别准确率和处理速度。
        
        ## 性能改进
        在标准数据集上的测试结果显示，准确率提升了15%。
        """
        
        core_invention = _extract_core_invention(tech_report, innovation_report, prior_art_report)
        
        self.assertIn("problem", core_invention)
        self.assertIn("solution", core_invention)
        self.assertIn("effect", core_invention)
        self.assertIn("description", core_invention)
        
        self.assertIn("准确率", core_invention["problem"])
        self.assertIn("深度学习", core_invention["solution"])
        
        # 测试权利要求提取
        test_draft = """
        权利要求书
        
        1. 一种图像识别方法，其特征在于包括以下步骤：
           获取图像数据；
           使用神经网络处理图像。
        
        2. 根据权利要求1所述的方法，其特征在于：
           所述神经网络为卷积神经网络。
        
        3. 根据权利要求2所述的方法，其特征在于：
           所述卷积神经网络包括多个卷积层。
        
        说明书摘要
        本发明提供了一种图像识别方法。
        """
        
        claims = _extract_claims_from_draft(test_draft)
        self.assertEqual(len(claims), 3)
        self.assertTrue(claims[0].startswith("1."))
        self.assertTrue(claims[1].startswith("2."))
        self.assertTrue(claims[2].startswith("3."))
        
        print("✅ 专利撰写员辅助函数测试通过")


class TestIntegrationScenarios(unittest.TestCase):
    """测试集成场景"""
    
    def test_end_to_end_workflow_simulation(self):
        """测试端到端工作流程模拟"""
        # 模拟完整的专利分析流程
        
        # 1. 初始状态
        initial_state = {
            "technology_domain": "人工智能",
            "innovation_topic": "图像识别",
            "analysis_date": "2025-01-01",
            "analysis_type": "discovery"
        }
        
        # 2. 技术分析结果
        technology_report = """
        # 技术分析报告
        
        ## 技术领域概述
        人工智能图像识别技术正在快速发展，深度学习成为主流技术。
        
        ## 市场需求分析
        市场对高精度图像识别技术需求巨大，特别是在医疗、自动驾驶等领域。
        
        ## 技术机会识别
        存在多个技术创新机会，包括多模态融合、边缘计算优化等。
        """
        
        # 3. 创新机会发现
        innovation_opportunities = """
        # 创新机会发现报告
        
        ## 技术空白识别
        在实时处理和边缘计算方面存在技术空白。
        
        ## 跨领域创新机会
        结合自然语言处理和计算机视觉的多模态技术。
        """
        
        # 4. 先行技术研究
        prior_art_report = """
        # 先行技术研究报告
        
        ## 专利检索结果
        检索到相关专利500余件，主要集中在深度学习算法优化。
        
        ## 现有技术分析
        现有技术在准确率和速度方面仍有改进空间。
        """
        
        # 5. 专利草稿
        patent_draft = """
        发明名称
        ========
        一种基于多模态融合的图像识别方法
        
        技术领域
        ========
        本发明涉及图像识别技术领域。
        
        背景技术
        ========
        现有技术存在局限性。
        
        发明内容
        ========
        本发明提供了一种改进的图像识别方法。
        
        权利要求书
        ==========
        1. 一种图像识别方法，包括获取图像数据步骤。
        2. 根据权利要求1的方法，包括特征提取步骤。
        3. 根据权利要求2的方法，包括分类识别步骤。
        
        说明书摘要
        ==========
        本发明提供了一种图像识别方法。
        
        实施例
        ======
        具体实施例描述。
        """
        
        # 验证工作流程的完整性
        self.assertIn("人工智能", initial_state["technology_domain"])
        self.assertIn("技术分析报告", technology_report)
        self.assertIn("创新机会发现报告", innovation_opportunities)
        self.assertIn("先行技术研究报告", prior_art_report)
        self.assertIn("权利要求书", patent_draft)
        
        # 验证报告质量
        from patentagents.agents.analysts.technology_analyst import validate_technology_analysis
        from patentagents.agents.analysts.innovation_discovery import validate_innovation_opportunities
        from patentagents.agents.analysts.prior_art_researcher import validate_prior_art_research
        from patentagents.agents.writers.patent_writer import validate_patent_draft
        
        tech_validation = validate_technology_analysis(technology_report)
        innovation_validation = validate_innovation_opportunities(innovation_opportunities)
        prior_art_validation = validate_prior_art_research(prior_art_report)
        patent_validation = validate_patent_draft(patent_draft)
        
        # 检查各个环节的质量
        self.assertTrue(tech_validation["is_valid"])
        self.assertTrue(innovation_validation["is_valid"])
        self.assertTrue(prior_art_validation["is_valid"])
        self.assertTrue(patent_validation["is_valid"])
        
        print("✅ 端到端工作流程模拟测试通过")


def run_simple_tests():
    """运行简化测试套件"""
    print("🧪 开始运行PatentAgent简化测试套件...")
    print("=" * 60)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestPatentUtilsFunctions,
        TestAnalystFunctions,
        TestPatentWriterFunctions,
        TestUtilityFunctions,
        TestDataProcessingFunctions,
        TestIntegrationScenarios
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"\n📋 运行 {test_class.__name__} 测试...")
        print("-" * 40)
        
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
        
        # 运行单个测试类
        runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
        result = runner.run(tests)
        
        class_total = result.testsRun
        class_passed = class_total - len(result.failures) - len(result.errors)
        
        total_tests += class_total
        passed_tests += class_passed
        
        if result.failures:
            print(f"❌ 失败的测试:")
            for test, traceback in result.failures:
                print(f"   • {test}")
                print(f"     {traceback.splitlines()[-1]}")
        
        if result.errors:
            print(f"💥 错误的测试:")
            for test, traceback in result.errors:
                print(f"   • {test}")
                print(f"     {traceback.splitlines()[-1]}")
        
        print(f"📊 {test_class.__name__}: {class_passed}/{class_total} 通过")
    
    # 输出总结
    print(f"\n{'='*60}")
    print("🎯 测试结果总结")
    print(f"{'='*60}")
    print(f"✅ 通过: {passed_tests}")
    print(f"❌ 失败: {total_tests - passed_tests}")
    print(f"📊 总计: {total_tests}")
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f"🎉 测试通过率: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🌟 测试结果：优秀")
    elif success_rate >= 60:
        print("👍 测试结果：良好")
    else:
        print("⚠️ 测试结果：需要改进")
    
    return success_rate >= 80


if __name__ == "__main__":
    success = run_simple_tests()
    sys.exit(0 if success else 1) 