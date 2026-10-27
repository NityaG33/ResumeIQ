
import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import RouteLoading from "../common/RouteLoading";

function PublicRoute({ children }) {
    const { user, loading } = useAuth();

    if (loading) {
        return <RouteLoading />;
    }

    if (user) {
        return <Navigate to="/dashboard" replace />;
    }

    return children;
}

export default PublicRoute;
