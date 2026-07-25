interface SpinnerProps {
  size?: number;
  text?: string;
}

export default function Spinner({ size = 20, text }: SpinnerProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-text-secondary">
      <svg
        className="animate-spin"
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M21 12a9 9 0 1 1-6.219-8.56" />
      </svg>
      {text && <p className="mt-2 text-sm">{text}</p>}
    </div>
  );
}

export function InlineSpinner({ size = 16 }: { size?: number }) {
  return (
    <svg
      className="animate-spin inline-block"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21 12a9 9 0 1 1-6.219-8.56" />
    </svg>
  );
}
