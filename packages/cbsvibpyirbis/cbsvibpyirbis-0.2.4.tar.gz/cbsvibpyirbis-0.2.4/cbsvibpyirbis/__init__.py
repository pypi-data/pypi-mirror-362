# coding: utf-8

"""
Модуль содержит основную функциональность по работе с сервером ИРБИС64,
в т. ч. для манипуляций с записями.
"""

# ManagedIrbis ported from C# to Python.
# Python supported: 3.6 and higher
# IRBIS64 supported: 2014 and higher

from cbsvibpyirbis._common import ADMINISTRATOR, BRIEF, CATALOGER, close_async, \
    init_async, get_event_loop, LAST, LOCKED, LOGICALLY_DELETED, \
    NON_ACTUALIZED, NOT_CONNECTED, PHYSICALLY_DELETED, prepare_format, \
    remove_comments

from cbsvibpyirbis.alphabet import AlphabetTable, load_alphabet_table, \
    UpperCaseTable, load_uppercase_table
from cbsvibpyirbis.database import DatabaseInfo
from cbsvibpyirbis.direct import DirectAccess, InvertedFile, MstControl, MstField,\
    MstFile, MstEntry, MstLeader, MstRecord, XrfFile, XrfRecord
from cbsvibpyirbis.error import IrbisError, IrbisFileNotFoundError
from cbsvibpyirbis.export import read_iso_record, read_text_record, STOP_MARKER, \
    write_iso_record, write_text_record
from cbsvibpyirbis.ini import IniFile, IniLine, IniSection
from cbsvibpyirbis.menus import load_menu, MenuEntry, MenuFile
from cbsvibpyirbis.opt import load_opt_file, OptFile
from cbsvibpyirbis.par import load_par_file, ParFile
from cbsvibpyirbis.process import Process
from cbsvibpyirbis.query import ClientQuery
from cbsvibpyirbis.records import Field, RawRecord, Record, SubField
from cbsvibpyirbis.resource import Resource, ResourceDictionary
from cbsvibpyirbis.response import ServerResponse
from cbsvibpyirbis.search import CellResult, FoundLine, SearchParameters, \
    SearchScenario, TextParameters, TextResult
from cbsvibpyirbis.specification import FileSpecification
from cbsvibpyirbis.stats import ClientInfo, ServerStat
from cbsvibpyirbis.table import TableDefinition
from cbsvibpyirbis.terms import PostingParameters, TermInfo, TermParameters, \
    TermPosting
from cbsvibpyirbis.tree import load_tree_file, TreeFile, TreeNode
from cbsvibpyirbis.user import UserInfo
from cbsvibpyirbis.version import ServerVersion

from cbsvibpyirbis.connection import Connection


__version__ = '0.2'
__author__ = 'Alexey Mironov'
__email__ = 'amironov73@gmail.com'

__title__ = 'irbis'
__summary__ = 'universal client software for IRBIS64 - popular ' + \
              'russian library automation system'
__uri__ = 'http://arsmagna.ru'

__license__ = 'MIT License'
__copyright__ = 'Copyright 2018-2021 Alexey Mironov'

__all__ = ['ADMINISTRATOR', 'AlphabetTable', 'BRIEF', 'CATALOGER',
           'CellResult', 'ClientInfo', 'ClientQuery', 'close_async',
           'Connection', 'DatabaseInfo', 'DirectAccess', 'irbis_event_loop',
           'IrbisError', 'IrbisFileNotFoundError', 'Field',
           'FileSpecification', 'FoundLine', 'IniFile', 'IniLine',
           'IniSection', 'init_async', 'InvertedFile',
           'load_alphabet_table', 'load_menu', 'load_opt_file',
           'load_par_file', 'load_tree_file', 'load_uppercase_table',
           'LAST', 'LOCKED', 'LOGICALLY_DELETED', 'MenuEntry',
           'MenuFile', 'MstControl', 'MstField', 'MstFile',
           'MstEntry', 'MstLeader', 'MstRecord', 'NON_ACTUALIZED',
           'NOT_CONNECTED', 'OptFile', 'ParFile', 'PHYSICALLY_DELETED',
           'PostingParameters', 'prepare_format', 'Process', 'RawRecord',
           'read_iso_record', 'read_text_record', 'Record', 'remove_comments',
           'Resource', 'ResourceDictionary', 'SearchParameters',
           'SearchScenario', 'ServerResponse', 'ServerStat', 'ServerVersion',
           'STOP_MARKER', 'SubField', 'TableDefinition', 'TermInfo',
           'TermParameters', 'TextResult', 'TermPosting', 'TextParameters',
           'TreeFile', 'TreeNode', 'UpperCaseTable', 'UserInfo',
           'write_iso_record', 'write_text_record', 'XrfFile', 'XrfRecord']
