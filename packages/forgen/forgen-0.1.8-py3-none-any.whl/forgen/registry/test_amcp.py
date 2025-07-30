import json
import tempfile
import os
from datetime import datetime
from unittest.mock import Mock, patch
import pytest

from forgen.registry.amcp import AMCPComponent, export_amcp_registry, load_amcp_registry, StrategyFunction
from forgen.registry.registered_module import RegisteredModule
from forgen.tool.module import BaseModule


class MockModule(BaseModule):
    def __init__(self, name="test_module", input_schema=None, output_schema=None):
        self.name = name
        self.input_schema = input_schema or {"text": str}
        self.output_schema = output_schema or {"result": str}
        self.description = f"Mock module {name}"
    
    def execute(self, input_data):
        return {"result": f"processed: {input_data.get('text', 'no text')}"}
    
    def validate_schema(self):
        pass
    
    def to_amcp_spec(self):
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema
        }


class TestAMCPRegistryFunctions:
    def test_export_amcp_registry_success(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name
        
        try:
            modules = [MockModule("module1"), MockModule("module2")]
            export_amcp_registry(modules, tmp_path)
            
            with open(tmp_path, 'r') as f:
                data = json.load(f)
            
            assert len(data) == 2
            assert data[0]["name"] == "module1"
            assert data[1]["name"] == "module2"
        finally:
            os.unlink(tmp_path)
    
    def test_export_amcp_registry_io_error(self):
        invalid_path = "/invalid/path/registry.json"
        modules = [MockModule()]
        
        with pytest.raises(RuntimeError, match="Failed to export AMCP registry"):
            export_amcp_registry(modules, invalid_path)
    
    def test_load_amcp_registry_success(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            json.dump([{"name": "test", "description": "test module"}], tmp)
            tmp_path = tmp.name
        
        try:
            data = load_amcp_registry(tmp_path)
            assert len(data) == 1
            assert data[0]["name"] == "test"
        finally:
            os.unlink(tmp_path)
    
    def test_load_amcp_registry_file_not_found(self):
        data = load_amcp_registry("nonexistent.json")
        assert data == []
    
    def test_load_amcp_registry_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp.write("invalid json content")
            tmp_path = tmp.name
        
        try:
            with pytest.raises(RuntimeError, match="Failed to load AMCP registry"):
                load_amcp_registry(tmp_path)
        finally:
            os.unlink(tmp_path)


class TestAMCPComponent:
    def create_test_component(self):
        module1 = RegisteredModule(
            id="mod1",
            name="module1",
            module=MockModule("module1"),
            tags=["test", "math"]
        )
        module2 = RegisteredModule(
            id="mod2", 
            name="module2",
            module=MockModule("module2"),
            tags=["test"]
        )
        
        return AMCPComponent(
            id="comp1",
            name="test_component",
            domain="test_domain",
            role="processor",
            context="testing context",
            modules=[module1, module2]
        )
    
    def test_component_creation(self):
        component = self.create_test_component()
        assert component.id == "comp1"
        assert component.name == "test_component"
        assert len(component.modules) == 2
        assert component.usage_stats == {}
    
    def test_serialize_deserialize(self):
        component = self.create_test_component()
        serialized = component.serialize()
        
        assert serialized["type"] == "AMCPComponent"
        assert serialized["id"] == "comp1"
        assert len(serialized["modules"]) == 2
        
        deserialized = AMCPComponent.deserialize(serialized)
        assert deserialized.id == component.id
        assert deserialized.name == component.name
        assert len(deserialized.modules) == len(component.modules)
    
    def test_find_module_by_name(self):
        component = self.create_test_component()
        
        module = component.find_module_by_name("module1")
        assert module is not None
        assert module.name == "module1"
        
        module = component.find_module_by_name("nonexistent")
        assert module is None
    
    def test_find_modules_by_tag(self):
        component = self.create_test_component()
        
        test_modules = component.find_modules_by_tag("test")
        assert len(test_modules) == 2
        
        math_modules = component.find_modules_by_tag("math")
        assert len(math_modules) == 1
        assert math_modules[0].name == "module1"
        
        empty_modules = component.find_modules_by_tag("nonexistent")
        assert len(empty_modules) == 0
    
    def test_list_module_capabilities(self):
        component = self.create_test_component()
        capabilities = component.list_module_capabilities()
        
        assert len(capabilities) == 2
        assert "module1" in capabilities
        assert "module2" in capabilities
        assert capabilities["module1"]["input_schema"] == {"text": str}
        assert capabilities["module1"]["tags"] == ["test", "math"]
    
    def test_validate_success(self):
        component = self.create_test_component()
        issues = component.validate()
        assert len(issues) == 0
    
    def test_validate_no_modules(self):
        component = AMCPComponent(id="empty", name="empty")
        issues = component.validate()
        assert "No modules registered" in issues
    
    def test_validate_duplicate_names(self):
        module1 = RegisteredModule(id="mod1", name="duplicate", module=MockModule("duplicate"))
        module2 = RegisteredModule(id="mod2", name="duplicate", module=MockModule("duplicate"))
        
        component = AMCPComponent(
            id="dup", 
            name="duplicate_test",
            modules=[module1, module2]
        )
        
        issues = component.validate()
        assert any("Duplicate module names" in issue for issue in issues)
    
    def test_validate_module_error(self):
        bad_module = Mock()
        bad_module.module.validate_schema.side_effect = Exception("Schema error")
        bad_module.name = "bad_module"
        
        component = AMCPComponent(
            id="bad",
            name="bad_test", 
            modules=[bad_module]
        )
        
        issues = component.validate()
        assert any("validation failed" in issue for issue in issues)
    
    def test_health_check(self):
        component = self.create_test_component()
        health = component.health_check()
        
        assert health["component_id"] == "comp1"
        assert health["module_count"] == 2
        assert len(health["validation_issues"]) == 0
        assert len(health["modules"]) == 2
        assert all(m["status"] == "healthy" for m in health["modules"])
    
    def test_execute_single_module_fallback(self):
        module = RegisteredModule(
            id="single",
            name="single_module", 
            module=MockModule("single")
        )
        component = AMCPComponent(
            id="single_comp",
            name="single_test",
            modules=[module]
        )
        
        result = component.execute({"text": "test input"})
        assert result["result"] == "processed: test input"
        assert component.usage_stats["single_module_fallback"] == 1
        assert component.usage_stats["total_executions"] == 1
    
    def test_execute_no_strategy_multiple_modules(self):
        component = self.create_test_component()
        
        with pytest.raises(ValueError, match="No strategy function defined"):
            component.execute({"text": "test"})
    
    def test_execute_with_strategy_single_step(self):
        def simple_strategy(user_request, context_info, execution_state):
            return {"tool_name": "module1", "input": user_request}
        
        component = self.create_test_component()
        component.strategy_function = simple_strategy
        
        result = component.execute({"text": "test input"})
        assert result["result"] == "processed: test input"
        assert component.usage_stats["module_module1"] == 1
    
    def test_execute_with_strategy_multi_step(self):
        def multi_strategy(user_request, context_info, execution_state):
            return {
                "steps": [
                    {"tool_name": "module1", "input": user_request},
                    {"tool_name": "module2"}
                ]
            }
        
        component = self.create_test_component()
        component.strategy_function = multi_strategy
        
        result = component.execute({"text": "test input"})
        assert result["result"] == "processed: processed: test input"
        assert component.usage_stats["module_module1"] == 1
        assert component.usage_stats["module_module2"] == 1
    
    def test_execute_tool_not_found(self):
        def bad_strategy(user_request, context_info, execution_state):
            return {"tool_name": "nonexistent", "input": user_request}
        
        component = self.create_test_component()
        component.strategy_function = bad_strategy
        
        with pytest.raises(ValueError, match="Tool 'nonexistent' not found"):
            component.execute({"text": "test"})
    
    def test_execute_tool_execution_error(self):
        error_module = Mock()
        error_module.module.execute.side_effect = Exception("Execution failed")
        error_module.name = "error_module"
        
        def error_strategy(user_request, context_info, execution_state):
            return {"tool_name": "error_module", "input": user_request}
        
        component = AMCPComponent(
            id="error_comp",
            name="error_test",
            modules=[error_module],
            strategy_function=error_strategy
        )
        
        with pytest.raises(RuntimeError, match="Error executing tool 'error_module'"):
            component.execute({"text": "test"})
    
    def test_track_usage(self):
        component = self.create_test_component()
        
        initial_time = component.last_used
        component._track_usage("test_event")
        
        assert component.usage_stats["test_event"] == 1
        assert component.last_used != initial_time
        assert isinstance(component.last_used, datetime)
        
        component._track_usage("test_event")
        assert component.usage_stats["test_event"] == 2


class TestStrategyFunction:
    def test_strategy_protocol_signature(self):
        def valid_strategy(user_request, context_info, execution_state):
            return {"tool_name": "test", "input": user_request}
        
        assert callable(valid_strategy)
        
        result = valid_strategy(
            {"text": "test"}, 
            {"domain": "test"}, 
            {}
        )
        assert result["tool_name"] == "test"


if __name__ == "__main__":
    pytest.main([__file__])