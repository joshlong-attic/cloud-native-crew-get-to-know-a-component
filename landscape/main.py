import random
import sys
import threading
import time
import typing
import urllib.request

if __name__ == '__main__':
    import yaml


    class Project:

        def __init__(self, name: str = '', url: str = '', tags: typing.List[str] = []) -> None:
            super().__init__()
            self.name = name.lower()
            self.url = url
            self.tags = [a.lower() for a in tags]


    def cncf() -> typing.List[Project]:
        ret = []
        with urllib.request.urlopen('https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml') as cncl:
            obj = yaml.load(cncl, Loader=yaml.FullLoader)
            landscape = obj['landscape']
            for category in landscape:
                for subcategory in category['subcategories']:
                    for item in subcategory['items']:
                        ret.append(
                            Project(
                                name=item['name'],
                                url=item['homepage_url'],
                                tags=[category['name'], subcategory['name'], 'cncf']
                            )
                        )
        return ret


    def spring() -> typing.List[Project]:
        ret = []
        with urllib.request.urlopen(
                'https://raw.githubusercontent.com/spring-io/start.spring.io/main/start-site/src/main/resources/application.yml') as projects_json:
            objs = yaml.load_all(projects_json, Loader=yaml.FullLoader)
            good = None
            for o in objs:
                if good is None:
                    good = o
            initializr = good['initializr']

            def build_url_from(c):
                parts = []
                for p in 'groupId,artifactId,version'.split(','):
                    if p in c:
                        parts.append(c[p])
                return ':'.join(parts)

            for d in initializr['dependencies']:
                # print('\t', d['name'])
                for c in d['content']:
                    projects.append(Project(
                        name=c['name'],
                        url=build_url_from(c),
                        tags=[d['name'], 'spring'])
                    )
        return ret


    projects = []
    for func in [cncf, spring]:
        projects.extend(func())
    import json

    json_s = json.dumps(projects , default=vars )
    with open('projects.json', 'w') as fp:
        fp.write(json_s)
