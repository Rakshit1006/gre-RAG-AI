import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export function Settings() {
  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-4xl font-bold tracking-tight">Settings</h1>

      <Card>
        <CardHeader>
          <CardTitle>Study Settings</CardTitle>
          <CardDescription>Configure your study preferences</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium">New Words Per Day</label>
            <Input type="number" defaultValue={50} className="mt-2" />
            <p className="text-xs text-muted-foreground mt-1">
              Default: 50 words per day
            </p>
          </div>

          <div>
            <label className="text-sm font-medium">Daily Study Time Goal (minutes)</label>
            <Input type="number" defaultValue={60} className="mt-2" />
          </div>

          <Button className="mt-4">Save Settings</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Data Management</CardTitle>
          <CardDescription>Manage your local data</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">
            All data is stored locally on your device. No remote backups are created by default.
          </p>
          <div className="flex gap-4">
            <Button variant="outline">Export Data</Button>
            <Button variant="destructive">Clear All Data</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
