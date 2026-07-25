import { useEffect, useState } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import ScorePill from '@/components/ScorePill';
import Spinner from '@/components/Spinner';
import EmptyState from '@/components/EmptyState';
import { getHypotheses, type Hypothesis } from '@/lib/api';

interface HypothesesProps {
  runId: string | null;
}

function sortHypotheses(list: Hypothesis[], sortBy: string): Hypothesis[] {
  const map: Record<string, (h: Hypothesis) => number> = {
    'Composite Score': (h) => (h.novelty_score + h.causal_rigor_score + h.testability_score + h.impact_score) / 4,
    Novelty: (h) => h.novelty_score,
    'Causal Rigor': (h) => h.causal_rigor_score,
    Testability: (h) => h.testability_score,
    Impact: (h) => h.impact_score,
  };
  const fn = map[sortBy] || map['Composite Score'];
  return [...list].sort((a, b) => fn(b) - fn(a));
}

function filterHypotheses(list: Hypothesis[], filterBy: string): Hypothesis[] {
  switch (filterBy) {
    case 'High Impact (>0.7)':
      return list.filter((h) => h.impact_score > 0.7);
    case 'Novel (>0.8)':
      return list.filter((h) => h.novelty_score > 0.8);
    case 'With Critiques':
      return list.filter((h) => h.critique_notes.length > 0);
    case 'With Safety Flags':
      return list.filter((h) => h.safety_flags.length > 0);
    default:
      return list;
  }
}

export default function HypothesesPage({ runId }: HypothesesProps) {
  const [hypotheses, setHypotheses] = useState<Hypothesis[]>([]);
  const [loading, setLoading] = useState(false);
  const [sortBy, setSortBy] = useState('Composite Score');
  const [filterBy, setFilterBy] = useState('All');
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    if (!runId) return;
    setLoading(true);
    getHypotheses(runId).then(setHypotheses).finally(() => setLoading(false));
  }, [runId]);

  if (!runId) {
    return <EmptyState title="No hypotheses" description="Run the pipeline to generate and rank hypotheses." />;
  }

  if (loading) {
    return <Spinner text="Loading hypotheses..." />;
  }

  const sorted = sortHypotheses(
    hypotheses.length > 0 ? filterHypotheses(hypotheses, filterBy) : [],
    sortBy
  );

  if (hypotheses.length === 0) {
    return <EmptyState title="No hypotheses generated" description="Check the Pipeline tab for any errors during execution." />;
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-4">
        <Select value={sortBy} onValueChange={(v) => v && setSortBy(v)}>
          <SelectTrigger className="w-[180px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="Composite Score">Composite Score</SelectItem>
            <SelectItem value="Novelty">Novelty</SelectItem>
            <SelectItem value="Causal Rigor">Causal Rigor</SelectItem>
            <SelectItem value="Testability">Testability</SelectItem>
            <SelectItem value="Impact">Impact</SelectItem>
          </SelectContent>
        </Select>
        <Select value={filterBy} onValueChange={(v) => v && setFilterBy(v)}>
          <SelectTrigger className="w-[180px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="All">All</SelectItem>
            <SelectItem value="High Impact (>0.7)">High Impact (&gt;0.7)</SelectItem>
            <SelectItem value="Novel (>0.8)">Novel (&gt;0.8)</SelectItem>
            <SelectItem value="With Critiques">With Critiques</SelectItem>
            <SelectItem value="With Safety Flags">With Safety Flags</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {sorted.map((h, i) => (
        <Card
          key={h.id}
          className="cursor-pointer"
          onClick={() => setExpanded(expanded === h.id ? null : h.id)}
        >
          <CardHeader>
            <CardTitle className="text-sm flex items-center gap-2">
              <span className="text-text-tertiary">#{i + 1}</span>
              {h.title}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-1 mb-2">
              <ScorePill label="Novelty" score={h.novelty_score} />
              <ScorePill label="Rigor" score={h.causal_rigor_score} />
              <ScorePill label="Test" score={h.testability_score} />
              <ScorePill label="Impact" score={h.impact_score} />
            </div>
            <p className="text-sm text-text-secondary line-clamp-2">{h.core_statement}</p>
          </CardContent>
          {expanded === h.id && (
            <div className="px-6 pb-4 space-y-3 text-sm">
              <Separator />
              <div>
                <p className="font-medium">Statement</p>
                <p className="text-text-secondary">{h.core_statement}</p>
              </div>
              {h.proposed_mechanism && (
                <div>
                  <p className="font-medium">Proposed Mechanism</p>
                  <p className="text-text-secondary">{h.proposed_mechanism}</p>
                </div>
              )}
              {h.supporting_evidence.length > 0 && (
                <div>
                  <p className="font-medium">Supporting Evidence</p>
                  <ul className="list-disc list-inside text-text-secondary">
                    {h.supporting_evidence.map((ev, idx) => (
                      <li key={idx}>{ev}</li>
                    ))}
                  </ul>
                </div>
              )}
              {h.critique_notes.length > 0 && (
                <div className="bg-accent-warning/10 border border-accent-warning/30 rounded p-2">
                  <p className="font-medium text-accent-warning">Critique Notes</p>
                  {h.critique_notes.map((note, idx) => (
                    <p key={idx} className="text-sm">{note}</p>
                  ))}
                </div>
              )}
              {h.safety_flags.length > 0 && (
                <div className="bg-accent-danger/10 border border-accent-danger/30 rounded p-2">
                  <p className="font-medium text-accent-danger">Safety Flags</p>
                  {h.safety_flags.map((flag, idx) => (
                    <p key={idx} className="text-sm">{flag}</p>
                  ))}
                </div>
              )}
            </div>
          )}
        </Card>
      ))}
    </div>
  );
}
