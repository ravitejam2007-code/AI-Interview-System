import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Loader2, TrendingUp, CheckCircle, Target } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const StatCard = ({ title, value, icon: Icon, colorClass, delay }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay }}
    className="bg-slate-900 p-8 rounded-3xl border border-white/5 flex items-start justify-between group hover:border-white/10 transition-all"
  >
    <div>
      <h3 className="text-slate-400 mb-2 font-medium">{title}</h3>
      <div className={`text-4xl font-black ${colorClass}`}>{value}</div>
    </div>
    <div className={`p-4 rounded-2xl ${colorClass.replace('text-', 'bg-').replace('-500', '-500/10')} group-hover:scale-110 transition-transform`}>
      <Icon className={colorClass} size={24} />
    </div>
  </motion.div>
);

const Dashboard = () => {
  const { token } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/v1/analytics/dashboard', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (!response.ok) throw new Error('Failed to load dashboard data');
        
        const result = await response.json();
        setData(result.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [token]);

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
      <Loader2 className="animate-spin text-indigo-500" size={48} />
      <p className="text-slate-400 font-medium">Loading your analytics...</p>
    </div>
  );

  if (error) return (
    <div className="text-center py-12">
      <div className="inline-block bg-red-500/10 text-red-500 px-6 py-4 rounded-2xl border border-red-500/20">
        {error}
      </div>
    </div>
  );

  // Formatting chart data for Recharts
  const chartData = data?.trends?.ats?.map((item, index) => ({
    date: item.date,
    ATS: item.score,
    Confidence: data.trends.confidence[index]?.score || 0,
    Technical: data.trends.technical[index]?.score || 0,
  })) || [];

  return (
    <div className="max-w-7xl mx-auto py-8">
      <div className="mb-12">
        <h2 className="text-4xl font-bold mb-2">Performance Dashboard</h2>
        <p className="text-slate-400">Track your interview readiness over time</p>
      </div>

      <div className="grid md:grid-cols-3 gap-8 mb-12">
        <StatCard 
          title="Total Interviews" 
          value={data?.total_interviews || 0} 
          icon={Target} 
          colorClass="text-indigo-500"
          delay={0.1}
        />
        <StatCard 
          title="Avg. ATS Score" 
          value={`${Math.round(data?.average_ats || 0)}%`} 
          icon={TrendingUp} 
          colorClass="text-emerald-500"
          delay={0.2}
        />
        <StatCard 
          title="Latest Confidence" 
          value={`${data?.trends?.confidence?.slice(-1)[0]?.score || 0}%`} 
          icon={CheckCircle} 
          colorClass="text-purple-500"
          delay={0.3}
        />
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          className="lg:col-span-2 bg-slate-900 p-8 rounded-3xl border border-white/5"
        >
          <h3 className="text-2xl font-bold mb-8">Progress Trends</h3>
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="date" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                  itemStyle={{ fontWeight: 'bold' }}
                />
                <Legend wrapperStyle={{ paddingTop: '20px' }}/>
                <Line type="monotone" dataKey="ATS" stroke="#10b981" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 8 }} />
                <Line type="monotone" dataKey="Confidence" stroke="#a855f7" strokeWidth={3} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="Technical" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-slate-900 p-8 rounded-3xl border border-white/5 flex flex-col"
        >
          <h3 className="text-2xl font-bold mb-6">Recent Insights</h3>
          <div className="flex-1 space-y-6 overflow-y-auto pr-2">
            {data?.recent_feedback?.map((feedback, idx) => (
              <div key={idx} className="flex gap-4">
                <div className="w-8 h-8 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center shrink-0 font-bold">
                  {idx + 1}
                </div>
                <p className="text-slate-300 leading-relaxed text-sm">
                  {feedback}
                </p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;
