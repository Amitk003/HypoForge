import { useEffect, useState } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  type Node,
  type Edge,
  MarkerType,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import Simulator from '@/components/Simulator';
import Spinner from '@/components/Spinner';
import EmptyState from '@/components/EmptyState';
import { getCausalGraph, type CausalGraph } from '@/lib/api';

interface CausalSimProps {
  runId: string | null;
}

export default function CausalSimPage({ runId }: CausalSimProps) {
  const [graph, setGraph] = useState<CausalGraph | null>(null);
  const [loading, setLoading] = useState(false);
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

  useEffect(() => {
    if (!runId) return;
    setLoading(true);
    getCausalGraph(runId)
      .then((g) => {
        setGraph(g);
        if (g.nodes.length > 0) {
          const flowNodes: Node[] = g.nodes.map((name, i) => ({
            id: name,
            position: {
              x: 150 + (i % 4) * 180,
              y: 60 + Math.floor(i / 4) * 120,
            },
            data: { label: name },
          }));
          const flowEdges: Edge[] = g.edges.map((e, i) => ({
            id: `e${i}`,
            source: e.source,
            target: e.target,
            label: e.weight ? String(e.weight) : undefined,
            markerEnd: { type: MarkerType.ArrowClosed },
            style: { strokeWidth: 2 },
          }));
          setNodes(flowNodes);
          setEdges(flowEdges);
        }
      })
      .finally(() => setLoading(false));
  }, [runId]);

  if (!runId) {
    return <EmptyState title="No data uploaded" description="Run the pipeline with a dataset to enable causal discovery." />;
  }

  if (loading) {
    return <Spinner text="Loading causal graph..." />;
  }

  if (!graph || graph.nodes.length === 0) {
    return <EmptyState title="No causal graph" description="Upload a dataset with numeric variables to enable causal discovery." />;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
      <div className="md:col-span-3 space-y-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Causal Graph (DAG)</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div style={{ height: 400 }} className="w-full">
              <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                fitView
                attributionPosition="bottom-left"
              >
                <Controls />
                <Background />
                <MiniMap />
              </ReactFlow>
            </div>
          </CardContent>
        </Card>
        <div className="flex flex-wrap gap-1">
          {graph.confounders.length > 0 && graph.confounders.map((c) => (
            <Badge key={c} className="bg-accent-info/20 text-accent-primary border border-accent-info/50">
              Confounder: {c}
            </Badge>
          ))}
          {graph.mediators.length > 0 && graph.mediators.map((m) => (
            <Badge key={m} className="bg-accent-info/20 text-accent-primary border border-accent-info/50">
              Mediator: {m}
            </Badge>
          ))}
        </div>
      </div>
      <div className="md:col-span-2">
        <Simulator runId={runId} variables={graph.nodes} />
      </div>
    </div>
  );
}
