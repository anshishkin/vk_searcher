from itertools import islice, repeat, takewhile


def split_every(n, iterable):
    iterator = iter(iterable)
    split_every_iter(n, iterator)


def split_every_iter(n, iterator):
    return takewhile(bool, (list(islice(iterator, n)) for _ in repeat(None)))


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def as_completed(*futures):
    futures = set(futures)
    completed = set()
    while len(completed) < len(futures):
        for future in futures.difference(completed):
            state = future.get_state()
            if state.is_completed():
                completed.add(future)
                yield state
