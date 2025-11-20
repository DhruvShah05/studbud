'use client'

import { Video, Download, Copy, Film } from 'lucide-react'
import { useState } from 'react'

interface VideoOverviewViewerProps {
  script: string
}

export default function VideoOverviewViewer({ script }: VideoOverviewViewerProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(script)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleDownload = () => {
    const blob = new Blob([script], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'video-overview-script.txt'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="h-full flex flex-col bg-slate-900">
      {/* Header */}
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl shadow-lg">
              <Video className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">Video Overview</h2>
              <p className="text-sm text-slate-400">Educational video script with timestamps</p>
            </div>
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={handleCopy}
              className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition-colors"
            >
              <Copy className="w-4 h-4" />
              {copied ? 'Copied!' : 'Copy'}
            </button>
            <button
              onClick={handleDownload}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700 text-white rounded-lg transition-all shadow-lg"
            >
              <Download className="w-4 h-4" />
              Download
            </button>
          </div>
        </div>
      </div>

      {/* Script Content */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-xl p-8 shadow-2xl">
            <div className="flex items-center gap-3 mb-6 pb-4 border-b border-slate-700">
              <Film className="w-5 h-5 text-orange-400" />
              <h3 className="text-lg font-semibold text-white">Video Script</h3>
            </div>
            
            <div className="prose prose-invert max-w-none">
              <div className="space-y-4 text-slate-200 leading-relaxed whitespace-pre-wrap font-mono text-sm">
                {script.split('\n').map((line, index) => {
                  // Highlight timestamps
                  if (line.match(/\[\d{2}:\d{2}/)) {
                    return (
                      <div key={index} className="flex items-start gap-3 py-2">
                        <span className="flex-shrink-0 px-3 py-1 bg-orange-600 text-white rounded-md font-bold text-xs">
                          {line.match(/\[(\d{2}:\d{2}[^\]]*)\]/)?.[1]}
                        </span>
                        <span className="flex-1 text-slate-300">{line.replace(/\[.*?\]/, '').trim()}</span>
                      </div>
                    )
                  }
                  // Highlight visual cues
                  else if (line.toLowerCase().includes('[visual:')) {
                    return (
                      <div key={index} className="pl-4 py-2 border-l-4 border-blue-500 bg-blue-900/20 rounded-r">
                        <span className="text-blue-300">{line}</span>
                      </div>
                    )
                  }
                  // Highlight script lines
                  else if (line.toLowerCase().includes('script:')) {
                    return (
                      <div key={index} className="pl-4 py-2 border-l-4 border-green-500 bg-green-900/20 rounded-r">
                        <span className="text-green-300">{line}</span>
                      </div>
                    )
                  }
                  // Regular lines
                  else if (line.trim()) {
                    return (
                      <p key={index} className="text-slate-300">
                        {line}
                      </p>
                    )
                  }
                  return null
                })}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
