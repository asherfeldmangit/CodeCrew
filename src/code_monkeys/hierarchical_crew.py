from __future__ import annotations

from typing import Optional

from crewai import Crew as BaseCrew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent  # type: ignore


class HierarchicalCrew(BaseCrew):
    """Crew subclass that keeps hierarchical flow but executes each task with its
    designated agent so that console logs display the real worker instead of the
    manager agent."""

    # pylint: disable=protected-access
    def _get_agent_to_use(self, task: Task) -> Optional[BaseAgent]:  # type: ignore[override]
        # In hierarchical mode default Crew returns manager_agent. For clearer
        # logs we prefer the task's own agent if it exists.
        if self.process == Process.hierarchical and task.agent is not None:
            return task.agent
        # Fall back to the default (manager or task agent)
        return self.manager_agent if self.process == Process.hierarchical else task.agent 