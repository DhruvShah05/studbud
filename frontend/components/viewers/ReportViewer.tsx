'use client'

import { FileBarChart } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

interface ReportViewerProps {
  content: string
}

export default function ReportViewer({ content }: ReportViewerProps) {
  if (!content) {
    return (
      <div className="text-center py-12 text-gray-400">
        <FileBarChart className="w-16 h-16 mx-auto mb-4 opacity-50" />
        <p className="text-sm">No report generated yet</p>
        <p className="text-xs mt-2">Select sources and click Report to generate</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2 mb-4">
        <FileBarChart className="w-5 h-5 text-blue-600" />
        <h3 className="font-semibold text-gray-800">Report</h3>
      </div>
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="markdown-content prose prose-sm max-w-none">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
