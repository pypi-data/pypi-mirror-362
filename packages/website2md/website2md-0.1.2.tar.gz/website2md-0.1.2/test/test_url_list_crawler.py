#!/usr/bin/env python3
"""
Test script for URL list crawler with various input formats
"""

import asyncio
import os
from website2md.url_list_crawler import URLListCrawler
from website2md.config import CrawlConfig

async def test_list_input():
    """Test with Python list input"""
    print("=" * 60)
    print("TEST 1: Python List Input")
    print("=" * 60)
    
    config = CrawlConfig(
        max_pages=5,
        bypass_cache=True,
        max_concurrent_requests=2,
        delay=1.0
    )
    
    crawler = URLListCrawler(config)
    
    # Test with list input
    url_list = [
        "https://httpbin.org/html",
        "https://httpbin.org/json",
        "httpbin.org/xml",  # Missing protocol - should be auto-added
        "https://httpbin.org/uuid",
        "https://httpbin.org/base64/aGVsbG8gd29ybGQ%3D"
    ]
    
    print(f"Input: {url_list}")
    
    summary = await crawler.crawl_url_list(
        url_list,
        "test_list_output",
        allowed_domains=["httpbin.org"]
    )
    
    print(f"Result: {summary['files_saved']} files saved, {summary['errors']} errors")
    print()

async def test_comma_separated():
    """Test with comma-separated string input"""
    print("=" * 60)
    print("TEST 2: Comma-Separated String Input")
    print("=" * 60)
    
    config = CrawlConfig(
        max_pages=3,
        bypass_cache=True,
        max_concurrent_requests=2,
        delay=1.0
    )
    
    crawler = URLListCrawler(config)
    
    # Test with comma-separated input
    url_string = "https://httpbin.org/html, httpbin.org/json, https://httpbin.org/xml"
    
    print(f"Input: {url_string}")
    
    summary = await crawler.crawl_url_list(
        url_string,
        "test_comma_output",
        allowed_domains=["httpbin.org"]
    )
    
    print(f"Result: {summary['files_saved']} files saved, {summary['errors']} errors")
    print()

async def test_line_separated():
    """Test with line-separated string input"""
    print("=" * 60)
    print("TEST 3: Line-Separated String Input")
    print("=" * 60)
    
    config = CrawlConfig(
        max_pages=3,
        bypass_cache=True,
        max_concurrent_requests=2,
        delay=1.0
    )
    
    crawler = URLListCrawler(config)
    
    # Test with line-separated input
    url_string = """https://httpbin.org/html
httpbin.org/json
https://httpbin.org/xml"""
    
    print(f"Input:\n{url_string}")
    
    summary = await crawler.crawl_url_list(
        url_string,
        "test_lines_output"
    )
    
    print(f"Result: {summary['files_saved']} files saved, {summary['errors']} errors")
    print()

async def test_single_url():
    """Test with single URL input"""
    print("=" * 60)
    print("TEST 4: Single URL Input")
    print("=" * 60)
    
    config = CrawlConfig(
        max_pages=1,
        bypass_cache=True,
        max_concurrent_requests=1,
        delay=0.5
    )
    
    crawler = URLListCrawler(config)
    
    # Test with single URL
    single_url = "https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/"
    
    print(f"Input: {single_url}")
    
    summary = await crawler.crawl_url_list(
        single_url,
        "test_single_output_cloudflare_workers_docs_nextjs"
    )
    
    print(f"Result: {summary['files_saved']} files saved, {summary['errors']} errors")
    print()

async def test_domain_filtering():
    """Test domain filtering functionality"""
    print("=" * 60)
    print("TEST 5: Domain Filtering")
    print("=" * 60)
    
    config = CrawlConfig(
        max_pages=10,
        bypass_cache=True,
        max_concurrent_requests=2,
        delay=1.0
    )
    
    crawler = URLListCrawler(config)
    
    # Mixed domains
    mixed_urls = [
        "https://httpbin.org/html",
        "https://example.com",
        "https://httpbin.org/json",
        "https://google.com",
        "https://httpbin.org/xml"
    ]
    
    print(f"Input URLs: {mixed_urls}")
    print("Domain filter: ['httpbin.org']")
    
    summary = await crawler.crawl_url_list(
        mixed_urls,
        "test_domain_output",
        allowed_domains=["httpbin.org"]
    )
    
    print(f"Result: {summary['files_saved']} files saved")
    print(f"URLs parsed: {summary['urls_parsed']}")
    print(f"URLs after filtering: {summary['urls_filtered']}")
    print()

