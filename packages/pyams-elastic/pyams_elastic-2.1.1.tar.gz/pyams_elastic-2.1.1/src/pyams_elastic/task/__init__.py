#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_elastic.task module

This module defines a PyAMS_scheduler task which can be used to schedule
Elasticsearch queries, and send notifications on (un)expected values.
"""

import json
import sys
import traceback

from elasticsearch import helpers
from elasticsearch.exceptions import TransportError
from zope.schema.fieldproperty import FieldProperty

from pyams_elastic.client import ElasticClient
from pyams_scheduler.interfaces.task.pipeline import IPipelineOutput
from pyams_scheduler.task.pipeline import BasePipelineOutput
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.dict import DotDict
from pyams_elastic.task.interfaces import IElasticReindexTask, IElasticReindexTaskInfo, \
    IElasticTask
from pyams_scheduler.interfaces.task import TASK_STATUS_ERROR, TASK_STATUS_FAIL, TASK_STATUS_OK
from pyams_scheduler.task import Task
from pyams_utils.factory import factory_config
from pyams_utils.text import render_text


__docformat__ = 'restructuredtext'

from pyams_elastic import _  # pylint: disable=ungrouped-imports


@factory_config(IElasticTask)
class ElasticTask(Task):
    """Elasticsearch task

    This task is used to execute an Elasticsearch search query; you can specify the
    number of records which are expected (a simple number or a range), and an error status
    is returned if a query is returning more or less items.
    """

    label = _("Elasticsearch query")
    icon_class = 'fab fa-searchengin'

    connection = FieldProperty(IElasticTask['connection'])
    query = FieldProperty(IElasticTask['query'])
    expected_results = FieldProperty(IElasticTask['expected_results'])
    output_fields = FieldProperty(IElasticTask['output_fields'])
    log_fields = FieldProperty(IElasticTask['log_fields'])

    def run(self, report, **kwargs):  # pylint: disable=unused-argument,too-many-locals,too-many-branches
        """Run an Elasticsearch query task"""
        try:  # pylint: disable=too-many-nested-blocks
            client = ElasticClient(using=self.connection,
                                   use_transaction=False)
            try:
                report.writeln('Elasticsearch query output', prefix='### ')
                results = []
                kwargs_params = kwargs.pop('params', {})
                if isinstance(kwargs_params, dict):
                    kwargs_params = [kwargs_params]
                for input_params in kwargs_params:
                    query = json.loads(render_text(self.query, **input_params))
                    query_results = client.es.search(index=self.connection.index, **query)
                    hits = DotDict(query_results['hits'])
                    expected = self.expected_results
                    total = hits.total
                    if isinstance(total, DotDict):
                        total = total.value
                    report.writeln(f"Expected results: {expected or '--'}  ")
                    report.writeln(f"Total results: {total}  ")
                    report.writeln(f"Query results: {len(hits.hits)}  ")
                    report.writeln(' ')
                    if self.output_fields:
                        query_results = []
                        for hit in hits.hits:
                            result = hit['_source']
                            output = {}
                            for field in self.output_fields:
                                record = result
                                if '=' in field:
                                    output_name, input_name = field.split('=', 1)
                                else:
                                    output_name = input_name = field
                                try:
                                    for name in input_name.split('.'):
                                        record = record[name]
                                    names = output_name.split('.')
                                    if len(names) == 1:
                                        output[names[0]] = record
                                    else:
                                        output_item = output.setdefault(names[0], {})
                                        for name in names[1:-1]:
                                            output_item = output_item.setdefault(name, {})
                                        output_item.setdefault(names[-1], record)
                                except KeyError:
                                    pass
                            if output:
                                query_results.append(output)
                    if self.log_fields:
                        for hit in hits.hits:
                            report.add_padding()
                            output = []
                            result = hit['_source']
                            for field in self.log_fields:
                                record = result
                                try:
                                    for attribute in field.split('.'):
                                        record = record[attribute]
                                    output.append(f' {field}: {record}')
                                except KeyError:
                                    output.append(f' {field}: no value')
                            report.write_code('\n'.join(output))
                            report.remove_padding()
                    if expected:
                        if '-' in expected:
                            mini, maxi = map(int, expected.split('-'))
                        else:
                            mini = maxi = int(expected)
                        if not mini <= total <= maxi:
                            return TASK_STATUS_ERROR, query_results
                    elif total > 0:
                        return TASK_STATUS_ERROR, results
                    results.extend(query_results)
                return TASK_STATUS_OK, results
            finally:
                client.close()
        except TransportError:
            report.writeln('**An Elasticsearch error occurred**', suffix='\n')
            report.write_exception(*sys.exc_info())
            return TASK_STATUS_FAIL, None


@adapter_config(required=IElasticTask,
                provides=IPipelineOutput)
class ElasticTaskPipelineOutput(BasePipelineOutput):
    """Elasticsearch task pipeline output adapter"""


@factory_config(IElasticReindexTask)
class ElasticReindexTask(Task):
    """Elasticsearch re-indexer task

    This task can be used to extract results of an Elasticsearch index to create documents
    into another index; original ID and timestamp, if any, are left unmodified. You can also
    specify the set of attributes which will be transferred into the new index, and you can rename
    these attributes.

    If an attribute is a string containing a serialized JSON object, it will be deserialized
    and contained attributes will be used as new properties of documents created in the new
    index.
    """

    label = _("Elasticsearch re-indexer")
    icon_class = 'fas fa-code-merge'

    source_connection = FieldProperty(IElasticReindexTask['source_connection'])
    source_query = FieldProperty(IElasticReindexTask['source_query'])
    source_fields = FieldProperty(IElasticReindexTask['source_fields'])
    page_size = FieldProperty(IElasticReindexTask['page_size'])
    target_connection = FieldProperty(IElasticReindexTask['target_connection'])

    def get_source_fields(self):
        """Source fields getter"""
        for field in self.source_fields:
            if '=' in field:
                target, source = field.split('=')
                yield source
            else:
                yield field

    def get_hits(self, results):
        """Internal hits iterator getter"""
        for hit in results.hits.hits:
            target_value = {}
            for field in self.source_fields:
                if '=' in field:
                    target_field, source_field = field.split('=')
                else:
                    target_field = source_field = field
                source_value = hit._source
                for attr in source_field.split('.'):
                    try:
                        source_value = source_value[attr]
                    except KeyError:
                        break
                try:
                    target_value[target_field] = json.loads(source_value)
                except (TypeError, json.JSONDecodeError):
                    target_value[target_field] = source_value
            yield {
                '_id': hit._id,
                '_source': target_value
            }

    def run(self, report, **kwargs):  # pylint: disable=unused-argument,too-many-locals,too-many-branches
        """Run Elasticsearch re-indexer query task"""
        try:  # pylint: disable=too-many-nested-blocks
            source = ElasticClient(using=self.source_connection,
                                   use_transaction=False)
            target = ElasticClient(using=self.target_connection,
                                   use_transaction=False)
            try:
                report.writeln('Elasticsearch query output', prefix='### ')
                report.writeln(f' - source index: {source.index}')
                report.writeln(f' - target index: {target.index}')
                input_params = kwargs.pop('params', {})
                source_query = json.loads(render_text(self.source_query, **input_params))
                source_query['_source'] = list(self.get_source_fields())
                source_query['size'] = self.page_size
                if 'sort' not in source_query:
                    source_query['sort'] = ['_score', '@timestamp']
                source_count = 0
                index_count = 0
                has_more_results = True
                last_sort = None
                while has_more_results:
                    if last_sort:
                        source_query['search_after'] = last_sort
                    results = DotDict(source.es.search(index=self.source_connection.index,
                                                       **source_query))
                    source_count += len(results.hits.hits)
                    actions, errors = helpers.bulk(target.es, self.get_hits(results),
                                                   index=target.index,
                                                   stats_only=False,
                                                   raise_on_error=False)
                    has_more_results = len(results.hits.hits) >= self.page_size
                    if has_more_results:
                        last_sort = results.hits.hits[-1].sort
                    index_count += actions
                    for error in errors:
                        report.writeln(f' - indexing error: {error}')
                report.writeln(f' - total source records: {source_count}')
                report.writeln(f' - total re-indexed records: {index_count}')
                return TASK_STATUS_OK, (source_count, index_count)
            finally:
                source.close()
                target.close()
        except TransportError:
            report.writeln('**An Elasticsearch error occurred**', suffix='\n')
            report.write_exception(*sys.exc_info())
            return TASK_STATUS_FAIL, None
