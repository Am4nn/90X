-- Lessons the Coach wrote on demand.
--
-- The Coach can be asked something no lesson covers. Rather than answer from
-- the model's own memory, it writes a lesson through the same gates the
-- pipeline uses - the structural contract, a fact check, and a search of the
-- downloaded corpus that must find material first - and stores it here beside
-- the authored ones.
--
-- `written_by` is the marker that keeps it alive. `pipeline publish` is a
-- convergence: it upserts every staging lesson with status 'ok' and then
-- DELETES every row in public.lessons that staging no longer has. A lesson the
-- pipeline never wrote is, to that delete, an orphan - so without this column
-- the next publish would silently remove it. publish.py now excludes rows where
-- written_by is not null, and the check-coach-tools script proves it.
--
-- Null means the pipeline wrote it, which is every existing row.

alter table public.lessons
    add column if not exists written_by uuid references auth.users (id) on delete set null;

-- Small and sparse: the only query is "is this one the pipeline's?", and
-- publish's delete needs it on every run.
create index if not exists lessons_written_by_idx
    on public.lessons (written_by) where written_by is not null;

comment on column public.lessons.written_by is
    'The user whose Coach wrote this lesson on demand. Null means the pipeline wrote it, and pipeline publish owns the row. Non-null rows survive publish.';

-- No insert or update policy, deliberately. The Coach writes over the server
-- connection, which bypasses RLS; `authenticated` still cannot write a lesson
-- through the API, which is what the read-only policy from
-- 20260928000013_lessons.sql already assumed.
