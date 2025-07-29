import pytest
import time
import os
from .feed2json import feed2json, struct_time_to_rfc3339, gfnn  

# 测试 struct_time_to_rfc3339 函数
def test_struct_time_to_rfc3339():
    # 创建测试时间
    struct_time = time.struct_time((2023, 5, 15, 12, 30, 45, 0, 135, 0))
    
    # 转换并验证格式
    result = struct_time_to_rfc3339(struct_time)
    assert result == "2023-05-15T12:30:45Z"
    
    # 测试无效输入
    assert struct_time_to_rfc3339(None) is None
    assert struct_time_to_rfc3339("invalid") is None

# 测试 gfnn 函数
def test_gfnn():
    test_dict = {
        "a": 1,
        "b": None,
        "c": 3
    }
    
    # 测试返回第一个非None值
    assert gfnn(test_dict, "a", "b") == 1
    assert gfnn(test_dict, "b", "c") == 3
    assert gfnn(test_dict, "d", "e") is None
    assert gfnn(test_dict, "d", "a") == 1

# 测试 feed2json 函数
def test_feed2json_no_args():
    # 测试没有提供任何参数时抛出异常
    with pytest.raises(ValueError, match="Must provide one of"):
        feed2json()

# 无效的 feed 内容
def test_feed2json_invalid_feed(): 
    # 测试空的feed内容
    with pytest.raises(ValueError, match="No feed found"):
        feed2json(feed_url="http://127.0.0.1")

def assert_feed(results):
    assert results["title"] == "示例博客"
    assert results["feed_url"] == "https://example.com/blog"
    assert results["home_page_url"] == "https://example.com/blog"
    assert results["description"] == "这是一个用于测试的示例RSS源"
    assert results["language"] == "zh-cn"
    assert len(results["items"]) == 3
    assert results["items"][0]["title"] == "第一篇测试文章"
    assert results["items"][0]["url"] == "https://example.com/blog/post1"
    assert results["items"][0]["date_published"] == "2025-07-15T09:00:00Z"
    assert results["items"][0]["date_modified"] == "2025-07-15T09:00:00Z"
    assert results["items"][0]["tags"] == ["测试", "技术"]
    assert results["items"][1]["title"] == "第二篇测试文章"
    assert results["items"][1]["url"] == "https://example.com/blog/post2"
    assert results["items"][1]["date_published"] == "2025-07-15T08:00:00Z"
    assert results["items"][1]["date_modified"] == "2025-07-15T08:00:00Z"
    assert results["items"][1]["tags"] == ["测试"]
    assert results["items"][1]["content_html"] == "<p>这是第二篇文章的详细内容</p>"
    assert results["items"][1]["content_text"] == "这是第二篇文章的纯文本内容"
    assert results["items"][2]["title"] == "带附件的文章"
    assert results["items"][2]["url"] == "https://example.com/blog/post3"
    assert results["items"][2]["date_published"] == "2025-07-15T07:00:00Z"
    assert results["items"][2]["date_modified"] == "2025-07-15T07:00:00Z"
    assert len(results["items"][2]["attachments"]) == 1
    assert results["items"][2]["attachments"][0]["url"] == "https://example.com/podcast.mp3"
    assert results["items"][2]["attachments"][0]["size_in_bytes"] == 10240000
    assert results["items"][2]["attachments"][0]["mime_type"] == "audio/mpeg"
    assert results["items"][2]["attachments"][0]["title"] == ""
    assert results["items"][2]["attachments"][0]["duration_in_seconds"] is None

