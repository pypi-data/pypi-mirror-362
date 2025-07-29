import os
import argparse
import openai
import json
import time
from typing import List, Dict, Any
from dataclasses import dataclass

# LLM Model
OPENAI_MODEL = "gpt-4o"
query = "How is brie cheese made?"

# Mock data for agent web search tool
MOCK_WEB_SEARCH_DATA = {
    "brie cheese making process": {
        "results": [
            {
                "title": "Traditional Brie Making Process",
                "content": "Brie cheese production involves specific bacterial cultures including Penicillium candidum for the white bloomy rind. The process requires careful temperature and humidity control during aging."
            },
            {
                "title": "French Cheese Making Techniques",
                "content": "Authentic brie uses raw or pasteurized cow's milk, rennet for coagulation, and requires 4-5 weeks of aging in controlled environments with 95% humidity."
            }
        ]
    },
    "brie cheese ingredients": {
        "results": [
            {
                "title": "Brie Cheese Ingredients",
                "content": "Primary ingredients: Cow's milk, mesophilic starter cultures, rennet (animal or vegetable), salt, Penicillium candidum mold culture."
            }
        ]
    }
}

@dataclass
class LLMResponse:
    content: str
    tokens_used: int
    response_time: float

class BaseLLM:
    """Demonstrates basic LLM functionality - single call, direct response"""
    
    def __init__(self, model="gpt-4o"):
        self.model = model
    
    def generate(self, prompt: str) -> LLMResponse:
        """Single forward pass through LLM"""
        print("🧠 BaseLLM: Making single API call...")
        start_time = time.time()
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        end_time = time.time()
        
        return LLMResponse(
            content=response.choices[0].message.content,
            tokens_used=response.usage.total_tokens,
            response_time=end_time - start_time
        )

class ReasoningLLM:
    """Demonstrates reasoning framework - multiple orchestrated calls"""
    
    def __init__(self, base_llm: BaseLLM):
        self.base_llm = base_llm
        self.conversation_history = []
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """Step 1: Analyze the type of query and create reasoning plan"""
        analysis_prompt = f"""
        Analyze this query and determine the best approach to answer it comprehensively:
        Query: "{query}"
        
        Respond with:
        1. Query type (factual, process, comparison, etc.)
        2. Key components to address
        3. Suggested breakdown steps
        
        Keep response concise and structured.
        """
        
        print("🔧 ReasoningLLM: Step 1 - Analyzing query...")
        response = self.base_llm.generate(analysis_prompt)
        return {"analysis": response.content, "tokens": response.tokens_used}
    
    def decompose_problem(self, query: str, analysis: str) -> List[str]:
        """Step 2: Break down into specific sub-questions"""
        decomposition_prompt = f"""
        Based on this analysis: {analysis}
        
        Break down the query "{query}" into 3-4 specific sub-questions that, when answered together, 
        will provide a comprehensive response. List only the questions, one per line.
        """
        
        print("🔧 ReasoningLLM: Step 2 - Decomposing problem...")
        response = self.base_llm.generate(decomposition_prompt)
        
        # Extract questions from response
        questions = [q.strip() for q in response.content.split('\n') if q.strip() and '?' in q]
        return questions[:4]  # Limit to 4 questions
    
    def answer_sub_question(self, question: str) -> str:
        """Step 3: Answer each sub-question specifically"""
        focused_prompt = f"""
        Answer this specific question about cheese making with precise, technical details:
        {question}
        
        Provide a clear, factual answer focusing only on this aspect.
        """
        
        print(f"🔧 ReasoningLLM: Step 3 - Answering: {question[:50]}...")
        response = self.base_llm.generate(focused_prompt)
        return response.content
    
    def verify_response(self, question: str, answer: str) -> Dict[str, Any]:
        """Step 4: Verify accuracy and completeness"""
        verification_prompt = f"""
        Question: {question}
        Answer: {answer}
        
        Evaluate this answer on a scale of 1-10 for:
        1. Accuracy
        2. Completeness
        3. Clarity
        
        Respond with just three numbers and any critical missing information.
        """
        
        print("🔧 ReasoningLLM: Step 4 - Verifying response...")
        response = self.base_llm.generate(verification_prompt)
        return {"verification": response.content}
    
    def synthesize_final_response(self, query: str, qa_pairs: List[tuple]) -> str:
        """Step 5: Combine all verified answers into structured response"""
        synthesis_prompt = f"""
        Original question: {query}
        
        Sub-questions and answers:
        {chr(10).join([f"Q: {q}{chr(10)}A: {a}{chr(10)}" for q, a in qa_pairs])}
        
        Synthesize these into a well-structured, comprehensive answer to the original question.
        Use clear steps/sections and ensure logical flow.
        """
        
        print("🔧 ReasoningLLM: Step 5 - Synthesizing final response...")
        response = self.base_llm.generate(synthesis_prompt)
        return response.content
    
    def reason(self, query: str) -> Dict[str, Any]:
        """Main reasoning orchestration method"""
        print(f"\n🔧 ReasoningLLM: Processing '{query}'")
        start_time = time.time()
        
        # Step 1: Analyze query
        analysis = self.analyze_query(query)
        
        # Step 2: Decompose into sub-questions
        sub_questions = self.decompose_problem(query, analysis['analysis'])
        
        # Step 3 & 4: Answer and verify each sub-question
        qa_pairs = []
        total_tokens = analysis['tokens']
        
        for question in sub_questions:
            answer = self.answer_sub_question(question)
            verification = self.verify_response(question, answer)
            qa_pairs.append((question, answer))
            total_tokens += 100  # Approximate token usage
        
        # Step 5: Synthesize final response
        final_response = self.synthesize_final_response(query, qa_pairs)
        
        end_time = time.time()
        
        return {
            "response": final_response,
            "reasoning_steps": {
                "analysis": analysis['analysis'],
                "sub_questions": sub_questions,
                "qa_pairs": qa_pairs
            },
            "total_tokens": total_tokens,
            "processing_time": end_time - start_time
        }

