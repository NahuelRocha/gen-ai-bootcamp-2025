import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Word } from "@/services/types";

interface WordCardProps {
  word: Word;
  showActions?: boolean;
}

export const WordCard = ({ word }: WordCardProps) => {
  // Calculate accuracy percentage
  const accuracy = word.correctCount + word.wrongCount > 0
    ? Math.round((word.correctCount / (word.correctCount + word.wrongCount)) * 100)
    : 0;

  // Determine badge color based on accuracy
  const getBadgeVariant = (accuracy: number) => {
    if (accuracy >= 70) return "success";
    if (accuracy >= 40) return "warning";
    return "destructive";
  };

  // Parse parts if it's a string
  const parts = typeof word.parts === 'string' ? JSON.parse(word.parts) : word.parts;

  return (
    <Card className="h-full">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-lg font-semibold">{word.spanish}</h3>
            <p className="text-sm text-muted-foreground">{word.pronunciation}</p>
          </div>
          <div className="text-right">
            <Badge variant={getBadgeVariant(accuracy)} className="mb-2">
              {accuracy}% Accuracy
            </Badge>
            <div className="text-xs text-muted-foreground">
              ✓ {word.correctCount} | ✗ {word.wrongCount}
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {parts.type && (
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="capitalize">
                {parts.type}
              </Badge>
              {parts.usage && (
                <Badge variant="outline" className="capitalize">
                  {parts.usage}
                </Badge>
              )}
              {parts.time && (
                <Badge variant="outline" className="capitalize">
                  {parts.time}
                </Badge>
              )}
            </div>
          )}
          <div className="text-sm">
            <p className="font-medium text-muted-foreground">Practice Stats:</p>
            <div className="mt-1 space-y-1">
              <div className="flex justify-between text-sm text-muted-foreground mb-1.5">
                <span>Total Attempts:</span>
                <span>{word.correctCount + word.wrongCount}</span>
              </div>
              <div className="flex justify-between text-sm text-muted-foreground">
                <span>Correct:</span>
                <span className="text-green-600">{word.correctCount}</span>
              </div>
              <div className="flex justify-between text-sm text-muted-foreground">
                <span>Wrong:</span>
                <span className="text-red-600">{word.wrongCount}</span>
              </div>
              <div className="mt-4">
                <div className="flex justify-between text-sm text-muted-foreground mb-1.5">
                  <span>Mastery Progress:</span>
                  <span>{accuracy}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div
                    className="bg-green-600 h-2.5 rounded-full transition-all"
                    style={{ width: `${accuracy}%` }}
                  />
                </div>
              </div>

            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
