"""
AMCP Registry Compatibility Module

This module provides backward compatibility by importing AMCP functionality
from the dedicated forgen.amcp package. All AMCP-related code has been
moved to forgen.amcp for better organization.

Deprecated: Use forgen.amcp directly instead of this module.
"""

import warnings
from typing import List, Dict, Any

# Import all AMCP functionality from the dedicated package
from forgen.amcp import (
    AMCPComponent,
    AMCPRegistry,
    export_amcp_registry,
    load_amcp_registry, 
    export_amcp_components,
    load_amcp_components,
    create_amcp_server,
    create_amcp_blueprint,
    AMCPClient,
    create_client,
    AMCPClientError
)

# Import the generative component for advanced use cases
from forgen.amcp.generative_component import GenerativeAMCPComponent

# Issue deprecation warning
warnings.warn(
    "forgen.registry.amcp is deprecated. Use forgen.amcp directly instead. "
    "The AMCP functionality has been moved to a dedicated package for better organization.",
    DeprecationWarning,
    stacklevel=2
)

# Export everything for backward compatibility
__all__ = [
    # Core classes
    "AMCPComponent",
    "GenerativeAMCPComponent",
    "AMCPRegistry",
    
    # Registry functions
    "export_amcp_registry",
    "load_amcp_registry",
    "export_amcp_components", 
    "load_amcp_components",
    
    # Server functions
    "create_amcp_server",
    "create_amcp_blueprint",
    
    # Client classes
    "AMCPClient",
    "create_client",
    "AMCPClientError"
]

# Note: AMCPComponent is now the unified BaseModule-compatible implementation
# Use GenerativeAMCPComponent for LLM-driven strategy generation if needed


def create_amcp_component(
    component_name: str,
    component_id: str = "",
    description: str = "",
    domain: str = None,
    role: str = None,
    context: str = None,
    modules: List = None,
    generative: bool = False,
    **kwargs
) -> AMCPComponent:
    """
    Factory function for creating AMCP components.
    
    Args:
        component_name: Name of the component
        component_id: Unique identifier
        description: Component description
        domain: Optional domain
        role: Optional role
        context: Optional context
        modules: List of modules
        generative: If True, creates GenerativeAMCPComponent; otherwise regular AMCPComponent
        **kwargs: Additional arguments
        
    Returns:
        Configured AMCP component instance
        
    Deprecated: Use forgen.amcp.create_simple_component or forgen.amcp.GenerativeAMCPComponent directly
    """
    warnings.warn(
        "create_amcp_component is deprecated. Use forgen.amcp.create_simple_component "
        "or instantiate forgen.amcp.GenerativeAMCPComponent directly.",
        DeprecationWarning,
        stacklevel=2
    )
    
    if modules is None:
        modules = []
    
    if generative:
        return GenerativeAMCPComponent(
            component_name=component_name,
            component_id=component_id,
            description=description,
            domain=domain,
            role=role,
            context=context,
            modules=modules,
            **kwargs
        )
    else:
        from forgen.amcp import create_simple_component
        from forgen.registry.registered_module import RegisteredModule
        
        # Convert modules if needed
        registered_modules = []
        for module in modules:
            if isinstance(module, RegisteredModule):
                registered_modules.append(module)
            else:
                # Wrap as RegisteredModule
                registered_modules.append(RegisteredModule(
                    id=getattr(module, 'id', module.__class__.__name__),
                    name=getattr(module, 'name', module.__class__.__name__),
                    module=module
                ))
        
        return create_simple_component(
            component_id=component_id or component_name,
            name=component_name,
            modules=registered_modules,
            domain=domain,
            role=role,
            context=context
        )