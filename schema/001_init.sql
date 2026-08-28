-- Phase 0: shared schema for all scraper modules.
-- Every module writes into this one table so the pipeline stays uniform
-- as modules B, C, D, E get added later.

create table if not exists scraped_data (
    id           bigserial primary key,
    module       text not null,        -- e.g. 'module_a' — which scraper wrote this row
    source_url   text not null,        -- the exact page scraped
    field        text not null,        -- name of the data point, e.g. 'price', 'title'
    value        text,                 -- the scraped value (kept as text; cast in queries as needed)
    scraped_at   timestamptz not null default now()
);

-- Speeds up "give me the latest value per module/field" queries,
-- which is what the dashboard will run most often.
create index if not exists idx_scraped_data_module_field_time
    on scraped_data (module, field, scraped_at desc);

-- Loose duplicate guard: same module+field+value+source on the same day
-- won't insert twice, so a rerun of a module doesn't pollute history.
create unique index if not exists uq_scraped_data_daily
    on scraped_data (module, source_url, field, value, (scraped_at::date));
