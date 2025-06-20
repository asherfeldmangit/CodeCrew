from crewai import Agent, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from code_monkeys.hierarchical_crew import HierarchicalCrew
from crewai_tools import SerperDevTool


@CrewBase
class EngineeringTeam():
    """Engineering team crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_delegation=True,
            allow_code_execution=True,
            code_execution_mode="safe", 
            max_execution_time=1200, 
            max_retry_limit=20,
            memory=True,
            tools=[SerperDevTool()]
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
            allow_delegation=True,
            allow_code_execution=True,
            code_execution_mode="safe", 
            max_execution_time=1200, 
            max_retry_limit=20,
            memory=True,
            tools=[SerperDevTool()]
        )
    
    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=600, 
            max_retry_limit=5,
            memory=True
        )

    @agent
    def architect_agent(self) -> Agent:
        """A senior software architect responsible for high-level design and code reviews."""
        return Agent(
            config=self.agents_config['architect_agent'],
            verbose=True,
            allow_delegation=True,
            memory=True,
            tools=[SerperDevTool()]
        )

    @agent
    def task_breaker(self) -> Agent:
        """Engineer that decomposes the high-level design into atomic tasks."""
        return Agent(
            config=self.agents_config['task_breaker'],
            verbose=True,
            memory=True
        )

    @task
    def design_task(self) -> Task:
        return Task(config=self.tasks_config['design_task'])

    @task
    def breaking_task(self) -> Task:
        return Task(config=self.tasks_config['breaking_task'])

    @task
    def backend_code_task(self) -> Task:
        return Task(config=self.tasks_config['backend_code_task'])

    @task
    def backend_code_review_task(self) -> Task:
        return Task(config=self.tasks_config['backend_code_review_task'])

    @task
    def fix_backend_comments_task(self) -> Task:
        return Task(config=self.tasks_config['fix_backend_comments_task'])

    @task
    def frontend_task(self) -> Task:
        return Task(config=self.tasks_config['frontend_task'])

    @task
    def dependency_audit_task(self) -> Task:
        return Task(config=self.tasks_config['dependency_audit_task'])

    @task
    def test_task(self) -> Task:
        return Task(config=self.tasks_config['test_task'])

    @task
    def frontend_code_review_task(self) -> Task:
        return Task(config=self.tasks_config['frontend_code_review_task'])

    @task
    def fix_frontend_comments_task(self) -> Task:
        return Task(config=self.tasks_config['fix_frontend_comments_task'])

    @task
    def end_to_end_test_task(self) -> Task:
        return Task(config=self.tasks_config['end_to_end_test_task'])

    @task
    def materialise_code_task(self) -> Task:
        return Task(config=self.tasks_config['materialise_code_task'])

    @agent
    def utility_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['utility_agent'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=300,
            max_retry_limit=5,
            memory=True
        )

    @crew
    def crew(self) -> HierarchicalCrew:
        """Creates the Code Monkeys crew"""

        manager = Agent(
            config=self.agents_config['engineering_lead'],
            allow_delegation=True, 
            verbose=True,
            memory=True
        )
            
        return HierarchicalCrew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,

            # Long-term memory for persistent storage across sessions
            long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/long_term_memory_storage.db"
                )
            ),
            # Short-term memory for current context using RAG
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                        embedder_config={
                            "provider": "openai",
                            "config": {
                                "model": 'text-embedding-3-small'
                            }
                        },
                        type="short_term",
                        path="./memory/"
                    )
                ),            
            # Entity memory for tracking key information about entities
            entity_memory = EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path="./memory/"
                )
            ),
        )
