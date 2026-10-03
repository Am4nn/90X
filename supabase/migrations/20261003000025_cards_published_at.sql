-- ===========================================================================
-- cards.published_at: which publish last sent this card.
--
-- `pipeline swap` activates "every archetyped card that is draft, live or
-- retired". Including `retired` is deliberate (a regenerated card keeps its id and
-- publish leaves `status` alone, so it arrives already retired), but it also
-- resurrects a card that was retired ON PURPOSE: one the refile check found did not
-- fit its archetype, or the key audit found contradicting its own explanation.
-- Production could not tell "in the current corpus" from "was in it once".
--
-- Every publish stamps each card it sends with one timestamp (the transaction's
-- now(), so identical across the whole run), and swap activates only cards that
-- carry the newest stamp. A card the latest publish left out keeps an older one and
-- stays retired.
--
-- Purely additive and nullable. Existing rows read NULL until the next publish
-- stamps them; swap refuses to run until some card carries a stamp.
-- ===========================================================================

alter table public.cards add column published_at timestamptz;

comment on column public.cards.published_at is
  'When the pipeline last published this card. Swap activates only the newest stamp.';
