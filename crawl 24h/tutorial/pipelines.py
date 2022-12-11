# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# from itemadapter import ItemAdapter

# class MysqlDemoPipeline:
#     def process_item(self, item, spider):
#         return item

# # useful for handling different item types with a single interface
import sqlite3

class SqliteDemoPipeline:

    def __init__(self):

        ## Create/Connect to database
        self.con = sqlite3.connect('crawl24h.db')

        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes(
            title TEXT,
            content TEXT,
            date TEXT,
            url TEXT,
            category TEXT,
            image TEXT  
        )
        """)


    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute("""
            INSERT INTO quotes (title, content, date, url, category, image) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            item['title'],
            str(item['content']),
            str(item['date']),
            item['url'],
            item['category'],
            item['image']
        ))

        ## Execute insert of data into database
        self.con.commit()
        return item
