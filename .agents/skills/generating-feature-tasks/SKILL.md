---
name: generating-feature-tasks
description: Generates dependency-ordered implementation tasks for an active Specify feature. Use when asked to create tasks.md, break a plan into tasks, or prepare a Specify feature for implementation.
---

# Generate Specify Feature Tasks

Run the Specify task-generation workflow for the active feature.

Treat the user's request as the workflow input. Read and follow every instruction in `.agents/commands/speckit.tasks.md`, replacing `$ARGUMENTS` with that input. Run commands from the repository root.
