from urllib.parse import urlparse
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from rich import box
from rich import print

from typing import List

from wxo_agentic_evaluation.metrics.llm_as_judge import Faithfulness
from wxo_agentic_evaluation.metrics.metrics import KnowledgeBaseMetricSummary
from wxo_agentic_evaluation.type import ConversationalConfidenceThresholdScore

console = Console()


class AgentMetricsTable:
    def __init__(self, data):
        self.table = Table(
            title="Agent Metrics",
            box=box.ROUNDED,
            show_lines=True,
        )

        if not data:
            return

        # Add columns with styling
        headers = list(data[0].keys())
        for header in headers:
            self.table.add_column(header, style="cyan")

        # Add rows
        for row in data:
            self.table.add_row(*[str(row.get(col, "")) for col in headers])

    def print(self):
        console.print(self.table)


def create_table(data: List[dict]) -> AgentMetricsTable:
    """
    Generate a Rich table from a list of dictionaries.
    Returns the AgentMetricsTable instance.
    """
    if isinstance(data, dict):
        data = [data]

    if not data:
        print("create_table() received an empty dataset. No table generated.")
        return None

    return AgentMetricsTable(data)


def safe_divide(nom, denom):
    if denom == 0:
        return 0
    else:
        return nom/denom

def is_saas_url(service_url: str) -> bool:
    hostname = urlparse(service_url).hostname
    return hostname not in ("localhost", "127.0.0.1", "0.0.0.0", "::1")


def is_ibm_cloud_url(service_url: str) -> bool:
    hostname = urlparse(service_url).hostname
    return ".cloud.ibm.com" in hostname


def add_line_seperator():
    console.print(Rule(style="grey42"))


class FaithfulnessTable:
    def __init__(
        self, faithfulness_metrics: List[Faithfulness], tool_call_ids: List[str]
    ):
        self.table = Table(title="Faithfulness", box=box.ROUNDED, show_lines=True)

        self.table.add_column("Tool Call Id", style="blue")
        self.table.add_column("Faithfulness Score", style="blue3")
        self.table.add_column("Evidence", style="cyan")
        self.table.add_column("Reasoning", style="yellow3")

        for tool_call_id, faithfulness in zip(tool_call_ids, faithfulness_metrics):
            faithfulness = faithfulness.table()
            self.table.add_row(
                tool_call_id,
                faithfulness["faithfulness_score"],
                faithfulness["evidence"],
                faithfulness["reason"],
            )

    def print(self):
        console.print(self.table)


class ConversationalSearchTable:
    def __init__(
        self,
        confidence_scores_list: List[ConversationalConfidenceThresholdScore],
        tool_call_ids: List[str],
    ):
        self.table = Table(
            title="Conversational Search", box=box.ROUNDED, show_lines=True
        )

        self.table.add_column("Tool Call Id", style="blue")
        self.table.add_column("Response Confidence", style="blue3")
        self.table.add_column("Response Confidence Threshold", style="cyan")
        self.table.add_column("Retrieval Confidence", style="blue3")
        self.table.add_column("Retrieval Confidence Threshold", style="cyan")

        for tool_call_id, confidence_scores in zip(
            tool_call_ids, confidence_scores_list
        ):
            confidence_scores = confidence_scores.table()
            self.table.add_row(
                tool_call_id,
                confidence_scores["response_confidence"],
                confidence_scores["response_confidence_threshold"],
                confidence_scores["retrieval_confidence"],
                confidence_scores["retrieval_confidence_threshold"],
            )


class KnowledgePanel:
    def __init__(
        self,
        dataset_name: str,
        tool_call_id: List[str],
        faithfulness: List[Faithfulness] = None,
        confidence_scores: List[ConversationalConfidenceThresholdScore] = None,
    ):
        self.faithfulness = FaithfulnessTable(faithfulness, tool_call_id)
        self.confidence_scores = ConversationalSearchTable(
            confidence_scores, tool_call_id
        )
        self.group = Group(self.faithfulness.table, self.confidence_scores.table)

        # Panel acts as a section
        self.section = Panel(
            self.group,
            title=f"Agent with Knowledge Metrics for {dataset_name}",
            border_style="grey37",
            title_align="left",
        )

    def print(self):
        console.print(self.section)


class SummaryPanel:
    def __init__(self, summary_metrics: KnowledgeBaseMetricSummary):

        self.table = Table(
            title="Agent with Knowledge Summary Metrics",
            box=box.ROUNDED,
            show_lines=True,
        )
        self.table.add_column("Dataset", style="blue3")
        self.table.add_column("Average Response Confidence", style="cyan")
        self.table.add_column("Average Retrieval Confidence", style="blue3")
        self.table.add_column("Average Faithfulness", style="cyan")
        self.table.add_column("Average Answer Relevancy", style="blue3")
        self.table.add_column("Number Calls to Knowledge Bases", style="cyan")
        self.table.add_column("Knowledge Bases Called", style="blue3")

        average_metrics = summary_metrics.average
        for dataset, metrics in average_metrics.items():
            self.table.add_row(
                dataset,
                str(round(metrics["average_response_confidence"], 4)),
                str(round(metrics["average_retrieval_confidence"], 4)),
                str(metrics["average_faithfulness"]),
                str(metrics["average_answer_relevancy"]),
                str(metrics["number_of_calls"]),
                metrics["knowledge_bases_called"],
            )

    def print(self):
        console.print(self.table)
