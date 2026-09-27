import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { BackLink } from "@/components/back-link";
import { Markdown } from "@/components/markdown";
import { PageHeader } from "@/components/page-header";
import { MarkStudied } from "@/components/tracker/missions";
import { requireViewer } from "@/lib/auth/viewer";
import { practiceFor, topicDetail } from "@/lib/library/queries";
import { isStudied } from "@/lib/tracker/service";

export async function generateMetadata({ params }: PageProps<"/library/topic/[slug]">): Promise<Metadata> {
  const { slug } = await params;
  return { title: slug.replace(/^[a-z]+-/, "").replace(/-/g, " ") };
}

export default async function TopicPage({ params }: PageProps<"/library/topic/[slug]">) {
  const viewer = await requireViewer();
  const { slug } = await params;
  const [detail, studied] = await Promise.all([topicDetail(slug), isStudied(viewer.id, slug)]);
  if (!detail?.lesson) notFound();
  const { topic, lesson, tricks } = detail;
  const practice = await practiceFor(lesson);

  return (
    <article className="mx-auto flex w-full max-w-3xl flex-col gap-6">
      <div className="flex flex-col gap-2">
        <BackLink href={`/library?area=${topic.domain}`}>Library</BackLink>
        <PageHeader title={topic.name} />
        <p className="text-small text-mute">{Math.max(1, Math.round((lesson.words ?? 0) / 200))} min read</p>
      </div>

      <Markdown>{lesson.bodyMd}</Markdown>

      {tricks.length > 0 && (
        <section className="flex flex-col gap-3">
          <h2 className="font-display text-heading font-semibold text-text">The shapes to reach for</h2>
          <div className="flex flex-col gap-3">
            {tricks.map((t) => (
              <div key={t.id} className="flex flex-col gap-2 rounded-xl border border-line bg-surface p-4">
                <h3 className="font-semibold text-text">{t.name}</h3>
                <Markdown>{t.idea}</Markdown>
              </div>
            ))}
          </div>
        </section>
      )}

      {practice.problems.length > 0 && (
        <section className="flex flex-col gap-3">
          <h2 className="font-display text-heading font-semibold text-text">Now go solve these</h2>
          <div className="divide-y divide-line rounded-xl border border-line bg-surface">
            {practice.problems.map((p) => (
              <Link
                key={p.slug}
                href={`/library/problem/${p.slug}`}
                className="flex items-baseline justify-between gap-3 px-4 py-3.5 hover:bg-surface-2"
              >
                <span className="flex flex-col gap-0.5">
                  <span className="font-semibold text-text">{p.title}</span>
                  {p.companies.length > 0 && <span className="text-small text-mute">Asked at {p.companies.join(", ")}</span>}
                </span>
                <span className="shrink-0 text-small text-mute">{p.difficulty}</span>
              </Link>
            ))}
          </div>
        </section>
      )}

      {practice.questions.length > 0 && (
        <section className="flex flex-col gap-3">
          <h2 className="font-display text-heading font-semibold text-text">Asked in real interviews</h2>
          <div className="divide-y divide-line rounded-xl border border-line bg-surface">
            {practice.questions.map((q) => (
              <a
                key={q.slug}
                href={q.url}
                target="_blank"
                rel="noreferrer"
                className="flex items-baseline justify-between gap-3 px-4 py-3.5 hover:bg-surface-2"
              >
                <span className="font-semibold text-text">{q.title} ↗</span>
                {q.difficulty && <span className="shrink-0 text-small text-mute">{q.difficulty}</span>}
              </a>
            ))}
          </div>
        </section>
      )}

      {topic.domain === "behavioral" && (
        <Link href="/me/stories" className="rounded-xl border border-line bg-surface p-4 text-small text-text-2 hover:border-cyan">
          The story is yours, not ours. Build it in your story bank &rarr;
        </Link>
      )}

      {topic.domain !== "dsa" && <MarkStudied slug={topic.slug} studied={studied} />}
    </article>
  );
}
