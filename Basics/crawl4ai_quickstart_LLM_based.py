import os,json,asyncio
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,LLMConfig,CacheMode#configures the LLM (OpenAI, Ollama, etc.).
from crawl4ai import LLMExtractionStrategy #nstructs Crawl4AI to extract data using an LLM rather than static CSS selectors. 
from pydantic import BaseModel, Field #defines a data schema for structured data

class OpenaiModelFee(BaseModel):
    model_name:str=Field(...,description="Name of OpenAI model")
    inputfee:str=Field(...,description="Fee for input token")
    outputfee:str=Field(...,description="Fee for output token")

async def extract_structured_data_using_llm(provider:str,api_token:str=None,extra_header:dict[str,str]=None):
    print("Extracting structured data using {provider}")

    if api_token is None and provider!="ollama/gemma3:1b-it-qat":
        print("API token is required for {provider}")
        return
    
    browser_config=BrowserConfig(headless=True)
    extra_args={"temperature":0,"top_p":0.9,"max_tokens":2000}#deterministic o/p probabilistic  sampling max o/p length
    if extra_header:
        extra_args["extra_header"]=extra_header

    crawler_config=CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=LLMExtractionStrategy(
            llm_config=LLMConfig(provider=provider,api_token=api_token),
            schema=OpenaiModelFee.model_json_schema(),
            extraction_type="schema",
            instruction="""From the crawled content, extract all mentioned model names along with their fees for input and output tokens. 
            Do not miss any models in the entire content.""",
            extra_args=extra_args,
        ),
        )
    async with AsyncWebCrawler() as crawler:
        result=await crawler.arun(url="https://openai.com/api/pricing/",config=crawler_config)
        print(result.extracted_content)

if __name__=="__main__":
        asyncio.run(extract_structured_data_using_llm(provider="ollama/gemma3:1b-it-qat"))
    

