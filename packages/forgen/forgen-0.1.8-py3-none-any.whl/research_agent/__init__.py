"""
Research Agent Package - Advanced AI-powered research tools and agents

This package provides a comprehensive suite of research tools built on the Forgen framework:

Tools:
- WebScraperTool: Extracts clean text content from web URLs
- TextAnalyzerTool: Analyzes text for insights, sentiment, and entities  
- SummaryGeneratorTool: Creates intelligent summaries using LLM integration

Agents:
- ResearchIntelligenceAgent: Multi-source research and analysis agent

Pipelines:
- ResearchPipeline: Orchestrates complex research workflows
"""

from .web_scraper_tool import create_web_scraper_tool
from .text_analyzer_tool import create_text_analyzer_tool  
from .summary_generator_tool import create_summary_generator_tool
from .research_intelligence_agent import create_research_intelligence_agent
from .research_pipeline import create_research_pipeline

__all__ = [
    'create_web_scraper_tool',
    'create_text_analyzer_tool', 
    'create_summary_generator_tool',
    'create_research_intelligence_agent',
    'create_research_pipeline'
]

__version__ = "1.0.0"
__author__ = "Forgen Research Team"