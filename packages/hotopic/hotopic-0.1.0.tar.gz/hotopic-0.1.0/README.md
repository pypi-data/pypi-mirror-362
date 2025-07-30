# Hot Topic Analyzer

Hot Topic Analyzer 是一个用于分析文本数据中热门话题的Python包。它使用先进的自然语言处理技术来识别和总结大量文本中的主要主题。

## 安装

你可以使用pip安装Hot Topic Analyzer：

```
pip install hot-topic-analyzer
```

## 使用方法

以下是一个基本的使用示例：

```python
from hotopic.hotopic import HoTopic
from hotopic.utils import Config

# 准备输入数据
input_data = [
    {"content_id": "1", "content": "这是第一篇关于黄金价格的文章..."},
    {"content_id": "2", "content": "这是第二篇关于黄金市场的文章..."},
    # ... 更多文章
]

# 创建配置
config = Config(
    min_content_length=10,
    max_content_length=1000,
    similarity_threshold=0.5,
    top_topics_count=10,
    max_keywords_per_topic=15,
    representative_docs_count=3,
    doc_preview_length=200,
    quality_weights={
        "coherence": 0.6,
        "distinctiveness": 0.2,
        "size_ratio": 0.2
    },
    seed=42,
    output_dir="../output"
)

# 初始化HotTopic
hot_topic = HoTopic(**config.__dict__)

# 运行热门话题分析
topic_metadata, topic_contents = hot_topic.run(input_data)

# 打印结果
for topic in topic_metadata:
    print(f"话题ID: {topic['topic_id']}")
    print(f"话题标题: {topic['topic_title']}")
    print(f"关键词: {', '.join(topic['topic_keywords'])}")
    print(f"文档数量: {topic['count']}")
    print(f"质量分数: {topic['quality_score']}")
    print("代表性文档:")
    for doc in topic['representative_docs']:
        print(f"  - {doc}")
    print("\n")
```

## 配置参数

你可以通过修改Config对象来自定义以下参数：

- min_content_length: 最小内容长度
- max_content_length: 最大内容长度
- similarity_threshold: 相似度阈值
- top_topics_count: 返回的热门话题数量
- max_keywords_per_topic: 每个话题的最大关键词数量
- representative_docs_count: 每个话题的代表性文档数量
- doc_preview_length: 文档预览长度
- quality_weights: 话题质量评分权重
- seed: 随机种子
- output_dir: 输出目录

## 许可证

本项目采用 MIT 许可证。详情请参见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何为这个项目做出贡献。

## 联系方式

如有任何问题或建议，请联系 [your.email@example.com](mailto:your.email@example.com)。
