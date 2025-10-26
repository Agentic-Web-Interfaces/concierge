import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Panel,
  useReactFlow,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { useWorkflowGraph } from '../hooks/useWorkflow'
import { StageNode } from './StageNode'
import { useCallback, useEffect } from 'react'
import { ZoomIn, ZoomOut, Maximize } from 'lucide-react'

interface WorkflowCanvasProps {
  workflowName: string
  selectedStage: string | null
  onSelectStage: (stageName: string) => void
}

const nodeTypes = {
  stage: StageNode,
}

export function WorkflowCanvas({
  workflowName,
  selectedStage,
  onSelectStage,
}: WorkflowCanvasProps) {
  const { data: graph, isLoading } = useWorkflowGraph(workflowName)
  const { fitView, zoomIn, zoomOut } = useReactFlow()

  useEffect(() => {
    if (graph) {
      setTimeout(() => fitView({ padding: 0.2 }), 100)
    }
  }, [graph, fitView])

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: any) => {
      onSelectStage(node.id)
    },
    [onSelectStage]
  )

  if (isLoading || !graph) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-muted-foreground">Loading graph...</div>
      </div>
    )
  }

  const nodes = graph.nodes.map((node) => ({
    ...node,
    data: {
      ...node.data,
      isSelected: node.id === selectedStage,
    },
  }))

  return (
    <ReactFlow
      nodes={nodes}
      edges={graph.edges}
      nodeTypes={nodeTypes}
      onNodeClick={onNodeClick}
      fitView
      attributionPosition="bottom-left"
      proOptions={{ hideAttribution: true }}
    >
      <Background />
      <Controls showInteractive={false} />
      <MiniMap
        className="bg-card border border-border"
        nodeColor={(node) => {
          if (node.data.isInitial) return '#10b981'
          return '#8b5cf6'
        }}
      />
      
      <Panel position="top-right" className="flex gap-2">
        <button
          onClick={() => zoomIn()}
          className="p-2 bg-card border border-border rounded-md hover:bg-accent transition-colors"
          title="Zoom in"
        >
          <ZoomIn className="w-4 h-4" />
        </button>
        <button
          onClick={() => zoomOut()}
          className="p-2 bg-card border border-border rounded-md hover:bg-accent transition-colors"
          title="Zoom out"
        >
          <ZoomOut className="w-4 h-4" />
        </button>
        <button
          onClick={() => fitView({ padding: 0.2 })}
          className="p-2 bg-card border border-border rounded-md hover:bg-accent transition-colors"
          title="Fit to screen"
        >
          <Maximize className="w-4 h-4" />
        </button>
      </Panel>
    </ReactFlow>
  )
}

