import type { PluginAPI, PluginCommandContext } from '@ampcode/plugin'

export const description = 'Adds Specify workflow commands to the Amp command palette for this project.'

type SpecifyCommand = {
  id: string
  title: string
  description: string
  skill: string
  inputLabel: string
  inputHelp: string
  required?: boolean
}

const commands: SpecifyCommand[] = [
  {
    id: 'specify',
    title: 'Specify feature',
    description: 'Create or update a feature specification from a natural-language request.',
    skill: 'specifying-features',
    inputLabel: 'Feature description',
    inputHelp: 'Describe the feature to specify.',
    required: true,
  },
  {
    id: 'clarify',
    title: 'Clarify specification',
    description: 'Identify and resolve ambiguous requirements in the active feature specification.',
    skill: 'clarifying-feature-specifications',
    inputLabel: 'Additional context',
    inputHelp: 'Optionally provide clarification context or leave this blank.',
  },
  {
    id: 'plan',
    title: 'Plan implementation',
    description: 'Generate technical design artifacts for the active feature.',
    skill: 'planning-feature-implementation',
    inputLabel: 'Planning context',
    inputHelp: 'Optionally provide technical constraints or leave this blank.',
  },
  {
    id: 'tasks',
    title: 'Generate tasks',
    description: 'Generate dependency-ordered implementation tasks for the active feature.',
    skill: 'generating-feature-tasks',
    inputLabel: 'Task-generation context',
    inputHelp: 'Optionally provide task-generation context or leave this blank.',
  },
  {
    id: 'implement',
    title: 'Implement feature',
    description: 'Execute the active feature implementation plan.',
    skill: 'implementing-feature-plans',
    inputLabel: 'Implementation context',
    inputHelp: 'Optionally provide implementation instructions or leave this blank.',
  },
  {
    id: 'analyze',
    title: 'Analyze feature consistency',
    description: 'Analyze generated feature artifacts for consistency and quality.',
    skill: 'analyzing-feature-consistency',
    inputLabel: 'Analysis context',
    inputHelp: 'Optionally provide a focus area or leave this blank.',
  },
  {
    id: 'converge',
    title: 'Converge feature work',
    description: 'Find unfinished specified work and append it to the active feature tasks.',
    skill: 'converging-feature-work',
    inputLabel: 'Convergence context',
    inputHelp: 'Optionally provide a focus area or leave this blank.',
  },
  {
    id: 'checklist',
    title: 'Create feature checklist',
    description: 'Create a requirements-quality checklist for the active feature.',
    skill: 'creating-feature-checklists',
    inputLabel: 'Checklist domain',
    inputHelp: 'Describe the domain to assess, such as security or accessibility.',
    required: true,
  },
  {
    id: 'constitution',
    title: 'Create project constitution',
    description: 'Create or update project governance principles.',
    skill: 'creating-project-constitutions',
    inputLabel: 'Constitution input',
    inputHelp: 'Describe the principles to create or revise.',
  },
]

async function runCommand(command: SpecifyCommand, ctx: PluginCommandContext) {
  if (!ctx.thread) {
    await ctx.ui.notify('Open a project thread before running a Specify command.')
    return
  }

  const input = await ctx.ui.input({
    title: `Specify: ${command.title}`,
    helpText: command.inputHelp,
    placeholder: command.inputLabel,
  })

  if (input === undefined || (command.required && !input.trim())) {
    return
  }

  const context = input.trim() || 'No additional input was provided.'
  await ctx.thread.append([
    {
      type: 'user-message',
      content: `Use the \`${command.skill}\` skill. Workflow input: ${context}`,
    },
  ])
}

export default function (amp: PluginAPI) {
  for (const command of commands) {
    amp.registerCommand(
      `speckit-${command.id}`,
      {
        title: command.title,
        category: 'Specify',
        description: command.description,
      },
      (ctx) => runCommand(command, ctx),
    )
  }
}
