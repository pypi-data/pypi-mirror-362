"""
Research Intelligence Agent - A powerful AI agent that can research topics from multiple sources
"""
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

from forgen.agent.agent import GenerativeAgent
from forgen.tool.module import BaseModule
from forgen.llm.interface import get_chat_message

# Import our custom tools
from research_agent.web_scraper_tool import create_web_scraper_tool
from research_agent.text_analyzer_tool import create_text_analyzer_tool
from research_agent.summary_generator_tool import create_summary_generator_tool

load_dotenv()


@dataclass
class ResearchIntelligenceAgent(GenerativeAgent):
    """
    Advanced research agent that can gather, analyze, and synthesize information from multiple sources.
    
    Capabilities:
    - Web scraping and content extraction
    - Text analysis and sentiment detection
    - Intelligent summarization
    - Multi-source synthesis
    - Research report generation
    """
    
    # Required fields for GenerativeAgent
    prompt: str = field(default_factory=lambda: ResearchIntelligenceAgent._get_default_prompt())
    agent_name: str = "ResearchIntelligenceAgent"
    agent_id: str = "research_intel_v1"
    description: str = "Advanced research agent for multi-source information gathering and analysis"
    modules: List[BaseModule] = field(default_factory=list)
    user_input_schema: Optional[Dict[str, type]] = field(default_factory=lambda: {
        "research_query": str,
        "sources": list,  # List of URLs or text sources
        "analysis_depth": str,  # "basic", "detailed", "comprehensive"
        "output_format": str,  # "report", "summary", "bullet_points"
        "max_sources": int  # Optional limit on number of sources
    })
    user_output_schema: Optional[Dict[str, type]] = field(default_factory=lambda: {
        "research_results": dict,
        "analysis_summary": str,
        "source_details": list,
        "recommendations": list,
        "confidence_score": float
    })
    max_iterations: int = 5
    
    def __post_init__(self):
        # Initialize tools after dataclass initialization
        self.web_scraper = create_web_scraper_tool()
        self.text_analyzer = create_text_analyzer_tool() 
        self.summarizer = create_summary_generator_tool()
        
        # Set modules list
        self.modules = [self.web_scraper, self.text_analyzer, self.summarizer]
        
        # Call parent post_init
        super().__post_init__()
    
    @staticmethod
    def _get_default_prompt() -> str:
        """Get the default agent prompt"""
        return """
You are a Research Intelligence Agent, an expert AI researcher capable of gathering, analyzing, and synthesizing information from multiple sources.

Your capabilities include:
1. Web scraping and content extraction from URLs
2. Deep text analysis including sentiment, keywords, and entity extraction
3. Intelligent summarization with different styles and lengths
4. Multi-source information synthesis
5. Research report generation with citations and recommendations

When given a research query, you should:
1. Analyze the query to understand what information is needed
2. Process all provided sources (URLs and text)
3. Extract and analyze key information from each source
4. Synthesize findings across sources to identify patterns, conflicts, and insights
5. Generate a comprehensive response based on the requested output format
6. Provide confidence scores and recommendations for further research

Always be thorough, accurate, and cite your sources. If you find conflicting information, highlight the discrepancies and provide balanced analysis.
"""
    
    def research_topic(self, research_query: str, sources: List[str], 
                      analysis_depth: str = "detailed", 
                      output_format: str = "report",
                      max_sources: int = 10) -> Dict[str, Any]:
        """
        Conduct comprehensive research on a topic using multiple sources.
        
        Args:
            research_query: The research question or topic
            sources: List of URLs or text content to analyze
            analysis_depth: Level of analysis ("basic", "detailed", "comprehensive")
            output_format: Output format ("report", "summary", "bullet_points")
            max_sources: Maximum number of sources to process
            
        Returns:
            Comprehensive research results
        """
        # Limit sources if needed
        if len(sources) > max_sources:
            sources = sources[:max_sources]
        
        source_results = []
        all_text_content = []
        
        print(f"🔍 Starting research on: {research_query}")
        print(f"📚 Processing {len(sources)} sources...")
        
        # Process each source
        for i, source in enumerate(sources, 1):
            print(f"  📄 Processing source {i}/{len(sources)}...")
            
            try:
                # Determine if source is URL or text
                if source.startswith(('http://', 'https://', 'www.')):
                    # Scrape web content
                    scrape_result = self.web_scraper.execute({"url": source})
                    
                    if scrape_result['status'] == 'success':
                        content = scrape_result['text']
                        title = scrape_result['title']
                        source_info = {
                            'type': 'url',
                            'source': source,
                            'title': title,
                            'word_count': scrape_result['word_count'],
                            'status': 'success'
                        }
                    else:
                        print(f"    ⚠️ Failed to scrape {source}: {scrape_result.get('error', 'Unknown error')}")
                        continue
                else:
                    # Treat as direct text content
                    content = source
                    source_info = {
                        'type': 'text',
                        'source': 'Direct text input',
                        'title': 'User provided text',
                        'word_count': len(content.split()),
                        'status': 'success'
                    }
                
                # Analyze the content
                if content.strip():
                    analysis_result = self.text_analyzer.execute({"text": content})
                    
                    # Generate summary based on analysis depth
                    summary_length = {"basic": 100, "detailed": 200, "comprehensive": 400}.get(analysis_depth, 200)
                    summary_result = self.summarizer.execute({
                        "text": content,
                        "summary_type": "comprehensive",
                        "target_length": summary_length
                    })
                    
                    source_info.update({
                        'content_preview': content[:300] + "..." if len(content) > 300 else content,
                        'analysis': analysis_result,
                        'summary': summary_result['summary'],
                        'keywords': analysis_result['keywords'][:10],
                        'sentiment': analysis_result['sentiment_analysis']['sentiment']
                    })
                    
                    all_text_content.append(content)
                    source_results.append(source_info)
                    print(f"    ✅ Successfully processed")
                else:
                    print(f"    ⚠️ No content found in source")
                    
            except Exception as e:
                print(f"    ❌ Error processing source: {e}")
                continue
        
        # Synthesize all information
        if all_text_content:
            combined_text = "\n\n---\n\n".join(all_text_content)
            
            # Generate comprehensive analysis
            overall_analysis = self.text_analyzer.execute({"text": combined_text})
            
            # Generate synthesis summary
            synthesis_length = {"basic": 300, "detailed": 600, "comprehensive": 1000}.get(analysis_depth, 600)
            synthesis_summary = self.summarizer.execute({
                "text": combined_text,
                "summary_type": "executive",
                "target_length": synthesis_length
            })
            
            # Generate final research output using LLM
            research_prompt = self._create_research_prompt(
                research_query, source_results, overall_analysis, 
                synthesis_summary['summary'], output_format
            )
            
            try:
                final_analysis = get_chat_message(
                    message_history=[],
                    system_content=self.prompt,
                    user_content=research_prompt,
                    username="research_agent",
                    increment_usage=lambda *args, **kwargs: None,
                    model=self.model or os.getenv("DEFAULT_MODEL_NAME", "gpt-3.5-turbo")
                )
            except Exception as e:
                final_analysis = f"Error generating final analysis: {e}\n\nFallback summary: {synthesis_summary['summary']}"
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(source_results, overall_analysis)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(source_results, overall_analysis)
            
            return {
                'research_results': {
                    'query': research_query,
                    'sources_processed': len(source_results),
                    'total_word_count': sum(s.get('word_count', 0) for s in source_results),
                    'analysis_depth': analysis_depth,
                    'output_format': output_format
                },
                'analysis_summary': final_analysis,
                'source_details': source_results,
                'overall_analysis': {
                    'top_keywords': overall_analysis['keywords'][:15],
                    'overall_sentiment': overall_analysis['sentiment_analysis'],
                    'readability': overall_analysis['readability'],
                    'key_entities': overall_analysis['entities']
                },
                'recommendations': recommendations,
                'confidence_score': confidence_score,
                'status': 'completed'
            }
        else:
            return {
                'research_results': {'error': 'No valid sources could be processed'},
                'analysis_summary': 'Unable to conduct research due to source processing failures.',
                'source_details': [],
                'recommendations': ['Try different sources or check URL accessibility'],
                'confidence_score': 0.0,
                'status': 'failed'
            }
    
    def _create_research_prompt(self, query: str, sources: List[Dict], analysis: Dict, 
                               synthesis: str, output_format: str) -> str:
        """Create a comprehensive research prompt for final analysis"""
        
        source_summaries = []
        for i, source in enumerate(sources, 1):
            summary = f"Source {i} ({source['type']}): {source['title']}\n"
            summary += f"Keywords: {', '.join(source.get('keywords', [])[:5])}\n"
            summary += f"Sentiment: {source.get('sentiment', 'unknown')}\n"
            summary += f"Summary: {source.get('summary', 'No summary available')[:200]}...\n"
            source_summaries.append(summary)
        
        format_instructions = {
            "report": "Generate a comprehensive research report with introduction, findings, analysis, and conclusions.",
            "summary": "Create a concise executive summary highlighting the most important findings.",
            "bullet_points": "Present findings as organized bullet points with clear categories."
        }.get(output_format, "Generate a comprehensive analysis.")
        
        return f"""
Research Query: {query}

Source Information:
{chr(10).join(source_summaries)}

Overall Synthesis:
{synthesis}

Top Keywords Across All Sources: {', '.join(analysis.get('keywords', [])[:10])}
Overall Sentiment: {analysis.get('sentiment_analysis', {}).get('sentiment', 'unknown')}

Instructions: {format_instructions}

Please provide a thorough analysis that:
1. Directly addresses the research query
2. Synthesizes information from all sources
3. Identifies key patterns, trends, or insights
4. Notes any conflicting information between sources
5. Provides evidence-based conclusions
6. Suggests areas for further research if applicable

Research Analysis:
"""
    
    def _calculate_confidence(self, sources: List[Dict], analysis: Dict) -> float:
        """Calculate confidence score based on source quality and consistency"""
        if not sources:
            return 0.0
        
        # Factors affecting confidence
        source_count = len(sources)
        successful_sources = len([s for s in sources if s.get('status') == 'success'])
        avg_word_count = sum(s.get('word_count', 0) for s in sources) / len(sources)
        
        # Base confidence from source success rate
        base_confidence = successful_sources / source_count if source_count > 0 else 0
        
        # Boost for multiple sources
        source_bonus = min(source_count * 0.1, 0.3)
        
        # Boost for substantial content
        content_bonus = min(avg_word_count / 1000, 0.2)
        
        # Sentiment consistency bonus (if most sources have similar sentiment)
        sentiments = [s.get('sentiment') for s in sources if s.get('sentiment')]
        if sentiments:
            most_common_sentiment = max(set(sentiments), key=sentiments.count)
            sentiment_consistency = sentiments.count(most_common_sentiment) / len(sentiments)
            consistency_bonus = (sentiment_consistency - 0.5) * 0.2 if sentiment_consistency > 0.5 else 0
        else:
            consistency_bonus = 0
        
        total_confidence = base_confidence + source_bonus + content_bonus + consistency_bonus
        return min(round(total_confidence, 2), 1.0)
    
    def _generate_recommendations(self, sources: List[Dict], analysis: Dict) -> List[str]:
        """Generate research recommendations based on findings"""
        recommendations = []
        
        # Check source diversity
        url_sources = [s for s in sources if s.get('type') == 'url']
        if len(url_sources) < 3:
            recommendations.append("Consider adding more diverse web sources for broader perspective")
        
        # Check content depth
        avg_words = sum(s.get('word_count', 0) for s in sources) / len(sources) if sources else 0
        if avg_words < 500:
            recommendations.append("Seek longer-form content sources for more detailed analysis")
        
        # Check sentiment consistency
        sentiments = [s.get('sentiment') for s in sources if s.get('sentiment')]
        if len(set(sentiments)) > 1:
            recommendations.append("Investigate conflicting viewpoints found across sources")
        
        # Check for technical content
        keywords = analysis.get('keywords', [])
        technical_indicators = ['system', 'method', 'process', 'technology', 'algorithm', 'data']
        if any(keyword in technical_indicators for keyword in keywords):
            recommendations.append("Consider consulting technical documentation or academic papers")
        
        # Default recommendations
        if not recommendations:
            recommendations = [
                "Research appears comprehensive with current sources",
                "Consider periodic updates as information may change over time"
            ]
        
        return recommendations[:5]  # Limit to top 5 recommendations

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the research agent with provided input"""
        research_query = input_data.get('research_query', '')
        sources = input_data.get('sources', [])
        analysis_depth = input_data.get('analysis_depth', 'detailed')
        output_format = input_data.get('output_format', 'report')
        max_sources = input_data.get('max_sources', 10)
        
        if not research_query:
            raise ValueError("Research query is required")
        if not sources:
            raise ValueError("At least one source is required")
        
        return self.research_topic(
            research_query=research_query,
            sources=sources,
            analysis_depth=analysis_depth,
            output_format=output_format,
            max_sources=max_sources
        )


def create_research_intelligence_agent() -> ResearchIntelligenceAgent:
    """Factory function to create a configured research intelligence agent"""
    return ResearchIntelligenceAgent()


if __name__ == "__main__":
    # Test the research intelligence agent
    agent = create_research_intelligence_agent()
    
    # Test case: Research AI developments
    test_input = {
        "research_query": "What are the latest developments in artificial intelligence and their impact on society?",
        "sources": [
            "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "https://openai.com/blog",
            """
            Recent advances in AI have been remarkable. Large language models like GPT-4 and Claude 
            have shown unprecedented capabilities in natural language understanding and generation.
            These developments are transforming industries from healthcare to education, but also 
            raising important questions about job displacement and ethical AI use.
            """
        ],
        "analysis_depth": "detailed",
        "output_format": "report",
        "max_sources": 5
    }
    
    print("🚀 Testing Research Intelligence Agent...")
    print("=" * 60)
    
    try:
        results = agent.execute(test_input)
        
        print(f"✅ Research Status: {results['status']}")
        print(f"📊 Sources Processed: {results['research_results']['sources_processed']}")
        print(f"🎯 Confidence Score: {results['confidence_score']}")
        print(f"📝 Analysis Summary:")
        print("-" * 40)
        print(results['analysis_summary'])
        print("-" * 40)
        print(f"💡 Recommendations:")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"  {i}. {rec}")
        
    except Exception as e:
        print(f"❌ Agent failed: {e}")