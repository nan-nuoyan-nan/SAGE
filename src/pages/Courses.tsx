import { Link } from "react-router-dom";
import { BookOpen, Headphones, Mic, Search, Filter } from "lucide-react";
import { useAuthStore } from "@/store/auth";

export default function Courses() {
  const user = useAuthStore((state) => state.user);

  const categories = [
    { id: "all", label: "All Modules" },
    { id: "vocab", label: "Vocabulary" },
    { id: "grammar", label: "Grammar" },
    { id: "listening", label: "Listening" },
    { id: "oral", label: "Oral Shadowing" },
  ];

  const courses = [
    { id: "unit-1-vocab", title: "Essential Nouns", category: "vocab", level: "Beginner", icon: <BookOpen className="text-blue-500" />, color: "bg-blue-100" },
    { id: "unit-2-grammar", title: "Present Tense Verbs", category: "grammar", level: "Beginner", icon: <BookOpen className="text-indigo-500" />, color: "bg-indigo-100" },
    { id: "unit-3-listening", title: "Daily Conversations", category: "listening", level: "Intermediate", icon: <Headphones className="text-purple-500" />, color: "bg-purple-100" },
    { id: "unit-4-oral", title: "Ordering Food (Shadowing)", category: "oral", level: "Beginner", icon: <Mic className="text-pink-500" />, color: "bg-pink-100" },
    { id: "unit-5-listening", title: "News Broadcast", category: "listening", level: "Advanced", icon: <Headphones className="text-purple-500" />, color: "bg-purple-100" },
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-zinc-900">Course Library</h1>
          <p className="text-zinc-500 mt-2">Explore modules tailored to your {user?.targetLanguage} learning journey.</p>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="relative">
            <input 
              type="text" 
              placeholder="Search courses..." 
              className="pl-10 pr-4 py-2.5 bg-white border border-zinc-200 rounded-full text-sm focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 w-64"
            />
            <Search size={18} className="absolute left-4 top-3 text-zinc-400" />
          </div>
          <button className="p-2.5 bg-white border border-zinc-200 rounded-full hover:bg-zinc-50 text-zinc-600 transition-colors">
            <Filter size={18} />
          </button>
        </div>
      </div>

      {/* Categories */}
      <div className="flex flex-wrap gap-3">
        {categories.map((cat, idx) => (
          <button 
            key={cat.id}
            className={`px-5 py-2 rounded-full text-sm font-semibold transition-colors ${
              idx === 0 ? "bg-zinc-900 text-white" : "bg-white border border-zinc-200 text-zinc-600 hover:border-zinc-300 hover:bg-zinc-50"
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Course Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {courses.map((course) => (
          <Link 
            key={course.id}
            to={`/courses/${course.id}`}
            className="bg-white rounded-3xl p-6 border border-zinc-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group"
          >
            <div className="flex items-start justify-between mb-4">
              <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${course.color} group-hover:scale-110 transition-transform`}>
                {course.icon}
              </div>
              <span className="px-3 py-1 bg-zinc-100 text-zinc-600 text-xs font-bold rounded-full uppercase tracking-wide">
                {course.level}
              </span>
            </div>
            
            <h3 className="text-xl font-bold text-zinc-900 mb-2">{course.title}</h3>
            <p className="text-sm text-zinc-500 mb-6">Master this specific skill to earn XP and progress to the next level.</p>
            
            <div className="flex items-center justify-between text-sm font-medium">
              <span className="text-indigo-600">Start Module</span>
              <span className="text-zinc-400 bg-zinc-100 px-2 py-1 rounded-md">+50 XP</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
