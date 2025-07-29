import logging
import os
import re
import sys
import time

from notion_client import Client
import pendulum
import requests
from retrying import retry
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
from weread2notionpro.utils  import (
    format_date,
    get_date,
    get_first_and_last_day_of_month,
    get_first_and_last_day_of_week,
    get_first_and_last_day_of_year,
    get_icon,
    get_number,
    get_relation,
    get_rich_text,
    get_title,
    timestamp_to_date,
    get_property_value,
    get_properties
)
TAG_ICON_URL = "https://www.notion.so/icons/tag_gray.svg"
USER_ICON_URL = "https://www.notion.so/icons/user-circle-filled_gray.svg"
TARGET_ICON_URL = "https://www.notion.so/icons/target_red.svg"
BOOKMARK_ICON_URL = "https://www.notion.so/icons/bookmark_gray.svg"


class NotionHelper:
    database_name_dict = {
        "BOOK_DATABASE_NAME": "书架",
        "REVIEW_DATABASE_NAME": "笔记",
        "BOOKMARK_DATABASE_NAME": "划线",
        "DAY_DATABASE_NAME": "日",
        "WEEK_DATABASE_NAME": "周",
        "MONTH_DATABASE_NAME": "月",
        "YEAR_DATABASE_NAME": "年",
        "CATEGORY_DATABASE_NAME": "分类",
        "AUTHOR_DATABASE_NAME": "作者",
        "CHAPTER_DATABASE_NAME": "章节",
        "READ_DATABASE_NAME": "阅读记录",
        "SETTING_DATABASE_NAME": "设置",
    }
    database_id_dict = {}
    heatmap_block_id = None
    show_color = True
    block_type = "callout"
    sync_bookmark = True
    def __init__(self):
        notion_dict = self.get_notion_data()
        if not notion_dict:
            sys.exit(0)
        self.client = Client(auth = notion_dict.get("access_token"),log_level=logging.ERROR)
        self.__cache = {}
        self.page_id = self.extract_page_id(notion_dict.get("duplicated_template_id"))
        self.search_database(self.page_id)
        for key in self.database_name_dict.keys():
            if os.getenv(key) != None and os.getenv(key) != "":
                self.database_name_dict[key] = os.getenv(key)
        self.book_database_id = self.database_id_dict.get(
            self.database_name_dict.get("BOOK_DATABASE_NAME")
        )
        self.review_database_id = self.database_id_dict.get(
            self.database_name_dict.get("REVIEW_DATABASE_NAME")
        )
        self.bookmark_database_id = self.database_id_dict.get(
            self.database_name_dict.get("BOOKMARK_DATABASE_NAME")
        )
        self.day_database_id = self.database_id_dict.get(
            self.database_name_dict.get("DAY_DATABASE_NAME")
        )
        self.week_database_id = self.database_id_dict.get(
            self.database_name_dict.get("WEEK_DATABASE_NAME")
        )
        self.month_database_id = self.database_id_dict.get(
            self.database_name_dict.get("MONTH_DATABASE_NAME")
        )
        self.year_database_id = self.database_id_dict.get(
            self.database_name_dict.get("YEAR_DATABASE_NAME")
        )
        self.category_database_id = self.database_id_dict.get(
            self.database_name_dict.get("CATEGORY_DATABASE_NAME")
        )
        self.author_database_id = self.database_id_dict.get(
            self.database_name_dict.get("AUTHOR_DATABASE_NAME")
        )
        self.chapter_database_id = self.database_id_dict.get(
            self.database_name_dict.get("CHAPTER_DATABASE_NAME")
        )
        self.read_database_id = self.database_id_dict.get(
            self.database_name_dict.get("READ_DATABASE_NAME")
        )  
        self.setting_database_id = self.database_id_dict.get(
            self.database_name_dict.get("SETTING_DATABASE_NAME")
        )
        self.update_book_database()
        if self.read_database_id is None:
            self.create_database()
        if self.setting_database_id is None:
            self.create_setting_database()
        if self.setting_database_id:
            self.insert_to_setting_database()
        self.bookmark_database_properties=self.get_property_type(self.bookmark_database_id)
        for key,value in self.bookmark_database_properties.items():
            if value  =="title":
                self.bookmark_database_title = key
        self.review_database_properties=self.get_property_type(self.review_database_id)
        for key,value in self.review_database_properties.items():
            if value  =="title":
                self.review_database_title = key

    def get_property_type(self,database_id):
        """获取一个database的property和类型的映射关系"""
        result = {}
        r = self.client.databases.retrieve(database_id=database_id)
        for key,value in r.get("properties").items():
            result[key] = value.get("type")
        return result

    def extract_page_id(self, notion_url):
        # 正则表达式匹配 32 个字符的 Notion page_id
        match = re.search(
            r"([a-f0-9]{32}|[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
            notion_url,
        )
        if match:
            return match.group(0)
        else:
            raise Exception(f"获取NotionID失败，请检查输入的Url是否正确")
    

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get_notion_data(self):
        api_endpoint = "https://api.notionhub.app/get-notion-data" # 根据您的实际 Worker URL 修改
        github_repo_env = os.getenv('REPOSITORY')
        token = os.getenv("TOKEN")
        if not token:
            return None
        body = {'url': f"https://github.com/{github_repo_env}", "token": token}
        response = requests.post(api_endpoint, json=body, timeout=30)
        if response.ok and response.json().get("success"):
            return response.json().get("notionData")
            
            

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def search_database(self, block_id):
        children = self.client.blocks.children.list(block_id=block_id)["results"]
        # 遍历子块
        for child in children:
            # 检查子块的类型
            if child["type"] == "child_database":
                self.database_id_dict[child.get("child_database").get("title")] = (
                    child.get("id")
                )
            elif child["type"] == "embed" and child.get("embed").get("url"):
                if child.get("embed").get("url").startswith("https://heatmap.malinkang.com/"):
                    self.heatmap_block_id = child.get("id")
            # 如果子块有子块，递归调用函数
            if "has_children" in child and child["has_children"]:
                self.search_database(child["id"])

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def update_book_database(self):
        """更新数据库"""
        response = self.client.databases.retrieve(database_id=self.book_database_id)
        id = response.get("id")
        properties = response.get("properties")
        update_properties = {}
        if (
            properties.get("阅读时长") is None
            or properties.get("阅读时长").get("type") != "number"
        ):
            update_properties["阅读时长"] = {"number": {}}
        if (
            properties.get("书架分类") is None
            or properties.get("书架分类").get("type") != "select"
        ):
            update_properties["书架分类"] = {"select": {}}
        if (
            properties.get("豆瓣链接") is None
            or properties.get("豆瓣链接").get("type") != "url"
        ):
            update_properties["豆瓣链接"] = {"url": {}}
        if (
            properties.get("我的评分") is None
            or properties.get("我的评分").get("type") != "select"
        ):
            update_properties["我的评分"] = {"select": {}}
        if (
            properties.get("字数") is None
            or properties.get("字数").get("type") != "rich_text"
        ):
            update_properties["字数"] = {"number": {}}
        if (
            properties.get("价格") is None
            or properties.get("价格").get("type") != "rich_text"
        ):
            update_properties["价格"] = {"number": {}}
        if len(update_properties) > 0:
            self.client.databases.update(database_id=id, properties=update_properties)
    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def create_database(self):
        title = [
            {
                "type": "text",
                "text": {
                    "content": self.database_name_dict.get("READ_DATABASE_NAME"),
                },
            },
        ]
        properties = {
            "标题": {"title": {}},
            "时长": {"number": {}},
            "时间戳": {"number": {}},
            "日期": {"date": {}},
            "书架": {
                "relation": {
                    "database_id": self.book_database_id,
                    "single_property": {},
                }
            },
        }
        parent = parent = {"page_id": self.page_id, "type": "page_id"}
        self.read_database_id = self.client.databases.create(
            parent=parent,
            title=title,
            icon=get_icon("https://www.notion.so/icons/target_gray.svg"),
            properties=properties,
        ).get("id")    
        
    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def create_setting_database(self):
        title = [
            {
                "type": "text",
                "text": {
                    "content": self.database_name_dict.get("SETTING_DATABASE_NAME"),
                },
            },
        ]
        properties = {
            "标题": {"title": {}},
            "NotinToken": {"rich_text": {}},
            "NotinPage": {"rich_text": {}},
            "WeReadCookie": {"rich_text": {}},
            "根据划线颜色设置文字颜色": {"checkbox": {}},
            "同步书签": {"checkbox": {}},
            # "Cookie状态": {
            #     "select": {
            #         "options": [
            #             {"name": "可用", "color": "green"},
            #             {"name": "过期", "color": "red"},
            #         ]
            #     }
            # },
            "样式": {
                "select": {
                    "options": [
                        {"name": "callout", "color": "blue"},
                        {"name": "quote", "color": "green"},
                        {"name": "paragraph", "color": "purple"},
                        {"name": "bulleted_list_item", "color": "yellow"},
                        {"name": "numbered_list_item", "color": "pink"},
                    ]
                }
            },
            "最后同步时间": {"date": {}},
        }
        parent = parent = {"page_id": self.page_id, "type": "page_id"}
        self.setting_database_id = self.client.databases.create(
            parent=parent,
            title=title,
            icon=get_icon("https://www.notion.so/icons/gear_gray.svg"),
            properties=properties,
        ).get("id")

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def insert_to_setting_database(self):
        existing_pages = self.query(database_id=self.setting_database_id, filter={"property": "标题", "title": {"equals": "设置"}}).get("results")
        properties = {
            "标题": {"title": [{"type": "text", "text": {"content": "设置"}}]},
            "最后同步时间": {"date": {"start": pendulum.now("Asia/Shanghai").isoformat()}},
        }
        if existing_pages:
            remote_properties = existing_pages[0].get("properties")
            self.show_color = get_property_value(remote_properties.get("根据划线颜色设置文字颜色"))
            self.sync_bookmark = get_property_value(remote_properties.get("同步书签"))
            self.block_type = get_property_value(remote_properties.get("样式"))
            page_id = existing_pages[0].get("id")
            self.client.pages.update(page_id=page_id, properties=properties)
        else:
            properties["根据划线颜色设置文字颜色"] = {"checkbox": True}
            properties["同步书签"] = {"checkbox": True}
            properties["样式"] = {"select": {"name": "callout"}}
            self.client.pages.create(
                parent={"database_id": self.setting_database_id},
                properties=properties,
            )
  
        
    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def update_heatmap(self, block_id, url):
        # 更新 image block 的链接
        return self.client.blocks.update(block_id=block_id, embed={"url": url})

    def get_week_relation_id(self, date):
        year = date.isocalendar().year
        week = date.isocalendar().week
        week = f"{year}年第{week}周"
        start, end = get_first_and_last_day_of_week(date)
        properties = {"日期": get_date(format_date(start), format_date(end))}
        return self.get_relation_id(
            week, self.week_database_id, self.get_date_icon(date, "week"), properties
        )

    def get_month_relation_id(self, date):
        month = date.strftime("%Y年%-m月")
        start, end = get_first_and_last_day_of_month(date)
        properties = {"日期": get_date(format_date(start), format_date(end))}
        return self.get_relation_id(
            month, self.month_database_id, self.get_date_icon(date, "month"), properties
        )

    def get_year_relation_id(self, date):
        year = date.strftime("%Y")
        start, end = get_first_and_last_day_of_year(date)
        properties = {"日期": get_date(format_date(start), format_date(end))}
        return self.get_relation_id(
            year, self.year_database_id, self.get_date_icon(date, "year"), properties
        )

    def get_date_icon(self, date, type):
        return f"https://notion-icon.malinkang.com/?type={type}&date={date.strftime('%Y-%m-%d')}"

    def get_day_relation_id(self, date):
        new_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        timestamp = (new_date - timedelta(hours=8)).timestamp()
        day = new_date.strftime("%Y年%m月%d日")
        properties = {
            "日期": get_date(format_date(date)),
            "时间戳": get_number(timestamp),
        }
        if self.year_database_id is not None:
            properties["年"] = get_relation(
                [
                    self.get_year_relation_id(new_date),
                ]
            )
        if self.month_database_id is not None:
            properties["月"] = get_relation(
                [
                    self.get_month_relation_id(new_date),
                ]
            )
        if self.week_database_id is not None:
            properties["周"] = get_relation(
                [
                    self.get_week_relation_id(new_date),
                ]
            )
        return self.get_relation_id(
            day, self.day_database_id, self.get_date_icon(date, "day"), properties
        )
    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get_relation_id(self, name, id, icon, properties={}):
        key = f"{id}{name}"
        if key in self.__cache:
            return self.__cache.get(key)
        filter = {"property": "标题", "title": {"equals": name}}
        response = self.client.databases.query(database_id=id, filter=filter)
        if len(response.get("results")) == 0:
            parent = {"database_id": id, "type": "database_id"}
            properties["标题"] = get_title(name)
            page_id = self.client.pages.create(
                parent=parent, properties=properties, icon=get_icon(icon)
            ).get("id")
        else:
            page_id = response.get("results")[0].get("id")
        self.__cache[key] = page_id
        return page_id

    def insert_bookmark(self, id, bookmark):
        icon = get_icon(BOOKMARK_ICON_URL)
        item = {
            self.bookmark_database_title: bookmark.get("markText", ""),
            "bookId": bookmark.get("bookId"),
            "range": bookmark.get("range"),
            "bookmarkId": bookmark.get("bookmarkId"),
            "blockId": bookmark.get("blockId"),
            "chapterUid": bookmark.get("chapterUid"),
            "bookVersion": bookmark.get("bookVersion"),
            "colorStyle": bookmark.get("colorStyle"),
            "type": bookmark.get("type"),
            "style": bookmark.get("style"),
            "书籍": [id],
        }
        if "createTime" in bookmark:
            item["Date"] = bookmark.get("createTime")
        properties = get_properties(item, self.bookmark_database_properties)
        if item["Date"]:
            self.get_date_relation(properties, timestamp_to_date(item["Date"]))
        parent = {"database_id": self.bookmark_database_id, "type": "database_id"}
        self.create_page(parent, properties, icon)

    def insert_review(self, id, review):
        time.sleep(0.1)
        icon = get_icon(TAG_ICON_URL)
        item = {
            self.review_database_title: review.get("content", ""),
            "bookId": review.get("bookId"),
            "reviewId":review.get("reviewId"),
            "blockId": review.get("blockId"),
            "chapterUid": review.get("chapterUid"),
            "bookVersion": review.get("bookVersion"),
            "type": review.get("type"),
            "书籍": [id],
        }
        if "range" in review:
            item["range"] = review.get("range")
        if "star" in review:
            item["star"] = review.get("star")
        if "abstract" in review:
            item["abstract"] = review.get("abstract")
        if "createTime" in review:
            item["Date"] = int(review.get("createTime"))
        properties = get_properties(item, self.review_database_properties)
        if item["Date"]:
            self.get_date_relation(properties, timestamp_to_date(item["Date"]))
        parent = {"database_id": self.review_database_id, "type": "database_id"}
        self.create_page(parent, properties, icon)

    def insert_chapter(self, id, chapter):
        time.sleep(0.1)
        icon = {"type": "external", "external": {"url": TAG_ICON_URL}}
        properties = {
            "Name": get_title(chapter.get("title")),
            "blockId": get_rich_text(chapter.get("blockId")),
            "chapterUid": {"number": chapter.get("chapterUid")},
            "chapterIdx": {"number": chapter.get("chapterIdx")},
            "readAhead": {"number": chapter.get("readAhead")},
            "updateTime": {"number": chapter.get("updateTime")},
            "level": {"number": chapter.get("level")},
            "书籍": {"relation": [{"id": id}]},
        }
        parent = {"database_id": self.chapter_database_id, "type": "database_id"}
        self.create_page(parent, properties, icon)

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def update_book_page(self, page_id, properties):
        return self.client.pages.update(page_id=page_id, properties=properties)

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def update_page(self, page_id, properties, cover=None):
        if cover is None:
            return self.client.pages.update(page_id=page_id, properties=properties)
        return self.client.pages.update(
            page_id=page_id, properties=properties, cover=cover
        )


    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def create_page(self, parent, properties, icon):
        return self.client.pages.create(parent=parent, properties=properties, icon=icon)

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def create_book_page(self, parent, properties, icon):
        return self.client.pages.create(
            parent=parent, properties=properties, icon=icon, cover=icon
        )

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def query(self, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v}
        return self.client.databases.query(**kwargs)

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get_block_children(self, id):
        response = self.client.blocks.children.list(id)
        return response.get("results")

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def append_blocks(self, block_id, children):
        return self.client.blocks.children.append(block_id=block_id, children=children)

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def append_blocks_after(self, block_id, children, after):
        #奇怪不知道为什么会多插入一个children，没找到问题，先暂时这么解决，搜索是否有parent
        parent = self.client.blocks.retrieve(after).get("parent")
        if(parent.get("type")=="block_id"):
            after = parent.get("block_id")
        return self.client.blocks.children.append(
            block_id=block_id, children=children, after=after
        )

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def delete_block(self, block_id):
        try:
            return self.client.blocks.delete(block_id=block_id)
        except Exception as e:
            print(f"Error deleting block with ID {block_id}: {e}")
            return None

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get_all_book(self):
        """从Notion中获取所有的书籍"""
        results = self.query_all(self.book_database_id)
        books_dict = {}
        for result in results:
            bookId = get_property_value(result.get("properties").get("BookId"))
            if bookId not in books_dict:
                books_dict[bookId] = {
                    "pageId": result.get("id"),
                    "readingTime": get_property_value(
                        result.get("properties").get("阅读时长")
                    ),
                    "category": get_property_value(
                        result.get("properties").get("书架分类")
                    ),
                    "Sort": get_property_value(result.get("properties").get("Sort")),
                    "douban_url": get_property_value(
                        result.get("properties").get("豆瓣链接")
                    ),
                    "cover": result.get("cover"),
                    "myRating": get_property_value(
                        result.get("properties").get("我的评分")
                    ), 
                    "price": get_property_value(result.get("properties").get("价格")),
                    "wordCount": get_property_value(result.get("properties").get("字数")),
                    "image": get_property_value(result.get("properties").get("封面")),
                    "status": get_property_value(result.get("properties").get("阅读状态")),
                }
            else:
                print(f"delete {result.get('properties').get('书名').get('title')[0].get('text').get('content')}")
                self.delete_block(result.get("id"))
        return books_dict

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def query_all_by_book(self, database_id, filter):
        results = []
        has_more = True
        start_cursor = None
        while has_more:
            response = self.client.databases.query(
                database_id=database_id,
                filter=filter,
                start_cursor=start_cursor,
                page_size=100,
            )
            start_cursor = response.get("next_cursor")
            has_more = response.get("has_more")
            results.extend(response.get("results"))
        return results

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def query_all(self, database_id):
        """获取database中所有的数据"""
        results = []
        has_more = True
        start_cursor = None
        while has_more:
            response = self.client.databases.query(
                database_id=database_id,
                start_cursor=start_cursor,
                page_size=100,
            )
            start_cursor = response.get("next_cursor")
            has_more = response.get("has_more")
            results.extend(response.get("results"))
        return results

    def get_date_relation(self, properties, date,include=True):
        if self.year_database_id is not None:
            properties["年"] = get_relation(
                [
                    self.get_year_relation_id(date),
                ]
            )
        if self.month_database_id is not None:
            properties["月"] = get_relation(
                [
                    self.get_month_relation_id(date),
                ]
            )
        if self.week_database_id is not None:
            properties["周"] = get_relation(
                [
                    self.get_week_relation_id(date),
                ]
            )
        if (self.day_database_id is not None) and include:
            properties["日"] = get_relation(
                [
                    self.get_day_relation_id(date),
                ]
            )