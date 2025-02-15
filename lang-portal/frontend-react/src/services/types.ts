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

export interface Page<T> {
  content: T[];
  pageable: {
    pageNumber: number;
    pageSize: number;
    sort: {
      sorted: boolean;
      unsorted: boolean;
      empty: boolean;
    };
  };
  totalElements: number;
  totalPages: number;
  last: boolean;
  size: number;
  number: number;
  sort: {
    sorted: boolean;
    unsorted: boolean;
    empty: boolean;
  };
  numberOfElements: number;
  first: boolean;
  empty: boolean;
}

export interface PaginationParams {
  page: number;
  sortBy?: string;
  order?: 'asc' | 'desc';
}

export interface StudySessionRequestDTO {
  groupId: number;
  studyActivityId: number;
}

export interface WordReviewRequestDTO {
  wordId: number;
  correct: boolean;
}

export interface LastStudySession {
  sessionId: number;
  groupName: string;
  activityName: string;
  correct: number;
  incorrect: number;
  createdAt: string;
}

export interface WordsCountResponse {
  totalWords: number;
  totalWordsLearned: number;
}