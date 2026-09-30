import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const ProtectedRoute = ({ children }) => {
    const { user, loading } = useAuth();

    // Wait until authentication check is complete
    if (loading) {
        return <div>Loading...</div>;
    }

    // User is not logged in
    if (!user) {
        return <Navigate to="/login" replace />;
    }

    // User is authenticated
    return children;
};

export default ProtectedRoute;