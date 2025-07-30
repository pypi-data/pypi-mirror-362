import asyncio
import argparse
from typing import List
from mcp.server.fastmcp import FastMCP
from openai import AsyncOpenAI
from pydantic import BaseModel
from agents import OpenAIChatCompletionsModel,Agent,Runner,set_default_openai_client, set_tracing_disabled,WebSearchTool
from agents.model_settings import ModelSettings

# 初始化 MCP 服务器
mcp = FastMCP("DeepResearch")
USER_AGENT = "deepresearch-app/1.0"
API_KEY = None

# 创建planner_agent
PROMPT = (
    "You are a helpful research assistant. Given a query, come up with a set of web searches "
    "to perform to best answer the query. Output between 10 and 20 terms to query for."
)


class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query."""


planner_agent = Agent(
    name="PlannerAgent",
    instructions=PROMPT,
    model="o3-mini",
    output_type=WebSearchPlan,
)

# 创建search_agent
INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succinctly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary "
    "itself."
)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
)

# 创建writer_agent
PROMPT_TEMP = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research "
    "assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 10-20 pages of content, at least 1500 words."
    "最终结果请用中文输出。"
)


class ReportData(BaseModel):
    short_summary: str
    """A short 2-3 sentence summary of the findings."""

    markdown_report: str
    """The final report"""

    follow_up_questions: list[str]
    """Suggested topics to research further"""


writer_agent = Agent(
    name="WriterAgent",
    instructions=PROMPT_TEMP,
    model="o3-mini",
    output_type=ReportData,
)

# 辅助函数组
async def _plan_searches(query: str) -> WebSearchPlan:
    """
    用于进行某个搜索主题的搜索规划
    """
    result = await Runner.run(
        planner_agent,
        f"Query: {query}",
    )
    return result.final_output_as(WebSearchPlan)

async def _perform_searches(search_plan: WebSearchPlan) -> List[str]:
    """
    用于实际执行搜索，并组成搜索条目列表
    """
    tasks = [asyncio.create_task(_search(item)) for item in search_plan.searches]
    results = []
    for task in asyncio.as_completed(tasks):
        result = await task
        if result is not None:
            results.append(result)
    return results

async def _search(item: WebSearchItem) -> str | None:
    """
    实际负责进行搜索，并完成每个搜索条目的短文本编写
    """
    try:
        result = await Runner.run(
            search_agent,
            input=f"Search term: {item.query}\nReason for searching: {item.reason}"
        )
        return str(result.final_output)
    except Exception:
        return None
    
async def _write_report(query: str, search_results: List[str]) -> ReportData:
    """
    根据搜索的段文档，编写长文本
    """
    result = await Runner.run(
        writer_agent,
        input=f"Original query: {query}\nSummarized search results: {search_results}",
    )
    return result.final_output_as(ReportData)

# MCP服务器主函数
@mcp.tool()
async def deepresearch(query: str) -> ReportData:
    """
    当用户明确表示需要围绕某个主题进行深入研究时，请调本函数。
    本函数能够围绕用户输入的问题进行联网搜索和深入研究，并创建一篇内容完整的markdown格式的研究报告。
    输入参数query:用户提出的研究主题，以字符串形式表示；
    函数返回结果为一个markdown格式的完整的研究报告文档。
    """
    search_plan = await _plan_searches(query)
    search_results = await _perform_searches(search_plan)
    report = await _write_report(query, search_results)
    return report

def main():
    parser = argparse.ArgumentParser(description="DeepResearch Server")
    parser.add_argument("--openai_api_key", type=str, required=True, help="你的 OpenAI API Key")
    args = parser.parse_args()

    # 初始化 external_client 和设置
    external_client = AsyncOpenAI(
        base_url = "https://use.52apikey.cn/v1",
        api_key = args.openai_api_key,
    )
    set_default_openai_client(external_client)
    set_tracing_disabled(True)
    
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
