'use client'

import { useState } from 'react'
import { HelpCircle, CheckCircle, XCircle } from 'lucide-react'

interface QuizQuestion {
  question: string
  options: string[]
  correct: string
  explanation: string
}

interface QuizViewerProps {
  questions: QuizQuestion[]
}

export default function QuizViewer({ questions }: QuizViewerProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [score, setScore] = useState(0)

  if (!questions || questions.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400">
        <HelpCircle className="w-16 h-16 mx-auto mb-4 opacity-50" />
        <p className="text-sm">No quiz generated yet</p>
        <p className="text-xs mt-2">Select sources and click Quiz to generate</p>
      </div>
    )
  }

  const currentQuestion = questions[currentIndex]
  const isCorrect = selectedAnswer === currentQuestion.correct

  const handleAnswer = (answer: string) => {
    if (showResult) return
    setSelectedAnswer(answer)
    setShowResult(true)
    if (answer === currentQuestion.correct) {
      setScore(score + 1)
    }
  }

  const nextQuestion = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1)
      setSelectedAnswer(null)
      setShowResult(false)
    }
  }

  const resetQuiz = () => {
    setCurrentIndex(0)
    setSelectedAnswer(null)
    setShowResult(false)
    setScore(0)
  }

  const isLastQuestion = currentIndex === questions.length - 1

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <HelpCircle className="w-5 h-5 text-blue-600" />
          <h3 className="font-semibold text-gray-800">Quiz</h3>
        </div>
        <span className="text-sm text-gray-500">
          Question {currentIndex + 1} / {questions.length}
        </span>
      </div>

      {/* Question */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <p className="text-lg font-medium text-gray-800 mb-6">{currentQuestion.question}</p>

        {/* Options */}
        <div className="space-y-3">
          {currentQuestion.options.map((option, idx) => {
            const isSelected = selectedAnswer === option
            const isCorrectOption = option === currentQuestion.correct
            
            let buttonClass = 'bg-gray-50 hover:bg-gray-100 border-gray-200'
            
            if (showResult) {
              if (isCorrectOption) {
                buttonClass = 'bg-green-50 border-green-500 text-green-800'
              } else if (isSelected && !isCorrect) {
                buttonClass = 'bg-red-50 border-red-500 text-red-800'
              }
            } else if (isSelected) {
              buttonClass = 'bg-blue-50 border-blue-500 text-blue-800'
            }

            return (
              <button
                key={idx}
                onClick={() => handleAnswer(option)}
                disabled={showResult}
                className={`w-full text-left px-4 py-3 rounded-lg border-2 transition-all ${buttonClass} disabled:cursor-default`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm">{option}</span>
                  {showResult && isCorrectOption && <CheckCircle className="w-5 h-5 text-green-600" />}
                  {showResult && isSelected && !isCorrect && <XCircle className="w-5 h-5 text-red-600" />}
                </div>
              </button>
            )
          })}
        </div>

        {/* Explanation */}
        {showResult && (
          <div className={`mt-6 p-4 rounded-lg ${isCorrect ? 'bg-green-50' : 'bg-red-50'}`}>
            <p className={`text-sm font-medium mb-2 ${isCorrect ? 'text-green-800' : 'text-red-800'}`}>
              {isCorrect ? '✓ Correct!' : '✗ Incorrect'}
            </p>
            <p className="text-sm text-gray-700">{currentQuestion.explanation}</p>
          </div>
        )}
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-600">
          Score: <span className="font-semibold">{score}</span> / {questions.length}
        </div>
        <div className="space-x-2">
          {showResult && !isLastQuestion && (
            <button
              onClick={nextQuestion}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Next Question
            </button>
          )}
          {showResult && isLastQuestion && (
            <button
              onClick={resetQuiz}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              Restart Quiz
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
