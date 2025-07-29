# uniqdeque

A hybrid data structure combining a [deque](https://en.wikipedia.org/wiki/Double-ended_queue) (double-ended queue) and a [set](https://en.wikipedia.org/wiki/Set_(abstract_data_type)) (unique elements).

## Features

- **Double-ended operations**:
  - `push_front(elem)`: Insert at front (if not a duplicate) in **O(1)** time.
  - `push_back(elem)`: Append at back (if not a duplicate) in **O(1)** time.
  - `pop_front()` / `pop_back()`: Remove from either end in **O(1)** time.
- **Uniqueness**: Automatically rejects duplicates on insertion.
- **Order-preserving**: Maintains insertion order.
- **Fast membership testing**: `elem in dq` checks in **O(1)** time.

## Use Cases

1. **LRU/LFU Caches**: Evict least-recently-used items while avoiding duplicates.
3. **Message Queues**: Deduplicate messages while supporting queue/dequeue at both ends.
4. **Sliding Window Analytics**: Track unique elements in a time window (e.g., "unique visitors in the last 5 minutes").

## Installation

```bash
pip install uniqdeque
```

## Usage Example

```python
from uniqdeque import uniqdeque

dq = uniqdeque([1, 2, 3])  # Initialize with elements
dq.push_front(0)            # -> [0, 1, 2, 3]
dq.push_back(3)             # No effect (duplicate)
dq.pop_back()               # Returns 3, dq -> [0, 1, 2]
```

## Performance

| Operation       | Time Complexity | Notes                       |
|-----------------|-----------------|-----------------------------|
| `push_*`        | O(1)            | Rejects duplicates in O(1). |
| `pop_*`         | O(1)            | Raises `KeyError` if empty. |
| `discard(elem)` | O(1)            | Safe removal if present.    |
| `len(dq)`       | O(1)            |                             |

## API Reference

### Core Methods

- **`push_front(elem: T) -> None`**
  Add to front if not a duplicate.
- **`push_back(elem: T) -> None`**
  Append to back if not a duplicate.
- **`pop_front() -> T`**
  Remove and return front element. Raises `KeyError` if empty.
- **`pop_back() -> T`**
  Remove and return back element. Raises `KeyError` if empty.

### Utilities

- **`discard(elem: T) -> None`**
  Remove element if present (no-op otherwise).
- **`clear() -> None`**
  Remove all elements.
- **`copy() -> uniqdeque[T]`**
  Return a shallow copy.

## Design Choices

- **Backed by**: An `OrderedDict` (for `O(1)` lookups and `O(1)` head/tail ops).
- **Alternatives**: Tree-based map (e.g., C++'s `std::map`) for ordered elements (`O(log n)` lookups).

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.

## License

MIT