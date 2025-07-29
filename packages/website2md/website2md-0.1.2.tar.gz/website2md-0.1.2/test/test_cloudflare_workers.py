#!/usr/bin/env python3
"""
Test script for crawling Cloudflare Workers documentation
Target: https://developers.cloudflare.com/workers/
"""

import asyncio
import os
from website2md.doc_crawler import DocSiteCrawler
from website2md.config import CrawlConfig

async def test_cloudflare_workers():
    """Test crawling Cloudflare Workers documentation with specific selectors"""
    
    # Configuration for Cloudflare Workers docs
    config = CrawlConfig(
        max_pages=1,  # Start with limited pages for testing
        bypass_cache=True,
        timeout=60,
        max_concurrent_requests=2,  # Be respectful to Cloudflare
        delay=2.0,  # Longer delay for external site
        content_selector="main",  # Main content area
        exclude_selectors=[
            "#starlight__sidebar",  # Left sidebar
            "starlight-toc",       # Right TOC
            ".header", 
            ".footer", 
            ".breadcrumb",
            ".navigation"
        ]
    )
    
    # Target URL
    start_url = "https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/"
    output_dir = "cloudflare_workers_docs_nextjs"
    
    print(f"Testing Cloudflare Workers documentation crawl")
    print(f"Target URL: {start_url}")
    print(f"Output directory: {output_dir}")
    print(f"Content selector: main")
    print(f"Excluding: {config.exclude_selectors}")
    print("-" * 60)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize crawler
    crawler = DocSiteCrawler(config)
    
    try:
        # Run the crawl
        summary = await crawler.crawl_documentation_site(start_url, output_dir)
        
        # Print results
        print("\n" + "="*60)
        print("CRAWL SUMMARY")
        print("="*60)
        print(f"URLs discovered: {summary.get('urls_discovered', 0)}")
        print(f"Pages crawled: {summary.get('pages_crawled', 0)}")
        print(f"Files saved: {summary.get('files_saved', 0)}")
        print(f"Files skipped: {summary.get('files_skipped', 0)}")
        print(f"Errors: {summary.get('errors', 0)}")
        
        if summary.get('error_details'):
            print("\nError details:")
            for error in summary['error_details']:
                print(f"  - {error}")
        
        print(f"\nOutput directory: {output_dir}")
        print("Test completed!")
        
    except Exception as e:
        print(f"Error during crawl: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_cloudflare_workers())