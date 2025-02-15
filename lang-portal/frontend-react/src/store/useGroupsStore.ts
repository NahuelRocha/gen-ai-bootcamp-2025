import { create } from 'zustand';
import { Group, PaginationParams, Page } from '../services/types';
import { groupsApi } from '../services/api';

interface GroupsState {
  groups: Group[];
  selectedGroup: Group | null;
  loading: boolean;
  error: string | null;
  currentPage: number;
  totalPages: number;
  fetchGroups: (params: PaginationParams) => Promise<Page<Group>>;
  fetchGroupById: (id: number) => Promise<Group>;
  setSelectedGroup: (group: Group | null) => void;
  setError: (error: string | null) => void;
  resetState: () => void;
}

export const useGroupsStore = create<GroupsState>((set) => ({
  groups: [],
  selectedGroup: null,
  loading: false,
  error: null,
  currentPage: 0,
  totalPages: 0,

  fetchGroups: async (params: PaginationParams) => {
    set({ loading: true });
    try {
      const response = await groupsApi.getGroups(params);
      set({ 
        groups: response.data.content,
        currentPage: response.data.number,
        totalPages: response.data.totalPages,
        error: null 
      });
      return response.data;
    } catch (error) {
      set({ error: 'Failed to fetch groups' });
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  fetchGroupById: async (id: number) => {
    set({ loading: true });
    try {
      const response = await groupsApi.getGroup(id);
      set({ 
        selectedGroup: response.data,
        error: null 
      });
      return response.data;
    } catch (error) {
      set({ error: `Failed to fetch group ${id}` });
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  setSelectedGroup: (group: Group | null) => set({ selectedGroup: group }),
  
  setError: (error: string | null) => set({ error }),
  
  resetState: () => set({ 
    groups: [],
    selectedGroup: null,
    loading: false,
    error: null,
    currentPage: 0,
    totalPages: 0
  })
}));
