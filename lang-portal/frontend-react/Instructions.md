# Language Learning Portal - Frontend Implementation Guide

## Project Overview
This guide provides step-by-step instructions for implementing the frontend of our Language Learning Portal. The frontend will consume the existing Spring Boot REST API and provide an intuitive interface for language learning.

## Prerequisites
- Node.js (v18 or higher)
- Existing Vite + React + TypeScript project
- TailwindCSS configured
- ShadcnUI installed

## Additional Dependencies

First, install these additional dependencies:

```bash
# HTTP client for API requests
npm install axios

# Client-side routing
npm install react-router-dom

# State management
npm install zustand

# Form handling
npm install react-hook-form

# Data visualization (for progress charts)
npm install recharts

# Loading states and animations
npm install framer-motion

# Date formatting
npm install date-fns
```

## Project Structure

Create the following folder structure:

```
src/
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Layout.tsx
│   ├── words/
│   │   ├── WordCard.tsx
│   │   ├── WordList.tsx
│   │   └── WordFilters.tsx
│   ├── groups/
│   │   ├── GroupCard.tsx
│   │   └── GroupList.tsx
│   └── study/
│       ├── StudySession.tsx
│       ├── ActivityCard.tsx
│       └── ReviewForm.tsx
├── pages/
│   ├── Dashboard.tsx
│   ├── Words.tsx
│   ├── Groups.tsx
│   └── Study.tsx
├── services/
│   ├── api.ts
│   └── types.ts
├── store/
│   ├── useWordsStore.ts
│   ├── useGroupsStore.ts
│   └── useStudyStore.ts
└── utils/
    ├── formatters.ts
    └── constants.ts
```

## Type Definitions

Create `services/types.ts`:

```typescript
export interface Word {
  id: number;
  english: string;
  spanish: string;
  pronunciation: string;
  parts: {
    type: string;
    usage?: string;
    category?: string;
  };
  correctCount: number;
  wrongCount: number;
}

export interface Group {
  id: number;
  name: string;
  wordsCount: number;
}

export interface StudyActivity {
  id: number;
  name: string;
  url: string;
}

export interface StudySession {
  id: number;
  groupId: number;
  studyActivityId: number;
  createdAt: string;
}

export interface WordReview {
  wordId: number;
  studySessionId: number;
  correct: boolean;
}

export interface PaginationParams {
  page: number;
  sortBy?: string;
  order?: 'asc' | 'desc';
}
```

## API Service

Create `services/api.ts`:

```typescript
import axios from 'axios';
import { Word, Group, StudySession, WordReview, PaginationParams } from './types';

const api = axios.create({
  baseURL: 'http://localhost:8080',
});

export const wordsApi = {
  getWords: (params: PaginationParams) => 
    api.get<Word[]>('/words', { params }),
  
  getWordsByGroup: (groupId: number, params: PaginationParams) =>
    api.get<Word[]>(`/groups/${groupId}`, { params }),
};

export const groupsApi = {
  getGroups: (params: PaginationParams) =>
    api.get<Group[]>('/groups', { params }),
  
  getGroup: (id: number) =>
    api.get<Group>(`/groups/${id}`),
};

export const studyApi = {
  createSession: (groupId: number, studyActivityId: number) =>
    api.post<StudySession>('/study_sessions', { groupId, studyActivityId }),
  
  submitReview: (sessionId: number, review: WordReview) =>
    api.post<void>(`/study_sessions/${sessionId}/review`, review),
};
```

## State Management

Create `store/useWordsStore.ts`:

```typescript
import create from 'zustand';
import { Word, PaginationParams } from '../services/types';
import { wordsApi } from '../services/api';

interface WordsStore {
  words: Word[];
  loading: boolean;
  error: string | null;
  fetchWords: (params: PaginationParams) => Promise<void>;
}

export const useWordsStore = create<WordsStore>((set) => ({
  words: [],
  loading: false,
  error: null,
  fetchWords: async (params) => {
    set({ loading: true });
    try {
      const response = await wordsApi.getWords(params);
      set({ words: response.data, error: null });
    } catch (error) {
      set({ error: 'Failed to fetch words' });
    } finally {
      set({ loading: false });
    }
  },
}));
```

Create similar stores for groups and study sessions.

## Components Implementation

### Layout Component

```typescript
// components/layout/Layout.tsx
import { Header } from './Header';
import { Sidebar } from './Sidebar';

export const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
};
```

### Word List Component

```typescript
// components/words/WordList.tsx
import { useEffect } from 'react';
import { useWordsStore } from '@/store/useWordsStore';
import { WordCard } from './WordCard';

export const WordList = () => {
  const { words, loading, error, fetchWords } = useWordsStore();

  useEffect(() => {
    fetchWords({ page: 1 });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {words.map((word) => (
        <WordCard key={word.id} word={word} />
      ))}
    </div>
  );
};
```

### Study Session Component

```typescript
// components/study/StudySession.tsx
import { useState } from 'react';
import { useStudyStore } from '@/store/useStudyStore';
import { Button } from '@/components/ui/button';

export const StudySession = ({ groupId }: { groupId: number }) => {
  const [sessionId, setSessionId] = useState<number | null>(null);
  const { startSession, submitReview } = useStudyStore();

  const handleStartSession = async (activityId: number) => {
    const session = await startSession(groupId, activityId);
    setSessionId(session.id);
  };

  // Implement session logic and review submission
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Study Session</h2>
      {/* Implement study interface */}
    </div>
  );
};
```

## Routing Setup

Update `App.tsx`:

```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { Dashboard } from './pages/Dashboard';
import { Words } from './pages/Words';
import { Groups } from './pages/Groups';
import { Study } from './pages/Study';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/words" element={<Words />} />
          <Route path="/groups" element={<Groups />} />
          <Route path="/study/:groupId" element={<Study />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
```

## Key Features to Implement

1. **Dashboard**
   - Display learning progress
   - Show recent study sessions
   - Quick access to study activities

2. **Words Page**
   - Paginated word list
   - Filtering and sorting options
   - Search functionality
   - Word cards with pronunciation

3. **Groups Page**
   - List of word groups
   - Group statistics
   - Quick study session start

4. **Study Page**
   - Activity selection
   - Session progress tracking
   - Word review interface
   - Results summary

## Additional Considerations

1. **Error Handling**
   - Implement proper error boundaries
   - Show user-friendly error messages
   - Add retry mechanisms for failed requests

2. **Loading States**
   - Add loading skeletons
   - Implement progressive loading
   - Show loading indicators for actions

3. **Responsive Design**
   - Ensure mobile-friendly layout
   - Implement proper breakpoints
   - Consider touch interactions

4. **Performance**
   - Implement pagination properly
   - Use proper caching strategies
   - Optimize bundle size

5. **Accessibility**
   - Add proper ARIA labels
   - Ensure keyboard navigation
   - Maintain proper contrast ratios