import { Navigate } from 'react-router-dom';

type Props = {
    isSignedIn: boolean;
};

function ProtectedRedirect({ isSignedIn }: Props): JSX.Element {
    if (!isSignedIn) {
        return <Navigate to='/login' replace />;
    } else {
        return <Navigate to='/dashboard/profile' replace />;
    }
}

export default ProtectedRedirect;
