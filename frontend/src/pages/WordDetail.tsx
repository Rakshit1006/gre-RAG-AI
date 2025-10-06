import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { wordsAPI } from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { ArrowLeft, Edit2, Save, Trash2 } from 'lucide-react'

export function WordDetail() {
  const { wordId } = useParams<{ wordId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [isEditing, setIsEditing] = useState(false)
  const [editedStory, setEditedStory] = useState('')

  const { data: word, isLoading } = useQuery({
    queryKey: ['word', wordId],
    queryFn: async () => {
      if (!wordId) throw new Error('No word ID')
      const response = await wordsAPI.get(wordId)
      setEditedStory(response.data.story || '')
      return response.data
    },
    enabled: !!wordId,
  })

  const updateMutation = useMutation({
    mutationFn: async (story: string) => {
      if (!wordId) throw new Error('No word ID')
      return wordsAPI.update(wordId, { story })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['word', wordId] })
      setIsEditing(false)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async () => {
      if (!wordId) throw new Error('No word ID')
      return wordsAPI.delete(wordId)
    },
    onSuccess: () => {
      navigate('/vocab')
    },
  })

  if (isLoading) return <div className="text-center py-12">Loading...</div>
  if (!word) return <div className="text-center py-12">Word not found</div>

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate('/vocab')}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div className="flex-1">
          <h1 className="text-4xl font-bold">{word.word}</h1>
          {word.pos && <p className="text-muted-foreground mt-1">{word.pos}</p>}
        </div>
        <Button variant="destructive" size="icon" onClick={() => {
          if (confirm('Delete this word?')) deleteMutation.mutate()
        }}>
          <Trash2 className="h-5 w-5" />
        </Button>
      </div>

      <Card>
        <CardHeader><CardTitle>Definition</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <div>
            <div className="font-semibold text-sm text-muted-foreground mb-1">GRE Definition</div>
            <p>{word.gre_definition}</p>
          </div>
          {word.pithy_definition && (
            <div>
              <div className="font-semibold text-sm text-muted-foreground mb-1">Quick Definition</div>
              <p>{word.pithy_definition}</p>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Mnemonic Story</CardTitle>
            {!isEditing ? (
              <Button variant="outline" size="sm" onClick={() => setIsEditing(true)}>
                <Edit2 className="h-4 w-4 mr-2" />Edit
              </Button>
            ) : (
              <Button size="sm" onClick={() => updateMutation.mutate(editedStory)}>
                <Save className="h-4 w-4 mr-2" />Save
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {isEditing ? (
            <Input value={editedStory} onChange={(e) => setEditedStory(e.target.value)} />
          ) : (
            <p className="italic">{word.story || 'No story yet'}</p>
          )}
        </CardContent>
      </Card>

      {word.associations.length > 0 && (
        <Card>
          <CardHeader><CardTitle>Associations</CardTitle></CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {word.associations.map((a, i) => <Badge key={i} variant="secondary">{a}</Badge>)}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
