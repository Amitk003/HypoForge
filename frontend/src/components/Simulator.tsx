import { useState, type ChangeEvent } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { runSimulation, type SimulationResult } from '@/lib/api';

interface SimulatorProps {
  runId: string;
  variables?: string[];
}

export default function Simulator({ runId, variables = [] }: SimulatorProps) {
  const [target, setTarget] = useState('');
  const [intervention, setIntervention] = useState('');
  const [value, setValue] = useState('');
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSimulate() {
    if (!target || !intervention || !value) return;
    setLoading(true);
    setError('');
    try {
      const res = await runSimulation(runId, target, intervention, Number(value));
      setResult(res);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  const variableOptions = variables.length > 0;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Counterfactual Simulator</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {variableOptions ? (
          <>
            <div>
              <Label>Target variable</Label>
              <Select value={target} onValueChange={(v) => v && setTarget(v)}>
                <SelectTrigger><SelectValue placeholder="Select target" /></SelectTrigger>
                <SelectContent>
                  {variables.map((v) => (
                    <SelectItem key={v} value={v}>{v}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Intervention variable</Label>
              <Select value={intervention} onValueChange={(v) => v && setIntervention(v)}>
                <SelectTrigger><SelectValue placeholder="Select intervention" /></SelectTrigger>
                <SelectContent>
                  {variables.map((v) => (
                    <SelectItem key={v} value={v}>{v}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </>
        ) : (
          <>
            <div>
              <Label>Target variable</Label>
              <Input
                placeholder="e.g. temperature"
                value={target}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setTarget(e.target.value)}
              />
            </div>
            <div>
              <Label>Intervention variable</Label>
              <Input
                placeholder="e.g. green_space"
                value={intervention}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setIntervention(e.target.value)}
              />
            </div>
          </>
        )}
        <div>
          <Label>Intervention value</Label>
          <Input
            type="number"
            placeholder="e.g. 96"
            value={value}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setValue(e.target.value)}
          />
        </div>
        <Button onClick={handleSimulate} disabled={loading} className="w-full">
          {loading ? 'Simulating...' : 'Run Simulation'}
        </Button>
        {error && <p className="text-sm text-accent-danger">{error}</p>}
        {result && (
          <div className="bg-bg-page border border-border-default rounded-md p-3 space-y-1 text-sm">
            <p>
              Baseline: <strong>{result.baseline_outcome.toFixed(4)}</strong>
            </p>
            <p>
              Predicted: <strong>{result.predicted_outcome.toFixed(4)}</strong>
            </p>
            <p>
              Delta:{' '}
              <strong className={result.delta >= 0 ? 'text-accent-success' : 'text-accent-danger'}>
                {result.delta >= 0 ? '+' : ''}{result.delta.toFixed(4)}
              </strong>
            </p>
            <p>
              95% CI: <code>[{result.ci_lower.toFixed(4)}, {result.ci_upper.toFixed(4)}]</code>
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
