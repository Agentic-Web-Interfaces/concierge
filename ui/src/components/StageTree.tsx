import { ChevronDown, ChevronRight, Circle, Wrench } from 'lucide-react'
import { useState } from 'react'
import type { Workflow } from '../types/workflow'
import { cn } from '../lib/utils'

interface StageTreeProps {
  workflow: Workflow
  selectedStage: string | null
  onSelectStage: (stageName: string) => void
}

export function StageTree({ workflow, selectedStage, onSelectStage }: StageTreeProps) {
  const [expandedStages, setExpandedStages] = useState<Set<string>>(
    new Set(Object.keys(workflow.stages))
  )

  const toggleStage = (stageName: string) => {
    const newExpanded = new Set(expandedStages)
    if (newExpanded.has(stageName)) {
      newExpanded.delete(stageName)
    } else {
      newExpanded.add(stageName)
    }
    setExpandedStages(newExpanded)
  }

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-border">
        <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
          Stages
        </h2>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
        {Object.entries(workflow.stages).map(([stageName, stage]) => {
          const isExpanded = expandedStages.has(stageName)
          const isSelected = selectedStage === stageName
          const isInitial = workflow.initial_stage === stageName
          const taskCount = Object.keys(stage.tasks).length

          return (
            <div key={stageName} className="mb-1">
              {/* Stage Item */}
              <button
                onClick={() => onSelectStage(stageName)}
                className={cn(
                  "w-full flex items-center gap-2 px-3 py-2 rounded-md text-sm transition-colors group",
                  isSelected
                    ? "bg-accent text-accent-foreground"
                    : "hover:bg-accent/50"
                )}
              >
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    toggleStage(stageName)
                  }}
                  className="hover:bg-accent/50 rounded p-0.5"
                >
                  {isExpanded ? (
                    <ChevronDown className="w-4 h-4" />
                  ) : (
                    <ChevronRight className="w-4 h-4" />
                  )}
                </button>

                {isInitial && (
                  <Circle className="w-3 h-3 text-green-500 fill-green-500" />
                )}
                
                <span className="flex-1 text-left font-medium">{stageName}</span>
                
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <Wrench className="w-3 h-3" />
                  <span>{taskCount}</span>
                </div>
              </button>

              {/* Tasks */}
              {isExpanded && (
                <div className="ml-8 mt-1 space-y-0.5">
                  {Object.entries(stage.tasks).map(([taskName]) => (
                    <div
                      key={taskName}
                      className="flex items-center gap-2 px-3 py-1.5 rounded-md text-sm text-muted-foreground hover:text-foreground hover:bg-accent/30 transition-colors"
                    >
                      <Wrench className="w-3 h-3" />
                      <span className="font-mono text-xs">{taskName}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

