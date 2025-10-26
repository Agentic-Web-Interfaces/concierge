import { WorkflowVisualizer } from './components/WorkflowVisualizer'

function App() {
  return (
    <div className="h-screen w-screen overflow-hidden bg-background">
      <WorkflowVisualizer workflowName="stock_test" />
    </div>
  )
}

export default App

