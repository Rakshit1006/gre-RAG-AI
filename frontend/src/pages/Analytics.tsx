import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function Analytics() {
  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-bold tracking-tight">Analytics</h1>
      <Card>
        <CardHeader>
          <CardTitle>Coming Soon</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Analytics and progress tracking features coming soon.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
