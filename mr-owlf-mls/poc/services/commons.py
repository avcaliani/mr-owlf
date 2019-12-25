from pandas import DataFrame, to_datetime, read_csv


def read(file_name: str) -> DataFrame:

    print(r'+-----------------------------------+')
    print(r'|           Reading File            |')
    print(r'+-----------------------------------+')

    print(f'\nReading file: "{file_name}"')
    df = read_csv(file_name)
    print(f'Shape: {df.shape}')
    print(f'Sample...\n{df.head()}\n...\n{df.tail()}\n')
    return df


def clean_data(df: DataFrame) -> None:

    print(r'+-----------------------------------+')
    print(r'|        Data Frame Clean Up        |')
    print(r'+-----------------------------------+')

    print(f'Old shape: {df.shape}')
    # Drop duplicate rows
    df.drop_duplicates(subset='title', inplace=True)    
    # Remove punctation
    df['title'] = df['title'].str.replace(r'[^\w\s]',' ')
    # Remove numbers 
    df['title'] = df['title'].str.replace(r'[^A-Za-z]',' ')
    # Make sure any double-spaces are single 
    df['title'] = df['title'].str.replace('  ',' ')
    df['title'] = df['title'].str.replace('  ',' ')
    # Transform all text to lowercase
    df['title'] = df['title'].str.lower()
    # Remove null values
    df.dropna(inplace=True)
    print(f'New shape: {df.shape}')


def show_statistics(df: DataFrame) -> None:
    
    print(r'+-----------------------------------+')
    print(r'|       Data Frame Statistics       |')
    print(r'+-----------------------------------+')

    # Convert Unix Timestamp to Datetime
    df['timestamp'] = to_datetime(df['timestamp'], unit='s')
    print(f'\nDate range of posts...')
    print(f'* Start date:\t{df["timestamp"].min()}')
    print(f'* End date:\t{df["timestamp"].max()}')
    
    # Set x values: # of posts 
    authors: DataFrame = df['author'].value_counts() 
    authors: DataFrame = authors[authors > 100].sort_values(ascending=False)
    print(f'\nMost Active Authors...\n{authors.head()}\n...\n{authors.tail()}\n')

    # Set x values: # of posts
    domains: DataFrame = df['domain'].value_counts() 
    domains: DataFrame = domains.sort_values(ascending=False).head(5)
    print(f'\nMost referenced domains...\n{domains.head()}\n...\n{domains.tail()}\n')
    