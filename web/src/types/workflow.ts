export interface Task {
  name: string
  description: string
  input_schema: {
    properties: Record<string, {
      type: string
      description?: string
    }>
    required?: string[]
  }
  output_schema: Record<string, unknown>
}

export interface Stage {
  name: string
  description: string
  tasks: Record<string, Task>
  transitions: string[]
  prerequisites: string[]
}

export interface Workflow {
  name: string
  description: string
  stages: Record<string, Stage>
  initial_stage: string
}

export interface GraphNode {
  id: string
  type: string
  data: {
    label: string
    description: string
    taskCount: number
    isInitial: boolean
    tasks: string[]
  }
  position: { x: number; y: number }
}

export interface GraphEdge {
  id: string
  source: string
  target: string
  label?: string
  animated?: boolean
}

export interface WorkflowGraph {
  nodes: GraphNode[]
  edges: GraphEdge[]
}

