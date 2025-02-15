import { create } from 'zustand';
import { StudySession, WordReview, LastStudySession } from '../services/types';
import { studyApi } from '../services/api';

interface StudyState {
  currentSession: StudySession | null;
  loading: boolean;
  error: string | null;
  reviews: WordReview[];
  createStudySession: (groupId: number, studyActivityId: number) => Promise<void>;
  submitWordReview: (sessionId: number, review: WordReview) => Promise<void>;
  setError: (error: string | null) => void;
  resetState: () => void;
  lastSession: LastStudySession | null;
  loadingLastSession: boolean;
  errorLastSession: string | null;
  fetchLastSession: () => Promise<void>;
}

export const useStudyStore = create<StudyState>((set, get) => ({
  currentSession: null,
  loading: false,
  error: null,
  reviews: [],
  lastSession: null,
  loadingLastSession: false,
  errorLastSession: null,

  fetchLastSession: async () => {
    set({ loadingLastSession: true, errorLastSession: null });
    try {
      const response = await studyApi.getLastStudySession();
      set({ lastSession: response.data, loadingLastSession: false });
    } catch (error) {
      set({ errorLastSession: 'Error loading session', loadingLastSession: false });
    }
  },

  createStudySession: async (groupId: number, studyActivityId: number) => {
    set({ loading: true });
    try {
      const response = await studyApi.createSession(groupId, studyActivityId);
      set({
        currentSession: response.data,
        reviews: [],
        error: null
      });
    } catch (error) {
      set({ error: 'Failed to create study session' });
    } finally {
      set({ loading: false });
    }
  },

  submitWordReview: async (sessionId: number, review: WordReview) => {
    set({ loading: true });
    try {
      await studyApi.submitReview(sessionId, review);
      const currentReviews = get().reviews;
      set({
        reviews: [...currentReviews, review],
        error: null
      });
    } catch (error) {
      set({ error: 'Failed to submit word review' });
    } finally {
      set({ loading: false });
    }
  },

  setError: (error: string | null) => set({ error }),

  resetState: () => set({
    currentSession: null,
    loading: false,
    error: null,
    reviews: []
  })
}));
