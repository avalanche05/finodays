import { createBrowserRouter } from 'react-router-dom';

import SignUp from '../pages/SignUp';
import Login from '../pages/Login';
import ProtectedRoute from './ProtectedRoute';
import AuthService from '../api/AuthService';
import UnauthorizedOnlyRoute from './UnauthorizedOnlyRoute';
import DashboardLayout from '../components/DashboardLayout';
import MyCfas from '../pages/MyCfas';
import Profile from '../pages/Profile';

export const router = createBrowserRouter([
    {
        path: '/signup',
        element: (
            <UnauthorizedOnlyRoute isSignedIn={AuthService.isAuthorized()}>
                <SignUp />
            </UnauthorizedOnlyRoute>
        ),
    },
    {
        path: '/login',
        element: (
            <UnauthorizedOnlyRoute isSignedIn={AuthService.isAuthorized()}>
                <Login />
            </UnauthorizedOnlyRoute>
        ),
    },
    {
        path: '/dashboard',
        element: (
            <ProtectedRoute isSignedIn={AuthService.isAuthorized()}>
                <DashboardLayout />
            </ProtectedRoute>
        ),
        children: [
            {
                path: '/dashboard/profile',
                element: <Profile />,
            },
            {
                path: '/dashboard/my-cfas',
                element: <MyCfas />,
            },
        ],
    },

    {
        path: '*',
        element: (
            <ProtectedRoute isSignedIn={false}>
                <DashboardLayout />
            </ProtectedRoute>
        ),
    },
]);
