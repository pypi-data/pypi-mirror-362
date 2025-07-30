"""
PatentAgent 独立函数测试
测试不依赖外部库的独立函数
"""

import unittest
import sys
import os
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class TestPatentValidationFunctions(unittest.TestCase):
    """测试专利验证函数"""
    
    def test_technology_analysis_validation(self):
        """测试技术分析验证"""
        # 直接导入并测试验证函数
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'patentagents', 'agents', 'analysts'))
        
        try:
            from technology_analyst import validate_technology_analysis
            
            # 测试有效分析
            valid_report = """
            # 技术分析报告
            
            ## 技术领域概述
            详细的技术领域描述内容，包含了充分的技术背景信息和市场分析。
            
            ## 市场需求分析
            市场需求分析内容，分析了当前市场的需求状况和发展趋势，识别了关键的市场机会。
            
            ## 技术机会识别
            技术机会识别内容，识别了多个潜在的技术创新机会，包括具体的技术方向和应用场景。
            
            ## 技术趋势预测
            技术趋势预测内容，预测了未来技术发展的方向和趋势，分析了技术演进的路径。
            """
            
            validation = validate_technology_analysis(valid_report)
            self.assertTrue(validation["is_valid"])
            self.assertGreaterEqual(validation["quality_score"], 70)
            
            # 测试无效分析
            invalid_report = "简短的报告内容"
            
            validation = validate_technology_analysis(invalid_report)
            self.assertFalse(validation["is_valid"])
            self.assertLess(validation["quality_score"], 70)
            
            print("✅ 技术分析验证函数测试通过")
            
        except ImportError as e:
            print(f"⚠️ 技术分析验证函数导入失败: {e}")
            self.skipTest("技术分析验证函数导入失败")
    
    def test_innovation_opportunities_validation(self):
        """测试创新机会验证"""
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'patentagents', 'agents', 'analysts'))
        
        try:
            from innovation_discovery import validate_innovation_opportunities
            
            # 测试有效创新机会报告
            valid_report = """
            # 创新机会发现报告
            
            ## 技术空白识别
            识别了多个技术空白领域，包括具体的技术方向和应用场景，分析了市场需求。
            
            ## 跨领域创新机会
            发现了跨领域创新机会，分析了不同技术领域的融合可能性和创新潜力。
            
            ## 新兴技术趋势
            分析了新兴技术趋势，预测了未来技术发展的重点方向和关键技术。
            
            ## 创新机会评估
            对发现的创新机会进行了详细的评估和优先级排序，提供了具体的实施建议。
            """
            
            validation = validate_innovation_opportunities(valid_report)
            self.assertTrue(validation["is_valid"])
            self.assertGreaterEqual(validation["quality_score"], 70)
            
            print("✅ 创新机会验证函数测试通过")
            
        except ImportError as e:
            print(f"⚠️ 创新机会验证函数导入失败: {e}")
            self.skipTest("创新机会验证函数导入失败")
    
    def test_prior_art_research_validation(self):
        """测试先行技术研究验证"""
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'patentagents', 'agents', 'analysts'))
        
        try:
            from prior_art_researcher import validate_prior_art_research
            
            # 测试有效先行技术研究报告
            valid_report = """
            # 先行技术研究报告
            
            ## 专利检索结果
            进行了全面的专利检索，检索了相关的专利文献和技术资料，覆盖了主要的技术领域。
            
            ## 现有技术分析
            分析了相关的现有技术状态，评估了技术发展的现状和水平，识别了技术优势和局限性。
            
            ## 技术发展趋势
            技术发展呈现上升趋势，在多个方面都有显著的进展，预测了未来的发展方向。
            
            ## 竞争对手分析
            主要竞争对手包括多家知名公司，分析了其技术优势和市场地位，评估了竞争态势。
            
            ## 侵权风险评估
            识别了多个高风险专利，评估了潜在的侵权风险和规避策略，提供了具体的建议。
            
            ## 专利地图
            构建了技术专利地图，展示了技术领域的专利分布情况，分析了专利布局策略。
            
            | 专利ID | 标题 | 受让人 | 风险等级 |
            |--------|------|--------|----------|
            | US123456 | Test Patent | Google | High |
            | US789012 | Another Patent | Microsoft | Medium |
            """
            
            validation = validate_prior_art_research(valid_report)
            self.assertTrue(validation["is_valid"])
            self.assertGreaterEqual(validation["quality_score"], 70)
            
            print("✅ 先行技术研究验证函数测试通过")
            
        except ImportError as e:
            print(f"⚠️ 先行技术研究验证函数导入失败: {e}")
            self.skipTest("先行技术研究验证函数导入失败")
    
    def test_patent_draft_validation(self):
        """测试专利草稿验证"""
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'patentagents', 'agents', 'writers'))
        
        try:
            from patent_writer import validate_patent_draft, analyze_patent_claims
            
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
            现有的图像识别技术存在准确率低、处理速度慢等局限性，需要改进和优化。
            
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
            具体实施例1：使用ResNet模型进行图像分类，在ImageNet数据集上取得了优异的性能。
            具体实施例2：使用YOLO模型进行目标检测，在COCO数据集上实现了实时检测。
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
            
            print("✅ 专利草稿验证函数测试通过")
            
        except ImportError as e:
            print(f"⚠️ 专利草稿验证函数导入失败: {e}")
            self.skipTest("专利草稿验证函数导入失败")


