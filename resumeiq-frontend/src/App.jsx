import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Results from "./pages/Results";
import Dashboard from "./pages/Dashboard";

import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";

import ProtectedRoute from "./components/auth/ProtectedRoute";
import NotFound from "./pages/NotFound";

import AnalysisHistory from "./pages/AnalysisHistory";
import PublicRoute from "./components/auth/PublicRoute";

function App() {
    return (
        <BrowserRouter>
            <Routes>

                {/* Public routes */}
                <Route path="/" element={<Home />} />
                <Route
                    path="/login"
                    element={
                        <PublicRoute>
                            <Login />
                        </PublicRoute>
                    }
                />

                <Route
                    path="/register"
                    element={
                        <PublicRoute>
                            <Register />
                        </PublicRoute>
                    }
                />

                {/* Protected routes */}
                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />

                {/* New analysis result */}
                <Route
                    path="/results"
                    element={
                        <ProtectedRoute>
                            <Results />
                        </ProtectedRoute>
                    }
                />

                {/* Historical analysis result */}
                <Route
                    path="/results/:analysisId"
                    element={
                        <ProtectedRoute>
                            <Results />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/analyses"
                    element={
                        <ProtectedRoute>
                            <AnalysisHistory />
                        </ProtectedRoute>
                    }
                />

                {/* 404 */}
                <Route path="*" element={<NotFound />} />

            </Routes>
        </BrowserRouter>
    );
}

export default App;