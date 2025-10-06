import { useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { sessionAPI } from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Brain, Check, X } from 'lucide-react'

export function Practice() {
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [showAnswer, setShowAnswer] = useState(false)
  const [items, setItems] = useState<any[]>([])

  const startSessionMutation = useMutation({
    mutationFn: async () => {
      const response = await sessionAPI.start({
        mode: 'flashcard',
        topics: ['vocab'],
        limit: 20,
      })
      return response.data
    },
    onSuccess: (data) => {
      setSessionId(data.session_id)
      setItems(data.items)
      setCurrentIndex(0)
      setShowAnswer(false)
    },
  })

  const recordAttemptMutation = useMutation({
    mutationFn: async (correct: boolean) => {
      if (!sessionId || !currentItem) return
      return sessionAPI.recordAttempt({
        item_id: currentItem.id,
        item_type: currentItem.type,
        response: correct ? 'correct' : 'incorrect',
        correct,
        latency_ms: 0,
        session_id: sessionId,
      })
    },
  })

  const currentItem = items[currentIndex]

  const handleResponse = (correct: boolean) => {
    recordAttemptMutation.mutate(correct)
    
    if (currentIndex < items.length - 1) {
      setCurrentIndex(currentIndex + 1)
      setShowAnswer(false)
    } else {
      // Session complete
      if (sessionId) {
        sessionAPI.end(sessionId)
      }
      setSessionId(null)
      setItems([])
    }
  }

  if (!sessionId) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight">Practice Session</h1>
          <p className="text-muted-foreground mt-2">
            Review your vocabulary with flashcards
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Start Practicing</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p>Ready to review your vocabulary? Click below to start a practice session.</p>
            <Button 
              size="lg" 
              onClick={() => startSessionMutation.mutate()}
              disabled={startSessionMutation.isPending}
            >
              <Brain className="mr-2 h-5 w-5" />
              Start Session
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!currentItem) {
    return (
      <div className="max-w-2xl mx-auto text-center space-y-6">
        <h1 className="text-4xl font-bold">Session Complete!</h1>
        <p className="text-muted-foreground">Great job! You've completed this practice session.</p>
        <Button onClick={() => startSessionMutation.mutate()}>
          Start Another Session
        </Button>
      </div>
    )
  }

  const word = currentItem.content

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Practice Session</h1>
        <Badge variant="secondary">
          {currentIndex + 1} / {items.length}
        </Badge>
      </div>

      <Card className="min-h-[400px]">
        <CardHeader>
          <CardTitle className="text-3xl text-center">{word.word}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {showAnswer ? (
            <div className="space-y-4">
              <div>
                <div className="font-semibold text-sm text-muted-foreground mb-2">Definition</div>
                <p>{word.gre_definition || word.pithy_definition}</p>
              </div>
              
              {word.story && (
                <div>
                  <div className="font-semibold text-sm text-muted-foreground mb-2">Mnemonic</div>
                  <p className="italic">{word.story}</p>
                </div>
              )}

              <div className="pt-6 flex gap-4">
                <Button
                  variant="destructive"
                  className="flex-1"
                  size="lg"
                  onClick={() => handleResponse(false)}
                >
                  <X className="mr-2 h-5 w-5" />
                  Incorrect
                </Button>
                <Button
                  className="flex-1"
                  size="lg"
                  onClick={() => handleResponse(true)}
                >
                  <Check className="mr-2 h-5 w-5" />
                  Correct
                </Button>
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-muted-foreground mb-6">Try to recall the definition...</p>
              <Button size="lg" onClick={() => setShowAnswer(true)}>
                Show Answer
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
