# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class P4Pipeline:
    def process_item(self, item, spider):  # type: ignore  # noqa: ARG002
        return item  # type: ignore
