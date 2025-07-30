"""
Research Pipeline - Orchestrates complex multi-step research workflows
"""
from typing import Dict, Any, List
from forgen.pipeline.builder import MultiPathPipelineBuilder as PipelineBuilder
from forgen.pipeline.item import PipelineItem
from forgen.pipeline.pipeline import MultiPathPipeline as Pipeline

# Import our research components
from research_agent.web_scraper_tool import create_web_scraper_tool
from research_agent.text_analyzer_tool import create_text_analyzer_tool
from research_agent.summary_generator_tool import create_summary_generator_tool
from research_agent.research_intelligence_agent import create_research_intelligence_agent


class ResearchPipeline:
    """
    Advanced research pipeline that orchestrates multiple research workflows:
    1. Multi-source parallel processing
    2. Comparative analysis
    3. Trend analysis across time periods
    4. Fact-checking and verification
    """
    
    def __init__(self):
        self.web_scraper = create_web_scraper_tool()
        self.text_analyzer = create_text_analyzer_tool()
        self.summarizer = create_summary_generator_tool()
        self.research_agent = create_research_intelligence_agent()
    
    def create_comparative_research_pipeline(self) -> Pipeline:
        """
        Creates a pipeline for comparative research across multiple topics or sources.
        Useful for competitive analysis, market research, or comparative studies.
        """
        builder = PipelineBuilder()
        builder.set_name("ComparativeResearchPipeline")
        builder.set_description("Compares research across multiple topics or sources")
        
        # Create pipeline items for each research step
        # Step 1: Web scraping for each source
        scraper_item = PipelineItem(
            module=self.web_scraper,
            _id="web_scraper"
        )
        
        # Step 2: Text analysis
        analyzer_item = PipelineItem(
            module=self.text_analyzer,
            _id="text_analyzer"
        )
        
        # Step 3: Summary generation
        summarizer_item = PipelineItem(
            module=self.summarizer,
            _id="summarizer"
        )
        
        # Add items and create flow
        builder.add_item(scraper_item)
        builder.add_item(analyzer_item)
        builder.add_item(summarizer_item)
        
        # Define sequential flow: scraping -> analysis -> summarization
        builder.add_engine_tuple("web_scraper", "text_analyzer")
        builder.add_engine_tuple("text_analyzer", "summarizer")
        
        return builder.build()
    
    def create_trend_analysis_pipeline(self) -> Pipeline:
        """
        Creates a pipeline for analyzing trends over time by processing
        sources from different time periods.
        """
        builder = PipelineBuilder()
        builder.set_name("TrendAnalysisPipeline")
        builder.set_description("Analyzes trends across different time periods")
        
        # Historical data collection
        historical_scraper = PipelineItem(
            module=self.web_scraper,
            _id="historical_scraper"
        )
        
        # Period-specific analysis
        period_analyzer = PipelineItem(
            module=self.text_analyzer,
            _id="period_analyzer"
        )
        
        # Trend synthesis
        trend_synthesizer = PipelineItem(
            module=self.summarizer,
            _id="trend_synthesizer"
        )
        
        # Add items and define sequential flow
        builder.add_item(historical_scraper)
        builder.add_item(period_analyzer)
        builder.add_item(trend_synthesizer)
        
        builder.add_engine_tuple("historical_scraper", "period_analyzer")
        builder.add_engine_tuple("period_analyzer", "trend_synthesizer")
        
        return builder.build()
    
    def create_fact_checking_pipeline(self) -> Pipeline:
        """
        Creates a pipeline for fact-checking claims against multiple sources.
        """
        builder = PipelineBuilder()
        builder.set_name("FactCheckingPipeline")
        builder.set_description("Fact-checks claims against authoritative sources")
        
        # Source verification using research agent
        source_verifier = PipelineItem(
            module=self.research_agent,
            _id="source_verifier"
        )
        
        # Claim analysis
        claim_analyzer = PipelineItem(
            module=self.text_analyzer,
            _id="claim_analyzer"
        )
        
        # Verification summary
        verification_reporter = PipelineItem(
            module=self.summarizer,
            _id="verification_reporter"
        )
        
        # Add items and define verification flow
        builder.add_item(source_verifier)
        builder.add_item(claim_analyzer)
        builder.add_item(verification_reporter)
        
        builder.add_engine_tuple("source_verifier", "claim_analyzer")
        builder.add_engine_tuple("claim_analyzer", "verification_reporter")
        
        return builder.build()
    
    def execute_competitive_analysis(self, companies: List[str], 
                                   analysis_criteria: List[str]) -> Dict[str, Any]:
        """
        Execute a competitive analysis comparing multiple companies or products.
        Uses the comparative research pipeline for structured analysis.
        
        Args:
            companies: List of company names to analyze
            analysis_criteria: What to analyze (e.g., ["products", "market_position", "financials"])
            
        Returns:
            Comprehensive competitive analysis results
        """
        results = {}
        
        print(f"🔍 Starting competitive analysis for {len(companies)} companies...")
        
        for company in companies:
            print(f"  📊 Analyzing {company}...")
            
            # Research each company using the research agent
            query = f"Company profile and analysis of {company}: {', '.join(analysis_criteria)}"
            sources = [
                f"https://en.wikipedia.org/wiki/{company.replace(' ', '_')}",
                f"{company.lower().replace(' ', '')}.com",
                f"https://www.crunchbase.com/organization/{company.lower().replace(' ', '-')}"
            ]
            
            try:
                company_research = self.research_agent.execute({
                    "research_query": query,
                    "sources": sources,
                    "analysis_depth": "detailed",
                    "output_format": "report",
                    "max_sources": 5
                })
                
                results[company] = {
                    "analysis": company_research['analysis_summary'],
                    "key_insights": company_research['overall_analysis']['top_keywords'][:10],
                    "sentiment": company_research['overall_analysis']['overall_sentiment']['sentiment'],
                    "confidence": company_research['confidence_score'],
                    "sources_analyzed": company_research['research_results']['sources_processed']
                }
                print(f"    ✅ {company} analysis completed (confidence: {company_research['confidence_score']:.2f})")
                
            except Exception as e:
                results[company] = {
                    "error": f"Failed to analyze {company}: {str(e)}",
                    "confidence": 0.0
                }
                print(f"    ❌ {company} analysis failed: {e}")
        
        # Generate comparative summary using pipeline
        print("  📋 Generating comparative summary...")
        all_analyses = []
        for company, data in results.items():
            if 'analysis' in data:
                all_analyses.append(f"{company}: {data['analysis'][:500]}...")
        
        if all_analyses:
            comparative_text = "\n\n".join(all_analyses)
            try:
                comparative_summary = self.summarizer.execute({
                    "text": comparative_text,
                    "summary_type": "executive",
                    "target_length": 600
                })
                results['competitive_summary'] = comparative_summary['summary']
                print("    ✅ Comparative summary generated")
            except Exception as e:
                results['competitive_summary'] = f"Failed to generate comparative summary: {e}"
                print(f"    ❌ Summary generation failed: {e}")
        
        return results
    
    def execute_market_research(self, market_topic: str, 
                              research_angles: List[str]) -> Dict[str, Any]:
        """
        Execute comprehensive market research from multiple angles.
        Uses trend analysis pipeline for structured market insights.
        
        Args:
            market_topic: The market or industry to research
            research_angles: Different perspectives (e.g., ["size", "trends", "key_players", "challenges"])
            
        Returns:
            Multi-faceted market research results
        """
        angle_results = {}
        
        print(f"🏭 Starting market research on {market_topic}...")
        
        for angle in research_angles:
            print(f"  📈 Researching {angle}...")
            
            query = f"{market_topic} market {angle}: analysis and insights"
            
            # Generate search sources
            sources = [
                f"https://en.wikipedia.org/wiki/{market_topic.replace(' ', '_')}_market",
                f"{market_topic.lower().replace(' ', '')}marketresearch.com",
                f"Market research and analysis of {market_topic} {angle}"  # This will be treated as text
            ]
            
            try:
                angle_research = self.research_agent.execute({
                    "research_query": query,
                    "sources": sources,
                    "analysis_depth": "comprehensive",
                    "output_format": "report",
                    "max_sources": 3
                })
                
                angle_results[angle] = {
                    "findings": angle_research['analysis_summary'],
                    "key_points": angle_research['overall_analysis']['top_keywords'][:8],
                    "confidence": angle_research['confidence_score']
                }
                print(f"    ✅ {angle} research completed (confidence: {angle_research['confidence_score']:.2f})")
                
            except Exception as e:
                angle_results[angle] = {
                    "error": f"Failed to research {angle}: {str(e)}",
                    "confidence": 0.0
                }
                print(f"    ❌ {angle} research failed: {e}")
        
        # Synthesize overall market view using pipeline
        print("  📊 Synthesizing market overview...")
        all_findings = []
        for angle, data in angle_results.items():
            if 'findings' in data:
                all_findings.append(f"{angle.title()}: {data['findings'][:400]}...")
        
        if all_findings:
            market_overview_text = "\n\n".join(all_findings)
            try:
                market_summary = self.summarizer.execute({
                    "text": market_overview_text,
                    "summary_type": "executive",
                    "target_length": 800
                })
                
                angle_results['market_overview'] = market_summary['summary']
                angle_results['overall_confidence'] = sum(
                    data.get('confidence', 0) for data in angle_results.values() 
                    if isinstance(data, dict) and 'confidence' in data
                ) / len([d for d in angle_results.values() if isinstance(d, dict) and 'confidence' in d])
                print("    ✅ Market overview synthesized")
            except Exception as e:
                angle_results['market_overview'] = f"Failed to synthesize market overview: {e}"
                print(f"    ❌ Market synthesis failed: {e}")
        
        return angle_results


