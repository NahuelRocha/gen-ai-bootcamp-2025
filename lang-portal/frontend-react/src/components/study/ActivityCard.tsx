import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { StudyActivity } from "@/services/types";

interface ActivityCardProps {
  activity: StudyActivity;
  onSelect: (activity: StudyActivity) => void;
}

export const ActivityCard = ({ activity, onSelect }: ActivityCardProps) => {
  return (
    <Card className="hover:border-primary transition-colors">
      <CardHeader>
        <CardTitle>{activity.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">
            Practice your vocabulary with {activity.name.toLowerCase()}
          </p>
          
          <Button 
            className="w-full"
            onClick={() => onSelect(activity)}
          >
            Start Activity
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
