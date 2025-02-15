import { createBrowserRouter, Navigate } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { Dashboard } from './pages/Dashboard';
import { Words } from './pages/Words';
import { Groups } from './pages/Groups';
import { Study } from './pages/Study';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: 'words',
        element: <Words />,
      },
      {
        path: 'groups',
        children: [
          {
            index: true,
            element: <Groups />,
          },
          {
            path: ':groupId',
            element: <Groups />,
          },
        ],
      },
      {
        path: 'study',
        children: [
          {
            index: true,
            element: <Study />,
          },
          {
            path: 'group/:groupId',
            element: <Study />,
          },
        ],
      },
      {
        path: '*',
        element: <Navigate to="/" replace />,
      },
    ],
  },
]);
