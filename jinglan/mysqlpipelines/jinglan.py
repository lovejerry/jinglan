from .sql import Sql
from jinglan.items import JinglanItem


class JinglanPipeline(object):
    def process_item(self, item, spider):
        # deferToThread(self.process_item, item, spider)
        if isinstance(item, JinglanItem):
            name_id = item['name_id']
            ret = Sql.select_name(name_id)
            if ret[0] == 1:
                print("已经存在了")
                pass
            else:
                xs_name = item['name']
                xs_author = item['author']
                category = item['category']
                Sql.inset_book_info(xs_name, xs_author, category, name_id)
                print('开始存小说标题')