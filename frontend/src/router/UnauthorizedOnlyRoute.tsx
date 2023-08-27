import { Navigate } from 'react-router-dom';

type Props = {
    isSignedIn: boolean;
    children: React.ReactNode;
};

function UnauthorizedOnlyRoute({ isSignedIn, children }: Props) {
    if (isSignedIn) {
        return <Navigate to='/dashboard' replace />;
    }
    return children;
}

export default UnauthorizedOnlyRoute;
