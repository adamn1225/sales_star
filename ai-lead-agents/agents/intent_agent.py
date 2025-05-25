from agents import Agent, Runner

class FindIntentAgent:
    def run(self, company: str, industry: str) -> str:
        intent_agent = Agent(
            name="Intent Agent",
            instructions=(
                "You are an intent detection assistant. Identify recent events or triggers that suggest the company has a need for logistics services."
            ),
        )
        prompt = f"Company: {company}\nIndustry: {industry}\nIdentify intent triggers."
        result = Runner.run_sync(intent_agent, prompt)
        return result.final_output