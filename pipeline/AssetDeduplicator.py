from typing import List, Dict
from models import NormalizedAsset
from pipeline.Strategies import (
   DeduplicationStrategy
)

class AssetDeduplicator:
   def __init__(self, strategies: List[DeduplicationStrategy], batch_size: int, threshold: float = 1):
       self.batch_size = batch_size
       self.strategies = strategies
       self.threshold = threshold
   
   def find_duplicates(self, assets: List[NormalizedAsset]) -> Dict[int, List[int]]:
       """
       Find duplicate assets within the provided list.
       """
       duplicates_map = {}
       processed = set()
       
       for asset_index in range(len(assets)):
           if asset_index in processed:
               continue  # Skip assets already identified as duplicates
               
           duplicates = []
           for asset_segment_index in range(asset_index + 1, len(assets)):
               if asset_segment_index in processed:
                   continue  # Skip assets already identified as duplicates
               
               # Count how many strategies consider these assets duplicates
               matching_strategies = 0
               for strategy in self.strategies:
                   if strategy.are_duplicates(assets[asset_index], assets[asset_segment_index]):
                       matching_strategies += 1
               
               # Calculate match percentage and compare to threshold
               match_percentage = matching_strategies / len(self.strategies)
               if match_percentage >= self.threshold:
                   duplicates.append(asset_segment_index)
                   processed.add(asset_segment_index)  # Mark as processed so it won't be compared again
           
           if duplicates:
               duplicates_map[asset_index] = duplicates
               
       return duplicates_map
   
   def deduplicate_batch(self, assets: List[NormalizedAsset]) -> List[NormalizedAsset]:
       """
       Process a batch of assets and remove duplicates.
       """
       if not assets:
           return []
       
       # Find all duplicates in the batch
       duplicates_map = self.find_duplicates(assets)
       
       result = []
       processed = set()  # Tracks which assets have been processed
       
       for asset_id in range(len(assets)):
           if asset_id in processed:
               continue
               
           if asset_id in duplicates_map:
               result.append(assets[asset_id])
               processed.add(asset_id)
           elif asset_id not in processed:
               result.append(assets[asset_id])
               processed.add(asset_id)
               
       return result
   
   def process_assets(self, asset_generator) -> List[NormalizedAsset]:
       """
       Process assets from a generator in batches.
       """
       deduplicated_assets = []
       current_batch = []
       
       for asset in asset_generator:
           current_batch.append(asset)
           
           if len(current_batch) >= self.batch_size:
               batch_results = self.deduplicate_batch(current_batch)
               deduplicated_assets.extend(batch_results)
               current_batch = []
       
       if current_batch:
           batch_results = self.deduplicate_batch(current_batch)
           deduplicated_assets.extend(batch_results)
       
       return deduplicated_assets