from crawl4ai import BrowserConfig, ProxyConfig
def BrowserConfig(
    
    browser_type: str = "chromium",
    headless: bool = True,
    browser_mode: str = "dedicated",
    use_managed_browser: bool = False,
    cdp_url: str = None,
    use_persistent_context: bool = False,
    user_data_dir: str = None,
    chrome_channel: str = "chromium",
    channel: str = "chromium",
    proxy: str = None,
    proxy_config: ProxyConfig | dict | None = None,
    viewport_width: int = 1080,
    viewport_height: int = 600,
    viewport: dict = None,
    accept_downloads: bool = False,
    downloads_path: str = None,
    storage_state: str | dict | None = None,
    ignore_https_errors: bool = True,
    java_script_enabled: bool = True,
    sleep_on_close: bool = False,
    verbose: bool = True,
    cookies: list = None,
    headers: dict = None,
    user_agent: str = "Mozilla/5.0 (X11; Linux x86_64)",
    user_agent_mode: str = "",
    user_agent_generator_config: dict = {},
    text_mode: bool = False,
    light_mode: bool = False,
    extra_args: list = None,
    debugging_port: int = 9222,
    host: str = "localhost",
    enable_stealth: bool = False
) -> BrowserConfig:
    """
    
    Configuration class for controlling the behavior of the browser instance 
    used in web crawling and scraping via Playwright.

    Parameters
    ----------
    browser_type : str, default="chromium"
        The browser type to use. Supported options: "chromium", "firefox", "webkit".
    headless : bool, default=True
        Run the browser in headless mode (no UI). Set to False to see browser actions.
    browser_mode : str, default="dedicated"
        Determines browser instance behavior ("dedicated" for isolated, "shared" for reuse).
    use_managed_browser : bool, default=False
        Whether to use a pre-managed browser instance.
    cdp_url : str, optional
        Chrome DevTools Protocol URL for connecting to an existing browser session.
    use_persistent_context : bool, default=False
        Enables persistent browser sessions with saved cookies and local storage.
    user_data_dir : str, optional
        Directory path to store persistent user data.
    chrome_channel : str, default="chromium"
        Chrome release channel (e.g., "chrome", "chrome-beta").
    channel : str, default="chromium"
        Alias for browser channel, often redundant with `chrome_channel`.
    proxy : str, optional
        Proxy URL string in the format `http://user:pass@host:port`.
    proxy_config : ProxyConfig | dict, optional
        Detailed proxy configuration object or dictionary.
    viewport_width : int, default=1080
        Default browser viewport width in pixels.
    viewport_height : int, default=600
        Default browser viewport height in pixels.
    viewport : dict, optional
        Custom viewport configuration dictionary, e.g., {"width": 1280, "height": 720}.
    accept_downloads : bool, default=False
        Allow browser to automatically handle file downloads.
    downloads_path : str, optional
        Directory where downloads should be saved.
    storage_state : str | dict, optional
        Path to or object representing browser storage state (cookies/local storage).
    ignore_https_errors : bool, default=True
        Whether to ignore SSL certificate errors during navigation.
    java_script_enabled : bool, default=True
        Enable or disable JavaScript execution.
    sleep_on_close : bool, default=False
        Delay browser closure for debugging or throttling.
    verbose : bool, default=True
        Enables detailed logging for browser events and errors.
    cookies : list, optional
        List of cookies to load into the browser session.
    headers : dict, optional
        Custom HTTP headers to include in all browser requests.
    user_agent : str, default="Mozilla/5.0 (X11; Linux x86_64)"
        Custom User-Agent string to simulate browser identity.
    user_agent_mode : str, optional
        Mode for selecting User-Agent (e.g., "mobile", "desktop", or "random").
    user_agent_generator_config : dict, optional
        Configuration options for random or custom User-Agent generation.
    text_mode : bool, default=False
        Disables heavy rendering to extract only textual data for faster crawling.
    light_mode : bool, default=False
        Reduces resource usage for low-performance systems.
    extra_args : list, optional
        Additional command-line arguments to pass to the browser instance.
    debugging_port : int, default=9222
        Port used for remote debugging connections.
    host : str, default="localhost"
        Host address for the browser debugging server.
    enable_stealth : bool, default=False
        Enables stealth mode to evade bot detection (hides automation traces).

    Returns
    -------
    BrowserConfig
        A fully configured browser settings object for Crawl4AI.
    """

