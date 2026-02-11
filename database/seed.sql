INSERT INTO organizations (name, subscription_tier)
VALUES ('Demo Org', 'professional')
ON CONFLICT (name) DO NOTHING;
