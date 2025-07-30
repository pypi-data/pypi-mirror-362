"""
Rich-Agents 基础功能测试
测试配置管理器、LLM适配器等核心组件
"""

import os
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# 导入待测试的模块
from shared.config.rich_agents_config_manager import RichAgentsConfigManager
from shared.llm_adapters.unified_llm_adapter import UnifiedLLMAdapter, LLMAdapterFactory


class TestRichAgentsConfigManager:
    """测试RichAgentsConfigManager"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        # 创建临时目录用于测试
        self.temp_dir = tempfile.mkdtemp()
        self.config_manager = RichAgentsConfigManager(self.temp_dir)
    
    def test_config_manager_initialization(self):
        """测试配置管理器初始化"""
        assert self.config_manager is not None
        assert self.config_manager.config_dir.exists()
        assert self.config_manager.main_config is not None
        assert self.config_manager.trading_config is not None
        assert self.config_manager.patent_config is not None
    
    def test_get_trading_config(self):
        """测试获取TradingAgent配置"""
        config = self.config_manager.get_trading_config()
        assert config["agent_type"] == "trading"
        assert "max_debate_rounds" in config
        assert "analysts" in config
        assert "markets" in config
    
    def test_get_patent_config(self):
        """测试获取PatentAgent配置"""
        config = self.config_manager.get_patent_config()
        assert config["agent_type"] == "patent"
        assert "analysis_types" in config
        assert "agents" in config
        assert "patent_databases" in config
    
    def test_get_llm_config(self):
        """测试获取LLM配置"""
        # 测试获取有效的LLM提供商配置
        dashscope_config = self.config_manager.get_llm_config("dashscope")
        assert "api_key_env" in dashscope_config
        assert "models" in dashscope_config
        assert "default_model" in dashscope_config
        
        # 测试获取无效的LLM提供商配置
        with pytest.raises(ValueError):
            self.config_manager.get_llm_config("invalid_provider")
    
    def test_get_available_llm_providers(self):
        """测试获取可用LLM提供商"""
        providers = self.config_manager.get_available_llm_providers()
        assert isinstance(providers, list)
        assert len(providers) > 0
        assert "dashscope" in providers
        assert "openai" in providers
    
    def test_get_available_models(self):
        """测试获取可用模型"""
        models = self.config_manager.get_available_models("dashscope")
        assert isinstance(models, list)
        assert len(models) > 0
        assert "qwen-turbo" in models
    
    def test_get_default_model(self):
        """测试获取默认模型"""
        default_model = self.config_manager.get_default_model("dashscope")
        assert default_model == "qwen-turbo"
    
    @patch.dict(os.environ, {"DASHSCOPE_API_KEY": "test_key"})
    def test_get_api_key_with_env(self):
        """测试从环境变量获取API密钥"""
        api_key = self.config_manager.get_api_key("dashscope")
        assert api_key == "test_key"
    
    def test_get_api_key_without_env(self):
        """测试没有环境变量时获取API密钥"""
        api_key = self.config_manager.get_api_key("invalid_provider")
        assert api_key is None
    
    @patch.dict(os.environ, {"DASHSCOPE_API_KEY": "test_key"})
    def test_check_api_keys(self):
        """测试检查API密钥状态"""
        status = self.config_manager.check_api_keys("trading")
        assert isinstance(status, dict)
        assert "dashscope_api" in status
        assert status["dashscope_api"] is True
    
    def test_validate_config(self):
        """测试配置验证"""
        result = self.config_manager.validate_config("trading")
        assert isinstance(result, dict)
        assert "valid" in result
        assert "errors" in result
        assert "warnings" in result
        assert "api_keys" in result
    
    def test_get_system_status(self):
        """测试获取系统状态"""
        status = self.config_manager.get_system_status()
        assert isinstance(status, dict)
        assert "config_loaded" in status
        assert "available_agents" in status
        assert "available_llm_providers" in status
        assert status["config_loaded"] is True


class TestUnifiedLLMAdapter:
    """测试UnifiedLLMAdapter"""
    
    def test_get_supported_providers(self):
        """测试获取支持的提供商"""
        providers = UnifiedLLMAdapter.get_supported_providers()
        assert isinstance(providers, list)
        assert "openai" in providers
        assert "dashscope" in providers
        assert "google" in providers
        assert "anthropic" in providers
    
    def test_validate_provider_config(self):
        """测试验证提供商配置"""
        # 测试有效配置
        valid_config = {"model": "gpt-4", "api_key": "test_key"}
        result = UnifiedLLMAdapter.validate_provider_config("openai", valid_config)
        assert result["valid"] is True
        assert len(result["errors"]) == 0
        
        # 测试无效配置
        invalid_config = {}
        result = UnifiedLLMAdapter.validate_provider_config("openai", invalid_config)
        assert result["valid"] is False
        assert len(result["errors"]) > 0
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    def test_create_adapter_with_env_key(self):
        """测试使用环境变量API密钥创建适配器"""
        # 由于需要实际的LLM库，这里只测试初始化参数验证
        with patch('shared.llm_adapters.unified_llm_adapter.UnifiedLLMAdapter._create_adapter'):
            adapter = UnifiedLLMAdapter("openai", "gpt-4")
            assert adapter.provider == "openai"
            assert adapter.model == "gpt-4"
            assert adapter.api_key == "test_key"
    
    def test_create_adapter_without_key(self):
        """测试没有API密钥时创建适配器"""
        with pytest.raises(ValueError):
            UnifiedLLMAdapter("openai", "gpt-4")
    
    def test_create_from_config(self):
        """测试从配置创建适配器"""
        config = {
            "provider": "openai",
            "model": "gpt-4",
            "api_key": "test_key"
        }
        
        with patch('shared.llm_adapters.unified_llm_adapter.UnifiedLLMAdapter._create_adapter'):
            adapter = UnifiedLLMAdapter.create_from_config(config)
            assert adapter.provider == "openai"
            assert adapter.model == "gpt-4"
            assert adapter.api_key == "test_key"
    
    def test_create_from_config_missing_fields(self):
        """测试从不完整配置创建适配器"""
        config = {"provider": "openai"}  # 缺少model
        
        with pytest.raises(ValueError):
            UnifiedLLMAdapter.create_from_config(config)


class TestLLMAdapterFactory:
    """测试LLMAdapterFactory"""
    
    def test_create_adapter(self):
        """测试工厂方法创建适配器"""
        with patch('shared.llm_adapters.unified_llm_adapter.UnifiedLLMAdapter._create_adapter'):
            adapter = LLMAdapterFactory.create_adapter("openai", "gpt-4", "test_key")
            assert adapter.provider == "openai"
            assert adapter.model == "gpt-4"
            assert adapter.api_key == "test_key"
    
    def test_create_from_config(self):
        """测试工厂方法从配置创建适配器"""
        config = {
            "provider": "openai",
            "model": "gpt-4", 
            "api_key": "test_key"
        }
        
        with patch('shared.llm_adapters.unified_llm_adapter.UnifiedLLMAdapter._create_adapter'):
            adapter = LLMAdapterFactory.create_from_config(config)
            assert adapter.provider == "openai"
    
    def test_create_multiple_adapters(self):
        """测试创建多个适配器"""
        configs = [
            {"provider": "openai", "model": "gpt-4", "api_key": "key1"},
            {"provider": "dashscope", "model": "qwen-turbo", "api_key": "key2"}
        ]
        
        with patch('shared.llm_adapters.unified_llm_adapter.UnifiedLLMAdapter._create_adapter'):
            adapters = LLMAdapterFactory.create_multiple_adapters(configs)
            assert len(adapters) == 2
            assert adapters[0].provider == "openai"
            assert adapters[1].provider == "dashscope"


def test_basic_import():
    """测试基础导入功能"""
    # 测试能否正常导入所有模块
    from shared.config.rich_agents_config_manager import RichAgentsConfigManager
    from shared.llm_adapters.unified_llm_adapter import UnifiedLLMAdapter
    
    assert RichAgentsConfigManager is not None
    assert UnifiedLLMAdapter is not None


def test_configuration_files_creation():
    """测试配置文件创建"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_manager = RichAgentsConfigManager(temp_dir)
        
        # 检查配置文件是否被创建
        assert config_manager.main_config_file.exists()
        assert config_manager.trading_config_file.exists()
        assert config_manager.patent_config_file.exists()


if __name__ == "__main__":
    # 运行基础测试
    print("运行Rich-Agents基础功能测试...")
    
    # 测试配置管理器
    print("测试配置管理器...")
    with tempfile.TemporaryDirectory() as temp_dir:
        config_manager = RichAgentsConfigManager(temp_dir)
        
        print("✅ 配置管理器初始化成功")
        
        trading_config = config_manager.get_trading_config()
        print(f"✅ TradingAgent配置: {len(trading_config)} 项配置")
        
        patent_config = config_manager.get_patent_config()
        print(f"✅ PatentAgent配置: {len(patent_config)} 项配置")
        
        providers = config_manager.get_available_llm_providers()
        print(f"✅ 可用LLM提供商: {', '.join(providers)}")
        
        status = config_manager.get_system_status()
        print(f"✅ 系统状态检查: {len(status)} 项状态信息")
    
    # 测试LLM适配器
    print("\n测试LLM适配器...")
    supported_providers = UnifiedLLMAdapter.get_supported_providers()
    print(f"✅ 支持的LLM提供商: {', '.join(supported_providers)}")
    
    print("\n🎉 所有基础功能测试通过!") 