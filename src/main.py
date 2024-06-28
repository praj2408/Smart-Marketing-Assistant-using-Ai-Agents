from dotenv import load_dotenv
from crewai import Crew
from tasks import MeetingPrepTask
from agents import MeetingPrepAgents

def main():
    # Load environment variables from a .env file
    load_dotenv()
    
    print("Welcome to the Meeting prep crew")
    print("----------------------------------------------------------------")
    
    # Collect input from the user about the meeting
    meeting_participants = input("What are the emails for the participants (other than you) in the meeting?\n")
    meeting_context = input("What are the context of the meeting?\n")
    meeting_objective = input("What are the objective for this meeting?\n")
    
    # Create instances of MeetingPrepTask and MeetingPrepAgents classes
    tasks = MeetingPrepTask()
    agents = MeetingPrepAgents()
    
    # Create agents for different tasks
    research_agent = agents.research_agent()
    industry_analysis_agent = agents.industry_analysis_agent()
    meeting_strategy_agent = agents.meeting_strategy_agent()
    summary_and_briefing_agent = agents.summary_and_briefing_agent()
    
    
    # Create tasks and assign them to agents
    research_task = tasks.research_task(research_agent, meeting_participants, meeting_context)
    industry_analysis_task = tasks.industry_analysis_task(industry_analysis_agent, meeting_participants, meeting_context)
    meeting_strategy_task = tasks.meeting_strategy_task(meeting_strategy_agent, meeting_context, meeting_objective)
    summary_and_briefing_task = tasks.summary_and_briefing_task(summary_and_briefing_agent, meeting_context, meeting_objective)
    
    # Set context dependencies for the meeting strategy task
    meeting_strategy_task.context = [research_task, industry_analysis_task]
    
    # Set context dependencies for the summary and briefing task
    summary_and_briefing_task.context = [research_task, industry_analysis_task, meeting_strategy_task]
    
    # Create a crew with the agents and tasks
    crew = Crew(
        agents=[
            research_agent,
            industry_analysis_agent,
            meeting_strategy_agent,
            summary_and_briefing_agent
        ],
        tasks=[
            research_task,
            industry_analysis_task,
            meeting_strategy_task,
            summary_and_briefing_task
        ]
    )
    
    # Kick off the crew tasks and get the result
    result = crew.kickoff()
    
    print(result)
     
if __name__ == "__main__":
    main()