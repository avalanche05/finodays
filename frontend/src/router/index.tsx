import { createBrowserRouter } from 'react-router-dom';

import SignUp from '../pages/SignUp';
import Login from '../pages/Login';

export const router = createBrowserRouter([
    {
        path: '/signup',
        element: <SignUp />,
    },
    {
        path: '/login',
        element: <Login />,
    },
]);
