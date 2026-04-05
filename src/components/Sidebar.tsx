import { Link, useLocation } from "react-router-dom";
import { LayoutDashboard, BookOpen, MessageCircle, LogOut } from "lucide-react";
import { useAuthStore } from "@/store/auth";

export default function Sidebar() {
  const location = useLocation();
  const logout = useAuthStore((state) => state.logout);

  const links = [
    { name: "Dashboard", path: "/dashboard", icon: <LayoutDashboard size={20} /> },
    { name: "Courses", path: "/courses", icon: <BookOpen size={20} /> },
    { name: "Community", path: "/community", icon: <MessageCircle size={20} /> },
  ];

  return (
    <aside className="w-64 bg-white border-r border-zinc-200 h-screen flex flex-col hidden md:flex sticky top-0">
      <div className="p-6">
        <Link to="/dashboard" className="text-2xl font-bold text-indigo-600 flex items-center gap-2">
          <span>LinguaFlow</span>
        </Link>
      </div>

      <nav className="flex-1 px-4 space-y-2 mt-4">
        {links.map((link) => {
          const isActive = location.pathname.startsWith(link.path);
          return (
            <Link
              key={link.path}
              to={link.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive
                  ? "bg-indigo-50 text-indigo-700 font-semibold"
                  : "text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900"
              }`}
            >
              {link.icon}
              {link.name}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-zinc-100">
        <button
          onClick={logout}
          className="flex items-center gap-3 px-4 py-3 rounded-xl text-zinc-500 hover:bg-red-50 hover:text-red-600 transition-colors w-full"
        >
          <LogOut size={20} />
          <span>Log out</span>
        </button>
      </div>
    </aside>
  );
}
