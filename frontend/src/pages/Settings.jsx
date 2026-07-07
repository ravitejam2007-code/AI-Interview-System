import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { Save, Key, User, Image, Cpu, RefreshCw, CheckCircle, XCircle, ExternalLink, Loader2 } from 'lucide-react';

const Settings = () => {
  const { token, user: authUser, login } = useAuth();
  const [user, setUser] = useState(null);
  const [name, setName] = useState('');
  const [avatar, setAvatar] = useState('');
  const [openrouterApiKey, setOpenrouterApiKey] = useState('');
  const [openrouterBaseUrl, setOpenrouterBaseUrl] = useState('https://openrouter.ai/api/v1');
  const [selectedModel, setSelectedModel] = useState('');
  const [freeModels, setFreeModels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [fetchingModels, setFetchingModels] = useState(false);
  const [testingKey, setTestingKey] = useState(false);
  const [keyValid, setKeyValid] = useState(null);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [avatarPreview, setAvatarPreview] = useState('');
  const fileInputRef = useRef(null);

  useEffect(() => {
    if (token) {
      fetchSettings();
    }
  }, [token]);

  const fetchSettings = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/v1/settings/settings', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Failed to load settings');
      const data = await res.json();
      setUser(data.user);
      setName(data.user.name || '');
      setAvatar(data.user.avatar || '');
      setAvatarPreview(data.user.avatar || '');
      setOpenrouterApiKey(data.user.openrouter_api_key || '');
      setOpenrouterBaseUrl(data.user.openrouter_base_url || 'https://openrouter.ai/api/v1');
      setSelectedModel(data.user.selected_model || '');
    } catch (err) {
      setMessage({ type: 'error', text: err.message });
    } finally {
      setLoading(false);
    }
  };

  const fetchFreeModels = async () => {
    if (!openrouterApiKey) {
      setMessage({ type: 'error', text: 'Please enter an API key first' });
      return;
    }
    setFetchingModels(true);
    setMessage({ type: '', text: '' });
    try {
      const res = await fetch('http://localhost:5000/api/v1/settings/settings/models', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          api_key: openrouterApiKey,
          base_url: openrouterBaseUrl
        })
      });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || 'Failed to fetch models');
      }
      const data = await res.json();
      setFreeModels(data.models || []);
      if (data.models.length === 0) {
        setMessage({ type: 'info', text: 'No free models available for this API key. Check your OpenRouter account.' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: err.message });
    } finally {
      setFetchingModels(false);
    }
  };

  const testApiKey = async () => {
    if (!openrouterApiKey) {
      setKeyValid(null);
      return;
    }
    setTestingKey(true);
    setKeyValid(null);
    try {
      const res = await fetch('http://localhost:5000/api/v1/settings/settings/test-key', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ api_key: openrouterApiKey, base_url: openrouterBaseUrl })
      });
      const data = await res.json();
      setKeyValid(data.valid);
    } catch {
      setKeyValid(false);
    } finally {
      setTestingKey(false);
    }
  };

  useEffect(() => {
    if (openrouterApiKey) {
      const timer = setTimeout(() => testApiKey(), 500);
      return () => clearTimeout(timer);
    } else {
      setKeyValid(null);
    }
  }, [openrouterApiKey]);

  const handleAvatarUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onloadend = () => {
      setAvatarPreview(reader.result);
      setAvatar(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage({ type: '', text: '' });
    try {
      const res = await fetch('http://localhost:5000/api/v1/settings/settings', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name,
          avatar,
          openrouter_api_key: openrouterApiKey,
          openrouter_base_url: openrouterBaseUrl,
          selected_model: selectedModel
        })
      });
      if (!res.ok) throw new Error('Failed to save settings');
      const data = await res.json();
      setUser(data.user);
      login(data.user, token);
      setMessage({ type: 'success', text: 'Settings saved successfully' });
      setTimeout(() => setMessage({ type: '', text: '' }), 3000);
    } catch (err) {
      setMessage({ type: 'error', text: err.message });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
        <Loader2 className="animate-spin text-indigo-500" size={48} />
        <p className="text-slate-400 font-medium">Loading settings...</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <div className="mb-10">
        <h2 className="text-4xl font-bold mb-2">Settings</h2>
        <p className="text-slate-400">Configure your profile and AI model preferences</p>
      </div>

      {message.text && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className={`mb-8 p-4 rounded-2xl border flex items-center gap-3 ${
            message.type === 'error'
              ? 'bg-red-500/10 border-red-500/20 text-red-400'
              : message.type === 'success'
              ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
              : 'bg-blue-500/10 border-blue-500/20 text-blue-400'
          }`}
        >
          {message.type === 'error' ? <XCircle size={20} /> : message.type === 'success' ? <CheckCircle size={20} /> : null}
          {message.text}
        </motion.div>
      )}

      <div className="space-y-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-slate-900 p-8 rounded-3xl border border-white/5"
        >
          <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
            <User className="text-indigo-400" size={24} />
            Profile
          </h3>

          <div className="flex flex-col md:flex-row gap-8 items-start">
            <div className="flex flex-col items-center gap-4">
              <div className="relative group">
                <div className="w-28 h-28 rounded-full bg-slate-800 border-2 border-slate-700 overflow-hidden flex items-center justify-center">
                  {avatarPreview ? (
                    <img src={avatarPreview} alt="Avatar" className="w-full h-full object-cover" />
                  ) : (
                    <User size={48} className="text-slate-500" />
                  )}
                </div>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="absolute inset-0 rounded-full bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
                >
                  <Image size={24} className="text-white" />
                </button>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleAvatarUpload}
                  className="hidden"
                />
              </div>
              <span className="text-xs text-slate-500">Click to upload</span>
            </div>

            <div className="flex-1 space-y-5 w-full">
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-2">Username</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  placeholder="Enter your name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-2">Email</label>
                <input
                  type="email"
                  value={user?.email || ''}
                  disabled
                  className="w-full bg-slate-800/50 border border-slate-700 rounded-xl px-4 py-3 text-slate-400 cursor-not-allowed"
                />
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-slate-900 p-8 rounded-3xl border border-white/5"
        >
          <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
            <Key className="text-amber-400" size={24} />
            OpenRouter Configuration
          </h3>

          <div className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-2">
                Base URL
              </label>
              <input
                type="text"
                value={openrouterBaseUrl}
                onChange={(e) => setOpenrouterBaseUrl(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                placeholder="https://openrouter.ai/api/v1"
              />
              <p className="text-xs text-slate-500 mt-1 flex items-center gap-1">
                <ExternalLink size={12} />
                <a href="https://openrouter.ai/keys" target="_blank" rel="noopener noreferrer" className="hover:text-indigo-400 transition-colors">
                  Generate API key on OpenRouter
                </a>
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-400 mb-2">
                API Key
              </label>
              <div className="relative">
                <input
                  type="password"
                  value={openrouterApiKey}
                  onChange={(e) => setOpenrouterApiKey(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all pr-12"
                  placeholder="sk-or-v1-..."
                />
                <div className="absolute right-4 top-1/2 -translate-y-1/2">
                  {testingKey ? (
                    <Loader2 size={20} className="animate-spin text-slate-400" />
                  ) : keyValid === true ? (
                    <CheckCircle size={20} className="text-emerald-400" />
                  ) : keyValid === false ? (
                    <XCircle size={20} className="text-red-400" />
                  ) : null}
                </div>
              </div>
              <p className="text-xs text-slate-500 mt-1">Key will be validated automatically</p>
            </div>

            <div className="flex items-center gap-4">
              <button
                onClick={fetchFreeModels}
                disabled={fetchingModels || !openrouterApiKey}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-800 disabled:text-slate-500 text-white px-6 py-3 rounded-xl transition-all font-medium"
              >
                {fetchingModels ? (
                  <Loader2 size={18} className="animate-spin" />
                ) : (
                  <RefreshCw size={18} />
                )}
                Fetch Available Models
              </button>
            </div>

            {freeModels.length > 0 && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="mt-4"
              >
                <label className="block text-sm font-medium text-slate-400 mb-3">
                  <Cpu className="inline mr-2" size={16} />
                  Select AI Model
                </label>
                <div className="grid gap-3 max-h-80 overflow-y-auto pr-2">
                  {freeModels.map((model) => (
                    <label
                      key={model.id}
                      className={`flex items-start gap-4 p-4 rounded-xl border cursor-pointer transition-all ${
                        selectedModel === model.id
                          ? 'border-indigo-500 bg-indigo-500/10'
                          : 'border-slate-700 bg-slate-800/50 hover:border-slate-600'
                      }`}
                    >
                      <input
                        type="radio"
                        name="model"
                        value={model.id}
                        checked={selectedModel === model.id}
                        onChange={(e) => setSelectedModel(e.target.value)}
                        className="mt-1 accent-indigo-500"
                      />
                      <div className="flex-1">
                        <div className="font-medium text-white">{model.name || model.id}</div>
                        <div className="text-sm text-slate-400 mt-1 line-clamp-2">{model.description}</div>
                        {model.context_length > 0 && (
                          <div className="text-xs text-slate-500 mt-2">
                            Context: {(model.context_length / 1024).toFixed(0)}K tokens
                          </div>
                        )}
                      </div>
                    </label>
                  ))}
                </div>
              </motion.div>
            )}
          </div>
        </motion.div>

        <div className="flex justify-end">
          <button
            onClick={handleSave}
            disabled={saving}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-800 disabled:text-slate-500 text-white px-8 py-3 rounded-xl transition-all font-medium text-lg"
          >
            {saving ? (
              <Loader2 size={20} className="animate-spin" />
            ) : (
              <Save size={20} />
            )}
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;