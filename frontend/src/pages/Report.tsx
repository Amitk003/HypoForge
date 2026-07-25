import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import Spinner from '@/components/Spinner';
import EmptyState from '@/components/EmptyState';
import { getReport, type ReportResponse } from '@/lib/api';

interface ReportProps {
  runId: string | null;
}

export default function ReportPage({ runId }: ReportProps) {
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!runId) return;
    setLoading(true);
    getReport(runId).then(setReport).finally(() => setLoading(false));
  }, [runId]);

  if (!runId) {
    return <EmptyState title="No report" description="Run the pipeline to generate a research report." />;
  }

  if (loading) {
    return <Spinner text="Loading report..." />;
  }

  if (!report) {
    return <EmptyState title="Run not found" description="The pipeline run data is no longer available." />;
  }

  const r = report;

  function handleDownload() {
    const blob = new Blob([r.meta_review_report], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'hypoforge_report.md';
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Executive Summary</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <p className="font-medium">Research Goal: {r.research_goal}</p>
          <p className="text-text-secondary text-sm">
            Generated {r.hypothesis_count} hypotheses, ran {r.simulation_count} simulations,
            designed {r.protocol_count} experiment protocols.
          </p>
          {r.top_hypothesis_title && (
            <p className="text-sm">
              Top hypothesis: <strong>{r.top_hypothesis_title}</strong> &mdash; Score:{' '}
              {r.top_hypothesis_score?.toFixed(2)}
            </p>
          )}
        </CardContent>
      </Card>

      <Separator />

      <div className="whitespace-pre-wrap font-mono text-sm leading-relaxed">
        {r.meta_review_report}
      </div>

      <Button onClick={handleDownload} className="w-full">
        Download Markdown
      </Button>
    </div>
  );
}
