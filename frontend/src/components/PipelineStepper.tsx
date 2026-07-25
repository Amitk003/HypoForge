const STAGE_LABELS = [
  'Literature Scout',
  'Data Analysis',
  'Generator',
  'Critic',
  'Evolver',
  'Simulator',
  'Experiment Designer',
  'Meta-Reviewer',
];

const STAGE_KEYS = [
  'literature_scout',
  'data_analysis',
  'hypothesis_generator',
  'critic',
  'evolver',
  'simulator',
  'experiment_designer',
  'meta_reviewer',
];

interface PipelineStepperProps {
  timings: Record<string, number>;
  errorKeys: string[];
}

function getStatus(key: string, timings: Record<string, number>, errorKeys: string[]) {
  if (key in timings) return 'complete';
  if (errorKeys.includes(key)) return 'error';
  return 'pending';
}

export default function PipelineStepper({ timings, errorKeys }: PipelineStepperProps) {
  return (
    <div className="flex items-center gap-0 my-6 overflow-x-auto">
      {STAGE_KEYS.map((key, i) => {
        const status = getStatus(key, timings, errorKeys);
        const dotClass =
          status === 'complete'
            ? 'bg-accent-success text-white'
            : status === 'error'
            ? 'bg-accent-danger text-white'
            : 'bg-border-default text-text-tertiary';
        const dotContent =
          status === 'complete' ? '\u2713' : status === 'error' ? '\u2717' : String(i + 1);

        const lineClass =
          i < STAGE_KEYS.length - 1 &&
          getStatus(STAGE_KEYS[i + 1], timings, errorKeys) === 'complete'
            ? 'bg-accent-success'
            : 'bg-border-default';

        return (
          <div key={key} className="flex items-center flex-1">
            <div className="flex flex-col items-center">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold flex-shrink-0 ${dotClass}`}
              >
                {dotContent}
              </div>
              <div className="text-[10px] text-text-secondary text-center mt-1 max-w-[80px] leading-tight">
                {STAGE_LABELS[i]}
              </div>
            </div>
            {i < STAGE_KEYS.length - 1 && (
              <div className={`h-0.5 flex-1 min-w-4 ${lineClass}`} />
            )}
          </div>
        );
      })}
    </div>
  );
}
