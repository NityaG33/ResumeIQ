import { BrainCircuit } from "lucide-react";
import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

function Navbar() {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

        {/* Logo */}

        <Link to="/" className="flex items-center gap-3">

          <BrainCircuit
            className="text-blue-600"
            size={34}
          />

          <div>
            <h1 className="text-2xl font-bold text-slate-900">
              ResumeIQ
            </h1>

            <p className="text-xs text-slate-500">
              AI Resume Intelligence
            </p>
          </div>

        </Link>

        {/* Navigation */}

        <div className="hidden md:flex items-center gap-8 text-slate-600 font-medium">

          <Link
            to="/"
            className="hover:text-blue-600"
          >
            Home
          </Link>

          <Link to="/#features" className="hover:text-blue-600">
              Features
          </Link>

          {user ? (
            <>
              <Link
                to="/dashboard"
                className="hover:text-blue-600"
              >
                Analyze
              </Link>

              <Link
                to="/analyses"
                className="hover:text-blue-600"
              >
                History
              </Link>

              <button
                onClick={handleLogout}
                className="hover:text-red-600"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="hover:text-blue-600"
              >
                Login
              </Link>

              <Link
                to="/register"
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Register
              </Link>
            </>
          )}

        </div>

      </div>
    </nav>
  );
}

export default Navbar;