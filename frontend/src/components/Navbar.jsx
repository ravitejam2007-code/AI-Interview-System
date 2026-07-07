import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Bot, FileText, LayoutDashboard, MessageSquare, Menu, X, LogOut, LogIn, Settings as SettingsIcon } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
    setIsMenuOpen(false);
  };

  const NavLinks = () => (
    <>
      <Link to="/upload" onClick={() => setIsMenuOpen(false)} className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
        <FileText size={18} />
        <span>Resume</span>
      </Link>
      <Link to="/interview" onClick={() => setIsMenuOpen(false)} className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
        <MessageSquare size={18} />
        <span>Mock Interview</span>
      </Link>
      <Link to="/feedback" onClick={() => setIsMenuOpen(false)} className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
        <LayoutDashboard size={18} />
        <span>Dashboard</span>
      </Link>
    </>
  );

  return (
    <nav className="border-b border-white/10 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 group">
          <div className="w-10 h-10 bg-indigo-600 rounded-lg flex items-center justify-center group-hover:rotate-12 transition-transform">
            <Bot className="text-white" size={24} />
          </div>
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
            AI Interviewer
          </span>
        </Link>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center gap-6">
          {user && <NavLinks />}
          {user ? (
            <div className="flex items-center gap-3 ml-4 border-l border-white/10 pl-4">
              <Link to="/settings" className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
                <SettingsIcon size={18} />
                <span>Settings</span>
              </Link>
              <button onClick={handleLogout} className="flex items-center gap-2 text-slate-400 hover:text-red-400 transition-colors">
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            </div>
          ) : (
            <Link to="/login" className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors font-medium">
              <LogIn size={18} />
              <span>Sign In</span>
            </Link>
          )}
        </div>

        {/* Mobile Menu Toggle */}
        <button 
          className="md:hidden text-slate-400 hover:text-white"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Nav */}
      {isMenuOpen && (
        <div className="md:hidden border-t border-white/10 bg-slate-900 absolute top-16 left-0 w-full px-4 py-4 flex flex-col gap-4 shadow-xl">
          {user && <NavLinks />}
          {user ? (
            <>
              <Link to="/settings" onClick={() => setIsMenuOpen(false)} className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
                <SettingsIcon size={18} />
                <span>Settings</span>
              </Link>
              <button onClick={handleLogout} className="flex items-center gap-2 text-red-400 hover:text-red-300 transition-colors mt-2 pt-4 border-t border-white/10">
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            </>
          ) : (
            <Link to="/login" onClick={() => setIsMenuOpen(false)} className="flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-3 rounded-lg transition-colors font-medium mt-2">
              <LogIn size={18} />
              <span>Sign In / Register</span>
            </Link>
          )}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
