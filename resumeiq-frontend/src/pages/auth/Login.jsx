import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

function Login() {
    const { login } = useAuth();
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        setError("");
        setLoading(true);

        try {
            await login({
                email,
                password,
            });

            navigate("/dashboard");
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                "Invalid email or password"
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
            <div className="w-full max-w-md bg-white rounded-2xl shadow-sm border border-slate-200 p-8">

                <h1 className="text-3xl font-bold text-slate-900">
                    Welcome back
                </h1>

                <p className="text-slate-500 mt-2">
                    Login to continue using ResumeIQ.
                </p>

                {error && (
                    <div className="mt-6 p-3 rounded-lg bg-red-50 text-red-600 text-sm">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="mt-6 space-y-5">

                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">
                            Email
                        </label>

                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="w-full px-4 py-3 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="you@example.com"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">
                            Password
                        </label>

                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="w-full px-4 py-3 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Enter your password"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
                    >
                        {loading ? "Logging in..." : "Login"}
                    </button>

                </form>

                <p className="text-center text-sm text-slate-500 mt-6">
                    Don't have an account?{" "}
                    <Link
                        to="/register"
                        className="text-blue-600 font-medium hover:underline"
                    >
                        Create one
                    </Link>
                </p>

            </div>
        </div>
    );
}

export default Login;