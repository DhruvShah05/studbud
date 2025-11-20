'use client'

import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { useStudioStore } from '@/lib/store'
import { sourceAPI } from '@/lib/api'
import { FileText, Upload, Trash2, CheckSquare, Square, Loader2 } from 'lucide-react'
import { useState } from 'react'

export default function SourcesPanel() {
  const { currentWorkspace, sources, addSource, removeSource, selectedSourceIds, toggleSourceSelection } = useStudioStore()
  const [isUploading, setIsUploading] = useState(false)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (!currentWorkspace) return

    setIsUploading(true)
    for (const file of acceptedFiles) {
      try {
        const source = await sourceAPI.upload(currentWorkspace.id, file)
        addSource(source)
      } catch (error) {
        console.error('Upload failed:', error)
      }
    }
    setIsUploading(false)
  }, [currentWorkspace, addSource])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
      'text/plain': ['.txt'],
      'image/png': ['.png'],
      'image/jpeg': ['.jpg', '.jpeg'],
    },
  })

  const handleDelete = async (sourceId: string) => {
    try {
      await sourceAPI.delete(sourceId)
      removeSource(sourceId)
    } catch (error) {
      console.error('Delete failed:', error)
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-800">Sources</h2>
        <p className="text-sm text-gray-500 mt-1">
          {sources.length} document{sources.length !== 1 ? 's' : ''}
        </p>
      </div>

      {/* Upload Area */}
      <div className="p-4">
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
          }`}
        >
          <input {...getInputProps()} />
          {isUploading ? (
            <div>
              <Loader2 className="w-8 h-8 text-blue-600 mx-auto mb-2 animate-spin" />
              <p className="text-sm text-gray-600">Uploading...</p>
            </div>
          ) : (
            <div>
              <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-600">
                {isDragActive ? 'Drop files here' : 'Drag & drop or click to upload'}
              </p>
              <p className="text-xs text-gray-400 mt-1">PDF, DOCX, TXT, Images</p>
            </div>
          )}
        </div>
      </div>

      {/* Sources List */}
      <div className="flex-1 overflow-y-auto px-4 pb-4">
        {sources.length === 0 ? (
          <div className="text-center py-8 text-gray-400">
            <FileText className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p className="text-sm">No sources yet</p>
          </div>
        ) : (
          <div className="space-y-2">
            {sources.map((source) => (
              <div
                key={source.id}
                className={`p-3 rounded-lg border transition-all cursor-pointer ${
                  selectedSourceIds.includes(source.id)
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300 bg-white'
                }`}
                onClick={() => toggleSourceSelection(source.id)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-2 flex-1">
                    {selectedSourceIds.includes(source.id) ? (
                      <CheckSquare className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                    ) : (
                      <Square className="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                    )}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-800 truncate">{source.filename}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {source.file_type.toUpperCase()} • {new Date(source.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleDelete(source.id)
                    }}
                    className="ml-2 p-1 text-gray-400 hover:text-red-600 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Selection Info */}
      {selectedSourceIds.length > 0 && (
        <div className="p-4 border-t border-gray-200 bg-blue-50">
          <p className="text-sm text-blue-800 font-medium">
            {selectedSourceIds.length} source{selectedSourceIds.length !== 1 ? 's' : ''} selected
          </p>
        </div>
      )}
    </div>
  )
}