# 测试有效的 RSS feed 解析
def test_feed2json_valid_rss():
    # 模拟RSS feed内容
    rss_feed = """
            <?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0">
            <channel>
                <title>示例博客</title>
                <link>https://example.com/blog</link>
                <description>这是一个用于测试的示例RSS源</description>
                <language>zh-cn</language>
                <pubDate>Tue, 15 Jul 2025 10:00:00 GMT</pubDate>
                <lastBuildDate>Tue, 15 Jul 2025 10:00:00 GMT</lastBuildDate>
                <generator>手动生成</generator>
                <managingEditor>editor@example.com</managingEditor>
                <webMaster>webmaster@example.com</webMaster>
                
                <item>
                <title>第一篇测试文章</title>
                <link>https://example.com/blog/post1</link>
                <description>这是第一篇测试文章的摘要内容</description>
                <author>author@example.com</author>
                <pubDate>Tue, 15 Jul 2025 09:00:00 GMT</pubDate>
                <guid isPermaLink="true">https://example.com/blog/post1</guid>
                <category>测试</category>
                <category>技术</category>
                </item>
                
                <item>
                <title>第二篇测试文章</title>
                <link>https://example.com/blog/post2</link>
                <description>这是第二篇测试文章的摘要内容</description>
                <author>author@example.com</author>
                <pubDate>Tue, 15 Jul 2025 08:00:00 GMT</pubDate>
                <guid isPermaLink="true">https://example.com/blog/post2</guid>
                <category>测试</category>
                <content:encoded><![CDATA[<p>这是第二篇文章的详细内容</p>]]></content:encoded>
                <text:plain>这是第二篇文章的纯文本内容</text:plain>
                </item>
                
                <item>
                <title>带附件的文章</title>
                <link>https://example.com/blog/post3</link>
                <description>包含媒体附件的测试文章</description>
                <author>author@example.com</author>
                <pubDate>Tue, 15 Jul 2025 07:00:00 GMT</pubDate>
                <guid isPermaLink="true">https://example.com/blog/post3</guid>
                <enclosure url="https://example.com/podcast.mp3" length="10240000" type="audio/mpeg"/>
                </item>
            </channel>
            </rss>
        """

    # 通过字符串解析
    results = feed2json(feed_string=rss_feed)
    assert_feed(results)

    # 通过文件解析
    with open("test_feed.xml", "w") as f:
        f.write(rss_feed)
    result_file = feed2json(feed_file_path="test_feed.xml")
    os.remove("test_feed.xml")
    assert_feed(result_file)

def test_feed2json_valid_atom():
    atom_feed = """
            <?xml version="1.0" encoding="UTF-8"?>
            <feed xmlns="http://www.w3.org/2005/Atom" 
                xmlns:content="http://purl.org/rss/1.0/modules/content/"
                xmlns:media="http://search.yahoo.com/mrss/">
            <title>示例博客</title>
            <link href="https://example.com/blog" rel="alternate"/>
            <id>https://example.com/blog</id>
            <updated>Tue, 15 Jul 2025 10:00:00 GMT</updated>
            <language>zh-cn</language>
            <author>
                <name>editor@example.com</name>
            </author>
            <generator>手动生成</generator>
            <subtitle>这是一个用于测试的示例RSS源</subtitle>

            <!-- 第一篇测试文章 -->
            <entry>
                <title>第一篇测试文章</title>
                <link href="https://example.com/blog/post1" rel="alternate"/>
                <id>https://example.com/blog/post1</id>
                <updated>2025-07-15T09:00:00Z</updated>
                <published>2025-07-15T09:00:00Z</published>
                <author>
                <name>author@example.com</name>
                </author>
                <summary>这是第一篇测试文章的摘要内容</summary>
                <category term="测试" />
                <category term="技术" />
            </entry>

            <!-- 第二篇测试文章 -->
            <entry>
                <title>第二篇测试文章</title>
                <link href="https://example.com/blog/post2" rel="alternate"/>
                <id>https://example.com/blog/post2</id>
                <published>Tue, 15 Jul 2025 08:00:00 GMT</published>
                <updated>Tue, 15 Jul 2025 08:00:00 GMT</updated>
                <author>
                <name>author@example.com</name>
                </author>
                <content type="text">这是第二篇文章的纯文本内容</content>
                <content type="html"><![CDATA[<p>这是第二篇文章的详细内容</p>]]></content>
                <category term="测试" />
            </entry>

            <!-- 带附件的文章 -->
            <entry>
                <title>带附件的文章</title>
                <link href="https://example.com/blog/post3" rel="alternate"/>
                <id>https://example.com/blog/post3</id>
                <published>Tue, 15 Jul 2025 07:00:00 GMT</published>
                <updated>Tue, 15 Jul 2025 07:00:00 GMT</updated>
                <author>
                <name>author@example.com</name>
                </author>
                <summary>包含媒体附件的测试文章</summary>
                <link rel="enclosure" 
                    href="https://example.com/podcast.mp3" 
                    type="audio/mpeg" 
                    length="10240000" />
            </entry>
            </feed>
        """

    # 通过字符串解析
    results = feed2json(feed_string=atom_feed)
    assert_feed(results)

    # 通过文件解析
    with open("test_feed.xml", "w") as f:
        f.write(atom_feed)
    result_file = feed2json(feed_file_path="test_feed.xml")
    os.remove("test_feed.xml")
    assert_feed(result_file)

