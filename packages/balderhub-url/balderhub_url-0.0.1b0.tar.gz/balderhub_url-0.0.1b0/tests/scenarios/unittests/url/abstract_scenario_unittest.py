import balder
import balderhub.unit.scenarios
from balderhub.url.lib.utils import Url

class AbstractScenarioUnittestUrl(balderhub.unit.scenarios.ScenarioUnit):

    @balder.fixture('setup')
    def url_without_path(self):
        return Url('https://balder.dev')

    @balder.fixture('setup')
    def url_without_path_with_backslash(self):
        return Url('https://balder.dev/')

    @balder.fixture('setup')
    def url_blog(self):
        return Url('https://balder.dev/blog')

    @balder.fixture('setup')
    def schema_url_blog(self):
        return Url('https://balder.dev/blog/<int:blog_id>')

    @balder.fixture('setup')
    def schema_url_strref(self):
        return Url('https://balder.dev/<str:object_name>')

    @balder.fixture('setup')
    def url_blog_article_1(self):
        return Url('https://balder.dev/blog/1')

    @balder.fixture('setup')
    def url_blog_article_2(self):
        return Url('https://balder.dev/blog/2')

    @balder.fixture('setup')
    def url_blog_article_2a(self):
        return Url('https://balder.dev/blog/2a')

    @balder.fixture('setup')
    def url_with_query(self):
        return Url('https://balder.dev/blog/?q=1')

    @balder.fixture('setup')
    def schema_with_query(self):
        return Url('https://balder.dev/blog/?q=<int:blog_id>')
