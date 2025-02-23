import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { useWordsStore } from '@/store/useWordsStore';
import { useGroupsStore } from '@/store/useGroupsStore';
import { WordCard } from '@/components/words/WordCard';
import { GroupCard } from '@/components/groups/GroupCard';
import { SessionStatsCard } from '@/components/study/SessionStatsCard';
import { LearningProgress } from '@/components/study/LearningProgress';

export const Dashboard = () => {
  const navigate = useNavigate();
  const { words, fetchWords } = useWordsStore();
  const { groups, fetchGroups } = useGroupsStore();

  useEffect(() => {
    // Fetch initial data


    console.log("Fetching initial data...");
    fetchWords({ page: 0, sortBy: 'english', order: 'asc' });
    fetchGroups({ page: 0, sortBy: 'name', order: 'asc' });
  }, []);

  const recentWords = words.slice(0, 3);
  const recentGroups = groups.slice(0, 3);

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">¡Bienvenido de nuevo!</h1>
        <Button onClick={() => navigate('/groups')}>Comenzar a estudiar</Button>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">


        <LearningProgress />

        <SessionStatsCard />
      </div>

      {/* Recent Words */}
      <section className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold">Palabras recientes</h2>
          <Button variant="link" onClick={() => navigate('/words')}>
            Ver todas las palabras
          </Button>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          {recentWords.map(word => (
            <WordCard key={word.id} word={word} showActions={false} />
          ))}
        </div>
      </section>

      {/* Recent Groups */}
      <section className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold">Grupos de palabras</h2>
          <Button variant="link" onClick={() => navigate('/groups')}>
            Ver todos los grupos
          </Button>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          {recentGroups.map(group => (
            <GroupCard key={group.id} group={group} />
          ))}
        </div>
      </section>
    </div>
  );
};
