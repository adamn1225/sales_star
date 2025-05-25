from agents import Agent, Runner


class ProspectAgent:
    def run(self, company: str, research: str, intent: str) -> str:
        prospect_agent = Agent(
            name="Prospect Agent",
            instructions=(
                "You are a sales strategist. Analyze the research and intent triggers to suggest the best prospecting strategy."
            ),
        )
        prompt = (
            f"Company: {company}\nResearch: {research}\nIntent: {intent}\n"
            "Suggest the best prospecting strategy."
        )
        result = Runner.run_sync(prospect_agent, prompt)
        return result.final_output