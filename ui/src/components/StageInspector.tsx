import { X, Wrench, ArrowRight, Code2, FileJson } from 'lucide-react'
import { useWorkflow } from '../hooks/useWorkflow'

interface StageInspectorProps {
  workflowName: string
  stageName: string
  onClose: () => void
}

export function StageInspector({ workflowName, stageName, onClose }: StageInspectorProps) {
  const { data: workflow } = useWorkflow(workflowName)
  
  if (!workflow) return null

  const stage = workflow.stages[stageName]
  if (!stage) return null

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-border flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold">{stageName}</h2>
          <p className="text-sm text-muted-foreground">{stage.description}</p>
        </div>
        <button
          onClick={onClose}
          className="p-2 hover:bg-accent rounded-md transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {/* Tasks */}
        <section>
          <div className="flex items-center gap-2 mb-3">
            <Wrench className="w-4 h-4 text-muted-foreground" />
            <h3 className="font-semibold">Tasks ({Object.keys(stage.tasks).length})</h3>
          </div>
          <div className="space-y-3">
            {Object.entries(stage.tasks).map(([taskName, task]) => (
              <div
                key={taskName}
                className="p-4 rounded-lg border border-border bg-card/50 space-y-3"
              >
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <Code2 className="w-4 h-4 text-purple-500" />
                    <span className="font-mono font-semibold">{taskName}</span>
                  </div>
                  <p className="text-sm text-muted-foreground">{task.description}</p>
                </div>

                {/* Input Schema */}
                {task.input_schema && Object.keys(task.input_schema.properties || {}).length > 0 && (
                  <div>
                    <div className="text-xs font-semibold text-muted-foreground mb-2">
                      INPUT
                    </div>
                    <div className="space-y-1">
                      {Object.entries(task.input_schema.properties).map(([paramName, param]) => (
                        <div
                          key={paramName}
                          className="flex items-center gap-2 text-sm font-mono"
                        >
                          <span className="text-foreground">{paramName}</span>
                          <span className="text-muted-foreground">:</span>
                          <span className="text-blue-400">{param.type}</span>
                          {task.input_schema.required?.includes(paramName) && (
                            <span className="text-xs px-1.5 py-0.5 bg-red-500/20 text-red-400 rounded">
                              required
                            </span>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Output Schema */}
                {task.output_schema && (
                  <div>
                    <div className="text-xs font-semibold text-muted-foreground mb-2">
                      OUTPUT
                    </div>
                    <pre className="text-xs font-mono bg-accent/50 p-2 rounded overflow-x-auto">
                      {JSON.stringify(task.output_schema, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* Transitions */}
        {stage.transitions && stage.transitions.length > 0 && (
          <section>
            <div className="flex items-center gap-2 mb-3">
              <ArrowRight className="w-4 h-4 text-muted-foreground" />
              <h3 className="font-semibold">Transitions ({stage.transitions.length})</h3>
            </div>
            <div className="space-y-2">
              {stage.transitions.map((target) => (
                <div
                  key={target}
                  className="flex items-center gap-2 p-3 rounded-lg border border-border bg-card/50"
                >
                  <ArrowRight className="w-4 h-4 text-green-500" />
                  <span className="font-medium">{target}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Prerequisites */}
        {stage.prerequisites && stage.prerequisites.length > 0 && (
          <section>
            <div className="flex items-center gap-2 mb-3">
              <FileJson className="w-4 h-4 text-muted-foreground" />
              <h3 className="font-semibold">Prerequisites</h3>
            </div>
            <div className="space-y-2">
              {stage.prerequisites.map((prereq) => (
                <div
                  key={prereq}
                  className="p-3 rounded-lg border border-border bg-card/50 font-mono text-sm"
                >
                  {prereq}
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  )
}

