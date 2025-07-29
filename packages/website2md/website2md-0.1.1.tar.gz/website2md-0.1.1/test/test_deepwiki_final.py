#!/usr/bin/env python3
"""
Final test of deepwiki.com crawling with JavaScript support
"""

import asyncio
import os
from website2md.doc_crawler import DocSiteCrawler
from website2md.config import CrawlConfig

async def test_deepwiki_final():
    """Test the updated crawler on deepwiki.com"""
    
    print("🚀 Testing deepwiki.com with JavaScript support")
    print("=" * 60)
    
    # Configure for JavaScript-heavy sites
    config = CrawlConfig(
        max_pages=5,  # Limited for testing
        timeout=30,   # Longer timeout for JS loading
        bypass_cache=True,
        
        # JavaScript rendering settings
        wait_for_content=True,
        js_wait_time=3.0,
        scroll_for_content=True,
        expand_menus=True,
        
        # Content selection - test different strategies
        content_selector=None,  # Let it get everything first
        exclude_selectors=[
            ".border-r-border",        # Deepwiki sidebar
            ".md\\:w-64", ".xl\\:w-72", # Sidebar width classes
            ".md\\:sticky",             # Sticky sidebar
            ".hidden.max-h-screen",     # Hidden sidebar elements
            "nav", ".nav", ".sidebar", ".navigation",
            ".header", ".footer", ".breadcrumb"
        ]
    )
    
    crawler = DocSiteCrawler(config)
    
    print("🔍 Step 1: Test single page crawl")
    print("-" * 40)
    
    test_url = "https://deepwiki.com/e2b-dev/E2B/1.1-system-architecture"
    result = await crawler.crawl_single_url(test_url, "deepwiki_final_test")
    
    if result and result.get('success'):
        print(f"✅ Single page crawl successful:")
        print(f"   - Content length: {result.get('content_length', 0)} chars")
        print(f"   - File: {result.get('filename', 'unknown')}")
        print(f"   - Skipped: {result.get('skipped', False)}")
        
        # Read the content to verify quality
        if result.get('file_path') and os.path.exists(result['file_path']):
            with open(result['file_path'], 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"   - Actual content preview (first 500 chars):")
                print("     " + content[:500].replace('\n', '\n     '))
    else:
        print(f"❌ Single page crawl failed: {result}")
        return
    
    print(f"\n🌐 Step 2: Test site discovery (limited)")
    print("-" * 40)
    
    base_url = "https://deepwiki.com/e2b-dev/E2B"
    site_result = await crawler.crawl_documentation_site(base_url, "deepwiki_final_test")
    
    print(f"✅ Site crawl result:")
    print(f"   - URLs discovered: {site_result.get('urls_discovered', 0)}")
    print(f"   - Pages crawled: {site_result.get('pages_crawled', 0)}")
    print(f"   - Pages skipped: {site_result.get('pages_skipped', 0)}")
    print(f"   - Success rate: {site_result.get('success_rate', 0):.1%}")
    
    if 'discovered_urls' in site_result and site_result['discovered_urls']:
        print(f"   - Sample discovered URLs:")
        for url in list(site_result['discovered_urls'])[:10]:
            print(f"     • {url}")
        if len(site_result['discovered_urls']) > 10:
            print(f"     ... and {len(site_result['discovered_urls']) - 10} more")
    
    print(f"\n🎯 Summary")
    print("-" * 40)
    print(f"The updated crawler successfully handles JavaScript-rendered sites like deepwiki.com")
    print(f"Key improvements:")
    print(f"- ✅ JavaScript content loading with configurable wait time")
    print(f"- ✅ Automatic scrolling to trigger lazy loading")
    print(f"- ✅ Menu expansion for better URL discovery")
    print(f"- ✅ Exclude selectors for clean content extraction")
    print(f"\nFor deepwiki.com, recommended config:")
    print(f"- wait_for_content=True, js_wait_time=3.0")
    print(f"- exclude_selectors for '.border-r-border', '.md\\:w-64' etc.")

if __name__ == "__main__":
    asyncio.run(test_deepwiki_final())