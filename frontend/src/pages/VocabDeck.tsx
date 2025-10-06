import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { wordsAPI } from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Search, Plus } from 'lucide-react'
import { Link } from 'react-router-dom'
import { formatDate, calculateDaysUntil } from '@/lib/utils'

export function VocabDeck() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedTags, setSelectedTags] = useState<string[]>([])

  const { data: words, isLoading } = useQuery({
    queryKey: ['words', searchQuery, selectedTags],
    queryFn: async () => {
      const response = await wordsAPI.search({
        q: searchQuery,
        tags: selectedTags.join(','),
        limit: 50,
      })
      return response.data
    },
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold tracking-tight">Vocabulary Deck</h1>
          <p className="text-muted-foreground mt-2">
            Browse and manage your vocabulary words
          </p>
        </div>
        <Link to="/import">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Add Words
          </Button>
        </Link>
      </div>

      {/* Search */}
      <Card>
        <CardContent className="pt-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search words..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
        </CardContent>
      </Card>

      {/* Words Grid */}
      {isLoading ? (
        <div className="text-center py-12 text-muted-foreground">
          Loading words...
        </div>
      ) : words && words.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {words.map((word) => {
            const daysUntilDue = word.srs.next_due 
              ? calculateDaysUntil(word.srs.next_due)
              : null

            return (
              <Link key={word.id} to={`/vocab/${word.id}`}>
                <Card className="h-full hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <CardTitle className="text-xl">{word.word}</CardTitle>
                      {word.pos && (
                        <Badge variant="secondary" className="text-xs">
                          {word.pos}
                        </Badge>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground line-clamp-2">
                      {word.pithy_definition || word.gre_definition}
                    </p>
                    
                    {word.story && (
                      <p className="text-sm mt-3 italic line-clamp-2">
                        "{word.story}"
                      </p>
                    )}

                    <div className="flex items-center gap-2 mt-4">
                      {word.tags.slice(0, 3).map((tag) => (
                        <Badge key={tag} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                    </div>

                    {daysUntilDue !== null && (
                      <div className="mt-3 text-xs text-muted-foreground">
                        {daysUntilDue <= 0 ? (
                          <span className="text-destructive font-medium">Due for review</span>
                        ) : (
                          <span>Review in {daysUntilDue} days</span>
                        )}
                      </div>
                    )}
                  </CardContent>
                </Card>
              </Link>
            )
          })}
        </div>
      ) : (
        <Card>
          <CardContent className="py-12 text-center">
            <p className="text-muted-foreground">
              {searchQuery ? 'No words found matching your search.' : 'No words yet. Start by importing or adding words!'}
            </p>
            <Link to="/import">
              <Button className="mt-4">
                <Plus className="mr-2 h-4 w-4" />
                Add Your First Word
              </Button>
            </Link>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
