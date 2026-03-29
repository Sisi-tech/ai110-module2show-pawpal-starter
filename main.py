from pawpal_system import Owner, Pet, Task, Scheduler

# Build owner/pets/tasks
owner = Owner("Jordan")
pet1 = Pet(pet_id=1, name="Mochi", species="dog", age_years=3)
pet2 = Pet(pet_id=2, name="Luna", species="cat", age_years=2)
owner.add_pet(pet1)
owner.add_pet(pet2)

# Add tasks out of order by time
pet1.add_task(Task(task_id=1, name="Vet visit", description="Checkup", category="health", duration_minutes=60, priority=4))
pet1.add_task(Task(task_id=2, name="Short walk", description="Quick walk", category="walk", duration_minutes=15, priority=3))
pet2.add_task(Task(task_id=3, name="Feed", description="Dinner feed", category="feeding", duration_minutes=10, priority=5))
pet2.add_task(Task(task_id=4, name="Groom", description="Brush coat", category="grooming", duration_minutes=20, priority=2))

# Mark one task complete
pet2.get_task(3).mark_complete()

scheduler = Scheduler(owner, daily_available_minutes=180)

print("Tasks sorted by duration ascending:")
for t in scheduler.sort_by_time(descending=False):
    print(f"{t.name} - {t.duration_minutes}m (completed={t.completed})")

print("\nTasks sorted by duration descending:")
for t in scheduler.sort_by_time(descending=True):
    print(f"{t.name} - {t.duration_minutes}m (completed={t.completed})")

print("\nFilter completed tasks:")
for t in scheduler.filter_tasks(completed=True):
    print(f"{t.name} - completed={t.completed}")

print("\nTasks for pet Luna:")
for t in scheduler.filter_tasks(pet_name="Luna"):
    print(f"{t.name} ({t.duration_minutes}m) - completed={t.completed}")

print("\nSchedule today:")
print(scheduler.schedule_today())
