import sys
import os
import types
import pytest
from unittest.mock import MagicMock, patch

# Add the euriai directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../euriai')))

import euri_crewai
from euri_crewai import EuriaiCrewAI

@pytest.fixture(autouse=True)
def patch_crewai():
    # Patch Agent, Task, Crew, Process in euri_crewai's namespace
    with patch('euri_crewai.Agent', MagicMock(name='Agent')) as agent_mock, \
         patch('euri_crewai.Task', MagicMock(name='Task')) as task_mock, \
         patch('euri_crewai.Crew', MagicMock(name='Crew')) as crew_mock, \
         patch('euri_crewai.Process', types.SimpleNamespace(sequential='seq', parallel='par')):
        yield

def test_import_euri_crewai():
    assert euri_crewai is not None 

def test_constructor():
    crewai = EuriaiCrewAI()
    assert crewai._agents == []
    assert crewai._tasks == []
    assert crewai._crew is None
    assert crewai.process == 'seq'

def test_add_agent():
    crewai = EuriaiCrewAI()
    config = {'foo': 'bar'}
    crewai.add_agent('agent1', config)
    assert 'agent1' in crewai.agents_config
    assert crewai._agents  # Should have one agent (mocked)

def test_add_task():
    crewai = EuriaiCrewAI()
    config = {'baz': 'qux'}
    crewai.add_task('task1', config)
    assert 'task1' in crewai.tasks_config
    assert crewai._tasks  # Should have one task (mocked)

def test_get_agents_and_tasks():
    crewai = EuriaiCrewAI()
    crewai.add_agent('agent1', {'foo': 'bar'})
    crewai.add_task('task1', {'baz': 'qux'})
    assert len(crewai.get_agents()) == 1
    assert len(crewai.get_tasks()) == 1

def test_reset():
    crewai = EuriaiCrewAI()
    crewai.add_agent('agent1', {'foo': 'bar'})
    crewai.add_task('task1', {'baz': 'qux'})
    crewai.reset()
    assert crewai._agents == []
    assert crewai._tasks == []
    assert crewai._crew is None 

def test_build_crew():
    crewai = EuriaiCrewAI()
    crewai.add_agent('agent1', {'foo': 'bar'})
    crewai.add_task('task1', {'baz': 'qux'})
    crew = crewai.build_crew()
    assert crew is not None
    assert crewai._crew is crew

def test_run():
    crewai = EuriaiCrewAI()
    crewai.add_agent('agent1', {'foo': 'bar'})
    crewai.add_task('task1', {'baz': 'qux'})
    # Patch the Crew.kickoff method to return a known value
    with patch('euri_crewai.Crew') as CrewMock:
        instance = CrewMock.return_value
        instance.kickoff.return_value = 'result123'
        crewai.build_crew()
        result = crewai.run({'input': 1})
        assert result == 'result123'
        instance.kickoff.assert_called_once()

def test_from_yaml(tmp_path):
    agents_yaml = tmp_path / 'agents.yaml'
    tasks_yaml = tmp_path / 'tasks.yaml'
    agents_yaml.write_text('agent1:\n  foo: bar\n')
    tasks_yaml.write_text('task1:\n  baz: qux\n')
    with patch('euri_crewai.Agent', MagicMock(name='Agent')):
        with patch('euri_crewai.Task', MagicMock(name='Task')):
            obj = EuriaiCrewAI.from_yaml(str(agents_yaml), str(tasks_yaml))
            assert isinstance(obj, EuriaiCrewAI)
            assert 'agent1' in obj.agents_config
            assert 'task1' in obj.tasks_config

def test_get_crew():
    crewai = EuriaiCrewAI()
    assert crewai.get_crew() is None
    crewai.add_agent('agent1', {'foo': 'bar'})
    crewai.add_task('task1', {'baz': 'qux'})
    crewai.build_crew()
    assert crewai.get_crew() is not None 