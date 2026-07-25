import { Badge } from '@/components/ui/badge';

interface ScorePillProps {
  label: string;
  score: number;
}

export default function ScorePill({ label, score }: ScorePillProps) {
  const variant = score > 0.7 ? 'default' : score < 0.4 ? 'secondary' : 'outline';
  const colorClass = score > 0.7
    ? 'border-accent-success text-accent-success'
    : score < 0.4
    ? 'border-accent-warning text-accent-warning'
    : '';

  return (
    <Badge variant={variant} className={`mr-1 mb-0.5 font-mono font-medium ${colorClass}`}>
      {label} {score.toFixed(2)}
    </Badge>
  );
}
