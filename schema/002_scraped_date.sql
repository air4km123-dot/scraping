-- Phase 2: replace the functional dedup index with a real stored column.
--
-- 001_init.sql's unique index used (scraped_at::date) directly, which
-- Postgres rejects for functional indexes unless every expression is
-- IMMUTABLE (a bare ::date cast is not, since it depends on session
-- timezone). We already switched that expression to a fixed UTC cast to
-- get past that error — but a stored generated column is cleaner going
-- forward: it's a normal column Supabase's upsert(on_conflict=...) can
-- target directly, and it's handy for querying "today's rows" too.

alter table scraped_data
    add column if not exists scraped_date date
    generated always as ((scraped_at at time zone 'utc')::date) stored;

drop index if exists uq_scraped_data_daily;

create unique index if not exists uq_scraped_data_daily
    on scraped_data (module, source_url, field, value, scraped_date);
