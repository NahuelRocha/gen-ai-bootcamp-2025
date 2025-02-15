import { create } from 'zustand';
import { Word, PaginationParams, Page, WordsCountResponse } from '../services/types';
import { wordsApi } from '../services/api';

interface WordsState {
  words: Word[];
  loading: boolean;
  error: string | null;
  currentPage: number;
  totalPages: number;
  wordsCount: WordsCountResponse;
  fetchWords: (params: PaginationParams) => Promise<Page<Word>>;
  fetchWordsCount: () => Promise<WordsCountResponse>;
  setError: (error: string | null) => void;
  resetState: () => void;
}

export const useWordsStore = create<WordsState>((set) => ({
  words: [],
  loading: false,
  error: null,
  currentPage: 0,
  totalPages: 0,
  wordsCount: { totalWords: 0, totalWordsLearned: 0 },

  fetchWords: async (params: PaginationParams) => {
    set({ loading: true });
    try {
      const response = await wordsApi.getWords(params);
      console.log("Fetched words:", response.data.content);
      set({
        words: response.data.content,
        currentPage: response.data.number,
        totalPages: response.data.totalPages,
        error: null
      });
      return response.data;
    } catch (error) {
      set({ error: 'Failed to fetch words' });
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  fetchWordsCount: async () => {
    set({ loading: true });
    try {
      const response = await wordsApi.getWordsCount();
      set({ wordsCount: response.data });
      return response.data;
    } catch (error) {
      set({ error: 'Failed to fetch words count' });
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  setError: (error: string | null) => set({ error }),

  resetState: () => set({
    words: [],
    loading: false,
    error: null,
    currentPage: 0,
    totalPages: 0,
    wordsCount: { totalWords: 0, totalWordsLearned: 0 }
  })
}));
