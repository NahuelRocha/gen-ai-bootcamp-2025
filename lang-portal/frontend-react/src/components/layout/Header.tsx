import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { ROUTES } from '@/utils/routes';

export const Header = () => {
  return (
    <header className="border-b">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <Link to={ROUTES.HOME} className="text-2xl font-bold text-primary">
            Language Portal
          </Link>
          
          <nav className="flex items-center gap-6">
            <Link to={ROUTES.WORDS} className="text-sm font-medium hover:text-primary">
              Words
            </Link>
            <Link to={ROUTES.GROUPS.LIST} className="text-sm font-medium hover:text-primary">
              Groups
            </Link>
            <Link to={ROUTES.STUDY.HOME} className="text-sm font-medium hover:text-primary">
              Study
            </Link>
            <Button variant="outline">
              ES / EN
            </Button>
          </nav>
        </div>
      </div>
    </header>
  );
};