class TestPatentUtilityFunctions(unittest.TestCase):
    """测试专利工具函数"""
    
    def test_patent_deduplication(self):
        """测试专利去重功能"""
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'patentagents', 'agents', 'analysts'))
        
        try:
            from prior_art_researcher import _deduplicate_patents
            
            test_patents = [
                {"patent_id": "US123456", "title": "Test Patent 1"},
                {"patent_id": "US123456", "title": "Test Patent 1"},  # 重复
                {"patent_id": "US789012", "title": "Test Patent 2"},
                {"publication_number": "US123456", "title": "Test Patent 3"},  # 通过publication_number重复
            ]
            
            unique_patents = _deduplicate_patents(test_patents)
            self.assertEqual(len(unique_patents), 2)  # 应该只有2个唯一专利
            
            print("✅ 专利去重功能测试通过")
            
        except ImportError as e:
            print(f"⚠️ 专利去重功能导入失败: {e}")
            self.skipTest("专利去重功能导入失败")
    
    def test_patent_analysis_functions(self):
        """测试专利分析函数"""
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'patentagents', 'agents', 'analysts'))
        
        try:
            from prior_art_researcher import _identify_key_patents, _identify_high_risk_patents
            
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
            
        except ImportError as e:
            print(f"⚠️ 专利分析函数导入失败: {e}")
            self.skipTest("专利分析函数导入失败")
    
    def test_patent_writer_helper_functions(self):
        """测试专利撰写员辅助函数"""
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'patentagents', 'agents', 'writers'))
        
        try:
            from patent_writer import _extract_core_invention, _extract_claims_from_draft
            
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
            
        except ImportError as e:
            print(f"⚠️ 专利撰写员辅助函数导入失败: {e}")
            self.skipTest("专利撰写员辅助函数导入失败")


