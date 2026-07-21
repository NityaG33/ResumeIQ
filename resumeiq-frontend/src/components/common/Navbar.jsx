import { BrainCircuit } from "lucide-react";

function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

        {/* Logo */}

        <div className="flex items-center gap-3">

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

        </div>

        {/* Navigation */}

        <div className="hidden md:flex gap-8 text-slate-600 font-medium">

          <a href="#" className="hover:text-blue-600">
            Home
          </a>

          <a href="#" className="hover:text-blue-600">
            Features
          </a>

          <a href="#" className="hover:text-blue-600">
            About
          </a>

        </div>

      </div>
    </nav>
  );
}

export default Navbar;