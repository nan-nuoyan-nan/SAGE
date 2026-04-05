import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Globe, Mail, Lock } from "lucide-react";
import { useAuthStore } from "@/store/auth";

export default function Login() {
  const [isRegister, setIsRegister] = useState(false);
  const login = useAuthStore((state) => state.login);
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Simulate auth
    login({
      id: "user-" + Math.random().toString(36).substr(2, 9),
      email: "demo@example.com",
      name: isRegister ? "New User" : "Alex",
      targetLanguage: "Japanese",
      level: "Beginner",
      xp: isRegister ? 0 : 450,
    });
    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen bg-zinc-50 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background blobs */}
      <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-200/40 rounded-full blur-3xl"></div>
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-purple-200/40 rounded-full blur-3xl"></div>

      <div className="w-full max-w-md bg-white rounded-3xl shadow-xl shadow-zinc-200/50 p-8 relative z-10">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-indigo-100 text-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Globe className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-zinc-900">
            {isRegister ? "Create your account" : "Welcome back"}
          </h2>
          <p className="text-zinc-500 mt-2">
            {isRegister ? "Start your language journey today." : "Continue your language journey."}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {isRegister && (
            <div>
              <label className="block text-sm font-medium text-zinc-700 mb-1">Name</label>
              <div className="relative">
                <input 
                  type="text" 
                  required 
                  className="w-full pl-10 pr-4 py-3 rounded-xl border border-zinc-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all"
                  placeholder="John Doe"
                />
                <Mail className="absolute left-3 top-3.5 w-5 h-5 text-zinc-400" />
              </div>
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-zinc-700 mb-1">Email</label>
            <div className="relative">
              <input 
                type="email" 
                required 
                className="w-full pl-10 pr-4 py-3 rounded-xl border border-zinc-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all"
                placeholder="you@example.com"
              />
              <Mail className="absolute left-3 top-3.5 w-5 h-5 text-zinc-400" />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-700 mb-1">Password</label>
            <div className="relative">
              <input 
                type="password" 
                required 
                className="w-full pl-10 pr-4 py-3 rounded-xl border border-zinc-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all"
                placeholder="••••••••"
              />
              <Lock className="absolute left-3 top-3.5 w-5 h-5 text-zinc-400" />
            </div>
          </div>

          <button 
            type="submit"
            className="w-full bg-indigo-600 text-white font-bold py-3 rounded-xl hover:bg-indigo-700 transition-colors mt-6 shadow-md shadow-indigo-200"
          >
            {isRegister ? "Sign Up" : "Log In"}
          </button>
        </form>

        <div className="mt-8 text-center text-sm text-zinc-600">
          {isRegister ? "Already have an account?" : "Don't have an account?"}
          <button 
            onClick={() => setIsRegister(!isRegister)}
            className="ml-2 font-bold text-indigo-600 hover:text-indigo-700"
          >
            {isRegister ? "Log in" : "Sign up"}
          </button>
        </div>
      </div>
    </div>
  );
}
