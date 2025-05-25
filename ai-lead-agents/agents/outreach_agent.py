from agents import Agent, Runner

class OutreachAgent:
    def run(self, company: str, research: str, intent: str, prospect: str) -> str:
        outreach_agent = Agent(
            name="Outreach Agent",
            instructions=(
                "You are an expert sales copywriter. Given a company, research findings, intent triggers, and prospecting strategy, "
                "generate a personalized cold call script and a cold email template."
            ),
        )
        prompt = (
            f"Company: {company}\nResearch: {research}\nIntent: {intent}\nProspect: {prospect}\n"
            "Generate a cold call script and a cold email template."
        )
        result = Runner.run_sync(outreach_agent, prompt)
        return result.final_output