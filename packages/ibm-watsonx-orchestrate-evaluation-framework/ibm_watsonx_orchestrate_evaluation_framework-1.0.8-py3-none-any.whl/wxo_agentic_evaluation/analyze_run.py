import json
import os
import csv
import rich
from rich.text import Text
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from typing import List
from wxo_agentic_evaluation.type import (
    ExtendedMessage,
    ContentType
)
from wxo_agentic_evaluation.metrics.metrics import ToolCallAndRoutingMetrics
from wxo_agentic_evaluation.arg_configs import AnalyzeConfig
from jsonargparse import CLI


def render(data: List[ExtendedMessage]):
    conversation_lines = []
    reason_lines = []

    for entry in data:
        msg = entry.message
        role = msg.role
        content = msg.content
        reason = entry.reason
        tool_name = None
        if role == "user":
            label = "👤 User"
        elif role == "assistant" and msg.type == ContentType.tool_call:
            if reason:
                label = "❌ Tool Call"
                tool_name = json.loads(msg.content)["name"]
            else:
                label = "✅ Tool Call"
        elif role == "assistant":
            label = "🤖 Assistant"
        else:
            label = "📦 Unknown"

        text_line = Text(f"{label}: {content}\n")
        if reason:
            text_line.stylize("bold red")
            reason_text = f"❌ {tool_name}: {json.dumps(reason)}\n\n"
            reason_lines.append(Text(reason_text, style="red"))
        conversation_lines.append(text_line)

    conversation_panel = Panel(
        Text().join(conversation_lines),
        title="Conversation History",
        border_style="blue",
    )
    reason_panel = Panel(
        Text().join(reason_lines), title="Analysis Results", border_style="red"
    )

    layout = Layout()
    layout.split_row(Layout(conversation_panel), Layout(reason_panel))

    return layout


def analyze(config: AnalyzeConfig):
    summary = []
    with open(os.path.join(config.data_path, "summary_metrics.csv"), "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            summary.append(dict(zip(header, row)))

    test_case_with_failed_tools = []
    for entry in summary:
        test_case_name = entry["dataset_name"]
        if test_case_name.lower().strip() == "summary (average)":
            continue
        if not entry["is_success"] or float(entry["tool_calls_with_incorrect_parameter"]) > 0 or float(entry["tool_call_precision"]) < 1.0\
                or float(entry["tool_call_recall"]) < 1.0:
            test_case_with_failed_tools.append(entry)
    if len(test_case_with_failed_tools) == 0:
        header_table = Table(show_header=False, box=None)
        header_table.add_row(f"No Tool Call Error found!")
        header_panel = Panel(
            header_table, title="[bold green]📋 Analysis Summary[/bold green]"
        )
        rich.print(header_panel)

    for test_case_entry in test_case_with_failed_tools:
        test_case_name = test_case_entry["dataset_name"]

        test_case_path = os.path.join(
            config.data_path, "messages", f"{test_case_name}.messages.analyze.json"
        )
        test_messages = []
        with open(test_case_path, "r", encoding="utf-8") as f:
            temp = json.load(f)
            for entry in temp:
                msg = ExtendedMessage(**entry)
                test_messages.append(msg)

        test_metrics_path = os.path.join(
            config.data_path, "messages", f"{test_case_name}.metrics.json"
        )
        with open(test_metrics_path, "r", encoding="utf-8") as f:
            metrics = ToolCallAndRoutingMetrics(**json.load(f))
        header_table = Table(show_header=False, box=None)
        header_table.add_row(f"Test Case Name: {test_case_name}")
        header_table.add_row((f"Expected Tool Calls: {metrics.expected_tool_calls}"))
        header_table.add_row(f"Correct Tool Calls: {metrics.correct_tool_calls}")
        header_table.add_row(f"Text Match: {metrics.text_match.value}")
        header_table.add_row(
            f"Journey Success: {metrics.is_success}"
        )
        header_panel = Panel(
            header_table, title="[bold green]📋 Analysis Summary[/bold green]"
        )
        rich.print(header_panel)
        layout = render(test_messages)
        rich.print(layout)


if __name__ == "__main__":
    analyze(CLI(AnalyzeConfig, as_positional=False))