class CrawlerRunConfig:
    
    """
    Configuration class that defines how Crawl4AI performs a crawl or scrape run,
    including extraction, rendering, waiting, caching, and content filtering.

    Parameters
    ----------
    word_count_threshold : int, default=MIN_WORD_THRESHOLD
        Minimum number of words required to consider a page or section valid.
    extraction_strategy : ExtractionStrategy, optional
        Strategy to extract data (e.g., JSON, CSS, XPath-based).
    chunking_strategy : ChunkingStrategy, default=RegexChunking()
        Defines how to split large text into smaller chunks.
    markdown_generator : MarkdownGenerationStrategy, default=DefaultMarkdownGenerator()
        Converts extracted HTML/text into structured Markdown output.
    only_text : bool, default=False
        If True, extracts only textual content and ignores HTML structure.
    css_selector : str, optional
        CSS selector to target specific page elements for scraping.
    target_elements : list[str], optional
        List of HTML tags or selectors to focus the extraction on.
    excluded_tags : list, optional
        HTML tags to exclude (e.g., ['script', 'style']).
    excluded_selector : str, optional
        CSS selector of elements to ignore.
    keep_data_attributes : bool, default=False
        Retains HTML `data-*` attributes in the extracted content.
    keep_attrs : list, optional
        List of HTML attributes to preserve (e.g., ['href', 'src']).
    remove_forms : bool, default=False
        Removes `<form>` elements to avoid unnecessary content.
    prettiify : bool, default=False
        Beautifies the output HTML for readability.
    parser_type : str, default="lxml"
        Parser type used to process HTML content ("lxml" or "html.parser").
    scraping_strategy : ContentScrapingStrategy, optional
        Advanced control for scraping logic (like lazy loading, JS-rendering).
    proxy_config : ProxyConfig | dict, optional
        Proxy settings for network requests.
    proxy_rotation_strategy : ProxyRotationStrategy, optional
        Strategy for rotating proxies during multi-page crawls.
    locale : str, optional
        Locale setting for the browser (e.g., "en-US").
    timezone_id : str, optional
        Sets the browser’s timezone.
    geolocation : GeolocationConfig, optional
        Simulates a geographic location for geo-sensitive pages.
    fetch_ssl_certificate : bool, default=False
        Fetches SSL certificate data for analysis.
    cache_mode : CacheMode, default=CacheMode.BYPASS
        Controls caching behavior (e.g., BYPASS, READ_WRITE, FORCE).
    session_id : str, optional
        Unique ID for identifying or persisting sessions.
    bypass_cache : bool, default=False
        Skips cache usage regardless of mode.
    disable_cache : bool, default=False
        Completely disables cache reads and writes.
    no_cache_read : bool, default=False
        Prevents cache from being read during this run.
    no_cache_write : bool, default=False
        Prevents new cache entries from being stored.
    shared_data : dict, optional
        Custom shared context data across multiple crawls.
    wait_until : str, default="domcontentloaded"
        When to consider the page fully loaded ("load", "networkidle", etc.).
    page_timeout : int, default=PAGE_TIMEOUT
        Maximum wait time (in ms) before aborting a page load.
    wait_for : str, optional
        CSS selector or condition to wait for before extraction.
    wait_for_timeout : int, optional
        Maximum waiting time for `wait_for` condition.
    wait_for_images : bool, default=False
        Waits for all images to load before extraction.
    delay_before_return_html : float, default=0.1
        Adds a small delay before returning rendered HTML.
    mean_delay : float, default=0.1
        Average delay between crawl steps to mimic human browsing.
    max_range : float, default=0.3
        Randomized delay factor for timing variation.
    semaphore_count : int, default=5
        Number of concurrent tasks allowed during crawl.
    js_code : str | list[str], optional
        JavaScript code(s) to inject and execute before scraping.
    c4a_script : str | list[str], optional
        Internal Crawl4AI scripts for advanced DOM manipulations.
    js_only : bool, default=False
        Extracts data exclusively from JavaScript-rendered content.
    ignore_body_visibility : bool, default=True
        Ignores hidden elements during extraction.
    scan_full_page : bool, default=False
        Scrolls and loads the entire page before extraction.
    scroll_delay : float, default=0.2
        Delay between each scroll step during infinite-scroll pages.
    max_scroll_steps : int, optional
        Maximum number of scroll iterations.
    process_iframes : bool, default=False
        Enables crawling within `<iframe>` elements.
    remove_overlay_elements : bool, default=False
        Removes modal overlays or cookie banners before extraction.
    simulate_user : bool, default=False
        Simulates user activity (mouse, keyboard) to trigger lazy loads.
    override_navigator : bool, default=False
        Overrides `navigator` object for anti-bot evasion.
    magic : bool, default=False
        Enables heuristic-based “smart” scraping improvements.
    adjust_viewport_to_content : bool, default=False
        Dynamically resizes viewport based on page content.
    screenshot : bool, default=False
        Captures screenshots of the page.
    screenshot_wait_for : float, optional
        Wait duration before taking a screenshot.
    screenshot_height_threshold : int, default=SCREENSHOT_HEIGHT_TRESHOLD
        Page height threshold to control screenshot cropping.
    pdf : bool, default=False
        Exports the rendered page as a PDF.
    capture_mhtml : bool, default=False
        Saves page as an MHTML (web archive) file.
    image_description_min_word_threshold : int, default=IMAGE_DESCRIPTION_MIN_WORD_THRESHOLD
        Minimum text required for AI-based image description.
    image_score_threshold : int, default=IMAGE_SCORE_THRESHOLD
        Image quality score threshold for filtering.
    table_score_threshold : int, default=7
        Table structure detection threshold.
    table_extraction : TableExtractionStrategy, optional
        Strategy to extract HTML tables into structured data.
    exclude_external_images : bool, default=False
        Excludes images hosted on external domains.
    exclude_all_images : bool, default=False
        Removes all images from extracted content.
    exclude_social_media_domains : list, optional
        List of social media domains to ignore (e.g., ["facebook.com"]).
    exclude_external_links : bool, default=False
        Excludes all outbound links.
    exclude_social_media_links : bool, default=False
        Removes social media links.
    exclude_domains : list, optional
        Domains to exclude during deep crawls.
    exclude_internal_links : bool, default=False
        Ignores internal (same-site) links.
    score_links : bool, default=False
        Assigns importance scores to hyperlinks.
    verbose : bool, default=True
        Enables detailed logging output.
    log_console : bool, default=False
        Captures browser console logs.
    capture_network_requests : bool, default=False
        Records network requests made during page load.
    capture_console_messages : bool, default=False
        Logs browser console messages.
    method : str, default="GET"
        HTTP method for requests.
    stream : bool, default=False
        Streams large responses instead of loading all at once.
    url : str, optional
        Target URL to crawl.
    check_robots_txt : bool, default=False
        Checks and respects `robots.txt` crawling rules.
    user_agent : str, optional
        Custom User-Agent string for this run.
    user_agent_mode : str, optional
        Mode for User-Agent selection ("random", "mobile", etc.).
    user_agent_generator_config : dict, optional
        Settings for generating randomized User-Agents.
    deep_crawl_strategy : DeepCrawlStrategy, optional
        Defines recursive crawling and link discovery behavior.
    link_preview_config : LinkPreviewConfig | dict, optional
        Configuration for generating link previews.
    virtual_scroll_config : VirtualScrollConfig | dict, optional
        Parameters for simulating scrolling-based loading.
    url_matcher : UrlMatcher, optional
        Filters which URLs are crawled based on patterns.
    match_mode : MatchMode, default=MatchMode.OR
        Defines URL matching logic ("AND", "OR").
    experimental : dict, optional
        Reserved for experimental Crawl4AI features.

    Returns
    -------
    CrawlerRunConfig
        A configuration object specifying crawl runtime behavior.
    """

