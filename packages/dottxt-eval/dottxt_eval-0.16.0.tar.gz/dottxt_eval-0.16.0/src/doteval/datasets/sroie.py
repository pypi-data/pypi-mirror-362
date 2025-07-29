from typing import Iterator

from PIL import Image

from doteval.datasets.base import Dataset


class SROIE(Dataset):
    """SROIE dataset for receipt information extraction

    This dataset tests the ability of models to extract key information
    from digitized receipts including company name, address, date, and total amount.
    """

    name = "sroie"
    splits = ["train", "test"]
    columns = ["images", "address", "company", "date", "total"]

    def __init__(self, split: str, **kwargs):
        # Lazy import to avoid circular import issues
        import datasets as hf_datasets

        # Load streaming dataset and get metadata
        self.dataset = hf_datasets.load_dataset(
            "sizhkhy/SROIE", split=split, streaming=True
        )
        self.num_rows = self.dataset.info.splits[split].num_examples

    def __iter__(self) -> Iterator[tuple[Image.Image, str, str, str, str]]:
        for item in self.dataset:
            image = item["images"]
            address = item["fields"]["ADDRESS"]
            company = item["fields"]["COMPANY"]
            date = item["fields"]["DATE"]
            total = item["fields"]["TOTAL"]

            yield (image, address, company, date, total)


from doteval.datasets.base import _registry  # noqa: E402

_registry.register(SROIE)
