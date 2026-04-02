"""initial

Revision ID: 0001
Revises:
Create Date: 2026-04-01

"""
from __future__ import annotations
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "gastos_mensais",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("municipio", sa.String(150), nullable=False),
        sa.Column("mes_ano", sa.Date(), nullable=False),
        sa.Column("total_cesta", sa.Numeric(10, 2), nullable=False),
        sa.Column("carne", sa.Numeric(10, 2), nullable=True),
        sa.Column("leite", sa.Numeric(10, 2), nullable=True),
        sa.Column("feijao", sa.Numeric(10, 2), nullable=True),
        sa.Column("arroz", sa.Numeric(10, 2), nullable=True),
        sa.Column("farinha", sa.Numeric(10, 2), nullable=True),
        sa.Column("batata", sa.Numeric(10, 2), nullable=True),
        sa.Column("tomate", sa.Numeric(10, 2), nullable=True),
        sa.Column("pao", sa.Numeric(10, 2), nullable=True),
        sa.Column("cafe", sa.Numeric(10, 2), nullable=True),
        sa.Column("banana", sa.Numeric(10, 2), nullable=True),
        sa.Column("acucar", sa.Numeric(10, 2), nullable=True),
        sa.Column("oleo", sa.Numeric(10, 2), nullable=True),
        sa.Column("manteiga", sa.Numeric(10, 2), nullable=True),
        sa.Column("criado_em", sa.DateTime(), server_default=sa.text("GETDATE()"), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(), server_default=sa.text("GETDATE()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("municipio", "mes_ano", name="uk_gasto_municipio_mes"),
    )

    op.create_table(
        "eventos_externos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("titulo", sa.String(150), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("data_inicio", sa.Date(), nullable=False),
        sa.Column("data_fim", sa.Date(), nullable=False),
        sa.Column("impacto", sa.String(20), nullable=False),
        sa.Column("criado_em", sa.DateTime(), server_default=sa.text("GETDATE()"), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(), server_default=sa.text("GETDATE()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("eventos_externos")
    op.drop_table("gastos_mensais")
