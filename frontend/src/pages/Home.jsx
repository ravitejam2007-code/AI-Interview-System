import { motion } from 'framer-motion';
import { ArrowRight, Cpu, LineChart, ShieldCheck } from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="py-12 px-6 flex flex-col items-center gap-24 max-w-7xl mx-auto">
      {/* Hero Section */}
      <section className="text-center max-w-screen-xl mx-auto px-4 sm:px-6">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-6xl md:text-8xl font-extrabold mb-6 tracking-tight"
        >
          Master Your Next <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500">AI Interview</span>
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-xl text-slate-400 mb-10 leading-relaxed"
        >
          An all-in-one preparation system that analyzes your resume, calculates your ATS score,
          and generates personalized mock interviews with real-time feedback.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          <Link to="/upload" className="px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl font-bold flex items-center gap-2 transition-all hover:scale-105 shadow-xl shadow-indigo-500/20">
            Get Started <ArrowRight size={20} />
          </Link>
          <button className="px-8 py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-2xl font-bold transition-all border border-white/10">
            Learn More
          </button>
        </motion.div>
      </section>

      {/* Features Grid */}
      <section className="grid md:grid-cols-3 gap-12 w-full">
        {[
          {
            title: "ATS Optimizer",
            desc: "Upload your resume and get a detailed score based on target job roles and keywords.",
            icon: LineChart,
            color: "text-blue-500"
          },
          {
            title: "AI Interviewer",
            desc: "Practice with custom questions generated specifically from your professional experience.",
            icon: Cpu,
            color: "text-purple-500"
          },
          {
            title: "Instant Feedback",
            desc: "Receive actionable insights on your answers, confidence, and technical accuracy.",
            icon: ShieldCheck,
            color: "text-emerald-500"
          }
        ].map((feature, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.1 + 0.3 }}
            className="p-8 rounded-3xl bg-slate-900 border border-white/5 hover:border-white/10 transition-all hover:shadow-2xl group"
          >
            <feature.icon className={`${feature.color} mb-6 group-hover:scale-110 transition-transform`} size={32} />
            <h3 className="text-2xl font-bold mb-3">{feature.title}</h3>
            <p className="text-slate-400 leading-relaxed">{feature.desc}</p>
          </motion.div>
        ))}
      </section>
    </div>
  );
};

export default Home;
