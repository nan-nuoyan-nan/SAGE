import { Trophy, Medal, Star, Flame } from "lucide-react";
import { useAuthStore } from "@/store/auth";

export default function Community() {
  const user = useAuthStore((state) => state.user);

  const leaderboard = [
    { rank: 1, name: "Sarah K.", xp: 12450, avatar: "bg-pink-100 text-pink-600" },
    { rank: 2, name: "David M.", xp: 11200, avatar: "bg-blue-100 text-blue-600" },
    { rank: 3, name: "Yuki T.", xp: 10800, avatar: "bg-green-100 text-green-600" },
    { rank: 4, name: "Elena R.", xp: 9400, avatar: "bg-purple-100 text-purple-600" },
    { rank: 5, name: user?.name || "You", xp: user?.xp || 450, avatar: "bg-indigo-100 text-indigo-600", isCurrentUser: true },
    { rank: 6, name: "Marcus P.", xp: 8200, avatar: "bg-orange-100 text-orange-600" },
  ];

  const achievements = [
    { id: 1, title: "First Steps", desc: "Completed your first module.", icon: <Star className="text-yellow-500" size={24} />, unlocked: true },
    { id: 2, title: "7-Day Streak", desc: "Practiced for 7 consecutive days.", icon: <Flame className="text-orange-500" size={24} />, unlocked: true },
    { id: 3, title: "Shadow Master", desc: "Scored 95%+ on 10 oral exercises.", icon: <Medal className="text-indigo-500" size={24} />, unlocked: false },
    { id: 4, title: "Polyglot", desc: "Started a course in a second language.", icon: <Trophy className="text-pink-500" size={24} />, unlocked: false },
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-zinc-900">Community & Achievements</h1>
        <p className="text-zinc-500 mt-2">See how you stack up against other learners and view your earned badges.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Leaderboard */}
        <div className="bg-white rounded-3xl border border-zinc-100 shadow-sm p-6 md:p-8">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-bold text-zinc-900 flex items-center gap-2">
              <Trophy className="text-yellow-500" /> Weekly Leaderboard
            </h2>
            <span className="text-sm text-zinc-500 bg-zinc-100 px-3 py-1 rounded-full font-medium">Top 50</span>
          </div>

          <div className="space-y-4">
            {leaderboard.sort((a, b) => b.xp - a.xp).map((player, idx) => (
              <div 
                key={player.name}
                className={`flex items-center justify-between p-4 rounded-2xl transition-colors ${
                  player.isCurrentUser ? "bg-indigo-50 border border-indigo-100" : "hover:bg-zinc-50 border border-transparent"
                }`}
              >
                <div className="flex items-center gap-4">
                  <div className={`w-8 font-bold text-center ${
                    idx === 0 ? "text-yellow-500 text-xl" : 
                    idx === 1 ? "text-zinc-400 text-xl" : 
                    idx === 2 ? "text-orange-400 text-xl" : "text-zinc-500"
                  }`}>
                    {idx + 1}
                  </div>
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${player.avatar}`}>
                    {player.name.charAt(0)}
                  </div>
                  <div>
                    <p className={`font-bold ${player.isCurrentUser ? "text-indigo-900" : "text-zinc-900"}`}>
                      {player.name} {player.isCurrentUser && "(You)"}
                    </p>
                  </div>
                </div>
                <div className="font-bold text-zinc-600">
                  {player.xp.toLocaleString()} <span className="text-xs text-zinc-400 font-medium">XP</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Achievements */}
        <div className="bg-white rounded-3xl border border-zinc-100 shadow-sm p-6 md:p-8 h-fit">
          <h2 className="text-xl font-bold text-zinc-900 flex items-center gap-2 mb-8">
            <Medal className="text-indigo-500" /> Your Badges
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {achievements.map((achievement) => (
              <div 
                key={achievement.id}
                className={`p-5 rounded-2xl border ${
                  achievement.unlocked 
                    ? "bg-gradient-to-br from-white to-zinc-50 border-zinc-200 shadow-sm" 
                    : "bg-zinc-50 border-zinc-100 opacity-60 grayscale"
                }`}
              >
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${
                  achievement.unlocked ? "bg-white shadow-md shadow-zinc-200" : "bg-zinc-200"
                }`}>
                  {achievement.icon}
                </div>
                <h3 className="font-bold text-zinc-900 mb-1">{achievement.title}</h3>
                <p className="text-xs text-zinc-500">{achievement.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
