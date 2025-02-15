import axios from 'axios';
import {
  Word,
  Group,
  StudySession,
  Page,
  PaginationParams,
  StudySessionRequestDTO,
  WordReviewRequestDTO,
  LastStudySession,
  WordsCountResponse
} from './types';

const api = axios.create({
  baseURL: 'http://localhost:8080',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: false
});

// Helper function to convert 0-based to 1-based pagination
const convertPaginationParams = (params: PaginationParams) => ({
  page: params.page + 1, // Convert to 1-based pagination
  sortBy: params.sortBy || 'english',
  order: params.order || 'asc'
});

export const wordsApi = {
  getWords: (params: PaginationParams) =>
    api.get<Page<Word>>('/words', {
      params: convertPaginationParams(params)
    }),
  getWordsCount: () => api.get<WordsCountResponse>('/words/count')
};

export const groupsApi = {
  getGroups: (params: PaginationParams) =>
    api.get<Page<Group>>('/groups', {
      params: { page: params.page + 1 } // Groups only uses page parameter
    }),

  getGroup: (id: number) =>
    api.get<Group>(`/groups/${id}`),

  getGroupWords: (id: number, params: PaginationParams) =>
    api.get<Page<Word>>(`/groups/${id}`, {
      params: convertPaginationParams(params)
    })
};

export const studyApi = {
  createSession: (groupId: number, studyActivityId: number) => {
    const requestDTO: StudySessionRequestDTO = {
      groupId,
      studyActivityId
    };
    return api.post<StudySession>('/study_sessions', requestDTO);
  },

  submitReview: (sessionId: number, review: WordReviewRequestDTO) =>
    api.post<void>(`/study_sessions/${sessionId}/review`, review),

  getLastStudySession: () =>
    api.get<LastStudySession>('/study_sessions/last')
};
