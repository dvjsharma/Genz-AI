'use client'

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { processInstagramData, getChatResponse } from "../actions"
import { Send, Loader2, Instagram } from 'lucide-react'
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeSanitize from 'rehype-sanitize';
import rehypeHighlight from 'rehype-highlight';

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [instagramId, setInstagramId] = useState('')
  const [processing, setProcessing] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [errorMessage, setErrorMessage] = useState("");

  const handleInstagramConnect = async () => {
    if (!instagramId) return
    setProcessing(true)
    try {
      const result = await processInstagramData(instagramId)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `${result.message} You can now ask specific questions about your content!`
      }])
      setIsConnected(true)
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, there was an error processing your Instagram data.'
      }])
      setErrorMessage("Failed to process Instagram data. Please try again.");
      setTimeout(() => setErrorMessage(""), 5000);
    }
    setProcessing(false)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setLoading(true)

    try {
      const response = await getChatResponse(userMessage)
      setMessages(prev => [...prev, { role: 'assistant', content: response.response }])
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request.'
      }])
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-400 via-purple-500 to-cyan-500 p-6">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="rounded-2xl backdrop-blur-xl bg-white/10 border border-white/20 shadow-lg p-4 mb-6">
          <h1 className="text-xl font-bold text-white text-center">
            Social Pulse Chat
          </h1>
        </div>

        {!isConnected ? (
          // Instagram Connection UI
          <div className="rounded-3xl backdrop-blur-xl bg-white/10 border border-white/20 shadow-lg p-12 text-center">
            <div className="max-w-md mx-auto space-y-6">
              <div className="w-20 h-20 mx-auto rounded-full backdrop-blur-xl bg-white/10 border border-white/20 flex items-center justify-center">
                <Instagram className="w-10 h-10 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-white">Connect Your Instagram</h2>
              <p className="text-white/80">
                Connect your Instagram account to get personalized insights about your content
              </p>
              {errorMessage && (
                <div className="bg-red-500 text-white rounded-lg px-4 py-2">
                  {errorMessage}
                </div>
              )}
              <div className="space-y-4">
                <Input
                  placeholder="Enter Instagram handle"
                  value={instagramId}
                  onChange={(e) => setInstagramId(e.target.value)}
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
                />
                <Button
                  onClick={handleInstagramConnect}
                  disabled={processing}
                  className="w-full bg-white/20 hover:bg-white/30 backdrop-blur-lg text-white border border-white/20 h-12"
                >
                  {processing ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Processing
                    </>
                  ) : (
                    'Connect Instagram'
                  )}
                </Button>
                <Button
                  onClick={() => setIsConnected(true)}
                  variant="ghost"
                  className="w-full text-white hover:bg-white/10"
                >
                  Skip for now
                </Button>
              </div>
            </div>
          </div>
        ) : (
          // Chat Interface
          <div className="rounded-3xl backdrop-blur-xl bg-white/10 border border-white/20 shadow-lg p-6">
            <ScrollArea className="h-[600px] mb-4 pr-4">
              <div className="space-y-4">
                {messages.map((message, i) => (
                  <div
                    key={i}
                    className={`flex ${
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`rounded-2xl px-4 py-2 max-w-[80%] backdrop-blur-xl ${
                        message.role === 'user'
                          ? 'bg-white/20 text-white'
                          : 'bg-white/10 text-white'
                      }`}
                    >
                      <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      rehypePlugins={[rehypeSanitize, rehypeHighlight]}
                      >
                        {message.content}
                      </ReactMarkdown>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex justify-start">
                    <div className="rounded-2xl px-4 py-2 bg-white/10 backdrop-blur-xl">
                      <Loader2 className="w-4 h-4 animate-spin text-white" />
                    </div>
                  </div>
                )}
              </div>
            </ScrollArea>

            <form onSubmit={handleSubmit} className="flex gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask anything about social media content..."
                className="flex-1 bg-white/10 border-white/20 text-white placeholder:text-white/50"
              />
              <Button
                type="submit"
                disabled={loading}
                className="bg-white/20 hover:bg-white/30 backdrop-blur-lg text-white border border-white/20"
              >
                {loading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
              </Button>
            </form>
          </div>
        )}
      </div>
    </div>
  )
}

