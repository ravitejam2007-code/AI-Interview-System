import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import Upload from './pages/Upload';
import ATSResults from './pages/ATSResults';
import Interview from './pages/Interview';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import Settings from './pages/Settings';
import Navbar from './components/Navbar';
import PrivateRoute from './components/PrivateRoute';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-slate-950 text-slate-200">
          <Navbar />
          <main className="responsive-wrapper mx-auto py-8 relative">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              
              {/* Protected Routes */}
              <Route path="/upload" element={<PrivateRoute><Upload /></PrivateRoute>} />
              <Route path="/ats" element={<PrivateRoute><ATSResults /></PrivateRoute>} />
              <Route path="/interview" element={<PrivateRoute><Interview /></PrivateRoute>} />
              <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
              <Route path="/settings" element={<PrivateRoute><Settings /></PrivateRoute>} />
              
              {/* Legacy fallback */}
              <Route path="/feedback" element={<Navigate to="/dashboard" replace />} />
            </Routes>
            
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
