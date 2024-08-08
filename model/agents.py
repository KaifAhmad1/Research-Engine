from langchain.llms import ChatGroq
from langchain.tools import Tool
from langchain.agents import Agent, Task, Crew
from config.apikeys import GROQ_API_KEY
from model.prompts import SYSTEM_PROMPT, THREAT_INTELLIGENCE_ANALYZER_PROMPT, VULNERABILITY_ASSESSMENT_GUIDE_PROMPT, INCIDENT_RESPONSE_COORDINATOR_PROMPT

# Define custom tools
class WebScraperTool(Tool):
    def __init__(self):
        super().__init__(
            name="WebScraperTool",
            description="A tool to scrape web pages for relevant information.",
            func=self.run
        )

    def run(self, input_text):
        return f"Web scraping results for: {input_text}"

class TwitterScraperTool(Tool):
    def __init__(self):
        super().__init__(
            name="TwitterScraperTool",
            description="A tool to scrape Twitter for relevant information.",
            func=self.run
        )

    def run(self, input_text):
        return f"Twitter scraping results for: {input_text}"

class NewsFetcherTool(Tool):
    def __init__(self):
        super().__init__(
            name="NewsFetcherTool",
            description="A tool to fetch news articles.",
            func=self.run
        )

    def run(self, input_text):
        return f"News fetching results for: {input_text}"

class CVEDataFetcherTool(Tool):
    def __init__(self):
        super().__init__(
            name="CVEDataFetcherTool",
            description="A tool to fetch CVE data.",
            func=self.run
        )

    def run(self, input_text):
        return f"CVE data for: {input_text}"

class ExaResearcherTool(Tool):
    def __init__(self):
        super().__init__(
            name="ExaResearcherTool",
            description="A tool to perform extensive research.",
            func=self.run
        )

    def run(self, input_text):
        return f"Extensive research results for: {input_text}"

class IOCExtractorTool(Tool):
    def __init__(self):
        super().__init__(
            name="IOCExtractorTool",
            description="A tool to extract Indicators of Compromise (IOCs).",
            func=self.run
        )

    def run(self, input_text):
        return f"Extracted IOCs for: {input_text}"

class TrendAnalyzerTool(Tool):
    def __init__(self):
        super().__init__(
            name="TrendAnalyzerTool",
            description="A tool to analyze trends.",
            func=self.run
        )

    def run(self, input_text):
        return f"Trend analysis for: {input_text}"

class SentimentAnalyzerTool(Tool):
    def __init__(self):
        super().__init__(
            name="SentimentAnalyzerTool",
            description="A tool to analyze sentiment.",
            func=self.run
        )

    def run(self, input_text):
        return f"Sentiment analysis for: {input_text}"

class VectorDBSearchTool(Tool):
    def __init__(self):
        super().__init__(
            name="VectorDBSearchTool",
            description="A tool to search a vector database.",
            func=self.run
        )

    def run(self, input_text):
        return f"Vector DB search results for: {input_text}"

class FactCheckerTool(Tool):
    def __init__(self):
        super().__init__(
            name="FactCheckerTool",
            description="A tool to fact-check information.",
            func=self.run
        )

    def run(self, input_text):
        # Use DuckDuckGo and Serper to fact-check the information
        duckduckgo_results = duckduckgo_search(input_text)
        serper_results = fetch_news(input_text)

        # Check if the information is present in the search results
        if any(input_text.lower() in result["snippet"].lower() for result in duckduckgo_results) or \
           any(input_text.lower() in result["snippet"].lower() for result in serper_results):
            return f"The information '{input_text}' is likely to be true."
        else:
            return f"The information '{input_text}' could not be verified and might be hallucinated."

# Initialize the Groq LLM
llm = ChatGroq(
    temperature=0,
    model="mixtral-8x7b-32768",
    api_key=GROQ_API_KEY
)

# Initialize tools
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
    EXASearchTool(),
    DuckDuckGoSearchRun(),
    FactCheckerTool()
]

# Integrate Prompts into Agent Creation
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

# Create Agents
researcher = create_agent(
    role="Cybersecurity Researcher",
    goal="Gather and provide relevant cybersecurity information. Collaborate with the analyst to ensure the data is accurate and comprehensive.",
    backstory="You are an expert cybersecurity researcher with years of experience in threat intelligence. You have a knack for finding obscure information and connecting the dots. You work closely with the analyst to ensure the data you gather is accurate and comprehensive.",
    prompt=SYSTEM_PROMPT
)

analyst = create_agent(
    role="Threat Analyst",
    goal="Analyze cybersecurity data and provide insights. Collaborate with the researcher to validate data and with the advisor to provide actionable recommendations.",
    backstory="You are a skilled threat analyst specializing in identifying and assessing cyber threats. You have a strong analytical mind and are able to see patterns where others see noise. You work closely with the researcher to validate data and with the advisor to provide actionable recommendations.",
    prompt=SYSTEM_PROMPT
)

