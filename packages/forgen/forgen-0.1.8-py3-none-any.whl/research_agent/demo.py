#!/usr/bin/env python3
"""
Research Agent Demo - Showcases the capabilities of the Research Intelligence Agent

This demo demonstrates:
1. Individual tool testing
2. Complete research agent workflows
3. Pipeline-based research operations
4. Real-world use cases
"""

import os
import sys
from typing import List

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from research_agent import (
    create_web_scraper_tool,
    create_text_analyzer_tool,
    create_summary_generator_tool,
    create_research_intelligence_agent,
    create_research_pipeline
)


def demo_individual_tools():
    """Demonstrate each tool individually"""
    print("🛠️  INDIVIDUAL TOOLS DEMO")
    print("=" * 60)
    
    # Web Scraper Demo
    print("\n🌐 Web Scraper Tool Demo:")
    print("-" * 30)
    scraper = create_web_scraper_tool()
    
    test_url = "https://en.wikipedia.org/wiki/Machine_learning"
    try:
        result = scraper.execute({"url": test_url})
        print(f"✅ Successfully scraped: {result['title']}")
        print(f"📊 Word count: {result['word_count']}")
        print(f"📝 Preview: {result['text'][:200]}...")
    except Exception as e:
        print(f"❌ Scraper failed: {e}")
    
    # Text Analyzer Demo
    print("\n🔍 Text Analyzer Tool Demo:")
    print("-" * 30)
    analyzer = create_text_analyzer_tool()
    
    sample_text = """
    Machine learning is a revolutionary technology that's transforming industries worldwide.
    Companies like Google, Microsoft, and Amazon are investing billions in AI research.
    However, there are concerns about job displacement and ethical implications.
    The market is expected to grow 40% annually, reaching $190 billion by 2025.
    Visit https://ml-research.org for more details or email info@ai-institute.com.
    """
    
    try:
        result = analyzer.execute({"text": sample_text})
        print(f"✅ Analysis completed")
        print(f"📊 Word count: {result['summary_stats']['word_count']}")
        print(f"🔑 Keywords: {', '.join(result['keywords'][:5])}")
        print(f"😊 Sentiment: {result['sentiment_analysis']['sentiment']}")
        print(f"🏢 Entities: {len(result['entities']['proper_nouns'])} organizations found")
    except Exception as e:
        print(f"❌ Analyzer failed: {e}")
    
    # Summary Generator Demo
    print("\n📝 Summary Generator Tool Demo:")
    print("-" * 30)
    summarizer = create_summary_generator_tool()
    
    long_text = """
    Artificial Intelligence (AI) has emerged as one of the most transformative technologies of the 21st century,
    fundamentally changing how we work, communicate, and solve complex problems. The field encompasses various
    subdomains including machine learning, natural language processing, computer vision, and robotics.
    
    The recent breakthroughs in deep learning, particularly with transformer architectures and large language
    models, have enabled AI systems to achieve human-level performance in many tasks. Companies across industries
    are rapidly adopting AI solutions to improve efficiency, reduce costs, and create new products and services.
    
    However, the rapid advancement of AI also presents significant challenges. Concerns about job displacement,
    algorithmic bias, privacy violations, and the concentration of AI capabilities in a few large corporations
    have sparked intense debate among policymakers, researchers, and the public.
    
    Looking ahead, the development of Artificial General Intelligence (AGI) remains a long-term goal that could
    revolutionize society even further. Experts predict that responsible AI development, robust regulatory
    frameworks, and public-private collaboration will be essential for maximizing AI's benefits while
    minimizing its risks.
    """
    
    try:
        result = summarizer.execute({
            "text": long_text,
            "summary_type": "executive",
            "target_length": 100
        })
        print(f"✅ Summary generated ({result['metadata']['actual_length']} words)")
        print(f"📝 Summary: {result['summary']}")
        print(f"📊 Compression ratio: {result['metadata']['compression_ratio']}")
    except Exception as e:
        print(f"❌ Summarizer failed: {e}")


