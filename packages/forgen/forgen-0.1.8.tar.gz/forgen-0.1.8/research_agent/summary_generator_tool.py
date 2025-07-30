"""
Summary Generator Tool - Creates intelligent summaries using LLM integration
"""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from forgen.tool.builder import ToolBuilder
from forgen.tool.tool import Tool
from forgen.llm.interface import get_chat_message
from forgen.tool.gen.metrics import GenerationMetrics

load_dotenv()


def create_summary_prompt(text: str, summary_type: str = "comprehensive", target_length: int = 300) -> str:
    """Create a tailored prompt for different summary types"""
    
    prompts = {
        "comprehensive": f"""
Please create a comprehensive summary of the following text in approximately {target_length} words. 
Include the main points, key findings, and important details while maintaining the original meaning and context.

Text to summarize:
{text}

Summary:""",
        
        "executive": f"""
Create an executive summary of the following text in approximately {target_length} words.
Focus on the most critical information that a decision-maker would need to know. 
Highlight key findings, recommendations, and actionable insights.

Text to summarize:
{text}

Executive Summary:""",
        
        "technical": f"""
Create a technical summary of the following text in approximately {target_length} words.
Focus on technical details, methodologies, specifications, and quantitative information.
Maintain technical accuracy and include specific metrics or data points.

Text to summarize:
{text}

Technical Summary:""",
        
        "bullet_points": f"""
Create a bullet-point summary of the following text with {target_length//20} main points.
Each bullet point should capture a key insight or important information.
Use clear, concise language and prioritize the most significant points.

Text to summarize:
{text}

Key Points:""",
        
        "one_sentence": """
Summarize the following text in exactly one sentence that captures the main idea or conclusion.

Text to summarize:
{text}

One-sentence summary:"""
    }
    
    return prompts.get(summary_type, prompts["comprehensive"])


def dummy_increment_usage(*args, **kwargs):
    """Dummy function for usage tracking"""
    pass


