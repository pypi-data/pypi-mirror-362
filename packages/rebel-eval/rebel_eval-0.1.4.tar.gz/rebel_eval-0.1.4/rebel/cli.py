import argparse

from rebel.workflow import Workflow
from rebel.extractor import Extractor
from rebel.collector import Collector, TSAPIClient
from rebel.evaluator import Evaluator
from rebel.aggregator import Aggregator
from rebel.saver import Saver


def main():
    """Main CLI entry point for rebel."""
    parser = argparse.ArgumentParser(description="REBEL - RAG Evaluation Benchmark and Evaluation Library")
    
    # Add CLI arguments
    parser.add_argument("--test-dir", required=True, help="Directory containing test files")
    parser.add_argument("--keyword", help="Filter tests by keyword")
    parser.add_argument("--tags", help="Filter tests by tags")
    parser.add_argument("--exclude-tags", help="Exclude tests with these tags")
    parser.add_argument("--num-workers-api", type=int, default=4, help="Number of API worker threads")
    parser.add_argument("--num-workers-eval", type=int, default=4, help="Number of evaluation worker threads")
    parser.add_argument("--api-url", help="API url for testing")
    
    args = parser.parse_args()
    
    extractor = Extractor(
        test_dir=args.test_dir,
        keyword=args.keyword,
        tags=args.tags,
        exclude_tags=args.exclude_tags
    )
    
    api_client = TSAPIClient(url=args.api_url)
    collector = Collector(api_client=api_client, num_workers=args.num_workers_api)
    evaluator = Evaluator(num_workers=args.num_workers_eval)
    aggregator = Aggregator()
    saver = Saver()
    
    workflow = Workflow(
        extractor=extractor,
        collector=collector,
        evaluator=evaluator,
        aggregator=aggregator,
        saver=saver
    )
    
    workflow.execute()


if __name__ == "__main__":
    main()
