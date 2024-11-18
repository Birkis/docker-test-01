from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

@CrewBase
class BirthdayPartyPlanningCrew:
    """Birthday Party Planning crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            verbose=True,
        )

    @agent
    def content_generator(self) -> Agent:
        return Agent(config=self.agents_config["content_generator"], verbose=True)

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def content_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config["content_generation_task"],
            
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Birthday Party Planning crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
