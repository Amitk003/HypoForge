interface HeaderProps {
  researchGoal?: string;
}

export default function Header({ researchGoal }: HeaderProps) {
  return (
    <div className="mb-2">
      <div>
        <span className="text-xl font-semibold text-text-primary">HypoForge</span>
        <span className="ml-1 text-xs text-text-tertiary">AI Co-Scientist</span>
      </div>
      {researchGoal && (
        <div className="mt-1 text-sm text-text-secondary truncate max-w-[600px]">
          {researchGoal}
        </div>
      )}
    </div>
  );
}
