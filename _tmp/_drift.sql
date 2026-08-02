SELECT 'draft_slot' t, count(*) n, min(created_at) first_c, max(created_at) last_c FROM engine_isolated.draft_slot
UNION ALL SELECT 'executable_draft', count(*), min(created_at), max(created_at) FROM engine_isolated.executable_draft;
