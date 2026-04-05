import { Bell, UserCircle } from "lucide-react";
import { useAuthStore } from "@/store/auth";

export default function Navbar() {
  const user = useAuthStore((state) => state.user);

  return (
    <header className="bg-white border-b border-zinc-200 h-16 flex items-center justify-between px-6 md:px-8 sticky top-0 z-10">
      <div className="flex items-center gap-4">
        {/* Mobile menu toggle would go here */}
        <h1 className="text-xl font-bold text-zinc-900 md:hidden">LinguaFlow</h1>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 bg-indigo-50 px-3 py-1.5 rounded-full text-sm font-semibold text-indigo-700">
          🔥 {user?.xp} XP
        </div>

        <button className="text-zinc-500 hover:text-zinc-900 transition-colors relative">
          <Bell size={22} />
          <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>

        <div className="flex items-center gap-3">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-semibold text-zinc-900">{user?.name}</p>
            <p className="text-xs text-zinc-500">{user?.targetLanguage} • {user?.level}</p>
          </div>
          <div className="w-10 h-10 bg-indigo-100 text-indigo-700 rounded-full flex items-center justify-center font-bold">
            {user?.name.charAt(0)}
          </div>
        </div>
      </div>
    </header>
  );
}
