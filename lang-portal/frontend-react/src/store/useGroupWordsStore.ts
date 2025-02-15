import { create } from 'zustand';
import { Word, PaginationParams } from '../services/types';
import { groupsApi } from '../services/api';

interface GroupWordsState {
    words: Word[];
    loading: boolean;
    error: string | null;
    currentPage: number;
    totalPages: number;
    currentGroupId: number | null;
    currentSortBy: string;
    currentOrder: 'asc' | 'desc';
    fetchGroupWords: (groupId: number, params: PaginationParams) => Promise<void>;
    setError: (error: string | null) => void;
    resetState: () => void;
}

export const useGroupWordsStore = create<GroupWordsState>((set) => ({
    words: [],
    loading: false,
    error: null,
    currentPage: 0,
    totalPages: 0,
    currentGroupId: null,
    currentSortBy: 'english',
    currentOrder: 'asc',

    fetchGroupWords: async (groupId: number, params: PaginationParams) => {
        set({ loading: true });
        try {
            const response = await groupsApi.getGroupWords(groupId, params);
            set({
                words: response.data.content,
                currentPage: response.data.number,
                totalPages: response.data.totalPages,
                currentGroupId: groupId,
                currentSortBy: params.sortBy || 'english',
                currentOrder: params.order || 'asc',
                error: null
            });
        } catch (error) {
            set({ error: 'Failed to fetch group words' });
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
        currentGroupId: null,
        currentSortBy: 'english',
        currentOrder: 'asc'
    })
}));