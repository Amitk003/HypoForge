import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import Simulator from '@/components/Simulator';
import { getCausalGraph, type CausalGraph } from '@/lib/api';

interface CausalSimProps {
  runId: string | null;
}

export default function CausalSimPage({ runId }: CausalSimProps) {
  const [graph, setGraph] = useState<CausalGraph | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!runId) return;
    setLoading(true);
    getCausalGraph(runId).then(setGraph).finally(() => setLoading(false));
  }, [runId]);

  if (!runId) {
    return (
      <div className="text-center py-12 text-text-secondary">
        Upload a dataset with numeric variables to enable causal discovery.
      </div>
    );
  }

  if (loading) {
    return <div className="text-center py-12 text-text-secondary">Loading...</div>;
  }

  if (!graph || graph.nodes.length === 0) {
    return (
      <div className="text-center py-12 text-text-secondary">
        Upload a dataset with numeric variables to enable causal discovery.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
      <div className="md:col-span-3">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Causal Graph (DAG)</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex flex-wrap gap-2">
              {graph.nodes.map((node) => (
                <Badge key={node} variant="outline" className="bg-text-primary text-white">
                  {node}
                </Badge>
              ))}
            </div>
            <div className="text-sm space-y-1">
              <p className="font-medium mt-2">Edges:</p>
              {graph.edges.map((e, i) => (
                <p key={i} className="text-text-secondary">
                  {e.source} -&gt; {e.target} {e.weight ? `(weight: ${e.weight})` : ''}
                </p>
              ))}
            </div>
            {graph.confounders.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-2">
                {graph.confounders.map((c) => (
                  <Badge key={c} className="bg-accent-info/20 text-accent-primary border border-accent-info/50">
                    Confounder: {c}
                  </Badge>
                ))}
              </div>
            )}
            {graph.mediators.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-1">
                {graph.mediators.map((m) => (
                  <Badge key={m} className="bg-accent-info/20 text-accent-primary border border-accent-info/50">
                    Mediator: {m}
                  </Badge>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
      <div className="md:col-span-2">
        <Simulator runId={runId} />
      </div>
    </div>
  );
}
