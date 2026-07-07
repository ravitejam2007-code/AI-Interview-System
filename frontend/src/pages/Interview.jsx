import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, Send, Bot, User, Loader2, CheckCircle, AlertCircle, Sparkles, Target } from 'lucide-react';
import { generateQuestions, evaluateAnswer } from '../services/api';
import { useAuth } from '../context/AuthContext';

const Interview = () => {
  const { token } = useAuth();
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  const [lastEvaluation, setLastEvaluation] = useState(null);
  const [scoreHistory, setScoreHistory] = useState([]);

  const speak = useCallback((text) => {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    synth.speak(utterance);
  }, []);

  useEffect(() => {
    const fetchQuestions = async () => {
      const resumeData = JSON.parse(localStorage.getItem('resume_data') || '{}');
      try {
        const response = await generateQuestions(
          resumeData.matched_skills || ["python", "machine learning", "sql", "react"],
          resumeData.text || "Technical skills: Python, Machine Learning, SQL, React"
        );
        const qList = response.data.questions.split('\n').filter(q => q.trim());
        setQuestions(qList);
        setChat([{ role: 'ai', text: qList[0] }]);
        speak(qList[0]);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [speak]);

  const handleSend = async () => {
    if (!answer.trim()) return;

    const currentQuestion = questions[currentIndex];
    const userAnswer = answer;
    const resumeData = JSON.parse(localStorage.getItem('resume_data') || '{}');

    const newChat = [...chat, { role: 'user', text: userAnswer }];
    setChat(newChat);
    setAnswer('');
    setEvaluating(true);

    try {
      const evalResponse = await evaluateAnswer(currentQuestion, userAnswer, resumeData.text || '', token);
      const evalData = evalResponse.data;
      setLastEvaluation(evalData);
      setScoreHistory(prev => [...prev, { technical: evalData.technical_score, confidence: evalData.confidence_score }]);
      
      setChat(prev => [...prev, { 
        role: 'ai', 
        text: `**Feedback:** ${evalData.feedback}\n\n**Technical Score:** ${evalData.technical_score}/100 | **Confidence Score:** ${evalData.confidence_score}/100`,
        isFeedback: true
      }]);

      if (currentIndex < questions.length - 1) {
        setTimeout(() => {
          const nextQ = questions[currentIndex + 1];
          setChat(prev => [...prev, { role: 'ai', text: nextQ }]);
          setCurrentIndex(currentIndex + 1);
          setLastEvaluation(null);
          speak(nextQ);
        }, 2000);
      } else {
        setTimeout(() => {
          setChat(prev => [...prev, { role: 'ai', text: "Interview completed! Great job. You can see your feedback in the dashboard." }]);
        }, 2000);
      }
    } catch (err) {
      console.error(err);
      setChat(prev => [...prev, { role: 'ai', text: "Couldn't evaluate your answer. Moving to next question..." }]);
      if (currentIndex < questions.length - 1) {
        setTimeout(() => {
          const nextQ = questions[currentIndex + 1];
          setChat(prev => [...prev, { role: 'ai', text: nextQ }]);
          setCurrentIndex(currentIndex + 1);
          speak(nextQ);
        }, 1000);
      }
    } finally {
      setEvaluating(false);
    }
  };

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
      <Loader2 className="animate-spin text-indigo-500" size={48} />
      <p className="text-slate-400 font-medium">Generating your interview session...</p>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto py-4 sm:py-8 px-4">
      <div className="bg-slate-900 rounded-3xl border border-white/5 overflow-hidden flex flex-col h-[75vh] sm:h-[70vh]">
        {/* Header */}
        <div className="p-4 sm:p-6 border-b border-white/5 bg-slate-800/50 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${isSpeaking ? 'bg-emerald-500 animate-pulse' : 'bg-slate-600'}`} />
            <h3 className="font-bold text-sm sm:text-base">Technical Interview Session</h3>
          </div>
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-6">
            <div className="text-xs sm:text-sm text-slate-500">Question {currentIndex + 1} of {questions.length}</div>
            {scoreHistory.length > 0 && (
              <div className="flex gap-4 text-xs sm:text-sm">
                <span className="flex items-center gap-1 text-emerald-400">
                  <Target size={12} />
                  Tech: {Math.round(scoreHistory.reduce((a, b) => a + b.technical, 0) / scoreHistory.length)}
                </span>
                <span className="flex items-center gap-1 text-purple-400">
                  <Sparkles size={12} />
                  Conf: {Math.round(scoreHistory.reduce((a, b) => a + b.confidence, 0) / scoreHistory.length)}
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 sm:space-y-6">
          <AnimatePresence>
            {chat.map((msg, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: msg.role === 'ai' ? -20 : 20 }}
                animate={{ opacity: 1, x: 0 }}
                className={`flex ${msg.role === 'ai' ? 'justify-start' : 'justify-end'}`}
              >
                <div className={`flex gap-2 sm:gap-3 max-w-[90%] sm:max-w-[80%] ${msg.role === 'ai' ? 'flex-row' : 'flex-row-reverse'}`}>
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'ai' ? 'bg-indigo-600' : 'bg-slate-700'}`}>
                    {msg.role === 'ai' ? (msg.isFeedback ? <Sparkles size={16} className="text-amber-400" /> : <Bot size={16} />) : <User size={16} />}
                  </div>
                  <div className={`p-3 sm:p-4 rounded-2xl text-sm sm:text-base ${msg.isFeedback 
                    ? 'bg-amber-500/10 border border-amber-500/20 rounded-2xl' 
                    : msg.role === 'ai' ? 'bg-slate-800 rounded-tl-none' : 'bg-indigo-600 rounded-tr-none text-white'}`}>
                    <p className="leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        {/* Input Area */}
        <div className="p-4 sm:p-6 bg-slate-800/30 border-t border-white/5">
          <div className="relative">
            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder={evaluating ? "Evaluating your answer..." : "Type your answer here..."}
              disabled={evaluating}
              className="w-full bg-slate-900 border border-white/10 rounded-2xl p-3 sm:p-4 pr-12 sm:pr-14 focus:outline-none focus:border-indigo-500 transition-all resize-none h-20 sm:h-24 text-sm sm:text-base disabled:opacity-50"
            />
            <button
              onClick={handleSend}
              disabled={!answer.trim() || evaluating}
              className="absolute bottom-3 sm:bottom-4 right-3 sm:right-4 p-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-700 disabled:cursor-not-allowed rounded-xl transition-all text-white"
            >
              {evaluating ? <Loader2 className="animate-spin" size={18} /> : <Send size={18} />}
            </button>
          </div>
          <div className="mt-3 sm:mt-4 flex flex-col sm:flex-row gap-3 justify-between items-center">
            <button className="flex items-center gap-2 text-slate-500 hover:text-white transition-colors text-xs sm:text-sm" disabled={evaluating}>
              <Mic size={16} /> Use Voice Instead (Beta)
            </button>
            {evaluating && (
              <div className="flex items-center gap-2 text-amber-400 text-xs sm:text-sm">
                <Loader2 className="animate-spin" size={14} />
                Evaluating your answer...
              </div>
            )}
            {!evaluating && <p className="text-xs text-slate-600 hidden sm:block">Press Enter to send</p>}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Interview;
