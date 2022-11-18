from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_alive" BOOL NOT NULL  DEFAULT True,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "name" VARCHAR(50),
    "email" VARCHAR(320) NOT NULL UNIQUE,
    "password" VARCHAR(256) NOT NULL
);
COMMENT ON TABLE "user" IS 'User model';
CREATE TABLE IF NOT EXISTS "friendship" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_alive" BOOL NOT NULL  DEFAULT True,
    "status_code" VARCHAR(9) NOT NULL  DEFAULT 'REQUESTED',
    "addressee_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "requester_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "specifier_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_friendship_request_6b9cfc" UNIQUE ("requester_id", "addressee_id")
);
COMMENT ON COLUMN "friendship"."status_code" IS 'REQUESTED: REQUESTED\nACCEPTED: ACCEPTED\nDECLINED: DECLINED\nBLOCKED: BLOCKED';
COMMENT ON TABLE "friendship" IS 'Friendship model';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
