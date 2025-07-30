import os
from contextlib import contextmanager
from functools import lru_cache
from typing import List, Optional, Self

import jieba
from llama_index.core import QueryBundle
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.schema import NodeWithScore, TextNode
from sqlalchemy import Engine, create_engine, text


class DuckDBFTSDatabase:
    def __init__(self, db_file: str, table_name: str):
        self.db_file = db_file
        self.table_name = table_name
        self._engine: Optional[Engine] = None

        jieba.setLogLevel(jieba.logging.INFO)

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            self._engine = create_engine(f"duckdb:///{self.db_file}")
        return self._engine

    @contextmanager
    def get_connection(self):
        conn = self.engine.connect()
        try:
            conn.execute(text("INSTALL fts;"))
            conn.execute(text("LOAD fts;"))
            yield conn
        finally:
            conn.close()

    def reset_database(self) -> None:
        if self._engine:
            self._engine.dispose()
            self._engine = None

        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def setup_database(self) -> None:
        with self.get_connection() as conn:
            conn.execute(text("INSTALL fts;"))

            conn.execute(
                text(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY,
                    original_text TEXT NOT NULL,
                    tokenized_text TEXT NOT NULL
                );
            """)
            )

            conn.commit()

    def insert_documents(self, documents: List[str]) -> None:
        """批量插入文档数据并创建 FTS 索引"""
        if not documents:
            return

        print(f"正在向 DuckDB 表中批量插入 {len(documents)} 个文档...")

        with self.get_connection() as conn:
            for i, doc in enumerate(documents):
                tokenized_text = " ".join(jieba.cut(doc))
                conn.execute(
                    text(
                        f"INSERT INTO {self.table_name} (id, original_text, tokenized_text) VALUES (:id, :original_text, :tokenized_text)"
                    ),
                    {"id": i, "original_text": doc, "tokenized_text": tokenized_text},
                )

            conn.execute(text(f"PRAGMA create_fts_index('{self.table_name}', 'id', 'tokenized_text');"))
            conn.commit()

        print(f"数据填充完成，共插入 {len(documents)} 个文档。")
        print("DuckDB FTS 索引创建成功！")

    def initialize_with_documents(self, documents: List[str]) -> Self:
        """完整初始化数据库：重置、设置、插入数据"""
        self.reset_database()
        self.setup_database()
        self.insert_documents(documents)

        return self

    def close(self) -> None:
        """关闭数据库连接"""
        if self._engine:
            self._engine.dispose()
            self._engine = None


class DuckDBFTSRetriever(BaseRetriever):
    """基于 DuckDB FTS 的文档检索器 - 优化版本"""

    def __init__(self, database: DuckDBFTSDatabase, top_k: int = 2):
        self._database = database
        self._top_k = top_k
        super().__init__()

    @lru_cache(maxsize=128)
    def _tokenize_query(self, query: str) -> str:
        """缓存查询分词结果"""
        return " ".join(jieba.cut(query))

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """执行 FTS 检索"""
        tokenized_query = self._tokenize_query(query_bundle.query_str)

        with self._database.get_connection() as conn:
            fts_query = text(f"""
                SELECT
                    original_text,
                    score
                FROM (
                    SELECT
                        id,
                        fts_main_{self._database.table_name}.match_bm25(
                            id,
                            :tokenized_query
                        ) AS score
                    FROM {self._database.table_name}
                ) AS fts_result
                JOIN {self._database.table_name} ON fts_result.id = {self._database.table_name}.id
                WHERE score IS NOT NULL
                ORDER BY score DESC
                LIMIT :top_k;
            """)

            results = conn.execute(fts_query, {"tokenized_query": tokenized_query, "top_k": self._top_k}).fetchall()

        return [NodeWithScore(node=TextNode(text=original_text), score=score) for original_text, score in results]


def main():
    """主函数 - 优化版本"""
    documents = [
        "马斯克是特斯拉的首席执行官，该公司是电动汽车领域的领导者。",
        "他也是 SpaceX 的创始人和首席执行官，这是一家致力于太空探索的公司。",
        "此外，马斯克还参与了 Neuralink 和 The Boring Company 等项目。",
        "特斯拉不仅生产电动汽车，还涉足太阳能和储能解决方案。",
    ]

    retriever = DuckDBFTSRetriever(
        database=DuckDBFTSDatabase(
            db_file="generated/docs.duckdb",
            table_name="documents",
        ).initialize_with_documents(documents),
        top_k=3,
    )

    result = retriever.retrieve(QueryBundle(query_str="谁是特斯拉的CEO？"))
    for i, node_with_score in enumerate(result, 1):
        print(f"{i}. 文档内容: {node_with_score.node.get_content()}")
        print(f"   相关性分数 (BM25 Score): {node_with_score.score:.4f}")


if __name__ == "__main__":
    main()