def create_research_pipeline() -> ResearchPipeline:
    """Factory function to create a configured research pipeline"""
    return ResearchPipeline()


if __name__ == "__main__":
    # Test the research pipeline
    pipeline = create_research_pipeline()
    
    print("🚀 Testing Research Pipeline...")
    print("=" * 60)
    
    # Test competitive analysis
    print("\n📊 Testing Competitive Analysis:")
    print("-" * 40)
    
    try:
        comp_results = pipeline.execute_competitive_analysis(
            companies=["OpenAI", "Anthropic"],
            analysis_criteria=["AI_technology", "market_position", "funding"]
        )
        
        for company, data in comp_results.items():
            if company != 'competitive_summary':
                print(f"\n🏢 {company}:")
                if 'analysis' in data:
                    print(f"  📈 Sentiment: {data['sentiment']}")
                    print(f"  🎯 Confidence: {data['confidence']}")
                    print(f"  🔑 Key insights: {', '.join(data['key_insights'][:5])}")
                else:
                    print(f"  ❌ {data.get('error', 'Unknown error')}")
        
        if 'competitive_summary' in comp_results:
            print(f"\n📋 Competitive Summary:")
            print(comp_results['competitive_summary'][:400] + "...")
    
    except Exception as e:
        print(f"❌ Competitive analysis failed: {e}")
    
    # Test market research
    print("\n\n🏭 Testing Market Research:")
    print("-" * 40)
    
    try:
        market_results = pipeline.execute_market_research(
            market_topic="Artificial Intelligence",
            research_angles=["market_size", "key_trends", "major_players"]
        )
        
        for angle, data in market_results.items():
            if angle not in ['market_overview', 'overall_confidence']:
                print(f"\n📈 {angle.replace('_', ' ').title()}:")
                if 'findings' in data:
                    print(f"  🎯 Confidence: {data['confidence']}")
                    print(f"  🔑 Key points: {', '.join(data['key_points'][:4])}")
                else:
                    print(f"  ❌ {data.get('error', 'Unknown error')}")
        
        if 'market_overview' in market_results:
            print(f"\n📋 Market Overview:")
            print(market_results['market_overview'][:400] + "...")
            print(f"\n🎯 Overall Confidence: {market_results.get('overall_confidence', 0):.2f}")
    
    except Exception as e:
        print(f"❌ Market research failed: {e}")
    
    print("\n✅ Pipeline testing completed!")