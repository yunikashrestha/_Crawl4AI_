# import asyncio
# from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
# from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator


# async def scrape_single_url():
#     brows_config=BrowserConfig(headless=False,verbose=True)

#     run_config=CrawlerRunConfig(
#         cache_mode=CacheMode.BYPASS,
#         markdown_generator=DefaultMarkdownGenerator(),
#          word_count_threshold=20,

#         only_text=False,
#         css_selector="img.pdp-mod-common-image.gallery-preview-panel__image, h1.pdp-mod-product-badge-title, div.pdp-product-price, div.html-content.pdp-product-highlights",
#         excluded_tags=["header","nav","footer","form","style","script"],
#         scan_full_page=True,
#         js_code="""
#             window.scrollTo(0,document.body.scrollHeight);
#             return True;
#         """,
#         scroll_delay = 1.5,
#         delay_before_return_html=10.0,
#         max_scroll_steps = 3,
#         process_iframes = True,
#         remove_overlay_elements=True,

#         capture_console_messages=False,
#         capture_network_requests=False,
#     )
#     async with AsyncWebCrawler(config=brows_config) as crawler:
#         result=await crawler.arun(url="https://www.daraz.com.np/products/spot-inventory-free-shippingcod-marble-pattern-shell-suitable-for-iphone-16-15-14-13-12-11-propro-maxplus-12-mini-xsmax-xr-xs-x-7p-8-6p-mini-camera-lens-protection-soft-cover-i404804754-s1741847372.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253Acamera%253Bnid%253A404804754%253Bsrc%253ALazadaMainSrp%253Brn%253Adca2cc81e28cbcd8c4f37314e20658d8%253Bregion%253Anp%253Bsku%253A404804754_NP%253Bprice%253A344%253Bclient%253Adesktop%253Bsupplier_id%253A900270384409%253Bbiz_source%253Ah5_external%253Bslot%253A0%253Butlog_bucket_id%253A470687%253Basc_category_id%253A9543%253Bitem_id%253A404804754%253Bsku_id%253A1741847372%253Bshop_id%253A184820%253BtemplateInfo%253A1103_L%2523-1_A3_C%2523&freeshipping=0&fs_ab=1&fuse_fs=&lang=en&location=Overseas&price=344&priceCompare=skuId%3A1741847372%3Bsource%3Alazada-search-voucher%3Bsn%3Adca2cc81e28cbcd8c4f37314e20658d8%3BoriginPrice%3A34400%3BdisplayPrice%3A34400%3BsinglePromotionId%3A50000019218009%3BsingleToolCode%3ApromPrice%3BvoucherPricePlugin%3A0%3Btimestamp%3A1760417170920&ratingscore=5.0&request_id=dca2cc81e28cbcd8c4f37314e20658d8&review=1&sale=3&search=1&source=search&spm=a2a0e.searchlist.list.0&stock=1",config=run_config)

#         if result.success:
#             print("*******Crawled Successfull*******")
#             print(result.markdown)

#             with open("single_url.md","w",encoding="utf-8") as f:
#              f.write(result.markdown)
#             print("******Product Description saved successfully to single_url.md")

#         else:
#             print("*******Failed to fetch the url description****")
    
# async def main():
#     await scrape_single_url()

# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def scrape_multiple_urls():
    brows_config = BrowserConfig(headless=False, verbose=True)

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=DefaultMarkdownGenerator(),
        word_count_threshold=20,
        only_text=False,
        css_selector="img.pdp-mod-common-image.gallery-preview-panel__image, h1.pdp-mod-product-badge-title, div.pdp-product-price, div.html-content.pdp-product-highlights",
        excluded_tags=["header","nav","footer","form","style","script"],
        scan_full_page=True,
        js_code="""
            window.scrollTo(0,document.body.scrollHeight);
            return True;
        """,
        scroll_delay=1.5,
        delay_before_return_html=10.0,
        max_scroll_steps=3,
        process_iframes=True,
        remove_overlay_elements=True,
        capture_console_messages=False,
        capture_network_requests=False,
    )

    # List of URLs obtained previously
    with open("daraj_product_phonecase_links.txt", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    async with AsyncWebCrawler(config=brows_config) as crawler:
        for idx, url in enumerate(urls, start=1):
            print(f"\nScraping URL {idx}/{len(urls)}: {url}")
            result = await crawler.arun(url=url, config=run_config)

            if result.success:
                print("*******Crawled Successfully*******")
                print(result.markdown)

                # Save each product description in a single Markdown file (appending)
                with open("all_products.md", "a", encoding="utf-8") as f:
                    f.write(f"# Product {idx}\n")
                    f.write(f"URL: {url}\n\n")
                    f.write(result.markdown + "\n")
                    f.write("="*80 + "\n")  # separator
                print(f"******Saved product {idx} description******")
            else:
                print(f"*******Failed to fetch URL {url}*******")

async def main():
    await scrape_multiple_urls()

if __name__ == "__main__":
    asyncio.run(main())
