import { memo } from 'react'
import { Handle, Position } from 'reactflow'
import { Wrench, ArrowRight, Circle } from 'lucide-react'
import { cn } from '../lib/utils'

interface StageNodeData {
  label: string
  description: string
  taskCount: number
  isInitial: boolean
  tasks: string[]
  isSelected?: boolean
}

export const StageNode = memo(({ data }: { data: StageNodeData }) => {
  return (
    <div
      className={cn(
        "min-w-[240px] rounded-lg border-2 transition-all duration-200",
        data.isSelected
          ? "border-purple-500 shadow-lg shadow-purple-500/20"
          : "border-border hover:border-purple-400 hover:shadow-md"
      )}
    >
      <Handle type="target" position={Position.Left} className="w-2 h-2" />
      
      {/* Header */}
      <div className={cn(
        "px-4 py-3 rounded-t-md bg-gradient-to-br",
        data.isInitial
          ? "from-green-500/20 to-emerald-500/20"
          : "from-purple-500/20 to-pink-500/20"
      )}>
        <div className="flex items-center gap-2 mb-1">
          {data.isInitial && (
            <Circle className="w-3 h-3 text-green-500 fill-green-500" />
          )}
          <h3 className="font-semibold text-base">{data.label}</h3>
        </div>
        {data.description && (
          <p className="text-xs text-muted-foreground">{data.description}</p>
        )}
      </div>

      {/* Tasks */}
      <div className="px-4 py-3 bg-card space-y-1">
        <div className="flex items-center gap-1.5 text-xs text-muted-foreground mb-2">
          <Wrench className="w-3 h-3" />
          <span>{data.taskCount} {data.taskCount === 1 ? 'task' : 'tasks'}</span>
        </div>
        {data.tasks.slice(0, 3).map((task) => (
          <div
            key={task}
            className="flex items-center gap-2 px-2 py-1 rounded bg-accent/50 text-xs"
          >
            <ArrowRight className="w-3 h-3 text-muted-foreground" />
            <span className="font-mono">{task}</span>
          </div>
        ))}
        {data.taskCount > 3 && (
          <div className="text-xs text-muted-foreground pl-2">
            +{data.taskCount - 3} more
          </div>
        )}
      </div>

      <Handle type="source" position={Position.Right} className="w-2 h-2" />
    </div>
  )
})

StageNode.displayName = 'StageNode'