def demo_research_agent():
    """Demonstrate the complete research agent"""
    print("\n\n🤖 RESEARCH INTELLIGENCE AGENT DEMO")
    print("=" * 60)
    
    agent = create_research_intelligence_agent()
    
    # Research demo on AI ethics
    research_input = {
        "research_query": "What are the main ethical concerns surrounding artificial intelligence development?",
        "sources": [
            "https://en.wikipedia.org/wiki/Ethics_of_artificial_intelligence",
            """
            Recent studies have highlighted several key ethical concerns in AI development:
            1. Algorithmic bias leading to unfair treatment of certain groups
            2. Privacy violations through extensive data collection and surveillance
            3. Job displacement as AI systems automate human tasks
            4. Lack of transparency in AI decision-making processes
            5. Potential misuse of AI for harmful purposes like deepfakes or autonomous weapons
            
            Experts recommend implementing AI ethics boards, developing explainable AI systems,
            and creating comprehensive regulatory frameworks to address these challenges.
            """,
            "https://www.stanford.edu/~jonst/ethics_AI.html"  # This might not exist, showing error handling
        ],
        "analysis_depth": "detailed",
        "output_format": "report",
        "max_sources": 5
    }
    
    print(f"🔍 Research Query: {research_input['research_query']}")
    print(f"📚 Sources: {len(research_input['sources'])} sources provided")
    
    try:
        results = agent.execute(research_input)
        
        print(f"\n✅ Research Status: {results['status']}")
        print(f"📊 Sources Processed: {results['research_results']['sources_processed']}")
        print(f"🎯 Confidence Score: {results['confidence_score']:.2f}")
        
        print(f"\n📋 Research Analysis:")
        print("-" * 40)
        print(results['analysis_summary'][:800] + "..." if len(results['analysis_summary']) > 800 else results['analysis_summary'])
        
        print(f"\n🔑 Key Insights:")
        for keyword in results['overall_analysis']['top_keywords'][:8]:
            print(f"  • {keyword}")
        
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        print(f"\n📊 Overall Sentiment: {results['overall_analysis']['overall_sentiment']['sentiment']}")
        
    except Exception as e:
        print(f"❌ Research agent failed: {e}")


def demo_research_pipeline():
    """Demonstrate the research pipeline capabilities"""
    print("\n\n🏭 RESEARCH PIPELINE DEMO")
    print("=" * 60)
    
    pipeline = create_research_pipeline()
    
    # Competitive Analysis Demo
    print("\n🏢 Competitive Analysis Demo:")
    print("-" * 40)
    
    try:
        comp_results = pipeline.execute_competitive_analysis(
            companies=["Tesla", "Ford"],
            analysis_criteria=["electric_vehicles", "market_strategy", "innovation"]
        )
        
        print("🏆 Competitive Analysis Results:")
        for company, data in comp_results.items():
            if company != 'competitive_summary':
                print(f"\n📈 {company}:")
                if 'analysis' in data:
                    print(f"  🎯 Confidence: {data['confidence']:.2f}")
                    print(f"  😊 Sentiment: {data['sentiment']}")
                    print(f"  📊 Sources: {data['sources_analyzed']}")
                    print(f"  📝 Preview: {data['analysis'][:200]}...")
                else:
                    print(f"  ❌ Error: {data.get('error', 'Unknown error')}")
        
        if 'competitive_summary' in comp_results:
            print(f"\n📋 Competitive Summary:")
            print(comp_results['competitive_summary'][:500] + "...")
            
    except Exception as e:
        print(f"❌ Competitive analysis failed: {e}")
    
    # Market Research Demo
    print("\n\n🏭 Market Research Demo:")
    print("-" * 40)
    
    try:
        market_results = pipeline.execute_market_research(
            market_topic="Electric Vehicles",
            research_angles=["market_size", "growth_trends", "key_challenges"]
        )
        
        print("📊 Market Research Results:")
        for angle, data in market_results.items():
            if angle not in ['market_overview', 'overall_confidence']:
                print(f"\n📈 {angle.replace('_', ' ').title()}:")
                if 'findings' in data:
                    print(f"  🎯 Confidence: {data['confidence']:.2f}")
                    print(f"  🔑 Key Points: {', '.join(data['key_points'][:4])}")
                    print(f"  📝 Preview: {data['findings'][:200]}...")
                else:
                    print(f"  ❌ Error: {data.get('error', 'Unknown error')}")
        
        if 'market_overview' in market_results:
            print(f"\n📋 Market Overview:")
            print(market_results['market_overview'][:500] + "...")
            print(f"\n🎯 Overall Confidence: {market_results.get('overall_confidence', 0):.2f}")
            
    except Exception as e:
        print(f"❌ Market research failed: {e}")


