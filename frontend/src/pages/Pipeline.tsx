import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import PipelineStepper from '@/components/PipelineStepper';
import Spinner from '@/components/Spinner';
import EmptyState from '@/components/EmptyState';
import { getRunStatus, type PipelineResponse } from '@/lib/api';

interface PipelineProps {
  runId: string | null;
}

export default function PipelinePage({ runId }: PipelineProps) {
  const [result, setResult] = useState<PipelineResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!runId) return;
    setLoading(true);
    getRunStatus(runId).then(setResult).finally(() => setLoading(false));
  }, [runId]);

  if (!runId) {
    return <EmptyState title="No pipeline run" description="Run the pipeline from the Setup tab to see agent progress." />;
  }

  if (loading) {
    return <Spinner text="Loading pipeline status..." />;
  }

  if (!result) {
    return <EmptyState title="Run not found" description="The pipeline run data is no longer available." />;
  }

  const timings = result.timings || {};
  const errorKeys = result.errors.length > 0
    ? ['literature_scout', 'data_analysis', 'hypothesis_generator', 'critic', 'evolver', 'simulator', 'experiment_designer', 'meta_reviewer'].filter(
        (k) => result.errors.some((e) => e.toLowerCase().includes(k.replace(/_/g, ' ')) || e.toLowerCase().includes(k))
      )
    : [];

  return (
    <div className="space-y-6">
      <PipelineStepper timings={timings} errorKeys={errorKeys} />

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Stage Details</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {Object.entries(timings).map(([key, duration]) => {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
            const hasError = result.errors.some(
              (e) => e.toLowerCase().includes(key.replace(/_/g, ' ')) || e.toLowerCase().includes(key)
            );
            return (
              <div key={key} className="flex items-center justify-between text-sm">
                <div>
                  <span className="font-medium">{label}</span>
                  {hasError && (
                    <span className="ml-2 text-accent-danger text-xs">Failed</span>
                  )}
                  {!hasError && duration !== undefined && (
                    <span className="ml-2 text-accent-success text-xs">Complete</span>
                  )}
                </div>
                <span className="text-text-tertiary text-xs">{duration}s</span>
              </div>
            );
          })}
        </CardContent>
      </Card>
    </div>
  );
}
