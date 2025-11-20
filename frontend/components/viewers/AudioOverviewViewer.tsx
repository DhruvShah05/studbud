'use client'

import { Mic, Download, Copy, Volume2, Play, Loader2 } from 'lucide-react'
import { useState } from 'react'
import axios from 'axios'

interface AudioOverviewViewerProps {
  script: string
}

export default function AudioOverviewViewer({ script }: AudioOverviewViewerProps) {
  const [copied, setCopied] = useState(false)
  const [isGeneratingAudio, setIsGeneratingAudio] = useState(false)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

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
    a.download = 'audio-overview-script.txt'
    a.click()
    URL.revokeObjectURL(url)
  }

  const generateAudio = async () => {
    setIsGeneratingAudio(true)
    setError(null)
    
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
      const response = await axios.post(`${API_URL}/api/studio/audio-overview/generate-audio`, {
        script: script
      })
      
      setAudioUrl(response.data.audio_url)
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to generate audio')
    } finally {
      setIsGeneratingAudio(false)
    }
  }

  const parseScript = () => {
    const lines = script.split('\n').filter(line => line.trim())
    const parsed: Array<{ speaker: string; text: string }> = []
    
    lines.forEach(line => {
      if (line.includes('Alex:')) {
        parsed.push({ speaker: 'Alex', text: line.replace('Alex:', '').trim() })
      } else if (line.includes('Sam:')) {
        parsed.push({ speaker: 'Sam', text: line.replace('Sam:', '').trim() })
      } else if (line.trim()) {
        parsed.push({ speaker: 'narrator', text: line.trim() })
      }
    })
    
    return parsed
  }

  const parsedScript = parseScript()

  return (
    <div className="h-full flex flex-col bg-[var(--background)]">
      {/* Header */}
      <div className="p-6 border-b border-[var(--border)] bg-[var(--surface)]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="p-2.5 bg-gradient-to-br from-purple-400 to-purple-500 rounded-lg shadow-sm">
              <Mic className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-[var(--text-primary)]">Audio Overview</h2>
              <p className="text-xs text-[var(--text-tertiary)]">Podcast-style conversation</p>
            </div>
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={handleCopy}
              className="flex items-center gap-2 px-3 py-1.5 text-sm bg-[var(--surface-hover)] hover:bg-[var(--surface-dark)] text-[var(--text-primary)] rounded-lg border border-[var(--border)] transition-colors"
            >
              <Copy className="w-3.5 h-3.5" />
              {copied ? 'Copied!' : 'Copy'}
            </button>
            <button
              onClick={handleDownload}
              className="flex items-center gap-2 px-3 py-1.5 text-sm bg-[var(--surface-hover)] hover:bg-[var(--surface-dark)] text-[var(--text-primary)] rounded-lg border border-[var(--border)] transition-colors"
            >
              <Download className="w-3.5 h-3.5" />
              Script
            </button>
            <button
              onClick={generateAudio}
              disabled={isGeneratingAudio}
              className="flex items-center gap-2 px-4 py-1.5 text-sm bg-[var(--primary)] hover:bg-[var(--primary-hover)] text-white rounded-lg shadow-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGeneratingAudio ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Play className="w-4 h-4" />
                  Generate Podcast
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Audio Player */}
      {audioUrl && (
        <div className="p-6 border-b border-[var(--border)] bg-[var(--surface)]">
          <div className="max-w-4xl mx-auto">
            <div className="bg-[var(--surface-hover)] border border-[var(--primary)] rounded-xl p-6 shadow-sm">
              <div className="flex items-center gap-4 mb-4">
                <div className="p-2.5 bg-[var(--primary)] rounded-lg">
                  <Volume2 className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-[var(--text-primary)]">Podcast Audio Ready!</h3>
                  <p className="text-xs text-[var(--text-tertiary)]">Listen to your AI-generated podcast</p>
                </div>
              </div>
              
              <audio 
                controls 
                className="w-full mb-4"
                src={audioUrl}
                style={{
                  filter: 'invert(1) hue-rotate(180deg)',
                  borderRadius: '0.5rem'
                }}
              >
                Your browser does not support the audio element.
              </audio>
              
              <div className="flex gap-2">
                <a
                  href={audioUrl}
                  download="podcast.mp3"
                  className="flex items-center gap-2 px-3 py-1.5 text-sm bg-[var(--primary)] hover:bg-[var(--primary-hover)] text-white rounded-lg transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Download MP3
                </a>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="p-6 border-b border-[var(--border)] bg-[var(--surface)]">
          <div className="max-w-4xl mx-auto">
            <div className="bg-red-50 border border-red-300 rounded-lg p-4">
              <p className="text-red-700 font-medium text-sm">⚠️ {error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Script Content */}
      <div className="flex-1 overflow-y-auto p-6 space-y-3 bg-[var(--background)]">
        <div className="max-w-4xl mx-auto space-y-3">
        {parsedScript.map((item, index) => {
          if (item.speaker === 'Alex') {
            return (
              <div key={index} className="flex gap-3 animate-fade-in">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-500 flex items-center justify-center text-white font-semibold text-sm shadow-sm">
                  A
                </div>
                <div className="flex-1 bg-[var(--surface)] border border-[var(--border)] p-4 rounded-lg shadow-sm">
                  <p className="text-[var(--primary)] font-semibold text-sm mb-1.5 flex items-center gap-1.5">
                    <Volume2 className="w-3.5 h-3.5" />
                    Alex
                  </p>
                  <p className="text-[var(--text-primary)] leading-relaxed text-sm">{item.text}</p>
                </div>
              </div>
            )
          } else if (item.speaker === 'Sam') {
            return (
              <div key={index} className="flex gap-3 animate-fade-in">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-400 to-purple-500 flex items-center justify-center text-white font-semibold text-sm shadow-sm">
                  S
                </div>
                <div className="flex-1 bg-[var(--surface)] border border-[var(--border)] p-4 rounded-lg shadow-sm">
                  <p className="text-purple-600 font-semibold text-sm mb-1.5 flex items-center gap-1.5">
                    <Volume2 className="w-3.5 h-3.5" />
                    Sam
                  </p>
                  <p className="text-[var(--text-primary)] leading-relaxed text-sm">{item.text}</p>
                </div>
              </div>
            )
          } else {
            return (
              <div key={index} className="px-10 py-1.5">
                <p className="text-[var(--text-tertiary)] italic text-xs">{item.text}</p>
              </div>
            )
          }
        })}
        </div>
      </div>
    </div>
  )
}
