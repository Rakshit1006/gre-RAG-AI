import { useQuery } from '@tanstack/react-query'
import { sessionAPI, wordsAPI } from '@/lib/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { BookOpen, Brain, Target, TrendingUp } from 'lucide-react'
import { Link } from 'react-router-dom'

export function Dashboard() {
  const { data: stats } = useQuery({
    queryKey: ['session-stats'],
    queryFn: async () => {
      const response = await sessionAPI.stats()
      return response.data
    },
  })

  const { data: recentWords } = useQuery({
    queryKey: ['recent-words'],
    queryFn: async () => {
      const response = await wordsAPI.search({ limit: 5 })
      return response.data
    },
  })

  const dueToday = stats?.due_words || 0
  const newWords = stats?.new_words || 0
  const accuracy = stats?.accuracy ? Math.round(stats.accuracy * 100) : 0

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Welcome back! Here's your GRE prep overview.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Due Today</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dueToday}</div>
            <p className="text-xs text-muted-foreground">
              {dueToday > 0 ? 'Ready to review' : 'All caught up!'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">New Words</CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{newWords}</div>
            <p className="text-xs text-muted-foreground">
              Waiting to learn
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Accuracy</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{accuracy}%</div>
            <Progress value={accuracy} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Words</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total_words || 0}</div>
            <p className="text-xs text-muted-foreground">
              In your deck
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Start your study session</CardDescription>
        </CardHeader>
        <CardContent className="flex gap-4">
          <Link to="/practice">
            <Button size="lg">
              <Brain className="mr-2 h-4 w-4" />
              Start Practice
            </Button>
          </Link>
          <Link to="/vocab">
            <Button size="lg" variant="outline">
              <BookOpen className="mr-2 h-4 w-4" />
              Browse Vocab
            </Button>
          </Link>
        </CardContent>
      </Card>

      {/* Recent Words */}
      {recentWords && recentWords.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Recently Added</CardTitle>
            <CardDescription>Your latest vocabulary words</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentWords.map((word) => (
                <Link
                  key={word.id}
                  to={`/vocab/${word.id}`}
                  className="block rounded-lg border p-4 hover:bg-accent transition-colors"
                >
                  <div className="font-semibold">{word.word}</div>
                  <div className="text-sm text-muted-foreground mt-1">
                    {word.pithy_definition || word.gre_definition}
                  </div>
                </Link>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Today's Load Card */}
      <Card>
        <CardHeader>
          <CardTitle>Today's Load</CardTitle>
          <CardDescription>Estimated study time</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">
            {Math.ceil((dueToday + Math.min(newWords, 50)) * 1.2)} min
          </div>
          <p className="text-sm text-muted-foreground mt-2">
            Based on {dueToday} reviews and up to 50 new words
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
