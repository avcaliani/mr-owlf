from datetime import datetime

from pandas import DataFrame
from repository.author import AuthorRepository
from repository.domain import DomainRepository
from repository.statistic import StatisticRepository


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


def general(repository: StatisticRepository, df: DataFrame) -> any:
    clfs = df['classification'].value_counts()
    not_fake_count = int(clfs['NOT_FAKE'] if 'NOT_FAKE' in clfs else 0)
    fake_count = int(clfs['FAKE'] if 'FAKE' in clfs else 0)

    authors_series = df['author'].value_counts().head(5)
    authors_df = DataFrame({
        'author': authors_series.index, 'posts': authors_series.to_list()
    })
    popular_authors = authors_df.to_dict(orient='records')

    domains_series = df['domain'].value_counts().head(5)
    domains_df = DataFrame({
        'domain': domains_series.index, 'posts': domains_series.to_list()
    })
    popular_domains = domains_df.to_dict(orient='records')

    result = {
        'calculated_at': datetime.utcnow(),
        'statistics': {
            'general': {
                'posts': df.shape[0],
                'authors': df['author'].drop_duplicates().shape[0],
                'domains': df['domain'].drop_duplicates().shape[0]
            },
            'classification': {
                'not_fake': not_fake_count,
                'fake': fake_count
            },
            'popular_authors': popular_authors,
            'popular_domains': popular_domains
        }
    }

    repository.add(result)
    return result
