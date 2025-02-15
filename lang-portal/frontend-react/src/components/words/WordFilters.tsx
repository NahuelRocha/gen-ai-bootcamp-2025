import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface WordFiltersProps {
  onSearch: (value: string) => void;
  onSortChange: (value: string) => void;
  onFilterChange: (value: string) => void;
}

export const WordFilters = ({
  onSearch,
  onSortChange,
  onFilterChange
}: WordFiltersProps) => {
  return (
    <div className="flex flex-col sm:flex-row gap-4 mb-6">
      <Input
        placeholder="Search words..."
        className="sm:w-[300px]"
        onChange={(e) => onSearch(e.target.value)}
      />
      
      <Select onValueChange={onSortChange} defaultValue="english-asc">
        <SelectTrigger className="sm:w-[180px]">
          <SelectValue placeholder="Sort by" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="english-asc">English (A-Z)</SelectItem>
          <SelectItem value="english-desc">English (Z-A)</SelectItem>
          <SelectItem value="spanish-asc">Spanish (A-Z)</SelectItem>
          <SelectItem value="spanish-desc">Spanish (Z-A)</SelectItem>
        </SelectContent>
      </Select>

      <Select onValueChange={onFilterChange} defaultValue="all">
        <SelectTrigger className="sm:w-[180px]">
          <SelectValue placeholder="Filter by" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Words</SelectItem>
          <SelectItem value="mastered">Mastered (≥70%)</SelectItem>
          <SelectItem value="learning">Learning (≤69%)</SelectItem>
          <SelectItem value="new">New Words</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
};
