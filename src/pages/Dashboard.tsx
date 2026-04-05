import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuthStore } from "@/store/auth";
import { Flame, Trophy, Brain, ArrowRight, Play } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
  { name: 'Mon', xp: 120 },
  { name: 'Tue', xp: 200 },
  { name: 'Wed', xp: 150 },
  { name: 'Thu', xp: 80 },
  { name: 'Fri', xp: 220 },
  { name: 'Sat', xp: 300 },
  { name: 'Sun', xp: 450 },
];

export default function Dashboard() {
  const user = useAuthStore((state) => state.user);

  const stats = [
    { label: "Current Streak", value: "7 Days", icon: <Flame className="text-orange-500" size={24} />, bg: "bg-orange-100" },
    { label: "Total XP", value: user?.xp.toString() || "0", icon: <Trophy className="text-yellow-500" size={24} />, bg: "bg-yellow-100" },
    { label: "Words Learned", value: "342", icon: <Brain className="text-purple-500" size={24} />, bg: "bg-purple-100" },
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-zinc-900">Welcome back, {user?.name}! 👋</h1>
        <p className="text-zinc-500 mt-2 text-lg">You're making great progress in {user?.targetLanguage}. Keep it up!</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat, idx) => (
          <motion.div 
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="bg-white p-6 rounded-3xl border border-zinc-100 shadow-sm flex items-center gap-5"
          >
            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center ${stat.bg}`}>
              {stat.icon}
            </div>
            <div>
              <p className="text-sm font-medium text-zinc-500">{stat.label}</p>
              <p className="text-2xl font-bold text-zinc-900">{stat.value}</p>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content Area */}
        <div className="lg:col-span-2 space-y-8">
          {/* Next Lesson Recommendation */}
          <div className="bg-gradient-to-br from-indigo-600 to-purple-600 rounded-3xl p-8 text-white shadow-xl shadow-indigo-200 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3"></div>
            
            <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
              <div>
                <span className="inline-block px-3 py-1 bg-white/20 rounded-full text-sm font-semibold mb-4 backdrop-blur-md">
                  Recommended Next Step
                </span>
                <h2 className="text-3xl font-bold mb-2">Unit 4: Ordering Food</h2>
                <p className="text-indigo-100 max-w-md">Practice essential vocabulary and grammar for dining out in Tokyo. Includes oral shadowing exercises.</p>
              </div>
              <Link 
                to="/courses/unit-4"
                className="flex items-center gap-2 bg-white text-indigo-600 px-6 py-3 rounded-xl font-bold hover:bg-indigo-50 transition-colors shrink-0"
              >
                <Play size={20} fill="currentColor" />
                Start Lesson
              </Link>
            </div>
          </div>

          {/* Activity Chart */}
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-zinc-100 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-zinc-900">Activity Overview</h3>
              <span className="text-sm font-medium text-zinc-500 bg-zinc-100 px-3 py-1 rounded-full">This Week</span>
            </div>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                  <XAxis dataKey="name" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip 
                    contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Line type="monotone" dataKey="xp" stroke="#4f46e5" strokeWidth={4} dot={{ r: 6, fill: "#4f46e5", strokeWidth: 2, stroke: "#fff" }} activeDot={{ r: 8 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Sidebar / Path */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-3xl border border-zinc-100 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-bold text-zinc-900">Your Path</h3>
              <Link to="/courses" className="text-sm font-semibold text-indigo-600 hover:text-indigo-700 flex items-center gap-1">
                View all <ArrowRight size={16} />
              </Link>
            </div>

            <div className="space-y-6 relative before:absolute before:inset-0 before:ml-[1.4rem] before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-zinc-200 before:to-transparent">
              {/* Path items */}
              {[
                { title: "Unit 1: Basics", status: "completed", xp: 100 },
                { title: "Unit 2: Greetings", status: "completed", xp: 150 },
                { title: "Unit 3: Numbers", status: "completed", xp: 200 },
                { title: "Unit 4: Ordering Food", status: "current", xp: 0 },
                { title: "Unit 5: Directions", status: "locked", xp: 0 },
              ].map((item, i) => (
                <div key={i} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                  <div className={`flex items-center justify-center w-11 h-11 rounded-full border-4 border-white shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 ${
                    item.status === 'completed' ? 'bg-green-500' :
                    item.status === 'current' ? 'bg-indigo-600' : 'bg-zinc-200'
                  }`}>
                    {item.status === 'completed' ? <span className="text-white font-bold">✓</span> : 
                     item.status === 'current' ? <span className="w-3 h-3 bg-white rounded-full"></span> : 
                     <Lock size={16} className="text-zinc-400" />}
                  </div>
                  
                  <div className="w-[calc(100%-4rem)] md:w-[calc(50%-3rem)] p-4 rounded-2xl bg-zinc-50 border border-zinc-100">
                    <h4 className={`font-bold ${item.status === 'locked' ? 'text-zinc-400' : 'text-zinc-900'}`}>{item.title}</h4>
                    {item.status === 'completed' && <p className="text-sm text-green-600 font-medium">+{item.xp} XP Earned</p>}
                    {item.status === 'current' && <p className="text-sm text-indigo-600 font-medium">In Progress</p>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Lock Icon inline
function Lock(props: any) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    </svg>
  );
}
