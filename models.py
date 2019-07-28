import sqlalchemy as sa


metadata = sa.MetaData()


Currency = sa.Table(
    'currency', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String)
)


Rate = sa.Table(
    'rate', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('currency_id', None, sa.ForeignKey('currency.id')),
    sa.Column('date', sa.DateTime),
    sa.Column('rate', sa.Float),
    sa.Column('volume', sa.Float)
)


def create_tables(engine):
    metadata.create_all(engine)
