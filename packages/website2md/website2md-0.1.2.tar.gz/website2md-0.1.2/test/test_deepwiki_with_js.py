#!/usr/bin/env python3
"""
Test deepwiki.com with JavaScript support
"""

import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode

async def test_deepwiki_with_js():
    """Test deepwiki with JavaScript rendering"""
    
    url = "https://deepwiki.com/e2b-dev/E2B/1.1-system-architecture"
    
    browser_config = BrowserConfig(
        browser_type="chromium",
        headless=True
    )
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        print(f"🔍 Testing JavaScript-rendered deepwiki.com")
        print(f"URL: {url}")
        print("=" * 60)
        
        # Wait for JavaScript to load content
        config_with_wait = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=10,
            wait_for="[class*='flex']",  # Wait for main layout
            delay_before_return_html=3.0,  # Wait 3 seconds for JS
            js_code="""
            // Scroll down to trigger any lazy loading
            window.scrollTo(0, document.body.scrollHeight);
            
            // Wait a bit more for content to load
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Try to find and click any expandable menus
            const expandableElements = document.querySelectorAll('[aria-expanded="false"]');
            expandableElements.forEach(el => {
                try {
                    el.click();
                } catch (e) {
                    console.log('Could not click element:', e);
                }
            });
            
            // Wait after clicking
            await new Promise(resolve => setTimeout(resolve, 1000));
            """
        )
        
        result = await crawler.arun(url=url, config=config_with_wait)
        
        print(f"✅ JavaScript crawl result:")
        print(f"   Success: {result.success}")
        print(f"   Status: {result.status_code}")
        print(f"   HTML length: {len(result.fit_html or '')}")
        print(f"   Markdown length: {len(result.markdown or '')}")
        
        if result.markdown and len(result.markdown) > 100:
            with open("debug_deepwiki_js.md", "w", encoding="utf-8") as f:
                f.write(result.markdown)
            print(f"   📝 Full content saved to debug_deepwiki_js.md")
            
            # Show first 1000 chars
            print(f"\n📄 First 1000 chars of content:")
            print("-" * 40)
            print(result.markdown[:1000])
            
            # Test content selection with different strategies
            print(f"\n🧪 Testing content selectors on loaded page:")
            print("-" * 40)
            
            selectors_to_test = [
                ("main", "Main content area"),
                ("article", "Article element"),
                (".flex.h-full.flex-1.flex-col.overflow-hidden", "Target container"),
                ("[role='main']", "Main role"),
                (".content, .main-content", "Content classes"),
            ]
            
            for selector, description in selectors_to_test:
                try:
                    config_selector = CrawlerRunConfig(
                        cache_mode=CacheMode.BYPASS,
                        css_selector=selector,
                        delay_before_return_html=2.0,
                        exclude_selectors=[
                            ".border-r-border",
                            ".sidebar",
                            "nav",
                            ".navigation"
                        ]
                    )
                    
                    result_selector = await crawler.arun(url=url, config=config_selector)
                    content_length = len(result_selector.markdown or '')
                    
                    print(f"   {description:30} ({selector}): {content_length:5} chars")
                    
                    if content_length > 500:  # Found good content
                        filename = f"debug_deepwiki_{selector.replace('.', '_').replace(' ', '_').replace('[', '').replace(']', '').replace("'", '').replace('=', '_').replace('"', '')}.md"
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(result_selector.markdown or '')
                        print(f"                              → Saved to {filename}")
                        
                except Exception as e:
                    print(f"   {description:30} ERROR: {str(e)[:50]}...")
        else:
            print(f"❌ Still no content after JavaScript rendering!")
            if result.markdown:
                print(f"   Content: '{result.markdown}'")

if __name__ == "__main__":
    asyncio.run(test_deepwiki_with_js())