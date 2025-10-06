# GRE Mentor Frontend

React + TypeScript frontend with shadcn/ui components.

## Setup

```bash
npm install
npm run dev
```

## Features

- **Dashboard**: Overview of study progress and due words
- **Vocab Deck**: Browse and manage vocabulary
- **Word Detail**: Edit mnemonics and view word details
- **Practice**: Flashcard-based practice sessions with SRS
- **Import**: Add words via PDF, Anki, or manual entry
- **Analytics**: Track progress (coming soon)
- **Settings**: Configure study preferences

## Tech Stack

- React 18
- TypeScript
- Vite
- TailwindCSS
- shadcn/ui (Radix UI primitives)
- React Query for data fetching
- React Router for navigation

## API Integration

Configure backend URL in `.env`:

```env
VITE_API_URL=http://localhost:8000
```

## Build

```bash
npm run build
```

Output in `dist/` directory.
