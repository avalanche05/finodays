import { createBrowserRouter } from 'react-router-dom';

import SignUp from '../pages/SignUp';
import Login from '../pages/Login';
import ProtectedRoute from './ProtectedRoute';
import Dashboard from '../pages/Dashboard';
import AuthService from '../api/AuthService';
import UnauthorizedOnlyRoute from './UnauthorizedOnlyRoute';

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
                <Dashboard />
            </ProtectedRoute>
        ),
    },
    {
        path: '*',
        element: (
            <ProtectedRoute isSignedIn={false}>
                <Dashboard />
            </ProtectedRoute>
        ),
    },
]);
