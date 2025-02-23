import { WordCard } from './WordCard';
import { useWordsStore } from '@/store/useWordsStore';
import { useGroupWordsStore } from '@/store/useGroupWordsStore';
import { useParams } from 'react-router-dom';

export const WordList = () => {
  const { groupId } = useParams();
  const { words: globalWords, loading: globalLoading, error: globalError } = useWordsStore();
  const { words: groupWords, loading: groupLoading, error: groupError } = useGroupWordsStore();


  const words = groupId ? groupWords : globalWords;
  const loading = groupId ? groupLoading : globalLoading;
  const error = groupId ? groupError : globalError;

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="h-48 bg-muted animate-pulse rounded-lg" />
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
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {words.map((word) => (
        <WordCard key={word.id} word={word} />
      ))}
    </div>
  );
};