

from until.model_loader import ModelLoader

from prompts_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState ,START, END
from langgraph.prebuilt import ToolNode, tools_condition


class GraphBuilder:

    def __init__(self):
        pass

    def agent_function(self):
        """Main agent function"""
        user_question = state['messages']
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages" : [response]}

        pass

    def build_graph(self):

        graph_builder = StateGraph(MessagesState)

        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge('tools', 'agent')
        graph_builder.add_edge('agent', END)
        self.graph = graph_builder.compile()
        return self.graph

        pass

    def __call__(self):
        pass

