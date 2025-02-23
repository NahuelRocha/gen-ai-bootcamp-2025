import { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { WordList } from '@/components/words/WordList';
import { WordFilters } from '@/components/words/WordFilters';
import { useWordsStore } from '@/store/useWordsStore';
import { toast } from '@/hooks/use-toast';
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { cn } from "@/lib/utils";

export const Words = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [currentSortBy, setSortBy] = useState('english');
  const [currentOrder, setOrder] = useState<'asc' | 'desc'>('asc');
  const { fetchWords, currentPage, totalPages } = useWordsStore();

  // Initial data fetch
  useEffect(() => {
    loadWords();
  }, []); // Empty dependency array for initial load

  const loadWords = async (page = currentPage) => {
    try {
      await fetchWords({
        page,
        sortBy: currentSortBy,
        order: currentOrder,
      });
    } catch (error) {
      console.error('Error al recuperar palabras:', error);
      toast({
        variant: "destructive",
        title: "Error",
        description: "Error al recuperar palabras. Por favor, inténtelo de nuevo más tarde."
      });
    }
  };

  const handleSearch = async (value: string) => {
    setSearchQuery(value);
    try {
      await fetchWords({
        page: 0, // Reset to first page on new search
        sortBy: currentSortBy,
        order: currentOrder,
      });
    } catch (error) {
      console.error('Error al buscar palabras:', error);
      toast({
        variant: "destructive",
        title: "Error",
        description: "Error al buscar palabras. Por favor, inténtelo de nuevo."
      });
    }
  };

  const handleFilter = async (value: string) => {
    // Add your filter logic here
    console.log('Filter value:', value);
  };

  const handleSort = async (value: string) => {
    const [field, order] = value.split('-');
    setSortBy(field);
    setOrder(order as 'asc' | 'desc');
    try {
      await fetchWords({
        page: currentPage, // Maintain current page when sorting
        sortBy: field,
        order: order as 'asc' | 'desc',
      });
    } catch (error) {
      console.error('Error al ordenar palabras:', error);
      toast({
        variant: "destructive",
        title: "Error",
        description: "Error al ordenar palabras. Por favor, inténtelo de nuevo."
      });
    }
  };

  const handlePageChange = (newPage: number) => {
    loadWords(newPage);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Palabras</h1>
        <Button>Agregar nueva palabra</Button>
      </div>

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
                onClick={() => currentPage > 0 && handlePageChange(currentPage - 1)}
                className={cn(currentPage === 0 && "pointer-events-none opacity-50")}
                aria-disabled={currentPage === 0}
              />
            </PaginationItem>

            {Array.from({ length: totalPages }, (_, i) => (
              <PaginationItem key={i}>
                <PaginationLink
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    handlePageChange(i);
                  }}
                  isActive={currentPage === i}
                >
                  {i + 1}
                </PaginationLink>
              </PaginationItem>
            ))}

            <PaginationItem>
              <PaginationNext
                onClick={() => currentPage < totalPages - 1 && handlePageChange(currentPage + 1)}
                className={cn(currentPage === totalPages - 1 && "pointer-events-none opacity-50")}
                aria-disabled={currentPage === totalPages - 1}
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      )}
    </div>
  );
};
