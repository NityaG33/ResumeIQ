
import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import RouteLoading from "../common/RouteLoading";

const ProtectedRoute = ({ children }) => {
    const { user, loading } = useAuth();

    if (loading) {
        return <RouteLoading />;
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    return children;
};

export default ProtectedRoute;
