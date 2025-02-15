export const ROUTES = {
  HOME: '/',
  WORDS: '/words',
  GROUPS: {
    LIST: '/groups',
    DETAIL: (groupId: number) => `/groups/${groupId}`,
  },
  STUDY: {
    HOME: '/study',
    GROUP: (groupId: number) => `/study/group/${groupId}`,
  },
} as const;

export const NAV_ITEMS = [
  {
    title: 'Dashboard',
    path: ROUTES.HOME,
    icon: '📊',
  },
  {
    title: 'Words',
    path: ROUTES.WORDS,
    icon: '📚',
  },
  {
    title: 'Groups',
    path: ROUTES.GROUPS.LIST,
    icon: '📑',
  },
  {
    title: 'Study',
    path: ROUTES.STUDY.HOME,
    icon: '📝',
  },
] as const;
