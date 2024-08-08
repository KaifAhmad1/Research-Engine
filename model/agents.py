# agents.py 

from langchain.tools import Tool
from langchain.agents import Agent, Task, Crew
from model.model import initialize_llm
from model.prompts import (
    SYSTEM_PROMPT, 
    THREAT_INTELLIGENCE_ANALYZER_PROMPT, 
    VULNERABILITY_ASSESSMENT_GUIDE_PROMPT, 
    INCIDENT_RESPONSE_COORDINATOR_PROMPT
)

# Initialize the LLM
llm = initialize_llm()

# Define Custom Tools
class BaseTool(Tool):
    def __init__(self, name, description, func):
        super().__init__(name=name, description=description, func=func)

class WebScraperTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="WebScraperTool",
            description="Scrapes web pages for relevant information.",
            func=self.run
        )

    def run(self, input_text):
        # Implement the actual scraping logic here
        return f"Web scraping results for: {input_text}"

class TwitterScraperTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="TwitterScraperTool",
            description="Scrapes Twitter for relevant information.",
            func=self.run
        )

    def run(self, input_text):
        # Implement the actual scraping logic here
        return f"Twitter scraping results for: {input_text}"

class NewsFetcherTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="NewsFetcherTool",
            description="Fetches news articles.",
            func=self.run
        )

    def run(self, input_text):
        # Implement the actual news fetching logic here
        return f"News fetching results for: {input_text}"

class CVEDataFetcherTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="CVEDataFetcherTool",
            description="Fetches CVE data.",
            func=self.run
        )

    def run(self, input_text):
        # Implement the actual CVE data fetching logic here
        return f"CVE data for: {input_text}"

class ExaResearcherTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="ExaResearcherTool",
            description="Performs extensive research using external sources.",
            func=self.run
        )

    def run(self, input_text):
        # Implement the actual research logic here
        return f"Extensive research results for: {input_text}"

class IOCExtractorTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="IOCExtractorTool",
            description="Extracts Indicators of Compromise (IOCs).",
            func=self.run
        )

    def run(self, input_text):
        # Implement the actual IOC extraction logic here
        return f"Extracted IOCs for: {input_text}"

class TrendAnalyzerTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="TrendAnalyzerTool",
            description="Analyzes cybersecurity trends.",
            func=self.run
        )

    def run(self, input_text):
        # Implement the actual trend analysis logic here
        return f"Trend analysis for: {input_text}"

class SentimentAnalyzerTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="SentimentAnalyzerTool",
            description="Analyzes sentiment.",
            func=self.run
        )

    def run(self, input_text):
        # Implement the actual sentiment analysis logic here
        return f"Sentiment analysis for: {input_text}"

class VectorDBSearchTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="VectorDBSearchTool",
            description="Searches the vector database for relevant information.",
            func=self.run
        )

    def run(self, input_text):
        # Implement the actual vector DB search logic here
        return f"Vector DB search results for: {input_text}"

class FactCheckerTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="FactCheckerTool",
            description="Fact-checks information using multiple sources.",
            func=self.run
        )

    def run(self, input_text):
        # Implement the actual fact-checking logic here
        # Example with hypothetical duckduckgo_search and fetch_news functions
        duckduckgo_results = duckduckgo_search(input_text)
        serper_results = fetch_news(input_text)

        if any(input_text.lower() in result["snippet"].lower() for result in duckduckgo_results) or \
           any(input_text.lower() in result["snippet"].lower() for result in serper_results):
            return f"The information '{input_text}' is likely to be true."
        else:
            return f"The information '{input_text}' could not be verified and might be hallucinated."

# Initialize all tools
tools = [
    WebScraperTool(),
    TwitterScraperTool(),
    NewsFetcherTool(),
    CVEDataFetcherTool(),
    ExaResearcherTool(),
    IOCExtractorTool(),
    TrendAnalyzerTool(),
    SentimentAnalyzerTool(),
    VectorDBSearchTool(),
    FactCheckerTool()
]

# Agent creation function
def create_agent(role, goal, backstory, prompt):
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=True,
        allow_delegation=True,
        tools=tools,
        llm=llm,
        prompt=prompt
    )

