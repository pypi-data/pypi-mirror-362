"""
Text Analyzer Tool - Analyzes text for key insights, sentiment, and topics
"""
import re
from collections import Counter
from typing import Dict, Any, List
import math

from forgen.tool.builder import ToolBuilder
from forgen.tool.tool import Tool


def extract_keywords(text: str, num_keywords: int = 10) -> List[str]:
    """Extract key terms using simple TF-IDF-like scoring"""
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does',
        'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
        'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
        'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'about', 'into',
        'through', 'during', 'before', 'after', 'above', 'below', 'up', 'down', 'out', 'off',
        'over', 'under', 'again', 'further', 'then', 'once'
    }
    
    # Clean and tokenize text
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    words = [word for word in words if word not in stop_words]
    
    # Count word frequencies
    word_freq = Counter(words)
    
    # Simple scoring: frequency * length (longer words often more important)
    scored_words = [(word, freq * len(word)) for word, freq in word_freq.items()]
    scored_words.sort(key=lambda x: x[1], reverse=True)
    
    return [word for word, score in scored_words[:num_keywords]]


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """Basic sentiment analysis using keyword matching"""
    positive_words = {
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome',
        'positive', 'beneficial', 'effective', 'successful', 'improved', 'better',
        'advantages', 'benefits', 'opportunities', 'solution', 'breakthrough',
        'innovation', 'progress', 'achievement', 'success', 'helpful', 'useful'
    }
    
    negative_words = {
        'bad', 'terrible', 'awful', 'horrible', 'negative', 'problem', 'issue',
        'challenge', 'difficulty', 'failure', 'error', 'mistake', 'wrong',
        'worse', 'disadvantage', 'concern', 'risk', 'threat', 'crisis',
        'decline', 'decrease', 'loss', 'damage', 'harm', 'dangerous'
    }
    
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    total_words = len(words)
    
    if total_words == 0:
        return {'sentiment': 'neutral', 'confidence': 0.0, 'positive_ratio': 0.0, 'negative_ratio': 0.0}
    
    positive_ratio = positive_count / total_words
    negative_ratio = negative_count / total_words
    
    sentiment_score = positive_ratio - negative_ratio
    
    if sentiment_score > 0.01:
        sentiment = 'positive'
    elif sentiment_score < -0.01:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    confidence = min(abs(sentiment_score) * 10, 1.0)  # Scale confidence
    
    return {
        'sentiment': sentiment,
        'confidence': round(confidence, 2),
        'positive_ratio': round(positive_ratio, 3),
        'negative_ratio': round(negative_ratio, 3)
    }


def extract_entities(text: str) -> Dict[str, List[str]]:
    """Extract potential entities using pattern matching"""
    # Simple patterns for common entity types
    
    # URLs
    urls = re.findall(r'https?://[^\s]+', text)
    
    # Email addresses
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    
    # Dates (various formats)
    dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b', text)
    
    # Numbers (including percentages, currency)
    numbers = re.findall(r'\b\d+(?:\.\d+)?%?\b|\$\d+(?:\.\d+)?\b', text)
    
    # Capitalized words (potential proper nouns)
    proper_nouns = re.findall(r'\b[A-Z][a-zA-Z]+\b', text)
    # Filter common words
    common_words = {'The', 'This', 'That', 'And', 'But', 'For', 'With', 'By', 'In', 'On', 'At', 'To'}
    proper_nouns = [noun for noun in proper_nouns if noun not in common_words]
    
    return {
        'urls': urls[:5],  # Limit results
        'emails': emails[:5],
        'dates': dates[:5],
        'numbers': numbers[:10],
        'proper_nouns': list(set(proper_nouns))[:10]  # Remove duplicates
    }


