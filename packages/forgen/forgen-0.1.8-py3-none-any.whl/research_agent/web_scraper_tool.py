"""
Web Scraper Tool - Extracts clean text content from web URLs
"""
from typing import Dict, Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from forgen.tool.builder import ToolBuilder
from forgen.tool.tool import Tool


def web_scraper_function(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scrapes text content from a web URL and returns clean, readable text.
    
    Args:
        input_data: Dict containing 'url' key
        
    Returns:
        Dict with 'text', 'title', 'url', and 'word_count' keys
    """
    url = input_data.get('url')
    if not url:
        raise ValueError("URL is required")
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        # Make request with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "aside"]):
            script.decompose()
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title found"
        
        # Extract main content
        # Try to find main content areas first
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=['content', 'main-content', 'post-content'])
        
        if main_content:
            text = main_content.get_text()
        else:
            # Fall back to body content
            text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit text length to prevent overwhelming downstream processes
        if len(text) > 10000:
            text = text[:10000] + "... [Content truncated]"
        
        word_count = len(text.split())
        
        return {
            'text': text,
            'title': title_text,
            'url': url,
            'word_count': word_count,
            'status': 'success'
        }
        
    except requests.RequestException as e:
        return {
            'text': '',
            'title': '',
            'url': url,
            'word_count': 0,
            'status': 'error',
            'error': str(e)
        }


def preprocessing_function(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and clean input URL"""
    url = input_data.get('url', '').strip()
    if not url:
        raise ValueError("URL cannot be empty")
    
    # Basic URL validation
    parsed = urlparse(url if url.startswith(('http://', 'https://')) else 'https://' + url)
    if not parsed.netloc:
        raise ValueError("Invalid URL format")
    
    return {'url': url}


def postprocessing_function(output_data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean and validate output data"""
    if output_data.get('status') == 'success' and not output_data.get('text'):
        output_data['status'] = 'warning'
        output_data['text'] = 'No readable content found on the page'
    
    return output_data


def create_web_scraper_tool() -> Tool:
    """Factory function to create a configured web scraper tool"""
    
    input_schema = {"url": str}
    output_schema = {
        "text": str,
        "title": str, 
        "url": str,
        "word_count": int,
        "status": str
    }
    
    builder = ToolBuilder(
        name="WebScraperTool",
        input_schema=input_schema,
        output_schema=output_schema
    )
    
    builder.set_code(
        operative_function=web_scraper_function,
        preprocessor_code=preprocessing_function,
        postprocessor_code=postprocessing_function
    )
    
    tool = builder.build()
    tool.description = "Scrapes and extracts clean text content from web URLs"
    
    return tool


if __name__ == "__main__":
    # Test the web scraper tool
    scraper = create_web_scraper_tool()
    
    test_urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://python.org",
        "example.com"
    ]
    
    for url in test_urls:
        print(f"\n🔍 Testing web scraper with: {url}")
        try:
            result = scraper.execute({"url": url})
            print(f"✅ Status: {result['status']}")
            print(f"📄 Title: {result['title']}")
            print(f"📊 Word count: {result['word_count']}")
            if result['status'] == 'error':
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
            else:
                print(f"📝 Content preview: {result['text'][:200]}...")
        except Exception as e:
            print(f"❌ Failed: {e}")