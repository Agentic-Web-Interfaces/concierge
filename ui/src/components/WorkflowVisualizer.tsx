import { useState } from 'react'
import { ReactFlowProvider } from 'reactflow'
import { WorkflowCanvas } from './WorkflowCanvas'
import { StageTree } from './StageTree'
import { StageInspector } from './StageInspector'
import { Header } from './Header'
import { useWorkflow } from '../hooks/useWorkflow'

interface WorkflowVisualizerProps {
  workflowName: string
}

export function WorkflowVisualizer({ workflowName }: WorkflowVisualizerProps) {
  const [selectedStage, setSelectedStage] = useState<string | null>(null)
  const { data: workflow, isLoading, error } = useWorkflow(workflowName)

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-muted-foreground">Loading workflow...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-destructive">Error loading workflow: {error.message}</div>
      </div>
    )
  }

  if (!workflow) return null

  return (
    <ReactFlowProvider>
      <div className="flex flex-col h-full">
        <Header workflowName={workflow.name} description={workflow.description} />
        
        <div className="flex flex-1 overflow-hidden">
          {/* Left: Stage Tree */}
          <div className="w-64 border-r border-border bg-card flex-shrink-0">
            <StageTree
              workflow={workflow}
              selectedStage={selectedStage}
              onSelectStage={setSelectedStage}
            />
          </div>

          {/* Center: Canvas */}
          <div className="flex-1 relative">
            <WorkflowCanvas
              workflowName={workflowName}
              selectedStage={selectedStage}
              onSelectStage={setSelectedStage}
            />
          </div>

          {/* Right: Inspector */}
          {selectedStage && (
            <div className="w-96 border-l border-border bg-card flex-shrink-0">
              <StageInspector
                workflowName={workflowName}
                stageName={selectedStage}
                onClose={() => setSelectedStage(null)}
              />
            </div>
          )}
        </div>
      </div>
    </ReactFlowProvider>
  )
}

