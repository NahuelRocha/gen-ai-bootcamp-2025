import { useEffect, useState } from 'react';
import { GroupCard } from './GroupCard';
import { useGroupsStore } from '@/store/useGroupsStore';
import { Group } from '@/services/types';
import { Pagination } from '@/components/ui/pagination';

export const GroupList = () => {
  const { loading, error, currentPage, totalPages, fetchGroups } = useGroupsStore();
  const [localGroups, setLocalGroups] = useState<Group[]>([]);

  const handlePageChange = async (page: number) => {
    try {
      const response = await fetchGroups({ page });
      setLocalGroups(response.content);
    } catch (error) {
      console.error('Error fetching groups:', error);
    }
  };

  useEffect(() => {
    handlePageChange(0);
  }, []);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="h-40 bg-muted animate-pulse rounded-lg" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-destructive">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {localGroups.map((group) => (
          <GroupCard key={group.id} group={group} />
        ))}
      </div>

      {totalPages > 1 && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={handlePageChange}
        />
      )}
    </div>
  );
};
