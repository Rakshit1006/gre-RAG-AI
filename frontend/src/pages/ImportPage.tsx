import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { importAPI, mnemonicAPI } from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Upload, FileText, Package, Plus } from 'lucide-react'

export function ImportPage() {
  const [pdfFile, setPdfFile] = useState<File | null>(null)
  const [ankiFile, setAnkiFile] = useState<File | null>(null)
  const [manualWord, setManualWord] = useState('')

  const pdfMutation = useMutation({
    mutationFn: (file: File) => importAPI.pdf(file),
    onSuccess: (response) => {
      alert(`Successfully imported ${response.data.questions_extracted} questions`)
      setPdfFile(null)
    },
  })

  const ankiMutation = useMutation({
    mutationFn: (file: File) => importAPI.anki(file),
    onSuccess: (response) => {
      alert(`Successfully imported ${response.data.words_imported} words`)
      setAnkiFile(null)
    },
  })

  const generateMutation = useMutation({
    mutationFn: (word: string) => mnemonicAPI.generate({ word }),
    onSuccess: async (response) => {
      const result = await mnemonicAPI.save(response.data)
      alert(`Added "${manualWord}" to your vocabulary!`)
      setManualWord('')
    },
  })

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-4xl font-bold tracking-tight">Import Content</h1>

      <Card>
        <CardHeader>
          <CardTitle>Add Single Word</CardTitle>
          <CardDescription>Generate mnemonic for a new vocabulary word</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-4">
            <Input
              placeholder="Enter a word..."
              value={manualWord}
              onChange={(e) => setManualWord(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && manualWord) {
                  generateMutation.mutate(manualWord)
                }
              }}
            />
            <Button
              onClick={() => generateMutation.mutate(manualWord)}
              disabled={!manualWord || generateMutation.isPending}
            >
              <Plus className="mr-2 h-4 w-4" />
              Add Word
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Import PDF</CardTitle>
          <CardDescription>Extract questions from PDF files</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="border-2 border-dashed rounded-lg p-8 text-center">
            <FileText className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <Input
              type="file"
              accept=".pdf"
              onChange={(e) => setPdfFile(e.target.files?.[0] || null)}
              className="mb-4"
            />
            {pdfFile && (
              <div className="text-sm text-muted-foreground mb-4">
                Selected: {pdfFile.name}
              </div>
            )}
            <Button
              onClick={() => pdfFile && pdfMutation.mutate(pdfFile)}
              disabled={!pdfFile || pdfMutation.isPending}
            >
              <Upload className="mr-2 h-4 w-4" />
              {pdfMutation.isPending ? 'Importing...' : 'Import PDF'}
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Import Anki Deck</CardTitle>
          <CardDescription>Import vocabulary from Anki .apkg files</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="border-2 border-dashed rounded-lg p-8 text-center">
            <Package className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <Input
              type="file"
              accept=".apkg"
              onChange={(e) => setAnkiFile(e.target.files?.[0] || null)}
              className="mb-4"
            />
            {ankiFile && (
              <div className="text-sm text-muted-foreground mb-4">
                Selected: {ankiFile.name}
              </div>
            )}
            <Button
              onClick={() => ankiFile && ankiMutation.mutate(ankiFile)}
              disabled={!ankiFile || ankiMutation.isPending}
            >
              <Upload className="mr-2 h-4 w-4" />
              {ankiMutation.isPending ? 'Importing...' : 'Import Anki Deck'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