def calculate_readability(text: str) -> Dict[str, Any]:
    """Calculate basic readability metrics"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    
    if not sentences or not words:
        return {'avg_sentence_length': 0, 'total_sentences': 0, 'total_words': 0, 'complexity': 'unknown'}
    
    avg_sentence_length = len(words) / len(sentences)
    
    # Simple complexity assessment
    if avg_sentence_length < 15:
        complexity = 'simple'
    elif avg_sentence_length < 25:
        complexity = 'moderate'
    else:
        complexity = 'complex'
    
    return {
        'avg_sentence_length': round(avg_sentence_length, 1),
        'total_sentences': len(sentences),
        'total_words': len(words),
        'complexity': complexity
    }


def text_analyzer_function(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes text content for insights, sentiment, entities, and readability.
    
    Args:
        input_data: Dict containing 'text' key
        
    Returns:
        Dict with comprehensive text analysis results
    """
    text = input_data.get('text', '').strip()
    if not text:
        raise ValueError("Text content is required for analysis")
    
    # Perform various analyses
    keywords = extract_keywords(text)
    sentiment = analyze_sentiment(text)
    entities = extract_entities(text)
    readability = calculate_readability(text)
    
    # Generate summary stats
    char_count = len(text)
    word_count = len(re.findall(r'\b[a-zA-Z]+\b', text))
    paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
    
    return {
        'summary_stats': {
            'character_count': char_count,
            'word_count': word_count,
            'paragraph_count': paragraph_count
        },
        'keywords': keywords,
        'sentiment_analysis': sentiment,
        'entities': entities,
        'readability': readability,
        'analysis_status': 'completed'
    }


def preprocessing_function(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and clean input text"""
    text = input_data.get('text', '').strip()
    if not text:
        raise ValueError("Text cannot be empty")
    
    # Limit text length for processing
    if len(text) > 50000:
        text = text[:50000] + "... [Text truncated for analysis]"
    
    return {'text': text}


def postprocessing_function(output_data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean and validate output data"""
    # Ensure all expected keys are present
    required_keys = ['summary_stats', 'keywords', 'sentiment_analysis', 'entities', 'readability']
    for key in required_keys:
        if key not in output_data:
            output_data[key] = {}
    
    return output_data


def create_text_analyzer_tool() -> Tool:
    """Factory function to create a configured text analyzer tool"""
    
    input_schema = {"text": str}
    output_schema = {
        "summary_stats": dict,
        "keywords": list,
        "sentiment_analysis": dict,
        "entities": dict,
        "readability": dict,
        "analysis_status": str
    }
    
    builder = ToolBuilder(
        name="TextAnalyzerTool",
        input_schema=input_schema,
        output_schema=output_schema
    )
    
    builder.set_code(
        operative_function=text_analyzer_function,
        preprocessor_code=preprocessing_function,
        postprocessor_code=postprocessing_function
    )
    
    tool = builder.build()
    tool.description = "Analyzes text for keywords, sentiment, entities, and readability metrics"
    
    return tool


if __name__ == "__main__":
    # Test the text analyzer tool
    analyzer = create_text_analyzer_tool()
    
    test_text = """
    Artificial Intelligence (AI) is revolutionizing the way we work and live. This breakthrough technology
    offers tremendous opportunities for innovation and progress. Companies like Google, Microsoft, and OpenAI 
    are leading the charge with amazing developments in machine learning and natural language processing.
    
    However, there are also significant challenges and concerns about the future impact of AI on employment
    and society. Experts debate whether AI will create more jobs than it eliminates, and there are ongoing
    discussions about the ethical implications of autonomous systems.
    
    The market for AI solutions is expected to reach $190 billion by 2025, representing a 36.6% annual growth rate.
    Visit https://ai-research.org for more information, or contact research@ai-institute.com for detailed reports.
    """
    
    print("🔍 Testing text analyzer...")
    try:
        result = analyzer.execute({"text": test_text})
        print(f"✅ Analysis completed: {result['analysis_status']}")
        print(f"📊 Word count: {result['summary_stats']['word_count']}")
        print(f"🔑 Top keywords: {', '.join(result['keywords'][:5])}")
        print(f"😊 Sentiment: {result['sentiment_analysis']['sentiment']} (confidence: {result['sentiment_analysis']['confidence']})")
        print(f"📖 Complexity: {result['readability']['complexity']}")
        print(f"🏢 Entities found: {len(result['entities']['proper_nouns'])} proper nouns, {len(result['entities']['numbers'])} numbers")
    except Exception as e:
        print(f"❌ Analysis failed: {e}")