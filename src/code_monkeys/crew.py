from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool


@CrewBase
class CodeMonkeys:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def coder_agent(self) -> Agent:
        return Agent(config=self.agents_config['coder_agent'],
                     verbose=True,
                     allow_code_execution=True,
                     code_execution_mode="safe",
                     max_execution_time=360,
                     max_retry_limit=5,
                     )
    
    @task
    def coding_task(self) -> Task:
        return Task(config=self.tasks_config['coding_task'])
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
