from repository.author import AuthorRepository
from repository.domain import DomainRepository


def author(repository: AuthorRepository, post: any) -> None:
    _author = repository.find(post.author)
    if _author is None:
        repository.add(post.author, post.classification)
        return

    clf, count = post.classification, 1
    if post.classification in _author['classification']:
        count = _author['classification'][clf] + 1

    repository.update(_author['_id'], clf, count)


def domain(repository: DomainRepository, post: any) -> None:
    _domain = repository.find(post.domain)
    if _domain is None:
        repository.add(post.domain, post.classification)
        return

    clf, count = post.classification, 1
    if post.classification in _domain['classification']:
        count = _domain['classification'][clf] + 1

    repository.update(_domain['_id'], clf, count)
