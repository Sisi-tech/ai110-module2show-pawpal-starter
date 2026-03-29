# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

- Core action 1: Add and manage pet care tasks. Users can create tasks with duration, priority, and category, then update or remove them.
- Core action 2: Generate a daily schedule. The system selects and orders tasks within available time and explains the rationale.
- Core action 3: View today’s plan (scheduled tasks with time blocks) and explanation of why each task was selected.

**b. Building blocks**

- Task: stores id, name, category, duration, priority, status; methods to update/manage status.
- TaskManager: tracks tasks list; methods add/edit/remove/list tasks.
- Schedule: stores date, assignments, total used time, explanation; methods validate/serialize.
- Scheduler: uses TaskManager + constraints; methods select tasks, build plan, and generate reasoning.
- OwnerProfile: stores owner/pet availability and preferences; methods return available time.

**c. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

- Core action 1 mapped to constraint: task data correctness and edit flow (must be possible to create/update/delete tasks).
- Core action 2 mapped to constraint: available daily time budget and priority ordering to choose tasks.
- Core action 3 mapped to constraint: output clarity + reasoning explanation (users need to understand schedule decisions).

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
