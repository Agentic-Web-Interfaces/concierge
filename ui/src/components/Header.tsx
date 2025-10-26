import { Workflow, Sparkles } from 'lucide-react'

interface HeaderProps {
  workflowName: string
  description: string
}

export function Header({ workflowName, description }: HeaderProps) {
  return (
    <header className="h-14 border-b border-border bg-card px-6 flex items-center justify-between flex-shrink-0">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <span className="font-semibold text-lg">Concierge</span>
        </div>
        
        <div className="h-6 w-px bg-border" />
        
        <div className="flex items-center gap-2">
          <Workflow className="w-4 h-4 text-muted-foreground" />
          <span className="font-medium">{workflowName}</span>
          {description && (
            <span className="text-sm text-muted-foreground">· {description}</span>
          )}
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button className="px-3 py-1.5 text-sm font-medium hover:bg-accent rounded-md transition-colors">
          Export
        </button>
        <button className="px-3 py-1.5 text-sm font-medium hover:bg-accent rounded-md transition-colors">
          Docs
        </button>
      </div>
    </header>
  )
}

