from utils.model_loader import ModelLoader

from prompt_library.prompts import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState ,START, END
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool



class GraphBuilder:

    def __init__(self,model_provider: str = "openai"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        self.tools = [

            


        ]
        
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()
        
        self.tools.extend([* self.weather_tools.weather_tool_list, 
                           * self.place_search_tools.place_search_tool_list,
                           * self.calculator_tools.calculator_tool_list,
                           * self.currency_converter_tools.currency_converter_tool_list])
        
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
        self.graph = None
        
        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: MessagesState):
        """Main agent function for LangGraph.

        Parameters
        ----------
        state : MessagesState
            The current graph state which must contain a key ``"messages"``.

        Returns
        -------
        dict
            Updated state dict with the latest assistant response appended to the
            "messages" list so that downstream nodes can continue the
            conversation.
        """
        # Extract prior messages from the state
        user_messages = state["messages"] if "messages" in state else []

        # Pre-pend the system prompt so the model has the right context
        input_messages = [self.system_prompt] + user_messages
        print("[GraphBuilder] Invoking LLM with messages:", input_messages)

        # Call the LLM (already bound with tools) to get the next response
        assistant_response = self.llm_with_tools.invoke(input_messages)
        print("[GraphBuilder] Assistant response:", assistant_response)

        # Return the updated state – LangGraph expects a mapping
        return {"messages": user_messages + [assistant_response]}

    def build_graph(self):
        """Construct the LangGraph with the agent and tool nodes."""

        graph_builder = StateGraph(MessagesState)

        # Add nodes – an agent node and a generic tool node that LangGraph
        # understands will execute any tool returned by the agent.
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        # Define execution order and conditional branching based on whether the
        # agent decides to call a tool.
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)

        # Compile the graph which produces a runnable object exposing invoke()
        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        """Return a compiled graph ready to be invoked.

        The first time the instance is called we build and cache the graph so
        that subsequent calls are cheap.
        """
        if self.graph is None:
            self.build_graph()
        return self.graph

