import csv
import gzip
import os
import sys
import tempfile
import time
import traceback
from multiprocessing.pool import ThreadPool
from pathlib import Path
from subprocess import check_call
from typing import List, Dict, Optional
from urllib.request import urlopen

import requests
from requests_toolbelt.sessions import BaseUrlSession

from pipebio.column import Column
from pipebio.entities import Entities
from pipebio.models.sort import Sort
from pipebio.models.table_column_type import TableColumnType
from pipebio.util import Util


class Sequences:
    # Static property used to join entity_id with sequence_id.
    _merge_delimiter = '##@##'
    _is_aws: bool

    csv.field_size_limit(sys.maxsize)

    def __init__(self, session: BaseUrlSession, is_aws: bool):
        self._session = Util.mount_standard_session(session)
        self._entities = Entities(session)
        self._is_aws = is_aws

    def _parallel_download(self, entity_ids: List[int]) -> None:
        print('Download starting')
        entities = {}

        def download(entity_id: int) -> None:
            entities[entity_id] = self.download(entity_id, Sequences._get_filepath_for_entity_id(entity_id))

        list(ThreadPool(8).imap_unordered(download, entity_ids))

    def download_to_memory(self, entity_ids: List[int]):
        self._parallel_download(entity_ids)

        # Build an in memory map that matches this tsv.
        sequence_map = {}

        columns = [
            Column('id', TableColumnType.STRING),
            Column('name', TableColumnType.STRING),
            Column('sequence', TableColumnType.STRING),
            Column('annotations', TableColumnType.STRING),
            Column('type', TableColumnType.STRING),
        ]

        for entity_id in entity_ids:
            sequence_map = self._read_tsv_to_map(
                Sequences._get_filepath_for_entity_id(entity_id),
                str(entity_id),
                columns,
                sequence_map
            )

        return sequence_map

    @staticmethod
    def _read_tsv_to_map(filepath: str,
                         id_prefix: str,
                         columns: List[Column],
                         sequence_map: Dict[str, any] = None) -> Dict[str, any]:

        sequence_map = {} if sequence_map is None else sequence_map

        print(f'read_tsv_to_map::Reading filepath: "{filepath}"')
        # Read the file.
        with open(filepath, 'r') as tsvfile:

            replaced = (x.replace('\0', '') for x in tsvfile)
            reader = csv.DictReader(replaced, dialect='excel-tab')

            for row in reader:
                if 'id' not in row:
                    raise Exception('id not in row')

                row_id = int(row['id'])

                compound_id = f'{id_prefix}{Sequences._merge_delimiter}{row_id}'
                parsed = {}
                for column in columns:
                    name = column.name
                    # Avoid errors like "KeyError: 'type'".
                    parsed[column.name] = column.parse(row[name]) if name in row else column.parse('')

                sequence_map[compound_id] = parsed

        return sequence_map


    def download(self,
                 entity_id: int,
                 destination: str = None,
                 sort: List[Sort] = None,
                 query: str = None,
                 include_cols: Optional[List[str]] = None,
                 exclude_cols: Optional[List[str]] = None,
                 limit: int = None,
                 allow_deleted: bool = True, ) -> str:
        """
        Download sequences from a single entity.
        """

        sort = sort if sort is not None and len(sort) > 0 else []
        if not next((s for s in sort if s.col_id == 'id'), None):
            sort.append(Sort('id', 'asc'))
        sort_dicts = list(sort_item.to_json() for sort_item in sort) if sort else [Sort('id', 'asc').to_json()]

        # Build query parameters.
        include_sort_cols = True
        maybe_limit = f'pageLimit={limit}' if limit else None
        include_cols_joined = Sequences.get_joined_cols(include_cols, "includeCols")
        exclude_cols_joined = Sequences.get_joined_cols(exclude_cols, "excludeCols")
        maybe_include_sort_cols = f'includeSortCols={str(include_sort_cols).lower()}' if include_sort_cols else None
        # Join any query parameters together. Currently just one.
        query_string = '&'.join(
            query_param for query_param in
            [maybe_limit, include_cols_joined, exclude_cols_joined, maybe_include_sort_cols]
            if query_param is not None
        )

        query = query if query is not None else ''
        body = {
            'filter': query,
            'sort': sort_dicts,
        }

        query_param_connector = '&' if len(query_string) > 0 else ''
        file_path = Sequences._get_filepath_for_entity_id(entity_id)
        url = f'entities/{entity_id}/_extract?{query_string}{query_param_connector}{allow_deleted}'
        print(f'Downloading shards from "{url}" to "{file_path}".')

        paths = []
        with self._session.post(url, stream=True, timeout=10 * 60, json=body) as response:
            try:
                links = response.json()
                print('links', links)
                if 'statusCode' in links and links['statusCode'] != 200:
                    raise Exception(links['message'])
                elif len(links) == 0:
                    raise Exception(
                        f'Sequences:download - Error; no download links for {entity_id}. Does the table exist?')

                index = 0
                for link in links:
                    path = f'{file_path}-{index}.gz'
                    response = urlopen(link)
                    with open(path, 'wb') as file:
                        file.write(response.read())
                    paths.append(path)
                    index = index + 1


            except Exception as e:
                print('Sequences:download - error:', e)
                raise e

        sorted_paths = self._get_sorted_file_shard_list(entity_id, paths, [])

        print(f'Unzipping: entity_id={entity_id} to destination={destination}')

        skip_first = False

        if self._is_aws:
            for file_shard in sorted_paths:
                self.convert_parquet_to_tsv(file_shard, destination, skip_header=False)
        else:
            with open(destination, 'wb+') as target_file:
                for file_shard in sorted_paths:
                    with gzip.open(file_shard, 'rb') as g_zip_file:
                        first_line = True
                        for line in g_zip_file:
                            # We skip the first line of every file, except for the very first.
                            if not (first_line and skip_first):
                                line = Sequences._sanitize(line.decode("utf-8"))
                                target_file.write(line.encode("utf-8"))
                            first_line = False
                    # We skip the first line of every file, except for the very first.
                    skip_first = True

        return destination

    @staticmethod
    def get_joined_cols(cols, parameter):
        return f'{parameter}={",".join(cols)}' if cols else None

    @staticmethod
    def _sanitize(line: str) -> str:
        if '"' not in line:
            return line
        else:
            sanitized_line = []
            ending = "\n" if line.endswith("\n") else ""
            splits = line.rstrip("\n").split("\t")
            for split in splits:
                if not split.startswith('"'):
                    sanitized_line.append(split)
                else:
                    sanitized_line.append(split[1:-1].replace('""', '"'))
        return '\t'.join(sanitized_line) + ending

    @staticmethod
    def _get_filepath_for_entity_id(entity_id: any, extension='tsv'):
        file_name = f'{entity_id}.{extension}'
        return os.path.join(tempfile.gettempdir(), file_name)

    def _get_sorted_file_shard_list(self, entity_id: int, file_shard_list: List[str], sort: list):
        """
        Sorts the file_shard_list to ensure that the shards can be stitched back together in the correct order
        This is needed as the response 'chunks' are not necessarily named in the correct order.

        :param entity_id: - document to download
        :param file_shard_list: List[str] - All of the file names of the shards
        :param sort: List[Sort] - list of sorts applied, processed in order, same way SQL does, so order matters
        :return:  List[str] - All of the file names of the shards ordered by the sort
        """

        if sort is None or len(sort) == 0:
            return file_shard_list

        all_fields = self._entities.get_fields(entity_id=entity_id)

        shard_first_data_lines = []

        # get values of sort columns for first data line of each shard
        for file_shard in file_shard_list:
            with gzip.open(file_shard, 'rt') as g_zip_file:
                tsv_reader = csv.reader(g_zip_file, delimiter="\t")
                lines = 2
                header = None
                file_details = {'file_shard': file_shard}

                # reads the first line and headers of each files and pull out
                # all the values we need to sort on
                for i in range(lines):
                    row = next(tsv_reader)
                    if i == 0:
                        header = row
                    else:
                        for sort_column in sort:
                            col_id = sort_column.col_id
                            field = [x for x in all_fields if x.name == col_id][0]
                            col_index = header.index(col_id)
                            # Column.parse returns None for empty string INTEGER/NUMERIC columns,
                            # ideally would change that, but consequences unclear
                            # so overriding that to 0, otherwise take Column.parse output
                            parsed_value = float('-inf') \
                                if (field.kind == TableColumnType.INTEGER or field.kind == TableColumnType.NUMERIC) \
                                   and row[col_index] == '' \
                                else field.parse(row[col_index])
                            file_details[col_id] = parsed_value

            shard_first_data_lines.append(file_details)

        sorted_shard_first_lines = []
        # sort the shards, in reverse order, so last one done is primary sort
        sort.reverse()
        for column_to_sort in sort:
            sorted_shard_first_lines = sorted(shard_first_data_lines,
                                              key=lambda x: x[column_to_sort.col_id],
                                              reverse=column_to_sort.sort == 'desc')

        return list(map(lambda x: x['file_shard'], sorted_shard_first_lines))

    def create_signed_upload(self, entity_id: int, retries=5):
        try:
            response = self._session.post(f'sequences/signed-upload/{entity_id}')
            print('create_signed_upload: response.text', response.text)
            print('create_signed_upload: response.status', response.status_code)
            return response.json()
        except Exception as error:
            print('create_signed_upload:error: ', error)
            traceback.print_exc()
            if retries > 0:
                print('create_signed_upload:error, retrying', retries)
                time.sleep(5)
                return self.create_signed_upload(entity_id, retries - 1)
            else:
                raise error

    @staticmethod
    def maybe_compress_file(file_path) -> str:
        key = 'COMPRESS_BIGQUERY_UPLOADS'
        if key in os.environ:
            # Intentional string comparison, environment variables are always strings.
            should_compress = os.environ[key] == 'true'
            print(f'environment variable "{key}"="{should_compress}"')
            if should_compress:
                original_gz_size = Path(file_path).stat().st_size
                print(f'Original size:{original_gz_size}')
                check_call(['gzip', file_path])
                zipped_file_path = file_path + '.gz'
                zipped_gz_size = Path(zipped_file_path).stat().st_size
                print(f'Gzipped size:{zipped_gz_size} ')
                return zipped_file_path
            else:
                pass
        else:
            print(f'environment variable "{key}" not set. Not compressing.')
        return file_path

    def upload(self, url: str, file_path: str, retries=5):
        if retries == 0:
            raise Exception('Upload has timed out.')

        zipped_file_path = self.maybe_compress_file(file_path)
        with open(zipped_file_path, 'rb') as f:
            try:
                print('upload starting')
                print(f'remaining retries={retries}, uploading to:{url}')
                response = requests.put(url, data=f, timeout=10 * 60)
                print('upload: response.text', response.text)
                print('upload: response.status', response.status_code)
                print('upload:ok')
            except requests.exceptions.ConnectionError as e:
                track = traceback.format_exc()
                print(track)
                # RECURSION !!!!
                self.upload(url, file_path, retries - 1)

    def import_signed_upload(self, import_details: Dict, retries=5) -> bool:
        # Need a nice big sleep to avoid hitting rate limits.
        # Multiplying by retry count gives a nicely increasing delay.
        sleep_seconds = 10 * (6 - retries)

        try:
            print('import_signed_upload starting.')
            response = self._session.post('sequences/import-signed-upload',
                                         json=import_details,
                                         timeout=10 * 60)
            response_json = response.json()
            print(f'import_signed_upload:ok, status={response_json}')
            print('import_signed_upload: response.status', response.status_code)

            if response_json['state'] == 'SUCCESS':
                return True
            elif response_json['state'] == 'UNSPECIFIED':

                errors: List[str] = response_json['errors']
                print('any errors:', response_json['errors'])

                for error in errors:
                    if error.startswith('Exceeded rate limits') and retries > 0:

                        time.sleep(sleep_seconds)
                        # RECURSION!!!
                        return self.import_signed_upload(import_details, retries - 1)
                    else:
                        raise ImportError('import_signed_upload:error')

                time.sleep(sleep_seconds)
                # RECURSION!!!
                return self.import_signed_upload(import_details, retries - 1)
            else:
                # They're pending, so just poll again
                time.sleep(sleep_seconds)
                # RECURSION!!!
                return self.import_signed_upload(import_details, retries - 1)
        except ImportError as error:
            raise error
        except Exception as error:
            print('import_signed_upload:error: ', error)

            time.sleep(sleep_seconds)
            if retries > 0:
                # RECURSION!!!
                return self.import_signed_upload(import_details, retries - 1)
            else:
                raise error

    @staticmethod
    def convert_parquet_to_tsv(path_to_parquet_data: str,
                               path_to_tsv_file: str,
                               skip_header: bool = False,
                               chunk_size: int = 10000) -> None:
        import pyarrow.parquet as pq
        table_data = pq.read_table(path_to_parquet_data)

        if os.path.exists(path_to_tsv_file):
            os.remove(path_to_tsv_file)

        # Convert the table in chunks to CSV format. We convert each chunk to a Pandas dataframe because it allows
        # us to write the data without adding quotes, which the Pyarrow CSV writer does not.
        import csv
        for i in range(0, table_data.num_rows, chunk_size):
            chunk = table_data.slice(i, chunk_size)
            # NOTE: We cast integers with nulls to object because otherwise Pandas will convert them to floats,
            #       which can cause downstream issues, e.g. because 354 becomes 354.0, which BigQuery refuses to
            #       import as an integer.
            chunk_as_df = chunk.to_pandas(integer_object_nulls=True)
            # Convert all boolean columns to lowercase string.
            boolean_columns = list(chunk_as_df.select_dtypes(include='bool').columns)
            for boolean_col in boolean_columns:
                chunk_as_df[boolean_col] = chunk_as_df[boolean_col] \
                    .astype(str) \
                    .apply(lambda x: x.lower() if x is not None and str(x) != 'nan' else '')
            write_header = not skip_header and i == 0
            chunk_as_df.to_csv(
                path_to_tsv_file,
                sep='\t',
                mode='a',
                header=write_header,
                index=False,
                quoting=csv.QUOTE_NONE,
            )
