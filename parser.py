#!/usr/bin/env python

import os
import errno

def path_hierarchy(path):
    hierarchy = {
        '_type': 'folder',
        '_name': os.path.basename(path),
        '_path': path.replace('\\', '/').replace('/app/','/'),
    }

    try:
        hierarchy['children'] = [
            path_hierarchy(os.path.join(path, contents))
            for contents in os.listdir(path)
        ]
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        hierarchy['_type'] = 'file'

    return hierarchy

if __name__ == '__main__':
    import json
    import sys

    try:
        directory = sys.argv[1]
    except IndexError:
        directory = "."

    print(json.dumps(path_hierarchy(directory), indent=4, sort_keys=True, ensure_ascii=False))

    with open('/app/content_structure.json', 'w', encoding='utf-8') as f:
        json.dump(path_hierarchy(directory), f, indent=4, sort_keys=True, ensure_ascii=False)