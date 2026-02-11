CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE organizations (
  id UUID PRIMARY KEY,
  name VARCHAR(200) UNIQUE NOT NULL,
  subscription_tier VARCHAR(30) NOT NULL,
  settings JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE users (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  email VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  full_name VARCHAR(200) NOT NULL,
  role VARCHAR(20) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE calls (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  user_id UUID NOT NULL REFERENCES users(id),
  file_name VARCHAR(255) NOT NULL,
  storage_url VARCHAR(500) NOT NULL,
  transcript TEXT,
  status VARCHAR(30) NOT NULL,
  talk_ratio_rep DOUBLE PRECISION NOT NULL DEFAULT 0,
  talk_ratio_prospect DOUBLE PRECISION NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE call_analysis (
  id UUID PRIMARY KEY,
  call_id UUID UNIQUE NOT NULL REFERENCES calls(id),
  executive_summary TEXT NOT NULL,
  sentiment_score DOUBLE PRECISION NOT NULL,
  buying_intent_score DOUBLE PRECISION NOT NULL,
  objections JSONB NOT NULL,
  action_items JSONB NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE knowledge_base (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  content TEXT NOT NULL,
  content_embedding vector(1536),
  type VARCHAR(50) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
