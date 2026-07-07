import { Navigate } from 'react-router-dom';

const ATSResults = () => {
  const data = localStorage.getItem('resume_data');
  if (!data) return <Navigate to="/upload" />;

  return (
    <div className="max-w-4xl mx-auto py-8">
      <h2 className="text-3xl font-bold mb-8 text-center">Your ATS Analysis</h2>
      {/* Reusing logic from Upload for simplicity in this MVP */}
      <div className="bg-slate-900 p-8 rounded-3xl border border-white/5">
        <p className="text-slate-400">Detailed ATS breakdown coming soon...</p>
      </div>
    </div>
  );
};

export default ATSResults;
