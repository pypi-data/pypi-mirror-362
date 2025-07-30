from typing import List
import asyncio
from tqdm.asyncio import tqdm as async_tqdm

from rebel.models import TestAttemptExecuted, TestAttempt
from rebel.collector import APIClient


class Collector:
    def __init__(self, api_client: APIClient, num_workers: int):
        self.api_client = api_client
        self.num_workers = num_workers
    
    
    async def collect_test_results(self, test_attempts: List[TestAttempt]) -> List[TestAttemptExecuted]:
        pbar = async_tqdm(total=len(test_attempts), desc='Collecting test results')
        
        semaphore = asyncio.Semaphore(self.num_workers)
        
        async def worker(test_attempt: TestAttempt) -> TestAttemptExecuted:
            async with semaphore:
                try:
                    pbar.set_description(f"Processing: {test_attempt.get_name()}")
                    test_attempt_result = await self.api_client.request(test_attempt.input)

                    pbar.update()
                    pbar.set_postfix_str(f"✅ {test_attempt.get_name()}")

                    return test_attempt_result
                except Exception as e:
                    pbar.set_postfix_str(f"❌ {test_attempt.get_name()}: {str(e)}")
                    pbar.update()
                    return None
        

        print(f"🚀 Collecting test cases using {self.num_workers} parallel workers...")
        print(f"📊 Total test cases (with retries): {len(test_attempts)}")
        
        try:
            results = await asyncio.gather(*[worker(attempt) for attempt in test_attempts], return_exceptions=True)
            results = [result for result in results if result] # remove None
        finally:
            pbar.close()
        
        print(f'\n📊 Collected {len(results)} test cases')
        
        return results        
