import argparse

from rag.config import settings
from rag.retriever import CityFlowRetriever


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Natural-language permit question")
    parser.add_argument("-k", type=int, default=settings.top_k)
    args = parser.parse_args()

    retriever = CityFlowRetriever(
        index_dir=settings.faiss_index_dir,
        embedding_model=settings.embedding_model,
        top_k=args.k,
    )

    for i, item in enumerate(retriever.retrieve(args.query, args.k), start=1):
        print(f"\n--- Result {i} ---")
        print(f"Evidence ID: {item['evidence_id']}")
        print(f"Source: {item['source']}")
        print(f"Distance: {item['distance']:.6f}")
        print(item["text"])


if __name__ == "__main__":
    main()
