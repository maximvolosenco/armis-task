from pipeline import AssetDeduplicator, AssetRepository, QualysAsset, CrowdstrikeAsset, AssetNormalizer
from utils import logger
from pipeline import (
    IdStrategy,
    OsStrategy,
    IPAddressStrategy,
    NetworkInterfaceStrategy,
    SystemInfoStrategy,
    CloudInfoStrategy
)

def run():
    logger.info("Starting asset deduplication process...")
    qualys_client = QualysAsset()
    crowdstrike_client = CrowdstrikeAsset()

    # Uncomment/ Comment Strategies as needed
    strategies = [
            IPAddressStrategy(),
            IdStrategy(),
            OsStrategy(),
            # Unimplemented query for the following strategies, next updates coming soon!
            # SystemInfoStrategy(),
            # CloudInfoStrategy(),
            # NetworkInterfaceStrategy(),
        ]
    
    # Set batch size and threshold for deduplication for testing
    deduplicator = AssetDeduplicator(strategies, batch_size=3, threshold=0.8)


    repository = AssetRepository(deduplicator)

    qualys_deduplicated_assets = deduplicator.process_assets(qualys_client.iterate_normalized_hosts())
    crowdstrike_deduplicated_assets = deduplicator.process_assets(crowdstrike_client.iterate_normalized_hosts())

    repository.save_assets_with_deduplication(qualys_deduplicated_assets)
    repository.save_assets_with_deduplication(crowdstrike_deduplicated_assets)

    repository.print_statistics()
    logger.info("Asset deduplication process completed.")

run()