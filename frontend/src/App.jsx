import React, { useState, useEffect } from 'react';
import { 
  Sparkles, Calendar, User, Globe, Activity, Heart, 
  Compass, MessageSquare, Terminal, Eye, Download, 
  History, ChevronRight, FileText, Database, Layers, Clock, MapPin, Target, Hash
} from 'lucide-react';

export default function App() {
  // Method 1 Form State (Expanded)
  const [formData, setFormData] = useState({ 
    name: '', 
    dob: '', 
    birth_time: '', 
    birth_location: '', 
    age: '', 
    focus_area: 'Career & Life Purpose', 
    language: 'English' 
  });
  
  const [loading, setLoading] = useState(false);
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState('');
  const [downloading, setDownloading] = useState(false);
  const [showSources, setShowSources] = useState(false);

  // Method 2 Chat State
  const [chatInput, setChatInput] = useState('');
  const [chatLanguage, setChatLanguage] = useState('English');
  const [chatLog, setChatLog] = useState([]);
  const [chatLoading, setChatLoading] = useState(false);
  const [auditMode, setAuditMode] = useState(false);

  const [history, setHistory] = useState([]);

  const fetchHistory = async (fallbackItem = null) => {
    try {
      const response = await fetch('http://localhost:8000/api/profiles-history');
      if (response.ok) {
        const data = await response.json();
        if (data && data.length > 0) setHistory(data);
        else if (fallbackItem) setHistory([fallbackItem]);
      } else if (fallbackItem) setHistory([fallbackItem]);
    } catch (err) {
      if (fallbackItem) setHistory([fallbackItem]);
    }
  };

  useEffect(() => { fetchHistory(); }, []);

  const handleLanguageChange = (lang) => {
    setFormData(prev => ({ ...prev, language: lang }));
    setChatLanguage(lang);
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/energy-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error('Failed to generate profile reading.');
      const data = await response.json();
      setProfile(data);

      await fetchHistory({ name: formData.name || 'Anonymous', dob: formData.dob || 'Unspecified', language: formData.language });
    } catch (err) {
      setError(err.message || 'Error occurred while processing profile.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!formData.name) return;
    setDownloading(true);
    try {
      const url = `http://localhost:8000/api/download-blueprint?name=${encodeURIComponent(formData.name)}&dob=${encodeURIComponent(formData.dob)}&language=${encodeURIComponent(formData.language)}&focus_area=${encodeURIComponent(formData.focus_area)}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error('PDF compile failed.');
      
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', `Life_Blueprint_${formData.name.toLowerCase().replace(/\s+/g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      alert(`Download error: ${err.message}`);
    } finally {
      setDownloading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const userMsg = chatInput;
    setChatInput('');
    setChatLoading(true);
    setChatLog(prev => [...prev, { sender: 'user', text: userMsg, lang: chatLanguage }]);

    try {
      const response = await fetch('http://localhost:8000/api/chat-sandbox', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMsg,
          language: chatLanguage,
          context: profile ? JSON.stringify(formData) : "No context submitted."
        }),
      });

      if (!response.ok) throw new Error('Chat sandbox failed.');
      const data = await response.json();

      setChatLog(prev => [...prev, { sender: 'system', text: data.response, lang: chatLanguage }]);
    } catch (err) {
      setChatLog(prev => [...prev, { sender: 'system', text: `Error: ${err.message}`, lang: 'System' }]);
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans antialiased p-4 sm:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header */}
        <header className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <Compass className="text-indigo-400" size={28} />
            <h1 className="text-2xl font-bold tracking-tight">AURA <span className="text-indigo-400">ENERGY MATRIX</span></h1>
          </div>
          <div className="text-xs bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-full text-slate-400 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" /> Hybrid Form & Chat RAG Active
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          {/* Left Column: Form Controls (Method 1) */}
          <div className="lg:col-span-5 space-y-4">
            <div className="bg-slate-900/50 border border-slate-800 p-5 rounded-2xl shadow-xl">
              <h2 className="text-md font-bold mb-3 flex items-center gap-2 text-indigo-300">
                <Sparkles size={16} /> Method 1: Energy Inputs Form
              </h2>
              <form onSubmit={handleProfileSubmit} className="space-y-3">
                
                <div>
                  <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Full Name</label>
                  <div className="relative">
                    <User className="absolute left-3 top-2.5 text-slate-500" size={15} />
                    <input type="text" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2 pl-9 pr-3 text-xs text-white focus:outline-none focus:border-indigo-500" placeholder="Jane Doe" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Birth Date</label>
                    <div className="relative">
                      <Calendar className="absolute left-2.5 top-2.5 text-slate-500" size={14} />
                      <input type="date" value={formData.dob} onChange={e => setFormData({...formData, dob: e.target.value})}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2 pl-8 pr-2 text-xs text-white focus:outline-none focus:border-indigo-500" />
                    </div>
                  </div>

                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Birth Time</label>
                    <div className="relative">
                      <Clock className="absolute left-2.5 top-2.5 text-slate-500" size={14} />
                      <input type="time" value={formData.birth_time} onChange={e => setFormData({...formData, birth_time: e.target.value})}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2 pl-8 pr-2 text-xs text-white focus:outline-none focus:border-indigo-500" />
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Birth Location</label>
                    <div className="relative">
                      <MapPin className="absolute left-2.5 top-2.5 text-slate-500" size={14} />
                      <input type="text" value={formData.birth_location} onChange={e => setFormData({...formData, birth_location: e.target.value})}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2 pl-8 pr-2 text-xs text-white focus:outline-none focus:border-indigo-500" placeholder="City, Country" />
                    </div>
                  </div>

                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Age</label>
                    <div className="relative">
                      <Hash className="absolute left-2.5 top-2.5 text-slate-500" size={14} />
                      <input type="number" value={formData.age} onChange={e => setFormData({...formData, age: e.target.value})}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2 pl-8 pr-2 text-xs text-white focus:outline-none focus:border-indigo-500" placeholder="28" />
                    </div>
                  </div>
                </div>

                <div>
                  <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Focus Area</label>
                  <div className="relative">
                    <Target className="absolute left-3 top-2.5 text-slate-500" size={15} />
                    <select value={formData.focus_area} onChange={e => setFormData({...formData, focus_area: e.target.value})}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2 pl-9 pr-3 text-xs text-white focus:outline-none focus:border-indigo-500">
                      <option value="Career & Life Purpose">Career & Life Purpose</option>
                      <option value="Love & Relationships">Love & Relationships</option>
                      <option value="Personal Growth & Spiritual Path">Personal Growth & Spiritual Path</option>
                      <option value="Health & Energy Alignment">Health & Energy Alignment</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Output Language</label>
                  <div className="relative">
                    <Globe className="absolute left-3 top-2.5 text-slate-500" size={15} />
                    <select value={formData.language} onChange={e => handleLanguageChange(e.target.value)}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2 pl-9 pr-3 text-xs text-white focus:outline-none focus:border-indigo-500">
                      <option value="English">English</option>
                      <option value="Spanish">Español</option>
                      <option value="French">Français</option>
                      <option value="German">Deutsch</option>
                    </select>
                  </div>
                </div>

                <button type="submit" disabled={loading} className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-2.5 rounded-xl text-xs transition-all">
                  {loading ? "Calculating & Generating..." : "Generate Reading"}
                </button>
              </form>
              {error && <p className="text-red-400 text-xs mt-2">{error}</p>}
            </div>
          </div>

          {/* Right Column: Output Results */}
          <div className="lg:col-span-7">
            {!profile ? (
              <div className="border border-dashed border-slate-800 bg-slate-900/20 rounded-2xl h-full min-h-[380px] flex flex-col items-center justify-center p-6 text-center">
                <Activity size={32} className="text-slate-600 mb-2 animate-pulse" />
                <p className="text-slate-400 text-xs font-semibold">Awaiting Profile Generation or Query</p>
                <p className="text-slate-600 text-[11px] max-w-xs mt-1">Submit the inputs form on the left or type directly into the chat below. Incomplete data will be handled gracefully.</p>
              </div>
            ) : (
              <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-4">
                <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                  <h3 className="text-md font-bold text-amber-300 flex items-center gap-2">
                    <Heart size={16} /> Personalized Energy Reading
                  </h3>
                  <button onClick={handleDownloadPDF} disabled={downloading} className="bg-emerald-600/20 text-emerald-400 hover:bg-emerald-600 hover:text-white border border-emerald-500/30 px-3 py-1 rounded-xl text-xs font-bold transition-all">
                    {downloading ? "Exporting..." : "Export PDF"}
                  </button>
                </div>
                <div className="text-slate-300 text-xs sm:text-sm leading-relaxed whitespace-pre-line max-h-[420px] overflow-y-auto pr-2 custom-scrollbar">
                  {profile.interpretation}
                </div>
              </div>
            )}
          </div>

        </div>

        {/* Method 2 Chatbot Sandbox */}
        <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3">
          <div className="flex justify-between items-center border-b border-slate-800 pb-2">
            <h2 className="text-sm font-bold text-purple-400 flex items-center gap-2">
              <MessageSquare size={16} /> Method 2: Conversational Guidance Chatbot
            </h2>
            <span className="text-[10px] text-slate-500 font-mono">Target: {chatLanguage}</span>
          </div>

          <div className="bg-slate-950 border border-slate-800/80 rounded-xl h-48 p-3 overflow-y-auto space-y-3 custom-scrollbar">
            {chatLog.length === 0 ? (
              <p className="text-slate-600 text-xs text-center py-10 font-mono">Chatbot ready. Type your query or ask for a reading directly here...</p>
            ) : (
              chatLog.map((m, i) => (
                <div key={i} className={`p-2.5 rounded-xl max-w-[85%] text-xs ${m.sender === 'user' ? 'bg-indigo-600/20 text-indigo-200 ml-auto' : 'bg-slate-900 text-slate-300 border border-slate-800'}`}>
                  <p className="whitespace-pre-wrap">{m.text}</p>
                </div>
              ))
            )}
            {chatLoading && <p className="text-purple-400 text-xs animate-pulse font-mono">&gt; Analyzing query & extracting missing parameters...</p>}
          </div>

          <form onSubmit={handleSendMessage} className="flex gap-2">
            <input 
              type="text" 
              value={chatInput} 
              onChange={e => setChatInput(e.target.value)}
              placeholder="Ask a question or provide birth details naturally..." 
              className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500"
            />
            <button type="submit" disabled={chatLoading} className="bg-purple-600 hover:bg-purple-500 text-white font-bold px-4 py-2 rounded-xl text-xs transition-all">
              Send
            </button>
          </form>
        </div>

      </div>
    </div>
  );
}