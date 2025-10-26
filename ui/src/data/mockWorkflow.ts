import type { Workflow, WorkflowGraph } from '../types/workflow'

export const mockWorkflow: Workflow = {
  name: 'stock_test',
  description: 'A workflow for analyzing stock data and making recommendations',
  initial_stage: 'data_collection',
  stages: {
    data_collection: {
      name: 'data_collection',
      description: 'Collect stock market data from various sources',
      prerequisites: [],
      tasks: {
        fetch_stock_price: {
          name: 'fetch_stock_price',
          description: 'Fetches current stock price',
          input_schema: {
            properties: {
              symbol: { type: 'string', description: 'Stock ticker symbol' },
            },
            required: ['symbol'],
          },
          output_schema: {
            price: 0,
            timestamp: '',
          },
        },
        fetch_company_info: {
          name: 'fetch_company_info',
          description: 'Fetches company information and fundamentals',
          input_schema: {
            properties: {
              symbol: { type: 'string', description: 'Stock ticker symbol' },
            },
            required: ['symbol'],
          },
          output_schema: {
            name: '',
            sector: '',
            market_cap: 0,
          },
        },
      },
      transitions: ['analysis'],
    },
    analysis: {
      name: 'analysis',
      description: 'Analyze collected data and generate insights',
      prerequisites: ['data_collection'],
      tasks: {
        calculate_metrics: {
          name: 'calculate_metrics',
          description: 'Calculate financial metrics and ratios',
          input_schema: {
            properties: {
              price: { type: 'number', description: 'Stock price' },
              market_cap: { type: 'number', description: 'Market capitalization' },
            },
            required: ['price', 'market_cap'],
          },
          output_schema: {
            pe_ratio: 0,
            volatility: 0,
          },
        },
        sentiment_analysis: {
          name: 'sentiment_analysis',
          description: 'Analyze market sentiment from news and social media',
          input_schema: {
            properties: {
              symbol: { type: 'string', description: 'Stock ticker symbol' },
            },
            required: ['symbol'],
          },
          output_schema: {
            sentiment_score: 0,
            confidence: 0,
          },
        },
      },
      transitions: ['recommendation'],
    },
    recommendation: {
      name: 'recommendation',
      description: 'Generate investment recommendations based on analysis',
      prerequisites: ['analysis'],
      tasks: {
        generate_recommendation: {
          name: 'generate_recommendation',
          description: 'Generate buy/sell/hold recommendation',
          input_schema: {
            properties: {
              metrics: { type: 'object', description: 'Financial metrics' },
              sentiment: { type: 'object', description: 'Sentiment analysis results' },
            },
            required: ['metrics', 'sentiment'],
          },
          output_schema: {
            action: '',
            confidence: 0,
            reasoning: '',
          },
        },
        calculate_risk: {
          name: 'calculate_risk',
          description: 'Calculate risk score for the recommendation',
          input_schema: {
            properties: {
              volatility: { type: 'number', description: 'Stock volatility' },
              sentiment_score: { type: 'number', description: 'Sentiment score' },
            },
            required: ['volatility', 'sentiment_score'],
          },
          output_schema: {
            risk_score: 0,
            risk_level: '',
          },
        },
      },
      transitions: ['reporting'],
    },
    reporting: {
      name: 'reporting',
      description: 'Generate and format final report',
      prerequisites: ['recommendation'],
      tasks: {
        format_report: {
          name: 'format_report',
          description: 'Format all data into a comprehensive report',
          input_schema: {
            properties: {
              recommendation: { type: 'object', description: 'Recommendation data' },
              risk: { type: 'object', description: 'Risk analysis' },
              company_info: { type: 'object', description: 'Company information' },
            },
            required: ['recommendation', 'risk', 'company_info'],
          },
          output_schema: {
            report: '',
            charts: [],
          },
        },
      },
      transitions: [],
    },
  },
}

export const mockWorkflowGraph: WorkflowGraph = {
  nodes: [
    {
      id: 'data_collection',
      type: 'stage',
      position: { x: 100, y: 100 },
      data: {
        label: 'data_collection',
        description: 'Collect stock market data from various sources',
        taskCount: 2,
        isInitial: true,
        tasks: ['fetch_stock_price', 'fetch_company_info'],
      },
    },
    {
      id: 'analysis',
      type: 'stage',
      position: { x: 400, y: 100 },
      data: {
        label: 'analysis',
        description: 'Analyze collected data and generate insights',
        taskCount: 2,
        isInitial: false,
        tasks: ['calculate_metrics', 'sentiment_analysis'],
      },
    },
    {
      id: 'recommendation',
      type: 'stage',
      position: { x: 700, y: 100 },
      data: {
        label: 'recommendation',
        description: 'Generate investment recommendations based on analysis',
        taskCount: 2,
        isInitial: false,
        tasks: ['generate_recommendation', 'calculate_risk'],
      },
    },
    {
      id: 'reporting',
      type: 'stage',
      position: { x: 1000, y: 100 },
      data: {
        label: 'reporting',
        description: 'Generate and format final report',
        taskCount: 1,
        isInitial: false,
        tasks: ['format_report'],
      },
    },
  ],
  edges: [
    {
      id: 'e1',
      source: 'data_collection',
      target: 'analysis',
      animated: true,
    },
    {
      id: 'e2',
      source: 'analysis',
      target: 'recommendation',
      animated: true,
    },
    {
      id: 'e3',
      source: 'recommendation',
      target: 'reporting',
      animated: true,
    },
  ],
}