# 测试多内容类型的处理
def test_feed2json_multiple_content_types():
    # 模拟包含多种内容类型的Atom feed
    atom_feed = """<?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <title>Multi-Content Feed</title>
        <entry>
            <title>Test Entry</title>
            <content type="text/html">&lt;p&gt;HTML content&lt;/p&gt;</content>
            <content type="text/plain">Plain text content</content>
        </entry>
    </feed>"""
    
    result = feed2json(feed_string=atom_feed)
    item = result["items"][0]
    
    assert item["content_html"] == "<p>HTML content</p>"
    assert item["content_text"] == "Plain text content"

# 测试作者和标签处理
def test_feed2json_authors_and_tags():
    # 模拟包含作者和标签的RSS
    rss_feed = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
    <channel>
        <title>Author Test</title>
        <author>John Doe</author>
        <item>
            <title>Tagged Item</title>
            <category>Tech</category>
            <category>News</category>
            <author>Jane Smith</author>
        </item>
    </channel>
    </rss>"""
    
    result = feed2json(feed_string=rss_feed)
    
    # 检查feed级作者
    assert result["authors"][0]["name"] == "John Doe"
    
    # 检查item级作者和标签
    item = result["items"][0]
    assert item["authors"] == ["Jane Smith"]
    assert "Tech" in item["tags"]
    assert "News" in item["tags"]

# 测试日期转换
def test_feed2json_date_conversion():
    # 创建带日期的feed
    rss_feed = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
    <channel>
        <title>Date Test</title>
        <lastBuildDate>Mon, 15 May 2023 12:00:00 GMT</lastBuildDate>
        <item>
            <title>Date Item</title>
            <pubDate>Mon, 15 May 2023 10:00:00 GMT</pubDate>
        </item>
    </channel>
    </rss>"""
    
    result = feed2json(feed_string=rss_feed)
    item = result["items"][0]
    
    # 验证日期转换
    assert item["date_published"] == "2023-05-15T10:00:00Z"
    # 对于RSS 2.0，updated_parsed通常与published_parsed相同
    assert item["date_modified"] == "2023-05-15T10:00:00Z"

# 测试字段优先级
def test_gfnn_priority():
    test_data = {
        "primary": "value1",
        "secondary": "value2",
        "empty": None
    }
    
    # 测试优先级顺序
    assert gfnn(test_data, "primary", "secondary") == "value1"
    assert gfnn(test_data, "missing", "primary") == "value1"
    assert gfnn(test_data, "empty", "secondary") == "value2"
    assert gfnn(test_data, "missing1", "missing2") is None

# 测试图标和favicon处理
def test_feed2json_icons():
    # 模拟包含图标的feed
    atom_feed = """<?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <title>Icon Test</title>
        <icon>http://example.com/icon.ico</icon>
        <logo>http://example.com/logo.png</logo>
    </feed>"""
    
    result = feed2json(feed_string=atom_feed)
    
    # 验证图标分配
    assert result["icon"] == "http://example.com/icon.ico"
    assert result["favicon"] == "http://example.com/logo.png"

# 测试：部分无效的feed处理
def test_feed2json_partial_feed():
    # 模拟部分有效的feed
    partial_feed = """<rss version="2.0">
    <channel>
        <title>Partial Feed</title>
        <item>
            <title>Item without ID or Link</title>
        </item>
    </channel>
    </rss>"""
    
    result = feed2json(feed_string=partial_feed)
    assert result["title"] == "Partial Feed"
    item = result["items"][0]
    assert item["title"] == "Item without ID or Link"
    assert item["id"] is None
    assert item["url"] is None

# 测试：没有条目的feed
def test_feed2json_feed_without_items():
    # 模拟没有条目的feed
    no_items_feed = """<rss version="2.0">
    <channel>
        <title>Feed Without Items</title>
        <link>http://example.com</link>
    </channel>
    </rss>"""
    
    result = feed2json(feed_string=no_items_feed)
    assert result["title"] == "Feed Without Items"
    assert len(result["items"]) == 0

# 测试：时区处理
def test_feed2json_timezone_handling():
    # 创建带时区的feed
    rss_feed = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
    <channel>
        <title>Timezone Test</title>
        <item>
            <title>Timezone Item</title>
            <pubDate>Mon, 15 May 2023 10:00:00 +0200</pubDate>
        </item>
    </channel>
    </rss>"""
    
    result = feed2json(feed_string=rss_feed)
    item = result["items"][0]
    
    # 验证时区转换
    assert item["date_published"] == "2023-05-15T08:00:00Z"  # UTC时间