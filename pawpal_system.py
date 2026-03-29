from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, List, Optional


@dataclass
class Task:
    task_id: int
    name: str
    description: str
    category: str
    duration_minutes: int
    priority: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    frequency_days: Optional[int] = None
    deadline: Optional[datetime] = None
    completed: bool = False
    completed_at: Optional[datetime] = None

    def mark_complete(self, at: Optional[datetime] = None) -> None:
        """Mark the task complete and track when it was done."""
        self.completed = True
        self.completed_at = at or datetime.now()

    def reset(self) -> None:
        """Reset completion status to incomplete."""
        self.completed = False
        self.completed_at = None

    def update(self, **updates) -> None:
        """Update one or more task fields from keyword arguments."""
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self) -> Dict:
        """Serialize this task into a JSON-friendly dictionary."""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "frequency_days": self.frequency_days,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "completed": self.completed,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass
class Pet:
    pet_id: int
    name: str
    species: str
    age_years: int
    tasks: Dict[int, Task] = field(default_factory=dict)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks[task.task_id] = task

    def remove_task(self, task_id: int) -> None:
        """Remove a task by ID from this pet."""
        if task_id in self.tasks:
            del self.tasks[task_id]

    def get_task(self, task_id: int) -> Optional[Task]:
        """Return the task matching task_id, or None if missing."""
        return self.tasks.get(task_id)

    def list_tasks(self, include_completed: bool = True) -> List[Task]:
        all_tasks = list(self.tasks.values())
        if not include_completed:
            all_tasks = [t for t in all_tasks if not t.completed]
        return sorted(all_tasks, key=lambda t: (-t.priority, t.duration_minutes))

    def to_dict(self) -> Dict:
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "species": self.species,
            "age_years": self.age_years,
            "tasks": [task.to_dict() for task in self.list_tasks()],
        }


class Owner:
    def __init__(self, owner_name: str):
        self.owner_name = owner_name
        self.pets: Dict[int, Pet] = {}

    def add_pet(self, pet: Pet) -> None:
        """Add a pet record for this owner."""
        self.pets[pet.pet_id] = pet

    def remove_pet(self, pet_id: int) -> None:
        """Remove a pet record from this owner."""
        if pet_id in self.pets:
            del self.pets[pet_id]

    def get_pet(self, pet_id: int) -> Optional[Pet]:
        return self.pets.get(pet_id)

    def list_pets(self) -> List[Pet]:
        return list(self.pets.values())

    def all_tasks(self, include_completed: bool = True) -> List[Task]:
        tasks: List[Task] = []
        for pet in self.pets.values():
            tasks.extend(pet.list_tasks(include_completed=include_completed))
        return sorted(tasks, key=lambda t: (-t.priority, t.deadline or datetime.max))

    def to_dict(self) -> Dict:
        return {
            "owner_name": self.owner_name,
            "pets": [pet.to_dict() for pet in self.list_pets()],
        }


class Scheduler:
    def __init__(self, owner: Owner, daily_available_minutes: int = 120):
        self.owner = owner
        self.daily_available_minutes = daily_available_minutes

    def get_priority_queue(self, include_completed: bool = False) -> List[Task]:
        """Get all tasks ordered by priority for scheduling."""
        return self.owner.all_tasks(include_completed=include_completed)

    def sort_by_time(self, descending: bool = False) -> List[Task]:
        """Sort tasks by duration_minutes across all pets."""
        tasks = self.owner.all_tasks(include_completed=True)
        return sorted(tasks, key=lambda t: t.duration_minutes, reverse=descending)

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status or by pet name."""
        filtered: List[Task] = []
        pets = self.owner.list_pets() if pet_name is None else [p for p in self.owner.list_pets() if p.name == pet_name]
        for pet in pets:
            for task in pet.list_tasks(include_completed=True):
                if completed is None or task.completed == completed:
                    filtered.append(task)
        return filtered

    def schedule_today(self, target_date: Optional[date] = None) -> Dict:
        target_date = target_date or date.today()
        available = self.daily_available_minutes
        total = 0
        selected: List[Task] = []

        for task in self.get_priority_queue(include_completed=False):
            if total + task.duration_minutes > available:
                continue
            selected.append(task)
            total += task.duration_minutes

        explanation = [
            f"Scheduled {len(selected)} tasks for {target_date.isoformat()} (using {total}/{available} mins)"
        ]
        for task in selected:
            explanation.append(
                f"{task.name} ({task.category}) {task.duration_minutes}m priority {task.priority}"
            )

        return {
            "date": target_date.isoformat(),
            "available_minutes": available,
            "scheduled_minutes": total,
            "tasks": [task.to_dict() for task in selected],
            "explanation": explanation,
        }

    def detect_conflicts(self) -> List[str]:
        """Detect scheduling conflicts for tasks that have explicit start/end times."""
        conflicts: List[str] = []
        tasks = [t for t in self.owner.all_tasks(include_completed=True) if t.start_time and t.end_time]
        tasks_sorted = sorted(tasks, key=lambda t: t.start_time)

        for i, t1 in enumerate(tasks_sorted):
            for t2 in tasks_sorted[i + 1 :]:
                if t2.start_time >= t1.end_time:
                    break
                overlap = t1.end_time > t2.start_time
                if overlap:
                    conflicts.append(
                        f"Conflict between task '{t1.name}' and '{t2.name}' (start {t2.start_time}, end {t2.end_time})."
                    )

        return conflicts

    def add_task_to_pet(self, pet_id: int, task: Task) -> bool:
        pet = self.owner.get_pet(pet_id)
        if not pet:
            return False
        pet.add_task(task)
        return True

    def mark_task_complete(self, pet_id: int, task_id: int, completed_at: Optional[datetime] = None) -> bool:
        pet = self.owner.get_pet(pet_id)
        if not pet:
            return False
        task = pet.get_task(task_id)
        if not task:
            return False

        task.mark_complete(at=completed_at)

        # Recurring task support: daily/weekly tasks are recreated for next occurrence
        if task.frequency_days in (1, 7):
            next_deadline = None
            if task.deadline:
                next_deadline = task.deadline + timedelta(days=task.frequency_days)

            new_task_id = max(pet.tasks.keys(), default=0) + 1
            recurring_task = Task(
                task_id=new_task_id,
                name=task.name,
                description=task.description,
                category=task.category,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                frequency_days=task.frequency_days,
                deadline=next_deadline,
                completed=False,
                completed_at=None,
            )
            pet.add_task(recurring_task)

        return True