def summary_generator_function(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates intelligent summaries using LLM integration.
    
    Args:
        input_data: Dict containing:
            - 'text': Text to summarize (required)
            - 'summary_type': Type of summary ('comprehensive', 'executive', 'technical', 'bullet_points', 'one_sentence')
            - 'target_length': Target length in words (default: 300)
            - 'model': LLM model to use (optional)
            
    Returns:
        Dict with summary, metadata, and analysis
    """
    text = input_data.get('text', '').strip()
    if not text:
        raise ValueError("Text content is required for summarization")
    
    summary_type = input_data.get('summary_type', 'comprehensive')
    target_length = input_data.get('target_length', 300)
    model = input_data.get('model', os.getenv("DEFAULT_MODEL_NAME", "gpt-3.5-turbo"))
    
    # Handle different summary types
    if summary_type == 'one_sentence':
        target_length = 50  # Override for one-sentence summaries
    
    # Create the prompt
    prompt = create_summary_prompt(text, summary_type, target_length)
    
    try:
        # Generate summary using LLM
        response = get_chat_message(
            message_history=[],
            system_content="You are an expert summarization assistant. Create clear, accurate, and well-structured summaries.",
            user_content=prompt,
            username="research_agent",
            increment_usage=dummy_increment_usage,
            model=model
        )
        
        summary = response.get("output", "").strip()
        
        # Calculate compression ratio
        original_words = len(text.split())
        summary_words = len(summary.split())
        compression_ratio = round(summary_words / original_words, 3) if original_words > 0 else 0
        
        # Extract token usage from response
        input_tokens = response.get("input_tokens", 0)
        output_tokens = response.get("output_tokens", 0)
        
        # Create metrics object
        metrics = GenerationMetrics(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )
        
        # Generate metadata
        metadata = {
            'summary_type': summary_type,
            'target_length': target_length,
            'actual_length': summary_words,
            'original_length': original_words,
            'compression_ratio': compression_ratio,
            'model_used': model
        }
        
        return {
            'summary': summary,
            'metadata': metadata,
            'metrics': metrics.to_dict(),
            'original_text_preview': text[:200] + "..." if len(text) > 200 else text,
            'status': 'success'
        }
        
    except Exception as e:
        # Fallback to extractive summarization
        fallback_summary = create_extractive_summary(text, target_length)
        
        # Create empty metrics for fallback
        fallback_metrics = GenerationMetrics(
            model='extractive_fallback',
            input_tokens=0,
            output_tokens=0
        )
        
        return {
            'summary': fallback_summary,
            'metadata': {
                'summary_type': f'{summary_type}_fallback',
                'target_length': target_length,
                'actual_length': len(fallback_summary.split()),
                'original_length': len(text.split()),
                'compression_ratio': round(len(fallback_summary.split()) / len(text.split()), 3),
                'model_used': 'extractive_fallback',
                'llm_error': str(e)
            },
            'metrics': fallback_metrics.to_dict(),
            'original_text_preview': text[:200] + "..." if len(text) > 200 else text,
            'status': 'fallback'
        }


def create_extractive_summary(text: str, target_length: int) -> str:
    """Create a simple extractive summary as fallback"""
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    if not sentences:
        return "Unable to create summary from provided text."
    
    # Score sentences by length and position (simple heuristic)
    scored_sentences = []
    for i, sentence in enumerate(sentences):
        words = sentence.split()
        if len(words) < 5:  # Skip very short sentences
            continue
        
        # Simple scoring: length bonus + position bonus (first and last sentences)
        score = len(words)
        if i == 0:  # First sentence bonus
            score *= 1.5
        if i == len(sentences) - 1:  # Last sentence bonus
            score *= 1.2
        
        scored_sentences.append((sentence, score))
    
    # Sort by score and select top sentences
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    
    selected_sentences = []
    current_length = 0
    
    for sentence, score in scored_sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length <= target_length:
            selected_sentences.append(sentence)
            current_length += sentence_length
        if current_length >= target_length * 0.8:  # Stop when we reach 80% of target
            break
    
    # Restore original order
    original_order = []
    for sentence in sentences:
        if sentence in selected_sentences:
            original_order.append(sentence)
    
    return '. '.join(original_order) + '.' if original_order else sentences[0] + '.'


def preprocessing_function(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and clean input data"""
    text = input_data.get('text', '').strip()
    if not text:
        raise ValueError("Text cannot be empty")
    
    # Validate summary type
    valid_types = ['comprehensive', 'executive', 'technical', 'bullet_points', 'one_sentence']
    summary_type = input_data.get('summary_type', 'comprehensive')
    if summary_type not in valid_types:
        summary_type = 'comprehensive'
    
    # Validate target length
    target_length = input_data.get('target_length', 300)
    if not isinstance(target_length, int) or target_length < 10:
        target_length = 300
    
    # Limit text length for processing
    if len(text) > 20000:
        text = text[:20000] + "... [Text truncated for summarization]"
    
    return {
        'text': text,
        'summary_type': summary_type,
        'target_length': target_length,
        'model': input_data.get('model')
    }


def postprocessing_function(output_data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean and validate output data"""
    # Ensure summary is not empty
    if not output_data.get('summary', '').strip():
        output_data['summary'] = "Unable to generate summary from provided text."
        output_data['status'] = 'error'
    
    # Ensure metadata exists
    if 'metadata' not in output_data:
        output_data['metadata'] = {'error': 'Missing metadata'}
    
    return output_data


def create_summary_generator_tool() -> Tool:
    """Factory function to create a configured summary generator tool"""
    
    input_schema = {
        "text": str
    }
    
    output_schema = {
        "summary": str,
        "metadata": dict,
        "metrics": dict,
        "original_text_preview": str,
        "status": str
    }
    
    builder = ToolBuilder(
        name="SummaryGeneratorTool",
        input_schema=input_schema,
        output_schema=output_schema
    )
    
    builder.set_code(
        operative_function=summary_generator_function,
        preprocessor_code=preprocessing_function,
        postprocessor_code=postprocessing_function
    )
    
    tool = builder.build()
    tool.description = "Generates intelligent summaries using LLM integration with fallback options"
    
    return tool


if __name__ == "__main__":
    # Test the summary generator tool
    summarizer = create_summary_generator_tool()
    
    test_text = """
    Artificial Intelligence (AI) represents one of the most significant technological advances of the 21st century.
    This revolutionary field encompasses machine learning, natural language processing, computer vision, and robotics.
    
    The development of AI has been accelerated by several factors: exponential growth in computational power,
    availability of large datasets, and breakthrough algorithms like deep learning neural networks. Companies
    such as Google, Microsoft, OpenAI, and Meta have invested billions of dollars in AI research and development.
    
    AI applications span numerous industries. In healthcare, AI systems assist in medical diagnosis, drug discovery,
    and personalized treatment plans. The financial sector uses AI for fraud detection, algorithmic trading, and
    risk assessment. Transportation benefits from AI through autonomous vehicles and traffic optimization systems.
    
    However, the rapid advancement of AI also raises important concerns. Job displacement due to automation
    affects various sectors, from manufacturing to customer service. Privacy and security issues emerge as AI
    systems process vast amounts of personal data. Ethical considerations include algorithmic bias, transparency
    in decision-making, and the potential for misuse of AI technologies.
    
    Looking forward, experts predict that AI will continue to transform society in profound ways. The development
    of Artificial General Intelligence (AGI) remains a long-term goal, though current AI systems are still narrow
    in scope. Regulatory frameworks are being developed worldwide to ensure responsible AI development and deployment.
    
    The economic impact of AI is substantial, with McKinsey estimating that AI could contribute up to $13 trillion
    to global economic output by 2030. This growth will require significant investment in education and retraining
    programs to prepare the workforce for an AI-driven economy.
    """
    
    test_cases = [
        {"summary_type": "comprehensive", "target_length": 150},
        {"summary_type": "executive", "target_length": 100},
        {"summary_type": "bullet_points", "target_length": 200},
        {"summary_type": "one_sentence"}
    ]
    
    for test_case in test_cases:
        print(f"\n🎯 Testing {test_case['summary_type']} summary...")
        try:
            input_data = {"text": test_text, **test_case}
            result = summarizer.execute(input_data)
            
            print(f"✅ Status: {result['status']}")
            print(f"📝 Summary ({result['metadata']['actual_length']} words):")
            print(result['summary'])
            print(f"📊 Compression ratio: {result['metadata']['compression_ratio']}")
            print(f"🔢 Metrics: {result['metrics']['input_tokens']} in, {result['metrics']['output_tokens']} out, {result['metrics']['cost']} total tokens")
            
        except Exception as e:
            print(f"❌ Failed: {e}")