# Define Agents
def initialize_agents():
    researcher = create_agent(
        role="Cybersecurity Researcher",
        goal="Gather and provide relevant cybersecurity information.",
        backstory="An expert cybersecurity researcher with experience in threat intelligence.",
        prompt=SYSTEM_PROMPT
    )

    analyst = create_agent(
        role="Threat Analyst",
        goal="Analyze cybersecurity data and provide insights.",
        backstory="A skilled threat analyst specializing in identifying and assessing cyber threats.",
        prompt=SYSTEM_PROMPT
    )

    advisor = create_agent(
        role="Security Advisor",
        goal="Provide actionable recommendations based on cybersecurity analysis.",
        backstory="A seasoned security advisor helping organizations improve their security posture.",
        prompt=SYSTEM_PROMPT
    )

    incident_responder = create_agent(
        role="Incident Responder",
        goal="Provide guidance on handling cybersecurity incidents.",
        backstory="An expert in containing and mitigating cyber attacks, providing practical guidance.",
        prompt=INCIDENT_RESPONSE_COORDINATOR_PROMPT
    )

    fact_checker = create_agent(
        role="Fact Checker",
        goal="Verify the information gathered by other agents.",
        backstory="A meticulous fact checker with a strong commitment to accuracy.",
        prompt=SYSTEM_PROMPT
    )

    threat_intelligence_analyst = create_agent(
        role="Cybersecurity Threat Intelligence Analyst",
        goal="Analyze and synthesize threat intelligence from various sources.",
        backstory="A skilled threat intelligence analyst monitoring global cyber threat trends.",
        prompt=THREAT_INTELLIGENCE_ANALYZER_PROMPT
    )

    vulnerability_assessment_specialist = create_agent(
        role="Vulnerability Assessment Specialist",
        goal="Guide users through comprehensive vulnerability assessments.",
        backstory="An expert in vulnerability scanning and assessment.",
        prompt=VULNERABILITY_ASSESSMENT_GUIDE_PROMPT
    )

    incident_response_coordinator = create_agent(
        role="Cybersecurity Incident Response Coordinator",
        goal="Guide users through effective cybersecurity incident response.",
        backstory="An experienced incident response coordinator helping manage cybersecurity incidents.",
        prompt=INCIDENT_RESPONSE_COORDINATOR_PROMPT
    )

    return {
        "researcher": researcher,
        "analyst": analyst,
        "advisor": advisor,
        "incident_responder": incident_responder,
        "fact_checker": fact_checker,
        "threat_intelligence_analyst": threat_intelligence_analyst,
        "vulnerability_assessment_specialist": vulnerability_assessment_specialist,
        "incident_response_coordinator": incident_response_coordinator
    }

# Function to process a query using the agents
def process_query(query):
    agents = initialize_agents()

    tasks = [
        Task(
            description=f"Research the query: {query}",
            agent=agents["researcher"],
            expected_output="Detailed research findings related to the query"
        ),
        Task(
            description=f"Analyze the findings for the query: {query}",
            agent=agents["analyst"],
            expected_output="Analysis of the research findings with key insights"
        ),
        Task(
            description=f"Provide security recommendations based on the analysis of: {query}",
            agent=agents["advisor"],
            expected_output="Actionable security recommendations"
        ),
        Task(
            description=f"Outline incident response steps if needed for: {query}",
            agent=agents["incident_responder"],
            expected_output="Incident response plan if applicable"
        ),
        Task(
            description=f"Fact-check the gathered information for: {query}",
            agent=agents["fact_checker"],
            expected_output="Fact-checking results"
        ),
        Task(
            description=f"Analyze and synthesize threat intelligence for: {query}",
            agent=agents["threat_intelligence_analyst"],
            expected_output="Threat intelligence analysis and actionable insights"
        ),
        Task(
            description=f"Guide through vulnerability assessment for: {query}",
            agent=agents["vulnerability_assessment_specialist"],
            expected_output="Vulnerability assessment guidance and remediation strategies"
        ),
        Task(
            description=f"Coordinate incident response for: {query}",
            agent=agents["incident_response_coordinator"],
            expected_output="Incident response coordination and communication plan"
        ),
    ]

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=0
    )

    result = crew.kickoff()

    return result
