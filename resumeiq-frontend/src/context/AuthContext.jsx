import { createContext, useContext, useEffect, useState } from "react";
import {
    getCurrentUser,
    login as loginApi,
    register as registerApi,
    logout as logoutApi,
} from "../services/api";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Check if user is already logged in
    useEffect(() => {
        const checkAuth = async () => {
            try {
                const currentUser = await getCurrentUser();
                setUser(currentUser);
            } catch {
                setUser(null);
            } finally {
                setLoading(false);
            }
        };

        checkAuth();
    }, []);

    const login = async (credentials) => {
        await loginApi(credentials);

        // Get actual user after successful login
        const currentUser = await getCurrentUser();
        setUser(currentUser);
    };

    const register = async (userData) => {
        return await registerApi(userData);
    };

    const logout = async () => {
        await logoutApi();
        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                loading,
                login,
                register,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};