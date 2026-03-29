import pytest
from pawpal_system import Task, Pet


def test_task_completion_marks_task_complete():
    task = Task(
        task_id=1,
        name='Walk',
        description='Morning walk',
        category='walk',
        duration_minutes=30,
        priority=5,
    )

    assert not task.completed
    assert task.completed_at is None

    task.mark_complete()

    assert task.completed
    assert task.completed_at is not None


def test_pet_add_task_increases_task_count():
    pet = Pet(pet_id=1, name='Fido', species='dog', age_years=4)
    assert len(pet.tasks) == 0

    task = Task(
        task_id=1,
        name='Feed',
        description='Breakfast',
        category='feeding',
        duration_minutes=10,
        priority=4,
    )

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.get_task(1) is task