async def test_url_preview():
    """Test URL preview functionality"""
    print("=" * 60)
    print("TEST 6: URL Preview (No Crawling)")
    print("=" * 60)
    
    config = CrawlConfig()
    crawler = URLListCrawler(config)
    
    # Test preview with various formats
    test_inputs = [
        ["https://docs.python.org", "https://docs.python.org/3/tutorial/"],
        "docs.python.org, realpython.com, https://python.org",
        """https://developer.mozilla.org/en-US/docs/Web/JavaScript
https://developer.mozilla.org/en-US/docs/Web/HTML
developer.mozilla.org/en-US/docs/Web/CSS"""
    ]
    
    for i, url_input in enumerate(test_inputs, 1):
        print(f"\nPreview Test {i}:")
        print(f"Input: {url_input}")
        preview = crawler.preview_urls(url_input)
        print(f"Parsed: {preview['urls_parsed']}, Unique: {preview['urls_unique']}")

async def test_invalid_inputs():
    """Test handling of invalid inputs"""
    print("=" * 60)
    print("TEST 7: Invalid Input Handling")
    print("=" * 60)
    
    config = CrawlConfig(max_pages=1)
    crawler = URLListCrawler(config)
    
    # Test invalid inputs
    invalid_inputs = [
        "",  # Empty string
        [],  # Empty list
        "not-a-url",  # Invalid URL
        "mailto:test@example.com",  # Non-http protocol
        ["", "   ", "invalid"],  # List with invalid URLs
    ]
    
    for i, invalid_input in enumerate(invalid_inputs, 1):
        print(f"\nInvalid Test {i}: {invalid_input}")
        try:
            summary = await crawler.crawl_url_list(
                invalid_input,
                f"test_invalid_{i}_output"
            )
            print(f"Result: {summary['urls_parsed']} parsed, {summary['errors']} errors")
        except Exception as e:
            print(f"Exception: {e}")

async def run_all_tests():
    """Run all tests sequentially"""
    print("🧪 URL List Crawler Test Suite")
    print("Testing various input formats and features\n")
    
    tests = [
        test_list_input,
        test_comma_separated,
        test_line_separated,
        test_single_url,
        test_domain_filtering,
        test_url_preview,
        test_invalid_inputs
    ]
    
    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Small delay between tests
        await asyncio.sleep(1)
    
    print("✅ All tests completed!")

async def demo_interactive_features():
    """Demonstrate interactive features"""
    print("=" * 60)
    print("DEMO: Interactive Features")
    print("=" * 60)
    
    config = CrawlConfig(
        max_pages=3,
        bypass_cache=True,
        content_selector="body",
        exclude_selectors=[".navigation", ".sidebar"]
    )
    
    crawler = URLListCrawler(config)
    
    # Demo different input parsing
    demo_inputs = {
        "List format": ["https://httpbin.org/html", "https://httpbin.org/json"],
        "Comma format": "httpbin.org/html, httpbin.org/json",
        "Line format": "httpbin.org/html\nhttpbin.org/json",
        "Single URL": "https://httpbin.org/html"
    }
    
    for format_name, demo_input in demo_inputs.items():
        print(f"\n{format_name}:")
        print(f"Input: {demo_input}")
        
        # Show preview
        preview = crawler.preview_urls(demo_input, ["httpbin.org"])
        print(f"Would crawl {preview['urls_unique']} URLs: {preview['final_urls']}")

if __name__ == "__main__":
    import sys
    asyncio.run(test_single_url())
    
    # if len(sys.argv) > 1:
    #     if sys.argv[1] == "demo":
    #         asyncio.run(demo_interactive_features())
    #     elif sys.argv[1] == "quick":
    #         # Run just a few quick tests
    #         asyncio.run(test_url_preview())
    #     else:
    #         print("Usage: python test_url_list_crawler.py [demo|quick]")
    # else:
    #     asyncio.run(run_all_tests())