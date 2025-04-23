from typing import List
from models import NormalizedAsset
from utils import ConfigManager, MongoDBManager, logger
from pipeline import AssetDeduplicator

class AssetRepository:
    """
    Repository for storing and retrieving assets from MongoDB with deduplication support.
    """
    def __init__(self, deduplicator: AssetDeduplicator):
        self.db_manager = MongoDBManager()
        self.deduplicator = deduplicator
        self.total_assets_inserted = 0
        self.total_assets_dublicated = 0
        self.config = ConfigManager()
        self._create_indexes()
    
    def _create_indexes(self):
        with self.db_manager.get_db() as db:
            collection = db[self.config.get_collection_name()]
            # Create indexes for efficient querying
            collection.create_index("asset_id")
            collection.create_index("source")
            collection.create_index("netbios_name")
    
    def find_database_duplicates(self, asset: NormalizedAsset) -> List[NormalizedAsset]:
        """
        Find potential duplicates of an asset in the database.
        """
        # Build queries from strategies
        queries = []
        for strategy in self.deduplicator.strategies:
            query = strategy.get_query(asset)
            if query:
                queries.append(query)
        
        if not queries:
            return []
        
        # Find potential matches in the database
        with self.db_manager.get_db() as db:
            collection = db[self.config.get_collection_name()]
            cursor = collection.find({"$or": queries})
            
            potential_duplicates = [NormalizedAsset(**doc) for doc in cursor]
            
            # Confirm duplicates using the same threshold logic as batch deduplication
            confirmed_duplicates = []
            for potential_dup in potential_duplicates:
                matching_strategies = sum(1 for strategy in self.deduplicator.strategies
                                        if strategy.are_duplicates(asset, potential_dup))
                
                match_percentage = matching_strategies / len(self.deduplicator.strategies)
                
                if match_percentage >= self.deduplicator.threshold:
                    confirmed_duplicates.append(potential_dup)
            
            return confirmed_duplicates
    
    def save_asset_with_deduplication(self, asset: NormalizedAsset) -> bool:
        """
        Save a single asset with deduplication against existing database records.
        """
        database_duplicates = self.find_database_duplicates(asset)
        
        if database_duplicates:
            primary_duplicate = database_duplicates[0]
            logger.info(f"Duplicate found in the database: {primary_duplicate.asset_id}")
            self.total_assets_dublicated += 1
            return False
        else:
            with self.db_manager.get_db() as db:
                collection = db[self.config.get_collection_name()]
                collection.insert_one(asset.model_dump())
                logger.info(f"Inserted new asset: {asset.asset_id}")
                return True
    
    def save_assets_with_deduplication(self, assets: List[NormalizedAsset]) -> None:
        """
        Save multiple assets with deduplication
        """
        if not assets:
            logger.info("No new assets were inserted into the database")
            return
        
        operations_count = 0
        for asset in assets:
            value_saved = self.save_asset_with_deduplication(asset)
            if value_saved:
                operations_count += 1
                self.total_assets_inserted += 1
        
        if operations_count > 0:
            logger.info(f"Inserted {operations_count} new assets into the database")
        else:
            logger.info("No new assets were inserted into the database")
    
    def print_statistics(self) -> None:
        logger.info(f"Total assets inserted: {self.total_assets_inserted}")
        logger.info(f"Total assets duplicated: {self.total_assets_dublicated}")