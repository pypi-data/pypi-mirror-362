import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
import pytest
from flask import Flask

from forgen.service.amcp import amcp_endpoint, load_amcp_registry
from forgen.registry.amcp import AMCPComponent
from forgen.registry.registered_module import RegisteredModule
from forgen.tool.module import BaseModule


class MockModule(BaseModule):
    def __init__(self, name="test_module"):
        self.name = name
        self.input_schema = {"text": str}
        self.output_schema = {"result": str}
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


class MockUser:
    def __init__(self):
        self.domains = {}
    
    def create_domain(self, domain_id, name, role, context):
        self.domains[domain_id] = AMCPComponent(
            id=domain_id,
            name=name,
            role=role,
            context=context,
            modules=[]
        )
    
    def add_module_to_domain(self, domain_id, registered_module):
        if domain_id in self.domains:
            self.domains[domain_id].modules.append(registered_module)


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(amcp_endpoint, url_prefix='/amcp')
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_registry():
    module1 = RegisteredModule(
        id="mod1",
        name="module1",
        module=MockModule("module1")
    )
    module2 = RegisteredModule(
        id="mod2",
        name="module2", 
        module=MockModule("module2")
    )
    
    component = AMCPComponent(
        id="comp1",
        name="test_component",
        modules=[module1, module2]
    )
    
    return [component]


