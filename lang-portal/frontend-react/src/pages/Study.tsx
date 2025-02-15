import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, CardContent } from "@/components/ui/card";
import { StudySession } from '@/components/study/StudySession';
import { ActivityCard } from '@/components/study/ActivityCard';
import { ReviewForm } from '@/components/study/ReviewForm';
import { useStudyStore } from '@/store/useStudyStore';
import { useGroupWordsStore } from '@/store/useGroupWordsStore';
import { StudyActivity } from '@/services/types';
import { AlertCircle, ArrowRight } from "lucide-react";
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';

const STUDY_ACTIVITIES: StudyActivity[] = [
  {
    id: 1,
    name: 'Flashcards',
    url: '/study/flashcards'
  },
  {
    id: 2,
    name: 'Multiple Choice',
    url: '/study/quiz'
  },
  {
    id: 3,
    name: 'Writing Practice',
    url: '/study/writing'
  }
];

type StudyState = 'selection' | 'session' | 'review';

export const Study = () => {
  const navigate = useNavigate();
  const { groupId } = useParams();
  const [studyState, setStudyState] = useState<StudyState>('selection');
  const { createStudySession } = useStudyStore();
  const { words, fetchGroupWords } = useGroupWordsStore();

  useEffect(() => {
    if (groupId) {
      fetchGroupWords(parseInt(groupId), {
        page: 0,
        sortBy: 'english',
        order: 'asc'
      });
    }
  }, [groupId]);

  const handleActivitySelect = async (activity: StudyActivity) => {
    if (!groupId) return;

    await createStudySession(parseInt(groupId), activity.id);
    setStudyState('session');
  };

  const handleSessionComplete = () => {
    setStudyState('review');
  };

  const handleReviewComplete = () => {
    navigate('/groups');
  };

  if (studyState === 'session') {
    return (
      <div className="container mx-auto py-8">
        <StudySession
          words={words}
          onComplete={handleSessionComplete}
        />
      </div>
    );
  }

  if (studyState === 'review') {
    return (
      <div className="container mx-auto py-8">
        <ReviewForm onComplete={handleReviewComplete} />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Choose Study Activity</h1>
        <p className="text-muted-foreground">
          Select an activity to start studying your vocabulary
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {STUDY_ACTIVITIES.map((activity) => (
          <ActivityCard
            key={activity.id}
            activity={activity}
            onSelect={handleActivitySelect}
          />
        ))}
      </div>

      {!groupId && (
        <Card>
          <CardContent className="p-2 flex flex-col items-center justify-center min-h-[200px] gap-2">
            <AlertCircle className="w-8 h-8 text-yellow-500" />
            <p className="text-xl font-semibold text-center">Select a word group first to start studying</p>
            <Button asChild className="mt-4">
              <Link to="/groups" className="gap-2">
                <ArrowRight className="w-4 h-4" />
                Choose Word Group
              </Link>
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
