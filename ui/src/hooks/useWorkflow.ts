import { useQuery } from '@tanstack/react-query'
import type { Workflow, WorkflowGraph } from '../types/workflow'
import { mockWorkflow, mockWorkflowGraph } from '../data/mockWorkflow'

async function fetchWorkflow(_name: string): Promise<Workflow> {
  await new Promise(resolve => setTimeout(resolve, 300))
  return mockWorkflow
}

async function fetchWorkflowGraph(_name: string): Promise<WorkflowGraph> {
  await new Promise(resolve => setTimeout(resolve, 300))
  return mockWorkflowGraph
}

export function useWorkflow(name: string) {
  return useQuery({
    queryKey: ['workflow', name],
    queryFn: () => fetchWorkflow(name),
  })
}

export function useWorkflowGraph(name: string) {
  return useQuery({
    queryKey: ['workflow-graph', name],
    queryFn: () => fetchWorkflowGraph(name),
  })
}