class TestAMCPRegistryLoading:
    def test_load_amcp_registry_success(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            component_data = [{
                "id": "test_comp",
                "name": "test_component",
                "modules": []
            }]
            json.dump(component_data, tmp)
            tmp_path = tmp.name
        
        try:
            components = load_amcp_registry(tmp_path)
            assert len(components) == 1
            assert components[0].id == "test_comp"
        finally:
            os.unlink(tmp_path)


class TestAMCPEndpoints:
    def get_headers(self):
        return {'X-API-KEY': 'supersecret', 'Content-Type': 'application/json'}
    
    @patch('forgen.service.amcp.registry')
    def test_list_amcp_registry(self, mock_registry_var, client, mock_registry):
        mock_registry_var.__iter__ = Mock(return_value=iter(mock_registry))
        
        response = client.get('/amcp/registry', headers=self.get_headers())
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['id'] == 'comp1'
    
    def test_list_amcp_registry_unauthorized(self, client):
        response = client.get('/amcp/registry')
        assert response.status_code == 401
        
        response = client.get('/amcp/registry', headers={'X-API-KEY': 'wrong-key'})
        assert response.status_code == 401
    
    @patch('forgen.service.amcp.registry')
    def test_execute_registered_module_success(self, mock_registry_var, client, mock_registry):
        mock_registry_var.__iter__ = Mock(return_value=iter(mock_registry))
        
        payload = {
            "component_id": "comp1",
            "module_id": "mod1", 
            "input_data": {"text": "test input"}
        }
        
        response = client.post(
            '/amcp/execute',
            data=json.dumps(payload),
            headers=self.get_headers()
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "output" in data
        assert data["output"]["result"] == "processed: test input"
    
    @patch('forgen.service.amcp.registry')
    def test_execute_component_not_found(self, mock_registry_var, client, mock_registry):
        mock_registry_var.__iter__ = Mock(return_value=iter(mock_registry))
        
        payload = {
            "component_id": "nonexistent",
            "module_id": "mod1",
            "input_data": {"text": "test"}
        }
        
        response = client.post(
            '/amcp/execute',
            data=json.dumps(payload),
            headers=self.get_headers()
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "Component 'nonexistent' not found" in data["error"]
    
    @patch('forgen.service.amcp.registry')
    def test_execute_module_not_found(self, mock_registry_var, client, mock_registry):
        mock_registry_var.__iter__ = Mock(return_value=iter(mock_registry))
        
        payload = {
            "component_id": "comp1",
            "module_id": "nonexistent",
            "input_data": {"text": "test"}
        }
        
        response = client.post(
            '/amcp/execute',
            data=json.dumps(payload),
            headers=self.get_headers()
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "Module 'nonexistent' not found" in data["error"]
    
    @patch('forgen.service.amcp.registry')
    def test_execute_module_execution_error(self, mock_registry_var, client):
        error_module = Mock()
        error_module.id = "error_mod"
        error_module.module.execute.side_effect = Exception("Execution failed")
        
        component = AMCPComponent(
            id="error_comp",
            name="error_component",
            modules=[error_module]
        )
        
        mock_registry_var.__iter__ = Mock(return_value=iter([component]))
        
        payload = {
            "component_id": "error_comp",
            "module_id": "error_mod",
            "input_data": {"text": "test"}
        }
        
        response = client.post(
            '/amcp/execute', 
            data=json.dumps(payload),
            headers=self.get_headers()
        )
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert "Execution failed" in data["error"]
    
    @patch('forgen.service.amcp.get_user_from_request')
    def test_create_domain(self, mock_get_user, client):
        mock_user = MockUser()
        mock_get_user.return_value = mock_user
        
        payload = {
            "domain_id": "test_domain",
            "name": "Test Domain",
            "role": "processor",
            "context": "testing"
        }
        
        response = client.post(
            '/amcp/domain',
            data=json.dumps(payload),
            headers=self.get_headers()
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "created"
        assert "test_domain" in mock_user.domains
    
    @patch('forgen.service.amcp.get_user_from_request')
    @patch('forgen.service.amcp.deserialize_operand')
    def test_add_module(self, mock_deserialize, mock_get_user, client):
        mock_user = MockUser()
        mock_user.create_domain("test_domain", "Test", "role", "context")
        mock_get_user.return_value = mock_user
        
        mock_module = MockModule("test_module")
        mock_deserialize.return_value = mock_module
        
        payload = {
            "domain_id": "test_domain",
            "module_id": "mod123",
            "name": "test_module",
            "code": "serialized_module_code"
        }
        
        response = client.post(
            '/amcp/module',
            data=json.dumps(payload),
            headers=self.get_headers()
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "registered"
        assert len(mock_user.domains["test_domain"].modules) == 1
        assert mock_user.domains["test_domain"].modules[0].name == "test_module"
    
    @patch('forgen.service.amcp.get_user_from_request')
    def test_list_user_domain(self, mock_get_user, client):
        mock_user = MockUser()
        mock_user.create_domain("test_domain", "Test Domain", "processor", "testing")
        mock_get_user.return_value = mock_user
        
        response = client.get(
            '/amcp/test_domain/registry',
            headers=self.get_headers()
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == "test_domain"
        assert data["name"] == "Test Domain"
    
    @patch('forgen.service.amcp.get_user_from_request')
    def test_list_user_domain_not_found(self, mock_get_user, client):
        mock_user = MockUser()
        mock_get_user.return_value = mock_user
        
        response = client.get(
            '/amcp/nonexistent/registry',
            headers=self.get_headers()
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "Domain not found" in data["error"]
    
    @patch('forgen.service.amcp.get_user_from_request')
    def test_execute_tool_success(self, mock_get_user, client):
        mock_user = MockUser()
        mock_user.create_domain("test_domain", "Test", "role", "context")
        
        registered_module = RegisteredModule(
            id="mod1",
            name="test_module",
            module=MockModule("test_module")
        )
        mock_user.add_module_to_domain("test_domain", registered_module)
        mock_get_user.return_value = mock_user
        
        payload = {
            "module_id": "mod1",
            "input_data": {"text": "test input"}
        }
        
        response = client.post(
            '/amcp/test_domain/execute',
            data=json.dumps(payload),
            headers=self.get_headers()
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "output" in data
        assert data["output"]["result"] == "processed: test input"
    
    @patch('forgen.service.amcp.get_user_from_request')
    def test_execute_tool_domain_not_found(self, mock_get_user, client):
        mock_user = MockUser()
        mock_get_user.return_value = mock_user
        
        payload = {
            "module_id": "mod1",
            "input_data": {"text": "test"}
        }
        
        response = client.post(
            '/amcp/nonexistent/execute',
            data=json.dumps(payload),
            headers=self.get_headers()
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "Domain not found" in data["error"]
    
    @patch('forgen.service.amcp.get_user_from_request')
    def test_execute_tool_module_not_found(self, mock_get_user, client):
        mock_user = MockUser()
        mock_user.create_domain("test_domain", "Test", "role", "context")
        mock_get_user.return_value = mock_user
        
        payload = {
            "module_id": "nonexistent",
            "input_data": {"text": "test"}
        }
        
        response = client.post(
            '/amcp/test_domain/execute',
            data=json.dumps(payload),
            headers=self.get_headers()
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "Module not found" in data["error"]
    
    @patch('forgen.service.amcp.get_user_from_request')
    def test_execute_tool_execution_error(self, mock_get_user, client):
        mock_user = MockUser()
        mock_user.create_domain("test_domain", "Test", "role", "context")
        
        error_module = Mock()
        error_module.id = "error_mod"
        error_module.module.execute.side_effect = Exception("Module execution failed")
        
        registered_module = RegisteredModule(
            id="error_mod",
            name="error_module",
            module=error_module
        )
        mock_user.add_module_to_domain("test_domain", registered_module)
        mock_get_user.return_value = mock_user
        
        payload = {
            "module_id": "error_mod",
            "input_data": {"text": "test"}
        }
        
        response = client.post(
            '/amcp/test_domain/execute',
            data=json.dumps(payload),
            headers=self.get_headers()
        )
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert "Module execution failed" in data["error"]


class TestAMCPSecurity:
    def test_verify_key_missing_header(self, client):
        response = client.get('/amcp/registry')
        assert response.status_code == 401
    
    def test_verify_key_wrong_key(self, client):
        headers = {'X-API-KEY': 'wrong-key'}
        response = client.get('/amcp/registry', headers=headers)
        assert response.status_code == 401
    
    def test_verify_key_correct_key(self, client):
        with patch('forgen.service.amcp.registry', []):
            headers = {'X-API-KEY': 'supersecret'}
            response = client.get('/amcp/registry', headers=headers)
            assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__])