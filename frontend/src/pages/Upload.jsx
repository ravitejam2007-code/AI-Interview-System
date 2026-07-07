import { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload as UploadIcon, FileText, CheckCircle2, AlertCircle, Loader2, Target } from 'lucide-react';
import { uploadResume } from '../services/api';
import { useNavigate } from 'react-router-dom';

const Upload = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please upload a valid PDF file.');
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('resume', file);

    try {
      const response = await uploadResume(formData);
      setResult(response.data);
      localStorage.setItem('resume_data', JSON.stringify(response.data));
    } catch (err) {
      console.error("Upload error details:", err);
      setError('Upload failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold mb-4">Analyze Your Resume</h2>
        <p className="text-slate-400">Upload your PDF resume to see your ATS score and generate interview questions.</p>
      </div>

      {!result ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-slate-900 border-2 border-dashed border-white/10 rounded-3xl p-12 text-center"
        >
          <div className="flex flex-col items-center gap-6">
            <div className="w-20 h-20 bg-indigo-600/10 rounded-full flex items-center justify-center">
              <UploadIcon className="text-indigo-500" size={32} />
            </div>

            <div>
              <p className="text-xl font-semibold mb-2">Drag and drop or click to upload</p>
              <p className="text-sm text-slate-500">PDF documents only (max 5MB)</p>
            </div>

            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="hidden"
              id="resume-upload"
            />

            <label
              htmlFor="resume-upload"
              className="cursor-pointer px-6 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors"
            >
              Browse Files
            </label>

            {file && (
              <div className="flex items-center gap-2 text-indigo-400 font-medium">
                <FileText size={18} />
                <span>{file.name}</span>
              </div>
            )}

            {error && (
              <div className="flex items-center gap-2 text-red-500 bg-red-500/10 px-4 py-2 rounded-lg">
                <AlertCircle size={18} />
                <span>{error}</span>
              </div>
            )}

            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className="mt-4 px-10 py-4 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-800 disabled:text-slate-500 rounded-2xl font-bold transition-all shadow-xl shadow-indigo-500/20 flex items-center gap-2"
            >
              {loading ? <Loader2 className="animate-spin" /> : <Target size={20} />}
              {loading ? 'Analyzing...' : 'Analyze Now'}
            </button>
          </div>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="grid md:grid-cols-2 gap-8"
        >
          <div className="bg-slate-900 p-8 rounded-3xl border border-white/5">
            <div className="flex justify-between items-center mb-8">
              <h3 className="text-2xl font-bold text-white">ATS Score</h3>
              <div className="text-4xl font-black text-indigo-500">{result.ats_score}%</div>
            </div>

            <div className="h-4 bg-slate-800 rounded-full overflow-hidden mb-8">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${result.ats_score}%` }}
                className="h-full bg-gradient-to-r from-indigo-500 to-purple-500"
              />
            </div>

            <div className="space-y-4">
              <h4 className="font-semibold text-slate-300">Matched Skills:</h4>
              <div className="flex flex-wrap gap-2">
                {result.matched_skills.map((skill, i) => (
                  <span key={i} className="px-3 py-1 bg-emerald-500/10 text-emerald-500 rounded-full text-sm border border-emerald-500/20">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="bg-slate-900 p-8 rounded-3xl border border-white/5 flex flex-col justify-center items-center text-center">
            <CheckCircle2 className="text-emerald-500 mb-6" size={64} />
            <h3 className="text-2xl font-bold mb-4">Ready for Mock Interview?</h3>
            <p className="text-slate-400 mb-8">We've parsed your resume and identified key technical areas. You can now start a tailored mock interview.</p>
            <button
              onClick={() => navigate('/interview')}
              className="w-full py-4 bg-white text-slate-900 rounded-2xl font-bold hover:bg-slate-200 transition-all"
            >
              Start Interview
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Upload;
