"""Tablas definidas en 5FN

Revision ID: 94a1076ede3e
Revises: 
Create Date: 2025-04-05 21:57:28.943878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94a1076ede3e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('DIM_REGION',
    sa.Column('region_key', sa.UUID(), nullable=False),
    sa.Column('region_nombre', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('region_key'),
    sa.UniqueConstraint('region_nombre')
    )
    op.create_table('DIM_SEGMENTO',
    sa.Column('segmento_key', sa.UUID(), nullable=False),
    sa.Column('segmento_id', sa.String(length=50), nullable=False),
    sa.Column('nombre', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('segmento_key'),
    sa.UniqueConstraint('segmento_id')
    )
    op.create_table('DIM_CIUDAD',
    sa.Column('ciudad_key', sa.UUID(), nullable=False),
    sa.Column('ciudad_nombre', sa.String(length=100), nullable=False),
    sa.Column('region_key', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['region_key'], ['DIM_REGION.region_key'], ),
    sa.PrimaryKeyConstraint('ciudad_key'),
    sa.UniqueConstraint('ciudad_nombre')
    )
    op.create_table('DIM_CLIENTE_SEGMENTO',
    sa.Column('cliente_segmento_key', sa.UUID(), nullable=False),
    sa.Column('cliente_key', sa.UUID(), nullable=False),
    sa.Column('segmento_key', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['cliente_key'], ['DIM_CLIENTE.cliente_key'], ),
    sa.ForeignKeyConstraint(['segmento_key'], ['DIM_SEGMENTO.segmento_key'], ),
    sa.PrimaryKeyConstraint('cliente_segmento_key')
    )
    op.create_table('VENDEDOR_TIENDA',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('vendedor_key', sa.UUID(), nullable=False),
    sa.Column('tienda_key', sa.UUID(), nullable=False),
    sa.Column('fecha_contratacion', sa.Date(), nullable=False),
    sa.Column('fecha_renuncia', sa.Date(), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.CheckConstraint('fecha_renuncia IS NULL OR fecha_renuncia > fecha_contratacion', name='ck_fecha_renuncia_valida'),
    sa.ForeignKeyConstraint(['tienda_key'], ['DIM_TIENDA.tienda_key'], ),
    sa.ForeignKeyConstraint(['vendedor_key'], ['DIM_VENDEDOR.vendedor_key'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('DIM_CLIENTE', schema=None) as batch_op:
        batch_op.alter_column('ciudad',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('region',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.create_foreign_key(None, 'DIM_CIUDAD', ['ciudad'], ['ciudad_key'])
        batch_op.create_foreign_key(None, 'DIM_REGION', ['region'], ['region_key'])
        batch_op.drop_column('segmento')

    with op.batch_alter_table('DIM_TIENDA', schema=None) as batch_op:
        batch_op.alter_column('ciudad',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('region',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.create_unique_constraint('uq_nombre_direccion_ciudad', ['nombre_tienda', 'direccion', 'ciudad'])
        batch_op.create_foreign_key(None, 'DIM_CIUDAD', ['ciudad'], ['ciudad_key'])
        batch_op.create_foreign_key(None, 'DIM_REGION', ['region'], ['region_key'])

    with op.batch_alter_table('DIM_VENDEDOR', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_vendedor_id', ['vendedor_id'])
        batch_op.drop_constraint('DIM_VENDEDOR_tienda_key_fkey', type_='foreignkey')
        batch_op.drop_column('fecha_contratacion')
        batch_op.drop_column('fecha_renuncia')
        batch_op.drop_column('tienda_key')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('DIM_VENDEDOR', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tienda_key', sa.UUID(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('fecha_renuncia', sa.DATE(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('fecha_contratacion', sa.DATE(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('DIM_VENDEDOR_tienda_key_fkey', 'DIM_TIENDA', ['tienda_key'], ['tienda_key'])
        batch_op.drop_constraint('uq_vendedor_id', type_='unique')

    with op.batch_alter_table('DIM_TIENDA', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint('uq_nombre_direccion_ciudad', type_='unique')
        batch_op.alter_column('region',
               existing_type=sa.UUID(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('ciudad',
               existing_type=sa.UUID(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    with op.batch_alter_table('DIM_CLIENTE', schema=None) as batch_op:
        batch_op.add_column(sa.Column('segmento', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('region',
               existing_type=sa.UUID(),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.alter_column('ciudad',
               existing_type=sa.UUID(),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    op.drop_table('VENDEDOR_TIENDA')
    op.drop_table('DIM_CLIENTE_SEGMENTO')
    op.drop_table('DIM_CIUDAD')
    op.drop_table('DIM_SEGMENTO')
    op.drop_table('DIM_REGION')
    # ### end Alembic commands ###
