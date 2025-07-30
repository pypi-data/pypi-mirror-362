"""
PatentAgent 综合测试套件
测试专利智能体系统的各个组件
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from patentagents.agents.utils.patent_states import (
    PatentState, create_initial_patent_state, validate_patent_state
)
from patentagents.agents.utils.patent_utils import PatentToolkit
from patentagents.agents.analysts.technology_analyst import (
    create_technology_analyst, validate_technology_analysis
)
from patentagents.agents.analysts.innovation_discovery import (
    create_innovation_discovery_analyst, validate_innovation_opportunities
)
from patentagents.agents.analysts.prior_art_researcher import (
    create_prior_art_researcher, validate_prior_art_research
)
from patentagents.agents.writers.patent_writer import (
    create_patent_writer, validate_patent_draft
)
from patentagents.graph.patent_graph import PatentAgentsGraph, create_patent_agents_graph


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


class TestPatentStates(unittest.TestCase):
    """测试专利状态管理"""
    
    def test_create_initial_patent_state(self):
        """测试创建初始专利状态"""
        state = create_initial_patent_state(
            technology_domain="人工智能",
            innovation_topic="图像识别",
            analysis_type="discovery"
        )
        
        self.assertEqual(state["technology_domain"], "人工智能")
        self.assertEqual(state["innovation_topic"], "图像识别")
        self.assertEqual(state["analysis_type"], "discovery")
        self.assertIsNotNone(state["analysis_date"])
    
    def test_validate_patent_state(self):
        """测试专利状态验证"""
        # 测试有效状态
        valid_state = {
            "technology_domain": "人工智能",
            "innovation_topic": "图像识别",
            "analysis_date": "2025-01-01",
            "analysis_type": "discovery"
        }
        
        validation = validate_patent_state(valid_state)
        self.assertTrue(validation["is_valid"])
        
        # 测试无效状态
        invalid_state = {
            "technology_domain": "",
            "innovation_topic": "图像识别"
        }
        
        validation = validate_patent_state(invalid_state)
        self.assertFalse(validation["is_valid"])
        self.assertIn("缺少必需字段", validation["errors"])


class TestPatentToolkit(unittest.TestCase):
    """测试专利工具包"""
    
    def setUp(self):
        """设置测试环境"""
        self.config = {
            "google_patents": {"api_key": "test_key"},
            "zhihuiya": {"client_id": "test_id", "client_secret": "test_secret"}
        }
        self.toolkit = PatentToolkit(self.config)
    
    def test_toolkit_initialization(self):
        """测试工具包初始化"""
        self.assertIsNotNone(self.toolkit)
        self.assertEqual(self.toolkit.config, self.config)
    
    def test_get_toolkit_status(self):
        """测试获取工具包状态"""
        status = self.toolkit.get_toolkit_status()
        
        self.assertIn("google_patents_api", status)
        self.assertIn("zhihuiya_api", status)
        self.assertIn("toolkit_methods", status)
        self.assertIsInstance(status["toolkit_methods"], int)
        self.assertGreater(status["toolkit_methods"], 0)
    
    @patch('patentagents.dataflows.google_patents_utils.GooglePatentsAPI')
    def test_search_google_patents(self, mock_google_api):
        """测试Google Patents搜索"""
        # 模拟API响应
        mock_api_instance = Mock()
        mock_api_instance.search_patents.return_value = {
            "patents": [
                {"patent_id": "US123456", "title": "Test Patent"}
            ],
            "total_results": 1
        }
        mock_google_api.return_value = mock_api_instance
        
        # 测试搜索
        result = self.toolkit.search_google_patents("test query")
        
        self.assertIn("patents", result)
        self.assertEqual(len(result["patents"]), 1)
        self.assertEqual(result["patents"][0]["patent_id"], "US123456")


class TestTechnologyAnalyst(unittest.TestCase):
    """测试技术分析师"""
    
    def setUp(self):
        """设置测试环境"""
        self.mock_llm = MockLLM("""
        # 技术分析报告
        
        ## 技术领域概述
        人工智能图像识别技术正在快速发展。
        
        ## 市场需求分析
        市场对图像识别技术需求巨大。
        
        ## 技术机会识别
        存在多个技术创新机会。
        """)
        
        self.toolkit = PatentToolkit({})
        self.analyst = create_technology_analyst(self.mock_llm, self.toolkit)
    
    def test_technology_analyst_creation(self):
        """测试技术分析师创建"""
        self.assertIsNotNone(self.analyst)
        self.assertTrue(callable(self.analyst))
    
    def test_technology_analyst_execution(self):
        """测试技术分析师执行"""
        test_state = {
            "technology_domain": "人工智能",
            "innovation_topic": "图像识别",
            "analysis_date": "2025-01-01"
        }
        
        result = self.analyst(test_state)
        
        self.assertIn("technology_report", result)
        self.assertIn("sender", result)
        self.assertEqual(result["sender"], "Technology Analyst")
        self.assertIn("技术分析报告", result["technology_report"])
    
    def test_validate_technology_analysis(self):
        """测试技术分析验证"""
        # 测试有效分析
        valid_report = """
        # 技术分析报告
        
        ## 技术领域概述
        详细的技术领域描述
        
        ## 市场需求分析
        市场需求分析内容
        
        ## 技术机会识别
        技术机会识别内容
        
        ## 技术趋势预测
        技术趋势预测内容
        """
        
        validation = validate_technology_analysis(valid_report)
        self.assertTrue(validation["is_valid"])
        self.assertGreaterEqual(validation["quality_score"], 70)
        
        # 测试无效分析
        invalid_report = "简短的报告"
        
        validation = validate_technology_analysis(invalid_report)
        self.assertFalse(validation["is_valid"])
        self.assertLess(validation["quality_score"], 70)


class TestInnovationDiscoveryAnalyst(unittest.TestCase):
    """测试创新发现师"""
    
    def setUp(self):
        """设置测试环境"""
        self.mock_llm = MockLLM("""
        # 创新发现报告
        
        ## 技术空白识别
        识别了多个技术空白领域。
        
        ## 跨领域创新机会
        发现了跨领域创新机会。
        
        ## 新兴技术趋势
        分析了新兴技术趋势。
        """)
        
        self.toolkit = PatentToolkit({})
        self.analyst = create_innovation_discovery_analyst(self.mock_llm, self.toolkit)
    
    def test_innovation_discovery_execution(self):
        """测试创新发现师执行"""
        test_state = {
            "technology_domain": "人工智能",
            "innovation_topic": "图像识别",
            "analysis_date": "2025-01-01",
            "technology_report": "技术分析背景"
        }
        
        result = self.analyst(test_state)
        
        self.assertIn("innovation_opportunities", result)
        self.assertIn("sender", result)
        self.assertEqual(result["sender"], "Innovation Discovery Analyst")
        self.assertIn("创新发现报告", result["innovation_opportunities"])


class TestPriorArtResearcher(unittest.TestCase):
    """测试先行技术研究员"""
    
    def setUp(self):
        """设置测试环境"""
        self.mock_llm = MockLLM("""
        # 先行技术研究报告
        
        ## 专利检索结果
        检索了相关专利文献。
        
        ## 现有技术分析
        分析了现有技术状态。
        
        ## 侵权风险评估
        评估了侵权风险。
        """)
        
        self.toolkit = PatentToolkit({})
        self.researcher = create_prior_art_researcher(self.mock_llm, self.toolkit)
    
    def test_prior_art_researcher_execution(self):
        """测试先行技术研究员执行"""
        test_state = {
            "technology_domain": "人工智能",
            "innovation_topic": "图像识别",
            "analysis_date": "2025-01-01",
            "technology_report": "技术分析背景",
            "innovation_opportunities": "创新机会背景"
        }
        
        result = self.researcher(test_state)
        
        self.assertIn("prior_art_report", result)
        self.assertIn("sender", result)
        self.assertEqual(result["sender"], "Prior Art Researcher")
        self.assertIn("先行技术研究报告", result["prior_art_report"])


class TestPatentWriter(unittest.TestCase):
    """测试专利撰写员"""
    
    def setUp(self):
        """设置测试环境"""
        self.mock_llm = MockLLM("""
        # 专利申请文档
        
        发明名称
        ========
        一种图像识别方法
        
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
        1. 一种图像识别方法，其特征在于包括以下步骤：
           获取图像数据；
           处理图像数据。
        
        2. 根据权利要求1所述的方法，其特征在于：
           所述处理步骤包括特征提取。
        
        说明书摘要
        ==========
        本发明提供了一种图像识别方法。
        """)
        
        self.toolkit = PatentToolkit({})
        self.writer = create_patent_writer(self.mock_llm, self.toolkit)
    
    def test_patent_writer_execution(self):
        """测试专利撰写员执行"""
        test_state = {
            "technology_domain": "人工智能",
            "innovation_topic": "图像识别",
            "analysis_date": "2025-01-01",
            "technology_report": "技术分析背景",
            "innovation_opportunities": "创新机会背景",
            "prior_art_report": "先行技术背景"
        }
        
        result = self.writer(test_state)
        
        self.assertIn("patent_draft", result)
        self.assertIn("sender", result)
        self.assertEqual(result["sender"], "Patent Writer")
        self.assertIn("专利申请文档", result["patent_draft"])
    
    def test_validate_patent_draft(self):
        """测试专利草稿验证"""
        # 测试有效草稿
        valid_draft = """
        发明名称
        ========
        一种图像识别方法
        
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
        1. 一种图像识别方法，其特征在于包括以下步骤：
           获取图像数据；
           处理图像数据。
        
        2. 根据权利要求1所述的方法，其特征在于：
           所述处理步骤包括特征提取。
        
        3. 根据权利要求2所述的方法，其特征在于：
           所述特征提取采用深度学习。
        
        说明书摘要
        ==========
        本发明提供了一种图像识别方法。
        
        实施例
        ======
        具体实施例描述。
        """
        
        validation = validate_patent_draft(valid_draft)
        self.assertTrue(validation["is_valid"])
        self.assertGreaterEqual(validation["quality_score"], 60)
        
        # 测试无效草稿
        invalid_draft = "简短的专利草稿"
        
        validation = validate_patent_draft(invalid_draft)
        self.assertFalse(validation["is_valid"])
        self.assertLess(validation["quality_score"], 60)


class TestPatentAgentsGraph(unittest.TestCase):
    """测试专利智能体图"""
    
    def setUp(self):
        """设置测试环境"""
        self.mock_llm = MockLLM("综合分析结果")
        self.config = {"test": "config"}
        self.graph = PatentAgentsGraph(self.mock_llm, self.config)
    
    def test_graph_initialization(self):
        """测试智能体图初始化"""
        self.assertIsNotNone(self.graph)
        self.assertEqual(self.graph.llm, self.mock_llm)
        self.assertEqual(self.graph.config, self.config)
        self.assertIsNotNone(self.graph.toolkit)
        self.assertIsNotNone(self.graph.technology_analyst)
        self.assertIsNotNone(self.graph.innovation_discovery)
        self.assertIsNotNone(self.graph.prior_art_researcher)
        self.assertIsNotNone(self.graph.patent_writer)
    
    def test_get_workflow_status(self):
        """测试获取工作流程状态"""
        status = self.graph.get_workflow_status()
        
        self.assertIn("available_agents", status)
        self.assertIn("workflow_nodes", status)
        self.assertIn("configuration", status)
        
        self.assertEqual(len(status["available_agents"]), 4)
        self.assertEqual(len(status["workflow_nodes"]), 7)
        self.assertEqual(status["configuration"], self.config)
    
    def test_check_analysis_completeness(self):
        """测试分析完整性检查"""
        # 测试完整状态
        complete_state = {
            "technology_report": "详细的技术分析报告" * 50,
            "innovation_opportunities": "详细的创新机会报告" * 50,
            "prior_art_report": "详细的先行技术报告" * 50,
            "patent_search_results": [{"patent_id": "US123456"}]
        }
        
        completeness = self.graph._check_analysis_completeness(complete_state)
        self.assertGreaterEqual(completeness["score"], 80)
        self.assertEqual(completeness["decision"], "proceed")
        
        # 测试不完整状态
        incomplete_state = {
            "technology_report": "短报告"
        }
        
        completeness = self.graph._check_analysis_completeness(incomplete_state)
        self.assertLess(completeness["score"], 60)
        self.assertEqual(completeness["decision"], "continue")
    
    def test_assess_patent_quality(self):
        """测试专利质量评估"""
        # 测试高质量专利
        high_quality_state = {
            "patent_draft": """
            发明名称
            ========
            一种图像识别方法
            
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
            1. 一种图像识别方法。
            2. 根据权利要求1的方法。
            3. 根据权利要求2的方法。
            
            实施例
            ======
            具体实施例描述。
            """ * 10,
            "patent_claims": ["权利要求1", "权利要求2", "权利要求3"]
        }
        
        quality = self.graph._assess_patent_quality(high_quality_state)
        self.assertGreaterEqual(quality["score"], 60)
        self.assertIn("approve", ["approve", "review"])
        
        # 测试低质量专利
        low_quality_state = {
            "patent_draft": "简短的专利草稿",
            "patent_claims": []
        }
        
        quality = self.graph._assess_patent_quality(low_quality_state)
        self.assertLess(quality["score"], 60)
        self.assertEqual(quality["decision"], "revise")


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.mock_llm = MockLLM("集成测试结果")
        self.config = {"integration": "test"}
    
    def test_create_patent_agents_graph(self):
        """测试创建专利智能体图"""
        graph = create_patent_agents_graph(self.mock_llm, self.config)
        
        self.assertIsInstance(graph, PatentAgentsGraph)
        self.assertEqual(graph.llm, self.mock_llm)
        self.assertEqual(graph.config, self.config)
    
    @patch('patentagents.graph.patent_graph.PatentToolkit')
    def test_end_to_end_workflow(self, mock_toolkit):
        """测试端到端工作流程"""
        # 模拟工具包
        mock_toolkit_instance = Mock()
        mock_toolkit_instance.get_toolkit_status.return_value = {"status": "ok"}
        mock_toolkit_instance.validate_patent_format.return_value = {"is_valid": True}
        mock_toolkit.return_value = mock_toolkit_instance
        
        # 创建智能体图
        graph = create_patent_agents_graph(self.mock_llm, self.config)
        
        # 测试状态获取
        status = graph.get_workflow_status()
        self.assertIn("available_agents", status)
        
        # 测试分析完整性检查
        test_state = {
            "technology_report": "详细报告" * 100,
            "innovation_opportunities": "详细机会" * 100,
            "prior_art_report": "详细先行技术" * 100,
            "patent_search_results": [{"patent_id": "US123456"}]
        }
        
        completeness = graph._check_analysis_completeness(test_state)
        self.assertGreaterEqual(completeness["score"], 80)


def run_all_tests():
    """运行所有测试"""
    print("🧪 开始运行PatentAgent测试套件...")
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestPatentStates,
        TestPatentToolkit,
        TestTechnologyAnalyst,
        TestInnovationDiscoveryAnalyst,
        TestPriorArtResearcher,
        TestPatentWriter,
        TestPatentAgentsGraph,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出结果统计
    print(f"\n{'='*60}")
    print("🎯 测试结果统计")
    print(f"{'='*60}")
    print(f"✅ 成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ 失败: {len(result.failures)}")
    print(f"💥 错误: {len(result.errors)}")
    print(f"📊 总计: {result.testsRun}")
    
    if result.failures:
        print(f"\n❌ 失败的测试:")
        for test, traceback in result.failures:
            print(f"   • {test}: {traceback.splitlines()[-1]}")
    
    if result.errors:
        print(f"\n💥 错误的测试:")
        for test, traceback in result.errors:
            print(f"   • {test}: {traceback.splitlines()[-1]}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\n🎉 测试通过率: {success_rate:.1f}%")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 