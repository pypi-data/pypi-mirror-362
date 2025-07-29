#!/usr/bin/env python3
"""
Test crawler for deepwiki.com/e2b-dev/E2B site
Testing different content selector strategies for complex layouts
"""

import asyncio
import os
from website2md.doc_crawler import DocSiteCrawler
from website2md.config import CrawlConfig

async def test_deepwiki_crawler():
    """Test different content selector configurations for deepwiki site"""
    
    print("🚀 Testing deepwiki.com E2B documentation crawler...")
    print("=" * 60)
    
    # Test configurations
    test_configs = [
        {
            "name": "Strategy 1: Direct main content selector",
            "config": CrawlConfig(
                max_pages=10,  # Limited for testing
                bypass_cache=True,
                timeout=60,
                content_selector='div.flex.h-full.flex-1.flex-col.overflow-hidden',
                exclude_selectors=[
                    '.border-r-border',  # Sidebar
                    '.md\\:w-64',       # Sidebar width
                    '.xl\\:w-72',       # Sidebar width
                    'nav',
                    '.nav',
                    '.sidebar'
                ]
            )
        },
        {
            "name": "Strategy 2: Exclude-based approach", 
            "config": CrawlConfig(
                max_pages=10,  # Limited for testing
                bypass_cache=True,
                timeout=60,
                content_selector=None,  # Let it find main content
                exclude_selectors=[
                    '.border-r-border',
                    '.hidden.max-h-screen',
                    '.md\\:sticky',
                    '.md\\:w-64',
                    '.xl\\:w-72',
                    '.md\\:left-0',
                    '.md\\:top-20',
                    'nav',
                    '.nav',
                    '.sidebar',
                    '.navigation',
                    '.header',
                    '.footer',
                    '.breadcrumb'
                ]
            )
        },
        {
            "name": "Strategy 3: Generic content selectors",
            "config": CrawlConfig(
                max_pages=10,  # Limited for testing
                bypass_cache=True,
                timeout=60,
                content_selector='main, article, [role="main"], .content, .main-content',
                exclude_selectors=[
                    '.border-r-border',
                    '.sidebar',
                    'nav',
                    '.navigation'
                ]
            )
        }
    ]
    
    base_url = "https://deepwiki.com/e2b-dev/E2B"
    test_url = "https://deepwiki.com/e2b-dev/E2B/1.1-system-architecture"
    
    for i, test_case in enumerate(test_configs, 1):
        print(f"\n📋 {test_case['name']}")
        print("-" * 50)
        
        config = test_case['config']
        crawler = DocSiteCrawler(config)
        
        try:
            # Test single page first
            print(f"🔍 Testing single page: {test_url}")
            single_result = await crawler.crawl_single_url(
                test_url, 
                f"deepwiki_test_strategy_{i}_single"
            )
            
            print(f"✅ Single page result:")
            print(f"   - Success: {single_result.get('success', False)}")
            print(f"   - Content length: {len(single_result.get('content', ''))}")
            print(f"   - Word count: {single_result.get('word_count', 0)}")
            
            # If single page works well, test full site discovery
            if single_result.get('success') and len(single_result.get('content', '')) > 500:
                print(f"\n🌐 Testing full site discovery from: {base_url}")
                site_result = await crawler.crawl_documentation_site(
                    base_url,
                    f"deepwiki_test_strategy_{i}_full"
                )
                
                print(f"✅ Full site result:")
                print(f"   - URLs discovered: {site_result.get('urls_discovered', 0)}")
                print(f"   - Pages crawled: {site_result.get('pages_crawled', 0)}")
                print(f"   - Pages skipped: {site_result.get('pages_skipped', 0)}")
                print(f"   - Success rate: {site_result.get('success_rate', 0):.1%}")
                
                # Show some discovered URLs
                if 'discovered_urls' in site_result:
                    print(f"   - Sample URLs found:")
                    for url in list(site_result['discovered_urls'])[:5]:
                        print(f"     • {url}")
                    if len(site_result['discovered_urls']) > 5:
                        print(f"     ... and {len(site_result['discovered_urls']) - 5} more")
                        
            else:
                print(f"❌ Single page test failed or insufficient content, skipping full site test")
                
        except Exception as e:
            print(f"❌ Error with {test_case['name']}: {str(e)}")
            continue
    
    print(f"\n🎯 Test Summary")
    print("=" * 60)
    print("Check the output directories to compare content quality:")
    print("- deepwiki_test_strategy_1_single/ - Direct selector approach")
    print("- deepwiki_test_strategy_2_single/ - Exclude-based approach") 
    print("- deepwiki_test_strategy_3_single/ - Generic selector approach")
    print("\nRecommendation: Choose the strategy that produces the cleanest content")
    print("without sidebars, navigation, or other clutter.")

if __name__ == "__main__":
    asyncio.run(test_deepwiki_crawler())