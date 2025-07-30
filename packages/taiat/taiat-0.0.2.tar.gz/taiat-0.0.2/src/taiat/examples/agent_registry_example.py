"""
Example demonstrating the use of AgentRegistry and TaiatGraphArchitect.

This example shows how to:
1. Create an AgentRegistry and register functions
2. Use TaiatGraphArchitect to build an AgentGraphNodeSet from a description
3. Have the LLM specify function names as strings, which get resolved to actual functions
"""

from typing import Dict, Any
from langchain_anthropic import ChatAnthropic
from taiat.graph_architect import AgentRegistry, TaiatGraphArchitect
from taiat.base import State, AgentData


def data_processor_agent(state: State) -> State:
    """
    Example agent that processes input data.
    """
    print("Processing data...")
    # Simulate some data processing
    if "raw_data" in state["data"]:
        processed_data = AgentData(
            name="processed_data",
            parameters={},
            description="Processed data ready for analysis",
            data=f"Processed: {state['data']['raw_data'].data}",
        )
        state["data"]["processed_data"] = processed_data
    return state


def analyzer_agent(state: State) -> State:
    """
    Example agent that analyzes processed data.
    """
    print("Analyzing data...")
    # Simulate analysis
    if "processed_data" in state["data"]:
        analysis_result = AgentData(
            name="analysis_result",
            parameters={},
            description="Analysis results",
            data=f"Analysis of: {state['data']['processed_data'].data}",
        )
        state["data"]["analysis_result"] = analysis_result
    return state


def report_generator_agent(state: State) -> State:
    """
    Example agent that generates a final report.
    """
    print("Generating report...")
    # Simulate report generation
    if "analysis_result" in state["data"]:
        final_report = AgentData(
            name="final_report",
            parameters={},
            description="Final report with insights",
            data=f"Report based on: {state['data']['analysis_result'].data}",
        )
        state["data"]["final_report"] = final_report
    return state


def main():
    """
    Main example function demonstrating the agent registry system.
    """
    # 1. Create an LLM
    llm = ChatAnthropic(model="claude-3-5-sonnet-latest")

    # 2. Create an agent registry and register functions
    registry = AgentRegistry()
    registry.register("data_processor", data_processor_agent)
    registry.register("analyzer", analyzer_agent)
    registry.register("report_generator", report_generator_agent)

    print("Registered functions:", registry.list_registered())

    # 3. Create the graph architect
    architect = TaiatGraphArchitect(
        llm=llm, agent_registry=registry, verbose=True, llm_explanation=True
    )

    # 4. Build an AgentGraphNodeSet from a description
    description = """
    I need a data processing pipeline that:
    1. Takes raw data as input
    2. Processes the data to clean and format it
    3. Analyzes the processed data to extract insights
    4. Generates a final report with the analysis results
    
    The pipeline should have three agents: one for data processing, one for analysis, and one for report generation.
    """

    try:
        agent_graph_node_set = architect.build(description)

        print("\n=== Generated AgentGraphNodeSet ===")
        print(
            f"Description: {agent_graph_node_set.description if hasattr(agent_graph_node_set, 'description') else 'N/A'}"
        )
        print(f"Number of nodes: {len(agent_graph_node_set.nodes)}")

        for i, node in enumerate(agent_graph_node_set.nodes):
            print(f"\nNode {i + 1}: {node.name}")
            print(f"  Description: {node.description}")
            print(f"  Function: {node.function.__name__ if node.function else 'None'}")
            print(f"  Inputs: {[input.name for input in node.inputs]}")
            print(f"  Outputs: {[output.name for output in node.outputs]}")

    except Exception as e:
        print(f"Error building AgentGraphNodeSet: {e}")


if __name__ == "__main__":
    main()
