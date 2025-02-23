import { useWordsStore } from '../../store/useWordsStore';
import { useEffect } from 'react';
import { Card, CardContent, CardHeader } from '../ui/card';
import { BookOpen, Badge } from 'lucide-react';
import { Skeleton } from '../ui/skeleton';

export const LearningProgress = () => {
    const { wordsCount, fetchWordsCount } = useWordsStore();

    useEffect(() => {
        fetchWordsCount();
    }, [fetchWordsCount]);

    const progressPercentage = wordsCount
        ? (wordsCount.totalWordsLearned / (wordsCount.totalWords || 1)) * 100
        : 0;

    return (
        <Card className="h-full">
            <CardHeader className="pb-2">
                <div className="flex justify-between items-start space-y-1">
                    <div className="space-y-5">
                        <div className="flex items-center space-x-2 -mt-1">
                            <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
                                <BookOpen className="h-6 w-6 text-primary" />
                            </div>
                            <h2 className="text-2xl font-semibold tracking-tight">Progreso</h2>
                        </div>
                        <p className="text-sm font-medium text-muted-foreground">Seguimiento de aprendizaje</p>
                    </div>
                    <Badge className="text-sm">
                        {Math.round(progressPercentage)}% Completado
                    </Badge>
                </div>
            </CardHeader>

            <CardContent>
                {!wordsCount ? (
                    <div className="space-y-4">
                        <Skeleton className="h-4 w-[200px]" />
                        <Skeleton className="h-4 w-[180px]" />
                        <Skeleton className="h-2 w-full" />
                    </div>
                ) : (
                    <div className="space-y-4">
                        <div className="grid gap-2">
                            <div className="flex items-center justify-between">
                                <p className="text-sm font-medium text-muted-foreground">Palabras aprendidas</p>
                                <span className="text-sm font-medium">{wordsCount.totalWordsLearned}</span>
                            </div>
                            <div className="flex items-center justify-between">
                                <p className="text-sm font-medium text-muted-foreground">Total de palabras</p>
                                <span className="text-sm font-medium">{wordsCount.totalWords}</span>
                            </div>
                        </div>
                        <div className="space-y-2">

                            <div className="flex justify-between text-sm text-muted-foreground mb-1.5">
                                <span className='text-sm font-medium text-muted-foreground'>Progreso actual:</span>
                                <span>{progressPercentage.toPrecision(2)}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2.5">
                                <div
                                    className="bg-green-600 h-2.5 rounded-full transition-all"
                                    style={{ width: `${progressPercentage}%` }}
                                />
                            </div>
                            <p className="text-xs text-center text-muted-foreground">
                                {wordsCount.totalWordsLearned} de {wordsCount.totalWords} palabras dominadas
                            </p>
                        </div>
                    </div>
                )}
            </CardContent>
        </Card>
    );
};