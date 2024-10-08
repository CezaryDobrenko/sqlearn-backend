"""tag

Revision ID: 739e42a02c87
Revises: e9f89acc3a9c
Create Date: 2022-11-03 21:19:31.940462

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "739e42a02c87"
down_revision = "e9f89acc3a9c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tag",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "modified",
            sa.DateTime(),
            server_default=sa.text("timezone('UTC', now())"),
            nullable=True,
        ),
        sa.Column(
            "created",
            sa.DateTime(),
            server_default=sa.text("timezone('UTC', now())"),
            nullable=True,
        ),
        sa.Column("name", sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tag")
    # ### end Alembic commands ###
