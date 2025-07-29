#!/usr/bin/env python3
"""
Limited test for Cloudflare Workers documentation
"""

import asyncio
import os
from website2md.doc_crawler import DocSiteCrawler
from website2md.config import CrawlConfig

async def test_cloudflare_workers_limited():
    """Test with limited pages to validate configuration"""
    
    config = CrawlConfig(
        max_pages=10,  # Limit to 10 pages for testing
        bypass_cache=True,
        timeout=60,
        max_concurrent_requests=2,
        delay=2.0,
        content_selector="main",
        exclude_selectors=[
            "#starlight__sidebar",
            "starlight-toc", 
            ".header",
            ".footer",
            ".breadcrumb"
        ]
    )
    
    start_url = "https://developers.cloudflare.com/workers/"
    output_dir = "cf_workers_test"
    
    print(f"Limited test: {start_url}")
    print(f"Max pages: {config.max_pages}")
    print("-" * 40)
    
    os.makedirs(output_dir, exist_ok=True)
    
    crawler = DocSiteCrawler(config)
    summary = await crawler.crawl_documentation_site(start_url, output_dir)
    
    print("\nTest Results:")
    print(f"URLs discovered: {summary.get('urls_discovered', 0)}")
    print(f"Pages crawled: {summary.get('pages_crawled', 0)}")
    print(f"Files saved: {summary.get('files_saved', 0)}")
    
    # Check first file content
    files = os.listdir(output_dir)
    if files:
        sample_file = os.path.join(output_dir, files[0])
        print(f"\nSample file: {files[0]}")
        with open(sample_file, 'r') as f:
            content = f.read()[:500]
            print(f"Content preview:\n{content}...")

if __name__ == "__main__":
    asyncio.run(test_cloudflare_workers_limited())