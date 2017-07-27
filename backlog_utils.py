from __future__ import print_function
import argparse
import re
import sys
import logging
from os import path, walk
from codecs import open
from unicodedata import normalize

from jyven import maven

maven('com.nulab-inc:backlog4j:2.2.0')
from com.nulabinc.backlog4j.conf import BacklogJpConfigure
from com.nulabinc.backlog4j import BacklogClientFactory, BacklogAPIException
from com.nulabinc.backlog4j.api.option import CreateWikiParams, UpdateWikiParams

logging.basicConfig(level=logging.INFO)

issue_pattern = re.compile(r'[A-Z0-9]+-[0-9]+')

props_file = path.expanduser('~/.backlog.properties')
if not path.isfile(props_file):
    print('Backlog credentials not found. Store the following in ~/.backlog.properties:\n'
          'apiKey=[your Backlog API key]\n'
          'spaceId=[the ID of your Backlog space]')
    sys.exit(1)

with open(props_file) as infile:
    credentials = dict(line.strip().split('=') for line in infile)

conf = BacklogJpConfigure(credentials['spaceId']).apiKey(credentials['apiKey'])
backlog = BacklogClientFactory(conf).newClient()

def print_tickets():
    keys = set(key for line in sys.stdin for key in issue_pattern.findall(line))
    for key in sorted(keys):
        try:
            issue = backlog.getIssue(key)
            print('%s %s' % (key, issue.summary))
        except:
            pass

def iter_files(basepath, ext):
    for root, _, files in walk(path.expanduser(basepath)):
        for f in files:
            if f.endswith(ext):
                yield path.join(root, f)

def wiki_sync(project, prefix, root, force=False):
    wikis = backlog.getWikis(project)
    project_id = wikis[0].projectId if wikis else backlog.getProject(project).id
    for file_path in iter_files(path.expanduser(root), '.txt'):
        basename, _ = path.splitext(file_path)
        rel_path = path.relpath(basename, start=root)
        title = normalize('NFC', '/'.join([prefix] + rel_path.split(path.sep)).decode('utf-8'))
        body = normalize('NFC', read_file_guess_encoding(file_path).replace(u'\r\n', u'\n'))
        wiki_id = find_wiki_id(wikis, title)
        if wiki_id:
            print('Going to update wiki entry: %s' % title)
            if force:
                update = UpdateWikiParams(wiki_id)
                update.content(body)
                backlog.updateWiki(update)
        else:
            print('Going to create wiki entry: %s' % title)
            if force:
                create = CreateWikiParams(project_id, title, body)
                backlog.createWiki(create)

def find_wiki_id(wikis, title):
    for wiki in wikis:
        if wiki.name == title:
            return wiki
    return None

def read_file_guess_encoding(path):
    try:
        with open(path, encoding='sjis') as infile:
            return infile.read()
    except UnicodeDecodeError, e:
        with open(path, encoding='utf-8') as infile:
            return infile.read()


def main():
    parser = argparse.ArgumentParser(description='Utils for Backlog')
    parser.add_argument('--verbose', '-v', action='count', default=0)

    subparsers = parser.add_subparsers(dest='tool')

    keys_parser = subparsers.add_parser('tickets', help='Look up ticket titles based on keys piped into stdin')

    wiki_parser = subparsers.add_parser('wiki', help='Sync a tree of .txt articles with a project wiki')
    wiki_parser.add_argument('project', help='Project code')
    wiki_parser.add_argument('prefix', help='Prefix for wiki titles')
    wiki_parser.add_argument('root', help='Root of local tree containing wiki articles in .txt format')
    wiki_parser.add_argument('--force', '-f', action='store_true', help='Actually make changes (not a dry run)')

    args = parser.parse_args()

    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels) - 1, args.verbose)]
    logging.getLogger().setLevel(level)

    if args.tool == 'tickets':
        print_tickets()
    elif args.tool == 'wiki':
        wiki_sync(args.project, args.prefix, args.root, force=args.force)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
