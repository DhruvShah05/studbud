'use client'

import { useState } from 'react'
import { Brain, Download, Share2, Copy, FileJson, FileImage } from 'lucide-react'

interface MindmapNode {
  topic: string
  children?: MindmapNode[]
}

interface MindmapViewerProps {
  data: MindmapNode | null
}

export default function MindmapViewer({ data }: MindmapViewerProps) {
  const [copied, setCopied] = useState(false)

  const downloadAsJSON = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `mindmap-${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const downloadAsText = () => {
    const convertToText = (node: MindmapNode, level: number = 0): string => {
      let text = '  '.repeat(level) + '- ' + node.topic + '\n'
      if (node.children) {
        node.children.forEach(child => {
          text += convertToText(child, level + 1)
        })
      }
      return text
    }
    const textContent = convertToText(data!)
    const blob = new Blob([textContent], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `mindmap-${Date.now()}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  const copyToClipboard = () => {
    const convertToText = (node: MindmapNode, level: number = 0): string => {
      let text = '  '.repeat(level) + '- ' + node.topic + '\n'
      if (node.children) {
        node.children.forEach(child => {
          text += convertToText(child, level + 1)
        })
      }
      return text
    }
    navigator.clipboard.writeText(convertToText(data!))
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const shareContent = async () => {
    const convertToText = (node: MindmapNode, level: number = 0): string => {
      let text = '  '.repeat(level) + '- ' + node.topic + '\n'
      if (node.children) {
        node.children.forEach(child => {
          text += convertToText(child, level + 1)
        })
      }
      return text
    }
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Mindmap',
          text: convertToText(data!),
        })
      } catch (err) {
        console.log('Share cancelled')
      }
    } else {
      copyToClipboard()
    }
  }

  if (!data) {
    return (
      <div className="text-center py-12 text-gray-400">
        <Brain className="w-16 h-16 mx-auto mb-4 opacity-50" />
        <p className="text-sm">No mindmap generated yet</p>
        <p className="text-xs mt-2">Select sources and click Mindmap to generate</p>
      </div>
    )
  }

  const renderNode = (node: MindmapNode, level: number = 0) => {
    const colors = [
      'bg-gradient-to-r from-blue-500 to-cyan-500 text-white border-blue-400',
      'bg-gradient-to-r from-purple-500 to-pink-500 text-white border-purple-400',
      'bg-gradient-to-r from-green-500 to-emerald-500 text-white border-green-400',
      'bg-gradient-to-r from-orange-500 to-red-500 text-white border-orange-400',
    ]

    const colorClass = colors[level % colors.length]

    return (
      <div key={node.topic} className="mb-4">
        <div
          className={`inline-block px-4 py-2 rounded-lg border ${colorClass} font-semibold text-sm shadow-lg`}
          style={{ marginLeft: `${level * 30}px` }}
        >
          {node.topic}
        </div>
        {node.children && node.children.length > 0 && (
          <div className="mt-2">
            {node.children.map((child, idx) => (
              <div key={idx}>{renderNode(child, level + 1)}</div>
            ))}
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col bg-slate-900">
      {/* Header */}
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl shadow-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">Mind Map</h2>
              <p className="text-sm text-slate-400">Visual knowledge structure</p>
            </div>
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={copyToClipboard}
              className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition-colors"
            >
              <Copy className="w-4 h-4" />
              {copied ? 'Copied!' : 'Copy'}
            </button>
            <button
              onClick={shareContent}
              className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition-colors"
            >
              <Share2 className="w-4 h-4" />
              Share
            </button>
            <button
              onClick={downloadAsText}
              className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition-colors"
            >
              <Download className="w-4 h-4" />
              TXT
            </button>
            <button
              onClick={downloadAsJSON}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white rounded-lg transition-all shadow-lg"
            >
              <FileJson className="w-4 h-4" />
              JSON
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-xl p-8 shadow-2xl">
          {renderNode(data)}
        </div>
      </div>
    </div>
  )
}