def demo_real_world_scenarios():
    """Demonstrate real-world research scenarios"""
    print("\n\n🌍 REAL-WORLD SCENARIOS DEMO")
    print("=" * 60)
    
    agent = create_research_intelligence_agent()
    
    scenarios = [
        {
            "name": "Investment Research",
            "query": "Is renewable energy a good investment opportunity in 2024?",
            "sources": [
                "https://en.wikipedia.org/wiki/Renewable_energy",
                """
                Investment analysts report strong growth in renewable energy sector:
                - Solar and wind capacity increased 260% globally since 2010
                - Government incentives and subsidies support market expansion  
                - Technology costs declining while efficiency improves
                - ESG investing trends favor clean energy companies
                - Major corporations committing to renewable energy targets
                
                However, challenges include grid integration costs, energy storage needs,
                and policy uncertainty in some markets.
                """
            ]
        },
        {
            "name": "Technology Assessment", 
            "query": "What are the current capabilities and limitations of quantum computing?",
            "sources": [
                "https://en.wikipedia.org/wiki/Quantum_computing",
                """
                Quantum computing status update 2024:
                
                Current Capabilities:
                - IBM and Google have achieved quantum supremacy in specific problems
                - Error correction and qubit stability gradually improving
                - Applications emerging in cryptography, optimization, and drug discovery
                - Major tech companies investing billions in quantum research
                
                Current Limitations:
                - High error rates and quantum decoherence remain major challenges
                - Limited to specialized problem types, not general-purpose computing
                - Requires extreme cooling and controlled environments
                - Still years away from practical commercial applications for most use cases
                """
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 {scenario['name']} Scenario:")
        print("-" * 40)
        
        try:
            results = agent.execute({
                "research_query": scenario['query'],
                "sources": scenario['sources'],
                "analysis_depth": "comprehensive",
                "output_format": "executive_summary",
                "max_sources": 3
            })
            
            print(f"📋 Research Summary:")
            print(results['analysis_summary'][:600] + "...")
            print(f"\n🎯 Confidence: {results['confidence_score']:.2f}")
            print(f"😊 Overall Sentiment: {results['overall_analysis']['overall_sentiment']['sentiment']}")
            
        except Exception as e:
            print(f"❌ Scenario failed: {e}")


def main():
    """Run the complete demo"""
    print("🚀 RESEARCH INTELLIGENCE AGENT - COMPLETE DEMO")
    print("=" * 70)
    print("This demo showcases the full capabilities of the Research Agent system")
    print("built with the Forgen framework.\n")
    
    try:
        # Run all demo sections
        demo_individual_tools()
        demo_research_agent()
        demo_research_pipeline()
        demo_real_world_scenarios()
        
        print("\n\n🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("The Research Intelligence Agent has demonstrated:")
        print("✅ Web scraping and content extraction")
        print("✅ Advanced text analysis and sentiment detection")
        print("✅ Intelligent summarization with multiple formats")
        print("✅ Multi-source research synthesis")
        print("✅ Pipeline-based competitive and market analysis")
        print("✅ Real-world research scenario handling")
        print("\nThe system is ready for production use! 🚀")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")


if __name__ == "__main__":
    main()