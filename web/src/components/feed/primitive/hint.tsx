/** The one muted line between a question and its answer area; it changes with state. */
export function Hint({ children }: { children: React.ReactNode }) {
  return <p className="text-small text-mute">{children}</p>;
}
