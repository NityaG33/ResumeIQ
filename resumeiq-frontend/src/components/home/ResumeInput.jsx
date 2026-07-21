import { useState } from "react";
import { useDropzone } from "react-dropzone";
import {
  UploadCloud,
  FileText,
  CheckCircle,
  Trash2,
  AlertCircle,
} from "lucide-react";

function ResumeInput({
    inputMode,
    setInputMode,
    selectedFile,
    setSelectedFile,
    resumeText,
    setResumeText,
    }) {
  const [error, setError] = useState("");

  const onDrop = (acceptedFiles, rejectedFiles) => {
    setError("");

    if (rejectedFiles.length > 0) {
      setError("Only PDF files up to 5 MB are allowed.");
      return;
    }

    if (acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0]);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: false,
    accept: {
      "application/pdf": [".pdf"],
    },
    maxSize: 5 * 1024 * 1024,
  });

  const removeFile = () => {
    setSelectedFile(null);
    setError("");
  };

  return (
    <div className="mb-8">

      <label className="text-lg font-semibold text-slate-800">
        Resume
      </label>

      {/* Toggle Buttons */}

      <div className="flex gap-3 mt-4">

        <button type="button" onClick={() => {
            setInputMode("upload");
            setResumeText("");
          }}
          className={`px-5 py-2 rounded-lg border transition ${
            inputMode === "upload"
              ? "bg-blue-600 text-white border-blue-600"
              : "bg-white text-slate-700 hover:border-blue-500"
          }`}
        >
          Upload PDF
        </button>

        <button type="button" onClick={() => {
            setInputMode("paste");
            removeFile();
          }}
          className={`px-5 py-2 rounded-lg border transition ${
            inputMode === "paste"
              ? "bg-blue-600 text-white border-blue-600"
              : "bg-white text-slate-700 hover:border-blue-500"
          }`}
        >
          Paste Resume
        </button>

      </div>

      {/* Upload Mode */}

      {inputMode === "upload" && (

        <div className="mt-6">

          {!selectedFile ? (

            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition

                ${
                  isDragActive
                    ? "border-blue-600 bg-blue-50"
                    : "border-slate-300 hover:border-blue-500 hover:bg-slate-50"
                }
              `}
            >

              <input {...getInputProps()} />

              <UploadCloud size={52}
                className="mx-auto text-blue-600"
              />

              <h3 className="text-xl font-semibold mt-5">
                {isDragActive
                  ? "Drop your PDF here"
                  : "Drag & Drop Resume"}
              </h3>
              <p className="text-slate-500 mt-3">
                or click to browse files
              </p>
              <p className="text-sm text-slate-400 mt-5">
                PDF • Maximum size: 5 MB
              </p>

            </div>

          ) : (

            <div className="border rounded-2xl p-6 bg-green-50 flex items-center justify-between">

              <div className="flex items-center gap-4">
                <CheckCircle size={34} className="text-green-600" />
                <div>
                  <p className="font-semibold text-slate-800">
                    {selectedFile.name}
                  </p>
                  <p className="text-sm text-slate-500">
                    {(selectedFile.size / 1024).toFixed(1)} KB
                  </p>
                </div>
              </div>

              <button type="button" onClick={removeFile}
                className="text-red-500 hover:text-red-700 transition">
                <Trash2 size={22} />
              </button>

            </div>
          )}

          {error && (
            <div className="mt-4 flex items-center gap-2 text-red-600">
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          )}
        </div>
      )}

      {/* Paste Resume */}

      {inputMode === "paste" && (
        <textarea
          rows={10}
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
          placeholder="Paste your resume here..."
          className="w-full mt-6 border rounded-2xl p-5 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      )}
    </div>
  );
}

export default ResumeInput;