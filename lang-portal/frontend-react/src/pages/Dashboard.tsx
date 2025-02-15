import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
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
        <h1 className="text-3xl font-bold">Welcome Back!</h1>
        <Button onClick={() => navigate('/study')}>
          Start Studying
        </Button>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Total Words</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{words.length}</p>
          </CardContent>
        </Card>

        <LearningProgress />

        <SessionStatsCard />
      </div>

      {/* Recent Words */}
      <section className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold">Recent Words</h2>
          <Button variant="link" onClick={() => navigate('/words')}>
            View All Words
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
          <h2 className="text-2xl font-bold">Word Groups</h2>
          <Button variant="link" onClick={() => navigate('/groups')}>
            View All Groups
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
