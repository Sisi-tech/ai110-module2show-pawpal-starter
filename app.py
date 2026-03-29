import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age_years = st.number_input("Pet age", min_value=0, max_value=30, value=2)

if "owner" not in st.session_state:
    st.session_state.owner = None

# Create or reuse owner instance
if st.button("Create/Select Owner"):
    if not st.session_state.owner:
        st.session_state.owner = Owner(owner_name)
    else:
        # Update owner name if changed
        st.session_state.owner.owner_name = owner_name
    st.success(f"Owner set to: {st.session_state.owner.owner_name}")

if st.session_state.owner:
    st.write(f"Owner: {st.session_state.owner.owner_name}")

# Add pet
if st.button("Add pet"):
    if st.session_state.owner is None:
        st.error("Create an owner first")
    else:
        pet = Pet(pet_id=len(st.session_state.owner.pets) + 1, name=pet_name, species=species, age_years=int(age_years))
        st.session_state.owner.add_pet(pet)
        st.success(f"Added pet: {pet_name}")

if st.session_state.owner and st.session_state.owner.pets:
    st.write("### Current pets")
    for pet in st.session_state.owner.list_pets():
        st.write(f"- {pet.pet_id}: {pet.name} ({pet.species}, {pet.age_years} yrs)")

st.divider()

st.subheader("Task management")
if "task_title" not in st.session_state:
    st.session_state.task_title = "Morning walk"

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value=st.session_state.task_title)
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task to selected pet"):
    if st.session_state.owner is None or not st.session_state.owner.pets:
        st.error("Add an owner and pet first")
    else:
        selected_pet = st.session_state.owner.get_pet(1)
        if selected_pet is None:
            st.error("Pet not found")
        else:
            task = Task(
                task_id=len(selected_pet.tasks) + 1,
                name=task_title,
                description=task_title,
                category=priority,
                duration_minutes=int(duration),
                priority=3 if priority == "high" else 2 if priority == "medium" else 1,
            )
            selected_pet.add_task(task)
            st.success(f"Added task '{task_title}' to pet {selected_pet.name}")

if st.session_state.owner and st.session_state.owner.pets:
    sel_pet = st.session_state.owner.get_pet(1)
    if sel_pet:
        st.write(f"### Tasks for {sel_pet.name}")
        st.table([t.to_dict() for t in sel_pet.list_tasks()])

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    if st.session_state.owner is None:
        st.error("Add owner and pet/tasks first")
    else:
        scheduler = Scheduler(st.session_state.owner, daily_available_minutes=120)
        result = scheduler.schedule_today()
        st.success("Schedule generated")
        st.write(result)

