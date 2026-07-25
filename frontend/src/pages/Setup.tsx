import { useState, type ChangeEvent } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { InlineSpinner } from '@/components/Spinner';
import { runPipeline, type PipelineResponse } from '@/lib/api';

const PRESETS = [
  {
    label: 'Urban Climate',
    goal: 'How does urban green space affect local air temperature and air quality?',
  },
  {
    label: 'Environmental Health',
    goal: 'How does long-term exposure to air pollution and noise affect sleep quality in urban populations?',
  },
  {
    label: 'Biodiversity',
    goal: 'How do changes in local temperature and precipitation affect species diversity in forest ecosystems?',
  },
];

interface SetupProps {
  onPipelineComplete: (result: PipelineResponse) => void;
  onResearchGoalChange: (goal: string) => void;
}

export default function Setup({ onPipelineComplete, onResearchGoalChange }: SetupProps) {
  const [goal, setGoal] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [alpha, setAlpha] = useState('0.05');
  const [maxH, setMaxH] = useState('10');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [lastRun, setLastRun] = useState<PipelineResponse | null>(null);

  function handleGoalChange(value: string) {
    setGoal(value);
    onResearchGoalChange(value);
  }

  function applyPreset(preset: typeof PRESETS[number]) {
    handleGoalChange(preset.goal);
  }

  async function handleRun() {
    if (!goal.trim()) return;
    setLoading(true);
    setError('');
    try {
      const result = await runPipeline(goal, file || undefined, Number(alpha), Number(maxH));
      setLastRun(result);
      onPipelineComplete(result);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="md:col-span-2 space-y-4">
        <div>
          <Label htmlFor="goal">Research Goal</Label>
          <Textarea
            id="goal"
            placeholder="e.g. How does urban green space affect local air temperature and air quality?"
            className="h-[120px]"
            value={goal}
            onChange={(e: ChangeEvent<HTMLTextAreaElement>) => handleGoalChange(e.target.value)}
          />
        </div>
        <div className="flex flex-wrap gap-2">
          {PRESETS.map((p) => (
            <Button key={p.label} variant="outline" size="sm" onClick={() => applyPreset(p)}>
              {p.label}
            </Button>
          ))}
        </div>
        <div>
          <Label htmlFor="file">Upload data (CSV or Parquet)</Label>
          <Input
            id="file"
            type="file"
            accept=".csv,.parquet"
            onChange={(e: ChangeEvent<HTMLInputElement>) => setFile(e.target.files?.[0] || null)}
          />
        </div>
        <details className="text-sm text-text-secondary">
          <summary className="cursor-pointer font-medium">Advanced Settings</summary>
          <div className="mt-2 space-y-2 pl-2">
            <div>
              <Label htmlFor="alpha">Significance level (alpha)</Label>
              <Input
                id="alpha"
                type="number"
                step="0.001"
                value={alpha}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setAlpha(e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="maxH">Max hypotheses</Label>
              <Input
                id="maxH"
                type="number"
                step="1"
                value={maxH}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setMaxH(e.target.value)}
              />
            </div>
          </div>
        </details>
        <Button onClick={handleRun} disabled={loading || !goal.trim()} className="w-full">
          {loading ? <><InlineSpinner /> Running Pipeline...</> : 'Run Pipeline'}
        </Button>
        {error && (
          <div className="bg-accent-danger/10 border border-accent-danger/30 rounded-md p-3 text-sm text-accent-danger">
            {error}
          </div>
        )}
      </div>

      <div>
        {file && (
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Data Preview</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-text-secondary">{file.name}</p>
            </CardContent>
          </Card>
        )}
        {lastRun && (
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Last Run Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <p className="text-xs text-text-tertiary">Hypotheses</p>
                  <p className="font-semibold">{lastRun.hypothesis_count}</p>
                </div>
                <div>
                  <p className="text-xs text-text-tertiary">Simulations</p>
                  <p className="font-semibold">{lastRun.simulation_count}</p>
                </div>
                <div>
                  <p className="text-xs text-text-tertiary">Protocols</p>
                  <p className="font-semibold">{lastRun.protocol_count}</p>
                </div>
                <div>
                  <p className="text-xs text-text-tertiary">Errors</p>
                  <p className="font-semibold">{lastRun.error_count}</p>
                </div>
              </div>
              {lastRun.errors.length > 0 && (
                <>
                  <Separator className="my-2" />
                  <details>
                    <summary className="text-xs text-accent-warning cursor-pointer">
                      {lastRun.errors.length} warnings
                    </summary>
                    <div className="mt-1 space-y-1">
                      {lastRun.errors.map((e, i) => (
                        <p key={i} className="text-xs text-accent-warning">
                          {e}
                        </p>
                      ))}
                    </div>
                  </details>
                </>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