class Agent:
    """Demonstrates agent functionality - environmental perception, decision making, tool usage"""
    
    def __init__(self, base_llm: BaseLLM):
        self.base_llm = base_llm
        self.tools = {
            "web_search": self.mock_web_search,
            "knowledge_base": self.access_knowledge_base
        }
        self.working_memory = []
    
    def mock_web_search(self, query: str) -> Dict[str, Any]:
        """Mock tool: Simulate web search API"""
        print(f"🔍 Agent Tool: Searching web for '{query}'...")
        time.sleep(0.5)  # Simulate API delay
        
        # Simple keyword matching for mock data
        for key, data in MOCK_WEB_SEARCH_DATA.items():
            if any(word in query.lower() for word in key.split()):
                return {"tool": "web_search", "query": query, "results": data["results"]}
        
        return {"tool": "web_search", "query": query, "results": []}
    
    def access_knowledge_base(self, topic: str) -> Dict[str, Any]:
        """Mock tool: Access internal knowledge base"""
        print(f"📚 Agent Tool: Accessing knowledge base for '{topic}'...")
        knowledge = {
            "cheese_making": "Traditional cheese making involves milk, cultures, rennet, and aging processes.",
            "fermentation": "Controlled bacterial cultures convert lactose to lactic acid, affecting texture and flavor."
        }
        return {"tool": "knowledge_base", "topic": topic, "info": knowledge.get(topic, "No information found")}
    
    def perceive_environment(self, query: str) -> Dict[str, Any]:
        """Agent perceives the environment and available resources"""
        perception_prompt = f"""
        I need to answer: "{query}"
        
        Available tools: web_search, knowledge_base
        
        What information do I need to gather to answer this comprehensively? 
        What tools should I use and in what order?
        
        Respond with a brief action plan.
        """
        
        print("👁️ Agent: Perceiving environment and planning...")
        response = self.base_llm.generate(perception_prompt)
        return {"perception": response.content}
    
    def make_decision(self, perception: str, query: str) -> List[Dict[str, Any]]:
        """Agent decides which tools to use and in what order"""
        decision_prompt = f"""
        Query: {query}
        Perception: {perception}
        
        Based on this, decide which specific tool calls to make. 
        Respond with a simple list:
        1. Tool name and search query
        2. Tool name and search query
        etc.
        
        Keep it concise - just the decisions.
        """
        
        print("🤔 Agent: Making decisions about tool usage...")
        response = self.base_llm.generate(decision_prompt)
        
        # Parse decisions into action plan (simplified)
        actions = []
        if "web_search" in response.content.lower():
            if "process" in query.lower() or "made" in query.lower():
                actions.append({"tool": "web_search", "query": "brie cheese making process"})
            if "ingredient" in query.lower():
                actions.append({"tool": "web_search", "query": "brie cheese ingredients"})
        
        if "knowledge_base" in response.content.lower():
            actions.append({"tool": "knowledge_base", "query": "cheese_making"})
        
        return actions if actions else [{"tool": "web_search", "query": "brie cheese making process"}]
    
    def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Agent executes the decided action using appropriate tool"""
        tool_name = action["tool"]
        query = action["query"]
        
        print(f"⚡ Agent: Executing action - {tool_name}({query})")
        
        if tool_name in self.tools:
            result = self.tools[tool_name](query)
            self.working_memory.append(result)
            return result
        else:
            return {"error": f"Tool {tool_name} not available"}
    
    def synthesize_response(self, original_query: str) -> str:
        """Agent synthesizes all gathered information into final response"""
        context = "\n".join([
            f"Tool: {item.get('tool', 'unknown')}, Data: {str(item)[:200]}..." 
            for item in self.working_memory
        ])
        
        synthesis_prompt = f"""
        Original question: {original_query}
        
        Information gathered from tools:
        {context}
        
        Synthesize this information into a comprehensive, well-structured answer.
        Mention that information was gathered from external sources when relevant.
        """
        
        print("🎯 Agent: Synthesizing final response from all gathered information...")
        response = self.base_llm.generate(synthesis_prompt)
        return response.content
    
    def process(self, query: str) -> Dict[str, Any]:
        """Main agent processing method - perceive, decide, act, synthesize"""
        print(f"\n👤 Agent: Processing '{query}'")
        start_time = time.time()
        
        # Clear working memory for new task
        self.working_memory = []
        
        # Agent workflow: Perceive -> Decide -> Act -> Synthesize
        perception = self.perceive_environment(query)
        decisions = self.make_decision(perception["perception"], query)
        
        # Execute all decided actions
        action_results = []
        for action in decisions:
            result = self.execute_action(action)
            action_results.append(result)
        
        # Synthesize final response
        final_response = self.synthesize_response(query)
        
        end_time = time.time()
        
        return {
            "response": final_response,
            "agent_workflow": {
                "perception": perception["perception"],
                "decisions": decisions,
                "action_results": action_results,
                "working_memory": self.working_memory
            },
            "processing_time": end_time - start_time
        }

def simple_llm():
    print("simple_llm()")
	
    # Initialize
    base_llm = BaseLLM()

    print("\n" + "="*50)
    print("TEST 1: SIMPLE LLM")
    print("="*50)
    llm_result = base_llm.generate(query)
    print(f"Response: {llm_result.content}")
    print(f"Tokens: {llm_result.tokens_used}, Time: {llm_result.response_time:.2f}s")

def reasoning_llm():
    print("reasoning_llm()")
     
    # Initialize
    base_llm = BaseLLM()
    reasoning_llm = ReasoningLLM(base_llm)

    print("\n" + "="*50)
    print("TEST 2: REASONING LLM")
    print("="*50)
    reasoning_result = reasoning_llm.reason(query)
    print(f"Final Response: {reasoning_result['response']}")
    print(f"Sub-questions explored: {len(reasoning_result['reasoning_steps']['sub_questions'])}")
    print(f"Total tokens: {reasoning_result['total_tokens']}, Time: {reasoning_result['processing_time']:.2f}s")

def agent():
    print("agent()")
    
    # Initialize
    base_llm = BaseLLM()
    agent = Agent(base_llm)

    print("\n" + "="*50)
    print("TEST 3: AGENT")
    print("="*50)
    agent_result = agent.process(query)
    print(f"Final Response: {agent_result['response']}")
    print(f"Tools used: {len(agent_result['agent_workflow']['action_results'])}")
    print(f"Time: {agent_result['processing_time']:.2f}s")
	
def main(args=None):
	print("CLI Arguments:", args)

	if args.simple_llm:
		simple_llm()
	if args.reasoning:
		reasoning_llm()
	if args.agent:
		agent()

if __name__ == "__main__":
	# Generate the inputs arguments parser
	# if you type into the terminal '--help', it will provide the description
	parser = argparse.ArgumentParser(description="CLI")

	parser.add_argument("--simple_llm",action="store_true",help="Simple LLM")
	parser.add_argument("--reasoning",action="store_true",help="Reasoning LLM")
	parser.add_argument("--agent",action="store_true",help="Agent")
	
    # Parse arguments and call main
	args = parser.parse_args()
	main(args)