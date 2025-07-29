import json
import logging
import operator
import os
import shutil
from typing import Annotated, Any

from langgraph.graph import END, START, StateGraph
from langgraph.graph.graph import CompiledGraph
from typing_extensions import TypedDict

from airas.retrieve.retrieve_paper_from_query_subgraph2.input_data import (
    retrieve_paper_from_query_subgraph_input_data,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.nodes.extract_github_url_from_text import (
    extract_github_url_from_text,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.nodes.extract_paper_title import (
    extract_paper_title,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.nodes.openai_websearch_titles import (
    openai_websearch_titles,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.nodes.retrieve_arxiv_text_from_url import (
    retrieve_arxiv_text_from_url,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.nodes.search_arxiv import (
    search_arxiv,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.nodes.select_best_paper import (
    select_best_paper,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.nodes.summarize_paper import (
    summarize_paper,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.nodes.web_scrape import (
    web_scrape,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.prompt.extract_github_url_prompt import (
    extract_github_url_from_text_prompt,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.prompt.extract_paper_title_prompt import (
    extract_paper_title_prompt,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.prompt.openai_websearch_titles_prompt import (
    openai_websearch_titles_prompt,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.prompt.select_best_paper_prompt import (
    select_base_paper_prompt,
)
from airas.retrieve.retrieve_paper_from_query_subgraph2.prompt.summarize_paper_prompt import (
    summarize_paper_prompt,
)
from airas.typing.paper import CandidatePaperInfo
from airas.utils.check_api_key import check_api_key
from airas.utils.execution_timers import ExecutionTimeState, time_node
from airas.utils.logging_utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

retrieve_str = "retrieve_paper_from_query_subgraph"
retrieve_paper_from_query_timed = lambda f: time_node(retrieve_str)(f)  # noqa: E731


class RetrievePaperFromQueryInputState(TypedDict):
    base_queries: list[str]


class RetrievePaperFromQueryHiddenState(TypedDict):
    scraped_results: list[dict]
    extracted_paper_titles: list[str]
    search_paper_list: list[dict]
    search_paper_count: int
    paper_full_text: str
    github_url: str
    process_index: int
    candidate_base_papers_info_list: Annotated[list[CandidatePaperInfo], operator.add]
    selected_base_paper_arxiv_id: str
    selected_base_paper_info: CandidatePaperInfo


class RetrievePaperFromQueryOutputState(TypedDict):
    base_github_url: str
    base_method_text: CandidatePaperInfo


class RetrievePaperFromQueryState(
    RetrievePaperFromQueryInputState,
    RetrievePaperFromQueryHiddenState,
    RetrievePaperFromQueryOutputState,
    ExecutionTimeState,
):
    pass


class RetrievePaperFromQuerySubgraph:
    def __init__(
        self,
        llm_name: str,
        save_dir: str,
        scrape_urls: list,
        arxiv_query_batch_size: int = 10,
        arxiv_num_retrieve_paper: int = 1,
        arxiv_period_days: int | None = None,
        use_openai_websearch: bool = False,
    ):
        self.llm_name = llm_name
        self.save_dir = save_dir
        self.scrape_urls = scrape_urls
        self.arxiv_query_batch_size = arxiv_query_batch_size
        self.arxiv_num_retrieve_paper = arxiv_num_retrieve_paper
        self.arxiv_period_days = arxiv_period_days
        self.use_openai_websearch = use_openai_websearch

        self.papers_dir = os.path.join(self.save_dir, "papers")
        self.selected_papers_dir = os.path.join(self.save_dir, "selected_papers")
        os.makedirs(self.papers_dir, exist_ok=True)
        os.makedirs(self.selected_papers_dir, exist_ok=True)
        check_api_key(
            llm_api_key_check=True,
            fire_crawl_api_key_check=not self.use_openai_websearch,
        )

    def _initialize_state(
        self, state: RetrievePaperFromQueryState
    ) -> dict[str, list[str] | list[CandidatePaperInfo] | int]:
        return {
            "base_queries": state["base_queries"],
            "process_index": 0,
            "candidate_base_papers_info_list": [],
        }

    @retrieve_paper_from_query_timed
    def _web_scrape_node(
        self, state: RetrievePaperFromQueryState
    ) -> dict[str, list[str]]:
        scraped_results = web_scrape(
            queries=state["base_queries"],  # TODO: also scrape abstracts
            scrape_urls=self.scrape_urls,
        )
        return {"scraped_results": scraped_results}

    @retrieve_paper_from_query_timed
    def _extract_paper_title_node(
        self, state: RetrievePaperFromQueryState
    ) -> dict[str, list[str]]:
        extracted_paper_titles = extract_paper_title(
            llm_name="o3-mini-2025-01-31",
            queries=state["base_queries"],
            scraped_results=state["scraped_results"],
            prompt_template=extract_paper_title_prompt,
        )
        return {"extracted_paper_titles": extracted_paper_titles}

    @retrieve_paper_from_query_timed
    def _openai_websearch_titles_node(
        self, state: RetrievePaperFromQueryState
    ) -> dict[str, list[str]]:
        extracted_paper_titles = openai_websearch_titles(
            queries=state["base_queries"],
            max_results=5,
            sleep_sec=60.0,
            prompt_template=openai_websearch_titles_prompt,
            conference_preference="NeurIPS, ICML, ICLR, ICML",
        )
        return {"extracted_paper_titles": extracted_paper_titles or []}

    def _check_extracted_titles(self, state: RetrievePaperFromQueryState) -> str:
        logger.info("check_extracted_titles")
        if not state.get("extracted_paper_titles"):
            return "Stop"
        return "Continue"

    @retrieve_paper_from_query_timed
    def _search_arxiv_node(
        self, state: RetrievePaperFromQueryState
    ) -> dict[str, list[dict[Any, Any]] | int]:
        extract_paper_titles = state["extracted_paper_titles"]
        if not extract_paper_titles:
            return {
                "search_paper_list": [],
                "search_paper_count": 0,
            }
        batch_paper_titles = extract_paper_titles[
            : min(len(extract_paper_titles), self.arxiv_query_batch_size)
        ]
        search_paper_list = search_arxiv(
            queries=batch_paper_titles,
            num_retrieve_paper=self.arxiv_num_retrieve_paper,
        )
        return {
            "search_paper_list": search_paper_list,
            "search_paper_count": len(search_paper_list),
        }

    @retrieve_paper_from_query_timed
    def _retrieve_arxiv_text_from_url_node(
        self, state: RetrievePaperFromQueryState
    ) -> dict[str, str]:
        process_index = state["process_index"]
        logger.info(f"process_index: {process_index}")
        paper_info = state["search_paper_list"][process_index]
        paper_full_text = retrieve_arxiv_text_from_url(
            papers_dir=self.papers_dir, arxiv_url=paper_info["arxiv_url"]
        )
        return {"paper_full_text": paper_full_text}

    @retrieve_paper_from_query_timed
    def _extract_github_url_from_text_node(
        self, state: RetrievePaperFromQueryState
    ) -> dict[str, str | int]:
        paper_full_text = state["paper_full_text"]
        process_index = state["process_index"]
        paper_summary = state["search_paper_list"][process_index]["summary"]
        github_url = extract_github_url_from_text(
            text=paper_full_text,
            paper_summary=paper_summary,
            llm_name="gemini-2.0-flash-001",
            prompt_template=extract_github_url_from_text_prompt,
        )
        # If GitHub URL cannot be obtained, advance Process Index to process the next paper
        process_index = process_index + 1 if github_url == "" else process_index
        return {"github_url": github_url, "process_index": process_index}

    def _check_github_urls(self, state: RetrievePaperFromQueryState) -> str:
        if state["github_url"] == "":
            if state["process_index"] < state["search_paper_count"]:
                return "Next paper"
            return "All complete"
        else:
            return "Generate paper summary"

    @retrieve_paper_from_query_timed
    def _summarize_paper_node(
        self, state: RetrievePaperFromQueryState
    ) -> dict[str, list[CandidatePaperInfo] | int]:
        process_index = state["process_index"]
        (
            main_contributions,
            methodology,
            experimental_setup,
            limitations,
            future_research_directions,
        ) = summarize_paper(
            llm_name="gemini-2.0-flash-001",
            prompt_template=summarize_paper_prompt,
            paper_text=state["paper_full_text"],
        )

        paper_info = state["search_paper_list"][process_index]
        candidate_papers_info = {
            "arxiv_id": paper_info["arxiv_id"],
            "arxiv_url": paper_info["arxiv_url"],
            "title": paper_info.get("title", ""),
            "authors": paper_info.get("authors", ""),
            "published_date": paper_info.get("published_date", ""),
            "journal": paper_info.get("journal", ""),
            "doi": paper_info.get("doi", ""),
            "summary": paper_info.get("summary", ""),
            "github_url": state["github_url"],
            "main_contributions": main_contributions,
            "methodology": methodology,
            "experimental_setup": experimental_setup,
            "limitations": limitations,
            "future_research_directions": future_research_directions,
        }
        return {
            "process_index": process_index + 1,
            "candidate_base_papers_info_list": [
                CandidatePaperInfo(**candidate_papers_info)
            ],
        }

    def _check_paper_count(self, state: RetrievePaperFromQueryState) -> str:
        if state["process_index"] < state["search_paper_count"]:
            return "Next paper"
        return "All complete"

    @retrieve_paper_from_query_timed
    def _select_best_paper_node(
        self, state: RetrievePaperFromQueryState
    ) -> dict[str, str | CandidatePaperInfo | None]:
        candidate_papers_info_list = state["candidate_base_papers_info_list"]
        # TODO: I feel like the control of the number of paper searches is not working well
        selected_arxiv_ids = select_best_paper(
            llm_name="gemini-2.0-flash-001",
            prompt_template=select_base_paper_prompt,
            candidate_papers=candidate_papers_info_list,
        )

        # Get information of selected paper
        selected_arxiv_id = selected_arxiv_ids[0]
        selected_paper_info = next(
            (
                paper_info
                for paper_info in candidate_papers_info_list
                if paper_info["arxiv_id"] == selected_arxiv_id
            ),
            None,
        )
        # Copy selected paper to a separate directory
        for ext in ["txt", "pdf"]:
            source_path = os.path.join(self.papers_dir, f"{selected_arxiv_id}.{ext}")
            if os.path.exists(source_path):
                shutil.copy(
                    source_path,
                    os.path.join(
                        self.selected_papers_dir, f"{selected_arxiv_id}.{ext}"
                    ),
                )
        return {
            "selected_base_paper_arxiv_id": selected_arxiv_id,
            "selected_base_paper_info": selected_paper_info,
        }

    def _prepare_state(
        self, state: RetrievePaperFromQueryState
    ) -> dict[str, str | CandidatePaperInfo]:
        select_base_paper_info = state["selected_base_paper_info"]
        return {
            "base_github_url": select_base_paper_info["github_url"],
            "base_method_text": select_base_paper_info,
        }

    def build_graph(self) -> CompiledGraph:
        graph_builder = StateGraph(RetrievePaperFromQueryState)

        # Add all nodes
        graph_builder.add_node("initialize_state", self._initialize_state)
        graph_builder.add_node("web_scrape_node", self._web_scrape_node)
        graph_builder.add_node(
            "extract_paper_title_node", self._extract_paper_title_node
        )
        graph_builder.add_node(
            "openai_websearch_titles_node", self._openai_websearch_titles_node
        )
        graph_builder.add_node(
            "search_arxiv_node", self._search_arxiv_node
        )  # TODO: END if search results are empty
        graph_builder.add_node(
            "retrieve_arxiv_text_from_url_node", self._retrieve_arxiv_text_from_url_node
        )
        graph_builder.add_node(
            "extract_github_url_from_text_node", self._extract_github_url_from_text_node
        )
        graph_builder.add_node("summarize_paper_node", self._summarize_paper_node)
        graph_builder.add_node("select_best_paper_node", self._select_best_paper_node)
        graph_builder.add_node("prepare_state", self._prepare_state)

        # Add edges based on configuration
        graph_builder.add_edge(START, "initialize_state")

        if self.use_openai_websearch:
            # OpenAI Web Search path (direct title search)
            graph_builder.add_edge("initialize_state", "openai_websearch_titles_node")
            graph_builder.add_conditional_edges(
                source="openai_websearch_titles_node",
                path=self._check_extracted_titles,
                path_map={
                    "Stop": END,
                    "Continue": "search_arxiv_node",
                },
            )
        else:
            # Traditional path (web scrape + extract titles)
            graph_builder.add_edge("initialize_state", "web_scrape_node")
            graph_builder.add_edge("web_scrape_node", "extract_paper_title_node")
            graph_builder.add_conditional_edges(
                source="extract_paper_title_node",
                path=self._check_extracted_titles,
                path_map={
                    "Stop": END,
                    "Continue": "search_arxiv_node",
                },
            )

        # Common edges after title extraction
        graph_builder.add_edge("search_arxiv_node", "retrieve_arxiv_text_from_url_node")
        graph_builder.add_edge(
            "retrieve_arxiv_text_from_url_node", "extract_github_url_from_text_node"
        )
        graph_builder.add_conditional_edges(
            source="extract_github_url_from_text_node",
            path=self._check_github_urls,
            path_map={
                "Next paper": "retrieve_arxiv_text_from_url_node",
                "Generate paper summary": "summarize_paper_node",
                "All complete": "select_best_paper_node",
            },
        )
        graph_builder.add_conditional_edges(
            source="summarize_paper_node",
            path=self._check_paper_count,
            path_map={
                "Next paper": "retrieve_arxiv_text_from_url_node",
                "All complete": "select_best_paper_node",
            },
        )
        graph_builder.add_edge("select_best_paper_node", "prepare_state")
        graph_builder.add_edge("prepare_state", END)
        return graph_builder.compile()

    def run(self, state: dict[str, Any], config: dict | None = None) -> dict[str, Any]:
        config = {**{"recursion_limit": 100}, **(config or {})}

        input_state_keys = RetrievePaperFromQueryInputState.__annotations__.keys()
        output_state_keys = RetrievePaperFromQueryOutputState.__annotations__.keys()

        input_state = {k: state[k] for k in input_state_keys if k in state}
        result = self.build_graph().invoke(input_state, config=config or {})
        output_state = {k: result[k] for k in output_state_keys if k in result}

        cleaned_state = {k: v for k, v in state.items() if k != "subgraph_name"}

        return {
            "subgraph_name": self.__class__.__name__,
            **cleaned_state,
            **output_state,
        }


def main():
    scrape_urls = [
        "https://icml.cc/virtual/2024/papers.html?filter=title",
        # "https://iclr.cc/virtual/2024/papers.html?filter=title",
        # "https://nips.cc/virtual/2024/papers.html?filter=title",
        # "https://cvpr.thecvf.com/virtual/2024/papers.html?filter=title",
    ]
    llm_name = "o3-mini-2025-01-31"
    save_dir = "./data"
    input = retrieve_paper_from_query_subgraph_input_data

    # Traditional method (default): web scrape + extract titles
    # result = RetrievePaperFromQuerySubgraph(
    #     llm_name=llm_name,
    #     save_dir=save_dir,
    #     scrape_urls=scrape_urls,
    #     # use_openai_websearch=False,  # Default is False
    # ).run(input)

    # When using OpenAI Web Search (just uncomment the code below)
    result = RetrievePaperFromQuerySubgraph(
        llm_name=llm_name,
        save_dir=save_dir,
        scrape_urls=scrape_urls,  # Ignored when using OpenAI but kept for compatibility
        use_openai_websearch=True,  # Just set this to True to switch
    ).run(input)

    print(f"result: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
