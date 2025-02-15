import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useStudyStore } from "@/store/useStudyStore";

interface ReviewFormData {
  notes: string;
  difficulty: 'easy' | 'medium' | 'hard';
}

interface ReviewFormProps {
  onComplete: () => void;
}

export const ReviewForm = ({ onComplete }: ReviewFormProps) => {
  const { currentSession, reviews } = useStudyStore();
  const { register, handleSubmit } = useForm<ReviewFormData>();

  const correctAnswers = reviews.filter(r => r.correct).length;
  const totalAnswers = reviews.length;
  const percentage = Math.round((correctAnswers / totalAnswers) * 100);

  const onSubmit = (data: ReviewFormData) => {
    // Here you could send the review data to your backend
    console.log('Session Review:', {
      sessionId: currentSession?.id,
      ...data,
      score: percentage
    });
    onComplete();
  };

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-2">Session Complete!</h2>
        <p className="text-muted-foreground">
          You got {correctAnswers} out of {totalAnswers} words correct ({percentage}%)
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="space-y-2">
          <label className="text-sm font-medium">
            How difficult was this session?
          </label>
          <div className="flex gap-4">
            {['easy', 'medium', 'hard'].map((difficulty) => (
              <label
                key={difficulty}
                className="flex items-center space-x-2"
              >
                <input
                  type="radio"
                  value={difficulty}
                  {...register('difficulty')}
                  className="radio"
                />
                <span className="capitalize">{difficulty}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">
            Notes (optional)
          </label>
          <Textarea
            {...register('notes')}
            placeholder="Add any notes about this study session..."
            className="min-h-[100px]"
          />
        </div>

        <Button type="submit" className="w-full">
          Complete Review
        </Button>
      </form>
    </div>
  );
};
