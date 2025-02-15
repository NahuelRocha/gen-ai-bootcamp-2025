import { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useStudyStore } from '@/store/useStudyStore';
import { Word } from '@/services/types';

interface StudySessionProps {
  words: Word[];
  onComplete: () => void;
}

export const StudySession = ({ words, onComplete }: StudySessionProps) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const { submitWordReview, currentSession } = useStudyStore();

  const currentWord = words[currentIndex];
  const isLastWord = currentIndex === words.length - 1;

  const handleAnswer = async (correct: boolean) => {
    if (!currentSession) return;

    await submitWordReview(currentSession.id, {
      wordId: currentWord.id,
      studySessionId: currentSession.id,
      correct
    });

    if (isLastWord) {
      onComplete();
    } else {
      setCurrentIndex(prev => prev + 1);
      setShowAnswer(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <Card className="mb-4">
        <CardContent className="pt-6">
          <div className="text-center space-y-4">
            <p className="text-sm text-muted-foreground">
              Word {currentIndex + 1} of {words.length}
            </p>

            <div className="py-8">
              <h2 className="text-3xl font-bold mb-4">
                {showAnswer ? currentWord.english : currentWord.spanish}
              </h2>
              {showAnswer && (
                <div className="space-y-2">
                  <p className="text-lg">{currentWord.pronunciation}</p>
                  <p className="text-muted-foreground">{currentWord.parts.usage}</p>
                </div>
              )}
            </div>

            {!showAnswer ? (
              <Button
                size="lg"
                onClick={() => setShowAnswer(true)}
              >
                Show Answer
              </Button>
            ) : (
              <div className="flex justify-center gap-4">
                <Button
                  variant="outline"
                  size="lg"
                  onClick={() => handleAnswer(false)}
                >
                  Incorrect
                </Button>
                <Button
                  size="lg"
                  onClick={() => handleAnswer(true)}
                >
                  Correct
                </Button>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <div className="h-2 bg-muted rounded">
        <div
          className="h-full bg-primary rounded transition-all"
          style={{ width: `${((currentIndex + 1) / words.length) * 100}%` }}
        />
      </div>
    </div>
  );
};
