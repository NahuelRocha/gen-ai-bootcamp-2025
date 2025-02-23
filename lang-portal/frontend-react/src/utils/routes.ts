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
    title: 'Panel',
    path: ROUTES.HOME,
    icon: '📊',
  },
  {
    title: 'Palabras',
    path: ROUTES.WORDS,
    icon: '📚',
  },
  {
    title: 'Grupos',
    path: ROUTES.GROUPS.LIST,
    icon: '📑',
  },
  {
    title: 'Estudio',
    path: ROUTES.STUDY.HOME,
    icon: '📝',
  },
] as const;
