import { useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowLeft, Play, Pause, Mic, Check, X } from "lucide-react";
import { useAuthStore } from "@/store/auth";

export default function CoursePlayer() {
  const { id } = useParams();
  const navigate = useNavigate();
  const updateXP = useAuthStore((state) => state.updateXP);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [showResult, setShowResult] = useState(false);

  const audioRef = useRef<HTMLAudioElement | null>(null);

  const cards = [
    { native: "Konnichiwa", target: "こんにちは", romaji: "Konnichiwa", audio: "https://actions.google.com/sounds/v1/alarms/beep_short.ogg" },
    { native: "Thank you", target: "ありがとう", romaji: "Arigatou", audio: "https://actions.google.com/sounds/v1/alarms/beep_short.ogg" },
    { native: "Excuse me", target: "すみません", romaji: "Sumimasen", audio: "https://actions.google.com/sounds/v1/alarms/beep_short.ogg" },
  ];

  const handlePlayAudio = () => {
    setIsPlaying(true);
    if (audioRef.current) {
      audioRef.current.play();
      setTimeout(() => setIsPlaying(false), 1000); // Mock duration
    }
  };

  const handleRecord = () => {
    setIsRecording(true);
    setTimeout(() => {
      setIsRecording(false);
      setShowResult(true);
    }, 2000); // Simulate 2 seconds of recording
  };

  const handleNext = () => {
    if (currentIndex < cards.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      setShowResult(false);
    } else {
      updateXP(50);
      navigate("/dashboard");
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-24">
      {/* Header */}
      <div className="flex items-center justify-between">
        <button onClick={() => navigate("/courses")} className="flex items-center gap-2 text-zinc-500 hover:text-zinc-900 transition-colors font-medium">
          <ArrowLeft size={20} />
          Back to Courses
        </button>
        <div className="flex gap-2">
          {cards.map((_, i) => (
            <div key={i} className={`h-2 rounded-full transition-all duration-300 ${i <= currentIndex ? "w-8 bg-indigo-600" : "w-4 bg-zinc-200"}`} />
          ))}
        </div>
      </div>

      <div className="text-center mt-12 mb-8">
        <h2 className="text-xl font-bold text-zinc-500 uppercase tracking-widest mb-2">Oral Shadowing</h2>
        <p className="text-3xl font-extrabold text-zinc-900">Listen and repeat</p>
      </div>

      {/* Main Flashcard Area */}
      <div className="relative h-[400px] w-full perspective-1000">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, x: 50, rotateY: 10 }}
            animate={{ opacity: 1, x: 0, rotateY: 0 }}
            exit={{ opacity: 0, x: -50, rotateY: -10 }}
            transition={{ duration: 0.4 }}
            className="absolute inset-0 bg-white rounded-[3rem] shadow-2xl shadow-indigo-100/50 border border-indigo-50 flex flex-col items-center justify-center p-12 text-center"
          >
            <p className="text-xl text-zinc-500 mb-6">{cards[currentIndex].native}</p>
            <h1 className="text-7xl font-black text-zinc-900 mb-4">{cards[currentIndex].target}</h1>
            <p className="text-2xl text-indigo-600 font-medium">{cards[currentIndex].romaji}</p>

            <audio ref={audioRef} src={cards[currentIndex].audio} />
            
            {/* Audio Waveform Mock */}
            <div className="flex items-center justify-center gap-1 mt-12 h-8">
              {[...Array(15)].map((_, i) => (
                <motion.div
                  key={i}
                  animate={isPlaying ? { height: ["20%", "100%", "20%"] } : { height: "20%" }}
                  transition={{ repeat: Infinity, duration: 0.5, delay: i * 0.05 }}
                  className="w-1.5 bg-indigo-400 rounded-full"
                />
              ))}
            </div>
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Controls */}
      <div className="flex items-center justify-center gap-6 mt-12">
        <button
          onClick={handlePlayAudio}
          className="w-16 h-16 bg-white border border-zinc-200 rounded-full flex items-center justify-center text-indigo-600 hover:bg-indigo-50 hover:border-indigo-200 transition-all shadow-sm"
        >
          {isPlaying ? <Pause size={24} fill="currentColor" /> : <Play size={24} fill="currentColor" className="ml-1" />}
        </button>

        <button
          onClick={handleRecord}
          disabled={showResult}
          className={`relative w-24 h-24 rounded-full flex items-center justify-center transition-all duration-300 shadow-xl ${
            isRecording 
              ? "bg-red-500 text-white scale-110 animate-pulse shadow-red-200" 
              : showResult
                ? "bg-green-500 text-white shadow-green-200 cursor-not-allowed"
                : "bg-indigo-600 text-white hover:bg-indigo-700 hover:scale-105 shadow-indigo-200"
          }`}
        >
          {showResult ? <Check size={40} /> : <Mic size={40} />}
          {isRecording && (
            <div className="absolute inset-0 rounded-full border-4 border-red-400 animate-ping"></div>
          )}
        </button>

        <button
          onClick={handleNext}
          disabled={!showResult}
          className={`px-8 py-4 rounded-full font-bold text-lg transition-all ${
            showResult 
              ? "bg-zinc-900 text-white hover:bg-zinc-800 hover:scale-105 shadow-xl shadow-zinc-200" 
              : "bg-zinc-100 text-zinc-400 cursor-not-allowed"
          }`}
        >
          {currentIndex === cards.length - 1 ? "Finish Module" : "Continue"}
        </button>
      </div>

      {/* Result Feedback Toast */}
      <AnimatePresence>
        {showResult && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="fixed bottom-8 left-1/2 -translate-x-1/2 bg-white px-6 py-4 rounded-2xl shadow-2xl border border-zinc-100 flex items-center gap-4"
          >
            <div className="w-10 h-10 bg-green-100 text-green-600 rounded-full flex items-center justify-center">
              <Check size={20} />
            </div>
            <div>
              <p className="font-bold text-zinc-900">Excellent pronunciation!</p>
              <p className="text-sm text-zinc-500">98% match with native speaker</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
