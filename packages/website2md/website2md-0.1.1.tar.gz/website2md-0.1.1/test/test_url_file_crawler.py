#!/usr/bin/env python3
"""
Test script for URL file crawler using the Cursor URLs
"""

import asyncio
import os
from website2md.url_file_crawler import URLFileCrawler
from website2md.config import CrawlConfig

async def test_cursor_urls():
    """Test crawling URLs from the Cursor URL file"""
    
    # Configuration for Cursor docs
    config = CrawlConfig(
        max_pages=100,  # Limit for testing
        bypass_cache=True,
        timeout=60,
        max_concurrent_requests=3,
        delay=1.0,
        content_selector="article",  # Main content
        exclude_selectors=[
            ".sidebar", 
            ".nav", 
            ".header", 
            ".footer", 
            ".breadcrumb",
            ".toc"
        ]
    )
    
    # File paths
    url_file = "txt/opennext-js.txt"
    output_dir = "opennext_next_js_docs_from_file"
    
    print("Testing URL File Crawler with Cursor documentation")
    print(f"URL file: {url_file}")
    print(f"Output directory: {output_dir}")
    print("="*60)
    
    # Initialize crawler
    crawler = URLFileCrawler(config)
    
    try:
        # Test URL reading and deduplication first
        print("\n1. Reading and processing URLs...")
        raw_urls = crawler.read_urls_from_file(url_file)
        print(f"   Raw URLs found: {len(raw_urls)}")
        
        # Filter to Cursor domains only
        cursor_domains = ['opennext.js.org']
        filtered_urls = crawler.filter_urls_by_domain(raw_urls, cursor_domains)
        print(f"   After domain filtering: {len(filtered_urls)}")
        
        # Deduplicate
        unique_urls = crawler.deduplicate_urls(filtered_urls)
        print(f"   After deduplication: {len(unique_urls)}")
        
        # Show sample URLs
        print(f"\nSample unique URLs:")
        for i, url in enumerate(sorted(unique_urls)[:5]):
            print(f"   {i+1}. {url}")
        if len(unique_urls) > 5:
            print(f"   ... and {len(unique_urls) - 5} more")
        
        print(f"\n2. Starting crawl...")
        print("-" * 40)
        
        # Run the full crawl
        summary = await crawler.crawl_urls_from_file(
            url_file, 
            output_dir, 
            allowed_domains=cursor_domains
        )
        
        # Print results
        print("\n" + "="*60)
        print("CRAWL SUMMARY")
        print("="*60)
        print(f"URLs found in file: {summary.get('urls_found', 0)}")
        print(f"URLs after filtering: {summary.get('urls_filtered', 0)}")
        print(f"Unique URLs: {summary.get('urls_unique', 0)}")
        print(f"Pages crawled: {summary.get('pages_crawled', 0)}")
        print(f"Files saved: {summary.get('files_saved', 0)}")
        print(f"Files skipped: {summary.get('files_skipped', 0)}")
        print(f"Errors: {summary.get('errors', 0)}")
        
        if summary.get('error_details'):
            print(f"\nErrors encountered:")
            for error in summary['error_details'][:3]:  # Show first 3 errors
                print(f"  - {error}")
            if len(summary['error_details']) > 3:
                print(f"  ... and {len(summary['error_details']) - 3} more errors")
        
        print(f"\nOutput directory: {output_dir}")
        print("Test completed!")
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

async def test_url_processing_only():
    """Test just the URL processing without crawling"""
    
    config = CrawlConfig()
    crawler = URLFileCrawler(config)
    url_file = "txt/opennext-js.txt"
    
    print("Testing URL processing (no crawling)...")
    print("-" * 40)
    
    try:
        # Read URLs
        raw_urls = crawler.read_urls_from_file(url_file)
        print(f"Raw URLs: {len(raw_urls)}")
        
        # Show first few raw URLs
        print("\nFirst 5 raw URLs:")
        for i, url in enumerate(sorted(raw_urls)[:5]):
            print(f"  {i+1}. {url}")
            
        # Filter by domain
        cursor_urls = crawler.filter_urls_by_domain(raw_urls, ['opennext.js.org'])
        print(f"\nCursor docs URLs: {len(cursor_urls)}")
        
        # Deduplicate
        unique_urls = crawler.deduplicate_urls(cursor_urls)
        print(f"Unique Cursor docs URLs: {len(unique_urls)}")
        
        print("\nUnique Cursor docs URLs:")
        for i, url in enumerate(sorted(unique_urls)):
            print(f"  {i+1}. {url}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--process-only":
        asyncio.run(test_url_processing_only())
    else:
        asyncio.run(test_cursor_urls())