-- Documents leave the app database.
--
-- They were raw scraped source text - book chapters, link tables, PDF output
-- with broken ligatures - rendered to users as if they were lessons. The
-- authored `lessons` table replaces them everywhere a person reads, and the
-- master copy stays in the pipeline's staging database and in the vector
-- index, which is all Coach's retrieval needs. Nothing in the app queries
-- this table any more.
--
-- Cards are regenerated from lessons, so the old column linking a card to the
-- chunk it was written from goes too. That link is exactly what let a card
-- ask about "the reference solution" the reader could never see.

alter table public.cards drop column if exists document_id;
drop table if exists public.documents;
