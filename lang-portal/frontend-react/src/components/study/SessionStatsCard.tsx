import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useStudyStore } from "@/store/useStudyStore";
import { format } from 'date-fns';
import { useEffect } from 'react';

export const SessionStatsCard = () => {
    const { lastSession, loadingLastSession, errorLastSession, fetchLastSession } = useStudyStore();

    useEffect(() => {
        fetchLastSession();
    }, [fetchLastSession]);

    const total = lastSession ? lastSession.correct + lastSession.incorrect : 0;
    const accuracy = lastSession ? Math.round((lastSession.correct / (total || 1)) * 100) : 0;

    const getBadgeVariant = (accuracy: number) => {
        if (accuracy >= 70) return "success";
        if (accuracy >= 40) return "warning";
        return "destructive";
    };

    return (
        <Card className="h-full">
            <CardHeader className="pb-1">
                <div className="flex justify-between items-start">
                    <div>
                        <h1 className="text-2xl font-semibold tracking-tight mb-2.5">Última Sesión</h1>
                        <h3 className="text-lg font-semibold">{lastSession?.groupName || "Última Sesión"}</h3>
                        <h3 className="text-lg font-semibold">{lastSession?.activityName}</h3>
                    </div>
                    <div className="text-right mt-1">
                        <Badge variant={getBadgeVariant(accuracy)} className="mb-2">
                            {accuracy}% Precisión
                        </Badge>
                        {lastSession?.createdAt && (
                            <div className="text-xs text-muted-foreground">
                                {format(new Date(lastSession.createdAt), 'dd/MM/yy HH:mm')}
                            </div>
                        )}
                    </div>
                </div>
            </CardHeader>

            <CardContent>
                {loadingLastSession ? (
                    <div className="space-y-4">
                        <Skeleton className="h-4 w-[200px]" />
                        <Skeleton className="h-4 w-[180px]" />
                        <Skeleton className="h-2 w-full" />
                    </div>
                ) : errorLastSession ? (
                    <div className="text-center space-y-2">
                        <p className="text-red-600">{errorLastSession}</p>
                        <button
                            className="text-sm text-primary underline hover:text-primary/80"
                            onClick={fetchLastSession}
                        >
                            Reintentar
                        </button>
                    </div>
                ) : lastSession ? (
                    <div className="space-y-2">
                        <div className="text-sm">
                            <p className="font-medium text-lg text-muted-foreground">Estadísticas:</p>
                            <div className="mt-1 space-y-1">
                                <div className="flex justify-between ttext-sm font-medium text-muted-foreground mb-1.5">
                                    <span>Total de Intentos:</span>
                                    <span>{total}</span>
                                </div>
                                <div className="flex justify-between text-sm font-medium text-muted-foreground">
                                    <span>Correctas:</span>
                                    <span className="text-green-600">{lastSession.correct}</span>
                                </div>
                                <div className="flex justify-between text-sm font-medium text-muted-foreground">
                                    <span>Incorrectas:</span>
                                    <span className="text-red-600">{lastSession.incorrect}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="text-center text-muted-foreground">
                        No hay sesiones recientes
                    </div>
                )}
            </CardContent>
        </Card>
    );
};