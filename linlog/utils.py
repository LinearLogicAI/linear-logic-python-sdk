from typing import Generic, List, TypeVar, Union


T = TypeVar("T")


class Paginator(list, Generic[T]):
    """Paginator for list endpoints"""

    def __init__(
        self,
        results: List[T],
        count: int,
        limit: int,
        offset: int,
        previous_url: Union[str, None],
        next_url: Union[str, None]
    ):
        super().__init__(results)
        self.results = results
        self.count = count
        self.limit = limit
        self.offset = offset
        self.next_url = next_url
        self.previous_url = previous_url

    def transform_results(self, callback):
        self.results = list(map(
            lambda x: callback(x), self.results
        ))

    def __iter__(self):
        for elem in self.results:
            yield elem

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return self.__class__(self.results[idx])
        else:
            return self.results[idx]

    def __len__(self) -> int:
        return len(self.results)
