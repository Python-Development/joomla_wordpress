import sqlalchemy as db
import datetime
import transliterate
import re


def select_old_data(jos_table):
    engine = db.create_engine('mysql+pymysql://u_guzanov:12345@localhost/guzanov_db?charset=utf8mb4&binary_prefix=true')
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table(jos_table, metadata, autoload=True, autoload_with=engine)
    query = db.select([table])
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    return result_set


def insert_new_data():
    engine = db.create_engine('mysql+pymysql://root:''@localhost/guzanov?charset=utf8mb4&binary_prefix=true')
    connection = engine.connect()
    metadata = db.MetaData()

    wp_users = db.Table('wp_users', metadata,
                        db.Column('Id', db.Integer(), primary_key=True),
                        db.Column('user_login', db.String(60), unique=True),
                        db.Column('user_pass', db.String(255)),
                        db.Column('user_nicename', db.String(50), unique=True),
                        db.Column('user_email', db.String(100), unique=True),
                        db.Column('user_url', db.String(100), default=''),
                        db.Column('user_registered', db.DateTime()),
                        db.Column('user_activation_key', db.String(255)),
                        db.Column('user_status', db.Integer(), default=0),
                        db.Column('display_name', db.String(250))
                        )
    wp_posts = db.Table('wp_posts', metadata,
                        db.Column('Id', db.Integer()),
                        db.Column('post_author', db.Integer(), default=0),
                        db.Column('post_date', db.DateTime(), default='0000-00-00 00:00:00'),
                        db.Column('post_date_gmt', db.DateTime(), default='0000-00-00 00:00:00'),
                        db.Column('post_content', db.TEXT, default=''),
                        db.Column('post_title', db.TEXT, default=''),
                        db.Column('post_excerpt', db.TEXT, default=''),
                        db.Column('post_status', db.String(20), default='publish'),
                        db.Column('comment_status', db.String(20), default='open'),
                        db.Column('ping_status', db.String(20), default='open'),
                        db.Column('post_password', db.String(255)),
                        db.Column('post_name', db.String(200), unique=True),
                        db.Column('to_ping', db.TEXT, default=''),
                        db.Column('pinged', db.TEXT, default=''),
                        db.Column('post_modified', db.DateTime(), default='0000-00-00 00:00:00'),
                        db.Column('post_modified_gmt', db.DateTime(), default='0000-00-00 00:00:00'),
                        db.Column('post_content_filtered', db.TEXT, default=''),
                        db.Column('post_parent', db.Integer(), default=0),
                        db.Column('guid', db.String(255)),
                        db.Column('menu_order', db.Integer(), default=0),
                        db.Column('post_type', db.String(20), default='post'),
                        db.Column('post_mime_type', db.String(100), default=''),
                        db.Column('comment_count', db.Integer(), default=0),
                        )
    wp_terms = db.Table('wp_terms', metadata,
                        db.Column('term_id', db.Integer(), default=0),
                        db.Column('name', db.String(200), default='post'),
                        db.Column('slug', db.String(200), default='post'),
                        db.Column('term_group', db.Integer(), default=0),
                        )
    wp_term_relationships = db.Table('wp_term_relationships', metadata,
                                     db.Column('object_id', db.Integer(), default=0),
                                     db.Column('term_taxonomy_id', db.Integer(), default=0),
                                     db.Column('term_order', db.Integer(), default=0)
                                     )
    #  ----- запускаю цикл який потрібно -----
    # for item in select_old_data('jos_users'):
    #     query = db.insert(wp_users).values(
    #         user_login=item[2],
    #         user_pass='12345',
    #         user_nicename=item[1],
    #         user_email=item[3],
    #         user_registered=item[9],
    #         user_activation_key=item[11],
    #         display_name=item[2]
    #     )
    #     connection.execute(query)

    for item in select_old_data('jos_content'):
        query = db.insert(wp_posts).values(
            Id=item[0],
            post_author=item[10],
            post_date=item[16],
            post_content=item[4],
            post_title=item[1],
            post_name=transliterate.translit(re.sub("[@#$!?',.]", "", re.sub(" +", "-", item[1])), reversed=True),
            post_modified=item[12],
            post_parent=item[22],
        )
        connection.execute(query)

    # for item in select_old_data('jos_categories'):
    #     query = db.insert(wp_terms).values(
    #         term_id=item[0],
    #         name=item[3],
    #         slug=item[3],
    #     )
    #     connection.execute(query)

    # for post in select_old_data('jos_content'):
    #     query = db.insert(wp_term_relationships).values(
    #         object_id=post[0],
    #         term_taxonomy_id=post[8]
    #     )
    #     connection.execute(query)


if __name__ == '__main__':
    insert_new_data()
