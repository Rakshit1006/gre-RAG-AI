import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function QuestionBank() {
  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-bold tracking-tight">Question Bank</h1>
      <Card>
        <CardHeader>
          <CardTitle>Coming Soon</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Question bank feature will be available soon. Import questions from PDFs to get started.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
