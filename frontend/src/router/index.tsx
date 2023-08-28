import { createBrowserRouter } from 'react-router-dom';

import AuthService from '../api/AuthService';
import DashboardLayout from '../components/DashboardLayout';
import CreateCfa from '../pages/CreateCfa';
import Login from '../pages/Login';
import Profile from '../pages/Profile';
import SignUp from '../pages/SignUp';
import ProtectedRoute from './ProtectedRoute';
import UnauthorizedOnlyRoute from './UnauthorizedOnlyRoute';
import CfaMarket from '../pages/CfaMarket';

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
                path: '/dashboard/create-cfa',
                element: <CreateCfa />,
            },
            {
                path: '/dashboard/cfa-market',
                element: <CfaMarket />,
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