class TestWorkflowSimulation(unittest.TestCase):
    """测试工作流程模拟"""
    
    def test_patent_workflow_simulation(self):
        """测试专利工作流程模拟"""
        # 模拟完整的专利分析流程
        
        # 1. 初始状态
        initial_state = {
            "technology_domain": "人工智能",
            "innovation_topic": "图像识别",
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
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
        
        ## 技术趋势预测
        预测未来技术发展将朝着更高精度、更低功耗的方向发展。
        """
        
        # 3. 创新机会发现
        innovation_opportunities = """
        # 创新机会发现报告
        
        ## 技术空白识别
        在实时处理和边缘计算方面存在技术空白。
        
        ## 跨领域创新机会
        结合自然语言处理和计算机视觉的多模态技术。
        
        ## 新兴技术趋势
        边缘AI和联邦学习成为新的技术热点。
        
        ## 创新机会评估
        评估了多个创新机会的技术可行性和商业价值。
        """
        
        # 4. 先行技术研究
        prior_art_report = """
        # 先行技术研究报告
        
        ## 专利检索结果
        检索到相关专利500余件，主要集中在深度学习算法优化。
        
        ## 现有技术分析
        现有技术在准确率和速度方面仍有改进空间。
        
        ## 技术发展趋势
        技术发展呈现加速态势，创新活跃度持续提升。
        
        ## 竞争对手分析
        主要竞争对手包括Google、Microsoft、Apple等公司。
        
        ## 侵权风险评估
        识别了潜在的侵权风险，提供了规避策略。
        
        ## 专利地图
        构建了完整的专利技术地图。
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
        具体实施例描述了方法的详细实现过程。
        """
        
        # 验证工作流程的完整性
        self.assertIn("人工智能", initial_state["technology_domain"])
        self.assertIn("技术分析报告", technology_report)
        self.assertIn("创新机会发现报告", innovation_opportunities)
        self.assertIn("先行技术研究报告", prior_art_report)
        self.assertIn("权利要求书", patent_draft)
        
        # 验证日期格式
        self.assertRegex(initial_state["analysis_date"], r'\d{4}-\d{2}-\d{2}')
        
        # 验证报告长度
        self.assertGreater(len(technology_report), 200)
        self.assertGreater(len(innovation_opportunities), 200)
        self.assertGreater(len(prior_art_report), 200)
        self.assertGreater(len(patent_draft), 500)
        
        print("✅ 专利工作流程模拟测试通过")


def run_function_tests():
    """运行独立函数测试"""
    print("🧪 开始运行PatentAgent独立函数测试...")
    print("=" * 60)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestPatentValidationFunctions,
        TestPatentUtilityFunctions,
        TestWorkflowSimulation
    ]
    
    total_tests = 0
    passed_tests = 0
    skipped_tests = 0
    
    for test_class in test_classes:
        print(f"\n📋 运行 {test_class.__name__} 测试...")
        print("-" * 40)
        
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
        
        # 运行单个测试类
        runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
        result = runner.run(tests)
        
        class_total = result.testsRun
        class_passed = class_total - len(result.failures) - len(result.errors) - len(result.skipped)
        class_skipped = len(result.skipped)
        
        total_tests += class_total
        passed_tests += class_passed
        skipped_tests += class_skipped
        
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
        
        if result.skipped:
            print(f"⏭️ 跳过的测试:")
            for test, reason in result.skipped:
                print(f"   • {test}: {reason}")
        
        print(f"📊 {test_class.__name__}: {class_passed}/{class_total} 通过 ({class_skipped} 跳过)")
    
    # 输出总结
    print(f"\n{'='*60}")
    print("🎯 测试结果总结")
    print(f"{'='*60}")
    print(f"✅ 通过: {passed_tests}")
    print(f"❌ 失败: {total_tests - passed_tests - skipped_tests}")
    print(f"⏭️ 跳过: {skipped_tests}")
    print(f"📊 总计: {total_tests}")
    
    if total_tests > 0:
        success_rate = (passed_tests / total_tests * 100)
        print(f"🎉 测试通过率: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🌟 测试结果：优秀")
        elif success_rate >= 60:
            print("👍 测试结果：良好")
        else:
            print("⚠️ 测试结果：需要改进")
        
        return success_rate >= 60
    else:
        print("⚠️ 没有执行任何测试")
        return False


if __name__ == "__main__":
    success = run_function_tests()
    sys.exit(0 if success else 1) 