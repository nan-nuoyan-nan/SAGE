import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Globe, BookOpen, Headphones, Mic, Trophy } from "lucide-react";

export default function Home() {
  const languages = ["English", "Japanese", "Korean", "Spanish", "French"];
  const features = [
    { icon: <BookOpen className="w-6 h-6" />, title: "Leveled Courses", desc: "Structured learning paths from absolute beginner to advanced fluency." },
    { icon: <Mic className="w-6 h-6" />, title: "Oral Shadowing", desc: "Real-time voice feedback to perfect your pronunciation and accent." },
    { icon: <Headphones className="w-6 h-6" />, title: "Listening Training", desc: "Immersive audio exercises featuring native speakers and real-world contexts." },
    { icon: <Trophy className="w-6 h-6" />, title: "Community & XP", desc: "Compete on leaderboards, earn badges, and stay motivated." },
  ];

  return (
    <div className="min-h-screen bg-zinc-50 font-sans">
      <nav className="flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
        <div className="text-2xl font-bold text-indigo-600 flex items-center gap-2">
          <Globe className="w-8 h-8" />
          LinguaFlow
        </div>
        <div className="flex items-center gap-6 font-medium text-zinc-600">
          <a href="#features" className="hover:text-zinc-900 transition-colors">Features</a>
          <Link to="/login" className="text-indigo-600 hover:text-indigo-700 transition-colors">Login</Link>
          <Link to="/login" className="bg-indigo-600 text-white px-6 py-2.5 rounded-full hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200">
            Start Learning
          </Link>
        </div>
      </nav>

      <main>
        {/* Hero Section */}
        <section className="relative pt-24 pb-32 overflow-hidden">
          <div className="max-w-7xl mx-auto px-8 text-center relative z-10">
            <motion.h1 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-6xl md:text-7xl font-extrabold tracking-tight text-zinc-900 mb-8"
            >
              Master Any Language <br className="hidden md:block" />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">
                With Confidence
              </span>
            </motion.h1>
            
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-xl text-zinc-500 mb-12 max-w-2xl mx-auto leading-relaxed"
            >
              Immersive, interactive modules tailored to your level. From grammar drills to oral shadowing, fluency is just a few taps away.
            </motion.p>

            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="flex flex-col items-center gap-6"
            >
              <Link to="/login" className="bg-zinc-900 text-white px-8 py-4 rounded-full text-lg font-bold hover:bg-zinc-800 transition-transform transform hover:scale-105 shadow-xl shadow-zinc-200">
                Get Started for Free
              </Link>
              
              <div className="flex flex-wrap justify-center gap-3 mt-8">
                {languages.map((lang, i) => (
                  <span key={lang} className="px-4 py-2 bg-white border border-zinc-200 rounded-full text-zinc-600 font-medium shadow-sm flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-green-500"></span>
                    {lang}
                  </span>
                ))}
              </div>
            </motion.div>
          </div>
          
          {/* Background decoration */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-indigo-100/50 rounded-full blur-3xl -z-10"></div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-24 bg-white border-t border-zinc-100">
          <div className="max-w-7xl mx-auto px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-zinc-900 mb-4">Everything you need to be fluent</h2>
              <p className="text-lg text-zinc-500">A comprehensive suite of tools designed for serious learners.</p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, i) => (
                <motion.div 
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: i * 0.1 }}
                  className="p-8 rounded-3xl bg-zinc-50 border border-zinc-100 hover:border-indigo-100 hover:shadow-xl hover:shadow-indigo-50 transition-all group"
                >
                  <div className="w-14 h-14 bg-indigo-100 text-indigo-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-bold text-zinc-900 mb-3">{feature.title}</h3>
                  <p className="text-zinc-500 leading-relaxed">{feature.desc}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
