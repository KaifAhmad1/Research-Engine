# data/dataloading.py

from datafetching import (
    Website, SearchTerm, InputData, OutputData,
    scrape_websites, fetch_tweets, fetch_cve_data, exa_search, duckduckgo_search
)

# Expanded list of websites
websites = [
    Website(url="https://www.scmagazine.com/home/security-news/"),
    Website(url="https://thehackernews.com/"),
    Website(url="https://www.securityweek.com/"),
    Website(url="https://www.darkreading.com/"),
    Website(url="https://krebsonsecurity.com/"),
    Website(url="https://www.bleepingcomputer.com/"),
    Website(url="https://threatpost.com/"),
    Website(url="https://www.cyberscoop.com/"),
    Website(url="https://www.infosecurity-magazine.com/"),
    Website(url="https://www.zdnet.com/topic/security/"),
    Website(url="https://www.wired.com/category/security/"),
    Website(url="https://nakedsecurity.sophos.com/"),
    Website(url="https://www.cisomag.com/"),
    Website(url="https://www.databreachtoday.com/"),
    Website(url="https://www.cshub.com/"),
    Website(url="https://www.cybersecuritydive.com/"),
    Website(url="https://www.cybersecurity-insiders.com/"),
    Website(url="https://www.csoonline.com/"),
    Website(url="https://www.securitymagazine.com/topics/2236-cyber-security-news"),
    Website(url="https://www.helpnetsecurity.com/")
]

# Expanded list of search terms
search_terms = [
    SearchTerm(term="latest cybersecurity incidents"),
    SearchTerm(term="new malware attacks 2024"),
    SearchTerm(term="data breaches 2024"),
    SearchTerm(term="ransomware trends"),
    SearchTerm(term="zero-day vulnerabilities"),
    SearchTerm(term="APT group activity"),
    SearchTerm(term="cyber espionage campaigns"),
    SearchTerm(term="critical infrastructure cybersecurity"),
    SearchTerm(term="cloud security threats"),
    SearchTerm(term="AI in cybersecurity"),
    SearchTerm(term="IoT security risks"),
    SearchTerm(term="supply chain attacks"),
    SearchTerm(term="cybersecurity regulatory compliance"),
    SearchTerm(term="emerging cyber threats"),
    SearchTerm(term="cybersecurity best practices 2024"),
    SearchTerm(term="phishing campaign tactics"),
    SearchTerm(term="insider threats cybersecurity"),
    SearchTerm(term="quantum computing cybersecurity"),
    SearchTerm(term="cybersecurity skills gap"),
    SearchTerm(term="GDPR data protection violations"),
    SearchTerm(term="cybersecurity in remote work"),
    SearchTerm(term="blockchain security issues"),
    SearchTerm(term="5G network security"),
    SearchTerm(term="cyber insurance trends"),
    SearchTerm(term="cybersecurity automation"),
    SearchTerm(term="nation-state cyber attacks"),
    SearchTerm(term="cybersecurity for small businesses"),
    SearchTerm(term="medical device cybersecurity"),
    SearchTerm(term="automotive cybersecurity"),
    SearchTerm(term="deepfake threats"),
    SearchTerm(term="Cybersecurity"),
    SearchTerm(term="Cybersecurity News"),
    SearchTerm(term="Cyber Threats"),
    SearchTerm(term="Cybersecurity Trends"),
    SearchTerm(term="Network Security"),
    SearchTerm(term="Information Security (InfoSec)"),
    SearchTerm(term="Application Security (AppSec)"),
    SearchTerm(term="Security Operations (SecOps)"),
    SearchTerm(term="Endpoint Security"),
    SearchTerm(term="Threat Intelligence"),
    SearchTerm(term="Vulnerability Management"),
    SearchTerm(term="Cybercrime"),
    SearchTerm(term="Cybercrime News"),
    SearchTerm(term="Cybercrime Trends"),
    SearchTerm(term="Cyber Attacks"),
    SearchTerm(term="Hacking News"),
    SearchTerm(term="Malware"),
    SearchTerm(term="Ransomware"),
    SearchTerm(term="Phishing"),
    SearchTerm(term="Data Breaches"),
    SearchTerm(term="Fraud"),
    SearchTerm(term="Identity Theft"),
    SearchTerm(term="Threat Intelligence"),
    SearchTerm(term="Threat Intelligence News"),
    SearchTerm(term="Threat Hunting"),
    SearchTerm(term="Cyber Threat Intelligence (CTI)"),
    SearchTerm(term="Indicators of Compromise (IoC)"),
    SearchTerm(term="Threat Analysis"),
    SearchTerm(term="Cyber Espionage"),
    SearchTerm(term="Zero-Day Exploits"),
    SearchTerm(term="Advanced Persistent Threats (APT)"),
    SearchTerm(term="Cyber Warfare"),
    SearchTerm(term="Dark Web Monitoring"),
    SearchTerm(term="General Intelligence"),
    SearchTerm(term="Security Intelligence"),
    SearchTerm(term="Risk Management"),
    SearchTerm(term="Incident Response"),
    SearchTerm(term="Digital Forensics"),
    SearchTerm(term="Cyber Defense"),
    SearchTerm(term="Security Analytics"),
    SearchTerm(term="Cyber Policy"),
    SearchTerm(term="Security Awareness"),
    SearchTerm(term="Cyber Law"),
    SearchTerm(term="Privacy Protection")
]

# Main script
def load_data(show_sources=True):
    print("Starting comprehensive cybersecurity data collection and analysis...")

    # Collect data
    print("\nCollecting data from multiple sources...")
    input_data = InputData(websites=websites, search_terms=search_terms)
    web_data = scrape_websites(input_data.websites)
    tweet_data = [tweet for term in input_data.search_terms for tweet in fetch_tweets(term, max_tweets=50)]
    cve_data = fetch_cve_data()
    exa_data = [result for term in input_data.search_terms for result in exa_search(term)]
    duckduckgo_data = [result for term in input_data.search_terms for result in duckduckgo_search(term)]

    output_data = OutputData(
        web_data=web_data,
        tweet_data=tweet_data,
        cve_data=cve_data,
        exa_data=exa_data,
        duckduckgo_data=duckduckgo_data,
    )

    print(f"Collected {len(output_data.web_data) + len(output_data.tweet_data) + len(output_data.cve_data) + len(output_data.exa_data) + len(output_data.duckduckgo_data) } total data points")

    print("\nComprehensive cybersecurity data collection and analysis complete.")

    if show_sources:
        return output_data, {"sources": [website.url for website in websites]}
    else:
        return output_data, {}
