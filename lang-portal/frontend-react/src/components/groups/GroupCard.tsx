import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Group } from "@/services/types";

interface GroupCardProps {
  group: Group;
}

export const GroupCard = ({ group }: GroupCardProps) => {
  const navigate = useNavigate();

  return (
    <Card className="hover:border-primary transition-colors">
      <CardHeader>
        <CardTitle>{group.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">
            {group.wordsCount} {group.wordsCount === 1 ? 'word' : 'words'}
          </p>
          
          <div className="flex gap-2">
            <Button 
              variant="outline" 
              onClick={() => navigate(`/groups/${group.id}`)}
            >
              View Words
            </Button>
            <Button 
              onClick={() => navigate(`/study/group/${group.id}`)}
            >
              Study Now
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
