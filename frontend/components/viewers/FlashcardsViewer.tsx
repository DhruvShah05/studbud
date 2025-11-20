'use client'

import { useState } from 'react'
import { FileText, ChevronLeft, ChevronRight, RotateCw, Download, Share2, Copy } from 'lucide-react'

interface Flashcard {
  question: string
  answer: string
}

interface FlashcardsViewerProps {
  cards: Flashcard[]
}

export default function FlashcardsViewer({ cards }: FlashcardsViewerProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)
  const [copied, setCopied] = useState(false)

  const downloadFlashcards = () => {
    let content = 'FLASHCARDS\n\n'
    cards.forEach((card, index) => {
      content += `Card ${index + 1}:\n`
      content += `Q: ${card.question}\n`
      content += `A: ${card.answer}\n\n`
    })
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `flashcards-${Date.now()}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  const copyToClipboard = () => {
    let content = 'FLASHCARDS\n\n'
    cards.forEach((card, index) => {
      content += `Card ${index + 1}:\n`
      content += `Q: ${card.question}\n`
      content += `A: ${card.answer}\n\n`
    })
    navigator.clipboard.writeText(content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const shareFlashcards = async () => {
    let content = 'FLASHCARDS\n\n'
    cards.forEach((card, index) => {
      content += `Card ${index + 1}:\n`
      content += `Q: ${card.question}\n`
      content += `A: ${card.answer}\n\n`
    })
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Flashcards',
          text: content,
        })
      } catch (err) {
        console.log('Share cancelled')
      }
    } else {
      copyToClipboard()
    }
  }

  if (!cards || cards.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400">
        <FileText className="w-16 h-16 mx-auto mb-4 opacity-50" />
        <p className="text-sm">No flashcards generated yet</p>
        <p className="text-xs mt-2">Select sources and click Flashcards to generate</p>
      </div>
    )
  }

  const currentCard = cards[currentIndex]

  const nextCard = () => {
    setIsFlipped(false)
    setCurrentIndex((prev) => (prev + 1) % cards.length)
  }

  const prevCard = () => {
    setIsFlipped(false)
    setCurrentIndex((prev) => (prev - 1 + cards.length) % cards.length)
  }

  return (
    <div className="h-full flex flex-col bg-slate-900">
      {/* Header */}
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-gradient-to-br from-indigo-500 to-blue-500 rounded-xl shadow-lg">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">Flashcards</h2>
              <p className="text-sm text-slate-400">
                Card {currentIndex + 1} of {cards.length}
              </p>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={copyToClipboard}
              className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition-colors"
            >
              <Copy className="w-4 h-4" />
              {copied ? 'Copied!' : 'Copy All'}
            </button>
            <button
              onClick={shareFlashcards}
              className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition-colors"
            >
              <Share2 className="w-4 h-4" />
              Share
            </button>
            <button
              onClick={downloadFlashcards}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 text-white rounded-lg transition-all shadow-lg"
            >
              <Download className="w-4 h-4" />
              Download
            </button>
          </div>
        </div>
      </div>

      {/* Flashcard */}
      <div className="flex-1 flex items-center justify-center p-6">
        <div
          className="relative bg-gradient-to-br from-slate-800 to-slate-900 border-2 border-indigo-500 rounded-2xl shadow-2xl p-12 min-h-[400px] w-full max-w-2xl flex items-center justify-center cursor-pointer hover:shadow-indigo-500/50 transition-all hover:scale-105"
          onClick={() => setIsFlipped(!isFlipped)}
        >
          <div className="text-center">
            <div className="inline-block px-4 py-1 bg-indigo-600 text-white rounded-full text-xs font-semibold mb-6">
              {isFlipped ? 'ANSWER' : 'QUESTION'}
            </div>
            <p className="text-2xl font-medium text-white leading-relaxed">
              {isFlipped ? currentCard.answer : currentCard.question}
            </p>
          </div>
          <button
            className="absolute top-6 right-6 p-3 bg-slate-700 hover:bg-slate-600 text-white rounded-full transition-colors shadow-lg"
            onClick={(e) => {
              e.stopPropagation()
              setIsFlipped(!isFlipped)
            }}
          >
            <RotateCw className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Navigation */}
      <div className="p-6 border-t border-slate-700">
        <div className="flex items-center justify-between max-w-2xl mx-auto">
          <button
            onClick={prevCard}
            className="flex items-center gap-2 px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl transition-colors shadow-lg"
          >
            <ChevronLeft className="w-5 h-5" />
            <span className="font-medium">Previous</span>
          </button>
          <div className="text-slate-400 text-sm font-medium">
            Click card to flip
          </div>
          <button
            onClick={nextCard}
            className="flex items-center gap-2 px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl transition-colors shadow-lg"
          >
            <span className="font-medium">Next</span>
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  )
}
