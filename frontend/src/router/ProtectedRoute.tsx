import { Navigate } from 'react-router-dom';

type Props = {
    isSignedIn: boolean;
    children: React.ReactNode;
};

function ProtectedRoute({ isSignedIn, children }: Props) {
    if (!isSignedIn) {
        return <Navigate to='/login' replace />;
    }
    return children;
}

export default ProtectedRoute;
