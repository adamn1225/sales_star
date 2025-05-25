from agents import Agent, Runner


class ResearchAgent:
    def run(self, company: str, goal: str) -> str:
        research_agent = Agent(
            name="Research Agent",
            instructions="You are a research assistant. Research the company and provide insights based on the given goal."
        )
        prompt = f"Company: {company}\nGoal: {goal}\nProvide detailed research insights."
        result = Runner.run_sync(research_agent, prompt)
        return result.final_output