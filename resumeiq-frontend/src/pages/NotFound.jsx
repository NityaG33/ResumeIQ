import { Link } from "react-router-dom";

function NotFound() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-50 px-6">
            <div className="text-center">
                <h1 className="text-7xl font-bold text-slate-900">
                    404
                </h1>

                <h2 className="text-2xl font-semibold text-slate-800 mt-4">
                    Page Not Found
                </h2>

                <p className="text-slate-500 mt-2">
                    The page you're looking for doesn't exist.
                </p>

                <Link
                    to="/"
                    className="inline-block mt-6 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                    Go Home
                </Link>
            </div>
        </div>
    );
}

export default NotFound;