from repository.author import AuthorRepository


def author(repository: AuthorRepository, post: any) -> None:
    _author = repository.find(post.author)
    if _author is None:
        repository.add(post.author, post.classification)
        return

    clf, count = post.classification, 1
    if post.classification in _author['classification']:
        count = _author['classification'][clf] + 1

    repository.update(_author['_id'], clf, count)