advisor = create_agent(
    role="Security Advisor",
    goal="Provide recommendations based on cybersecurity analysis. Collaborate with the analyst to understand the data and with the incident responder to provide practical guidance.",
    backstory="You are a seasoned security advisor with a track record of helping organizations improve their security posture. You have a deep understanding of both the technical and human aspects of cybersecurity. You work closely with the analyst to understand the data and with the incident responder to provide practical guidance.",
    prompt=SYSTEM_PROMPT
)

incident_responder = create_agent(
    role="Incident Responder",
    goal="Provide guidance on handling cybersecurity incidents. Collaborate with the threat hunter to contain and mitigate threats and with the advisor to provide practical guidance.",
    backstory="You are a quick-thinking incident responder with expertise in containing and mitigating cyber attacks. You are calm under pressure and able to make tough decisions quickly. You work closely with the threat hunter to contain and mitigate threats and with the advisor to provide practical guidance.",
    prompt=INCIDENT_RESPONSE_COORDINATOR_PROMPT
)

fact_checker = create_agent(
    role="Fact Checker",
    goal="Verify the information gathered by the other agents. Collaborate with the researcher and analyst to ensure the data is accurate.",
    backstory="You are a meticulous fact checker with a keen eye for detail. You have a strong commitment to the truth and are not afraid to challenge assumptions. You work closely with the researcher and analyst to ensure the data is accurate.",
    prompt=SYSTEM_PROMPT
)

threat_intelligence_analyst = create_agent(
    role="Cybersecurity Threat Intelligence Analyst",
    goal="Analyze and synthesize threat intelligence from various sources to provide actionable insights on emerging cyber threats, threat actors, and attack vectors.",
    backstory="You are a skilled threat intelligence analyst with experience in monitoring global cyber threat trends and profiling threat actors. You provide early warning of potential cyber attacks and offer actionable recommendations for threat mitigation.",
    prompt=THREAT_INTELLIGENCE_ANALYZER_PROMPT
)

vulnerability_assessment_specialist = create_agent(
    role="Vulnerability Assessment Specialist",
    goal="Guide users through the process of conducting comprehensive vulnerability assessments on various systems, networks, or applications.",
    backstory="You are an expert in vulnerability scanning and assessment. You provide step-by-step guidance for setting up and running vulnerability scans, interpreting results, and developing remediation strategies.",
    prompt=VULNERABILITY_ASSESSMENT_GUIDE_PROMPT
)

incident_response_coordinator = create_agent(
    role="Cybersecurity Incident Response Coordinator",
    goal="Guide users through the process of effectively responding to and managing cybersecurity incidents.",
    backstory="You are an experienced incident response coordinator. You assist in assessing the severity and scope of cybersecurity incidents, provide step-by-step guidance through the incident response process, and help coordinate communication between different stakeholders.",
    prompt=INCIDENT_RESPONSE_COORDINATOR_PROMPT
)

# Process query function
def process_query(query):
    # Create tasks for each agent
    tasks = [
        Task(
            description=f"Research the query: {query}",
            agent=researcher,
            expected_output="Detailed research findings related to the query"
        ),
        Task(
            description=f"Analyze the findings for the query: {query}",
            agent=analyst,
            expected_output="Analysis of the research findings with key insights"
        ),
        Task(
            description=f"Provide security recommendations based on the analysis of: {query}",
            agent=advisor,
            expected_output="Actionable security recommendations"
        ),
        Task(
            description=f"Outline incident response steps if needed for: {query}",
            agent=incident_responder,
            expected_output="Incident response plan if applicable"
        ),
        Task(
            description=f"Fact-check the gathered information for: {query}",
            agent=fact_checker,
            expected_output="Fact-checking results"
        ),
        Task(
            description=f"Analyze and synthesize threat intelligence for: {query}",
            agent=threat_intelligence_analyst,
            expected_output="Threat intelligence analysis and actionable insights"
        ),
        Task(
            description=f"Guide through vulnerability assessment for: {query}",
            agent=vulnerability_assessment_specialist,
            expected_output="Vulnerability assessment guidance and remediation strategies"
        ),
        Task(
            description=f"Coordinate incident response for: {query}",
            agent=incident_response_coordinator,
            expected_output="Incident response coordination and communication plan"
        ),
    ]

    # Create a crew with all agents and tasks
    crew = Crew(
        agents=[researcher, analyst, advisor, incident_responder, fact_checker, threat_intelligence_analyst, vulnerability_assessment_specialist, incident_response_coordinator],
        tasks=tasks,
        verbose=0
    )

    # Execute the crew's tasks
    result = crew.kickoff()

    return result
