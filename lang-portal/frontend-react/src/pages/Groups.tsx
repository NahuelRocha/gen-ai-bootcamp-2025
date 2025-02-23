import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { GroupList } from '@/components/groups/GroupList';
import { WordList } from '@/components/words/WordList';
import { useGroupsStore } from '@/store/useGroupsStore';
import { useGroupWordsStore } from '@/store/useGroupWordsStore';
import { toast } from '@/hooks/use-toast';
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { WordFilters } from '@/components/words/WordFilters';
import { Card, CardContent } from "@/components/ui/card";
import { useNavigate } from 'react-router-dom';

export const Groups = () => {
  const { groupId } = useParams();
  const [searchQuery, setSearchQuery] = useState('');
  const { fetchGroups } = useGroupsStore();
  const {
    fetchGroupWords,
    currentPage,
    totalPages,
    currentSortBy,
    currentOrder
  } = useGroupWordsStore();
  const navigate = useNavigate();

  // Initial data fetch for groups
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        if (groupId) {
          await fetchGroupWords(parseInt(groupId), {
            page: 0,
            sortBy: 'english',
            order: 'asc'
          });
        } else {
          await fetchGroups({ page: 0, sortBy: 'name', order: 'asc' });
        }
      } catch (error) {
        console.error('Failed to fetch data:', error);
        toast({
          variant: "destructive",
          title: "Error",
          description: "Failed to fetch data. Please try again later."
        });
      }
    };

    loadInitialData();
  }, [groupId]); // Re-fetch when groupId changes

  const handleSearch = async (value: string) => {
    setSearchQuery(value);
    try {
      if (groupId) {
        await fetchGroupWords(parseInt(groupId), {
          page: currentPage,
          sortBy: currentSortBy,
          order: currentOrder,
        });
      } else {
        await fetchGroups({
          page: 0,
          sortBy: 'name',
          order: 'asc',
        });
      }
    } catch (error) {
      console.error('Error searching:', error);
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to search. Please try again."
      });
    }
  };

  const handleSort = async (value: string) => {
    if (!groupId) return;

    const [field, order] = value.split('-');
    try {
      await fetchGroupWords(parseInt(groupId), {
        page: currentPage,
        sortBy: field,
        order: order as 'asc' | 'desc',
      });
    } catch (error) {
      console.error('Error sorting words:', error);
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to sort words. Please try again."
      });
    }
  };


  const handleFilter = async (value: string) => {
    // Add your filter logic here
    console.log('Filter value:', value);
  };

  const handlePageChange = async (newPage: number) => {
    if (!groupId) return;

    try {
      await fetchGroupWords(parseInt(groupId), {
        page: newPage,
        sortBy: currentSortBy,
        order: currentOrder,
      });
    } catch (error) {
      console.error('Error changing page:', error);
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to change page. Please try again."
      });
    }
  };

  const GroupStats = () => {
    const { words } = useGroupWordsStore();

    // Calculate general statistics
    const totalWords = words.length;
    const totalAttempts = words.reduce((sum, word) => sum + word.correctCount + word.wrongCount, 0);
    const totalCorrect = words.reduce((sum, word) => sum + word.correctCount, 0);
    const totalWrong = words.reduce((sum, word) => sum + word.wrongCount, 0);

    // Calculate overall accuracy
    const overallAccuracy = totalAttempts > 0
      ? Math.round((totalCorrect / totalAttempts) * 100)
      : 0;

    // Calculate mastery levels
    const masteredWords = words.filter(word => {
      const accuracy = word.correctCount + word.wrongCount > 0
        ? (word.correctCount / (word.correctCount + word.wrongCount)) * 100
        : 0;
      return accuracy >= 70;
    }).length;

    const strugglingWords = words.filter(word => {
      const accuracy = word.correctCount + word.wrongCount > 0
        ? (word.correctCount / (word.correctCount + word.wrongCount)) * 100
        : 0;
      return accuracy < 40 && word.correctCount + word.wrongCount > 0;
    }).length;

    return (
      <Card className="mb-6">
        <CardContent className="pt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Overall Performance */}
            <div className="space-y-2">
              <h3 className="text-sm font-medium">Rendimiento general</h3>
              <div className="flex items-center gap-2">
                <div className="text-2xl font-bold">
                  {overallAccuracy}%
                </div>
                <span className="text-xl font-bold mt-1">Precisión</span>
              </div>
            </div>

            {/* Practice Stats */}
            <div className="space-y-2">
              <h3 className="text-sm font-medium">Estadísticas de práctica</h3>
              <div className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Intentos totales:</span>
                  <span>{totalAttempts}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Correctos:</span>
                  <span className="text-green-600">{totalCorrect}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Incorrectos:</span>
                  <span className="text-red-600">{totalWrong}</span>
                </div>
              </div>
            </div>

            {/* Mastery Progress */}
            <div className="space-y-2">
              <h3 className="text-sm font-medium">Progreso de dominio</h3>
              <div className="space-y-1">
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div
                    className="bg-green-600 h-2.5 rounded-full"
                    style={{ width: `${(masteredWords / totalWords) * 100}%` }}
                  />
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Dominados:</span>
                  <span>{masteredWords} de {totalWords}</span>
                </div>
              </div>
            </div>

            {/* Areas for Improvement */}
            <div className="space-y-2">
              <h3 className="text-sm font-medium">Áreas de mejora</h3>
              <div className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Luchando con:</span>
                  <span className="text-red-600">{strugglingWords} palabras</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">No practicadas:</span>
                  <span>{words.filter(w => w.correctCount + w.wrongCount === 0).length} palabras</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  };

  // If we have a groupId, show the words in that group
  if (groupId) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Palabras del grupo</h1>
          <div className="space-x-4">
            <Button variant="outline">Agregar palabras al grupo</Button>
            <Button onClick={() => navigate(`/study/group/${groupId}`)}>Estudiar ahora</Button>
          </div>
        </div>

        <GroupStats />

        <WordFilters
          onSearch={handleSearch}
          onSortChange={handleSort}
          onFilterChange={handleFilter}
        />

        <WordList />

        {totalPages > 1 && (
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={handlePageChange}
          >
            <PaginationContent>
              <PaginationItem>
                <PaginationPrevious
                  onClick={() => handlePageChange(currentPage - 1)}

                />
              </PaginationItem>

              {Array.from({ length: totalPages }, (_, i) => (
                <PaginationItem key={i}>
                  <PaginationLink
                    onClick={() => handlePageChange(i)}
                    isActive={currentPage === i}
                  >
                    {i + 1}
                  </PaginationLink>
                </PaginationItem>
              ))}

              <PaginationItem>
                <PaginationNext
                  onClick={() => handlePageChange(currentPage + 1)}

                />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        )}
      </div>
    );
  }

  // Otherwise, show the list of groups
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Grupos de palabras</h1>
        <Button>Crear nuevo grupo</Button>
      </div>

      <Input
        placeholder="Buscar grupos..."
        className="max-w-sm"
        value={searchQuery}
        onChange={(e) => handleSearch(e.target.value)}
      />

      <GroupList />
    </div>
  );
};