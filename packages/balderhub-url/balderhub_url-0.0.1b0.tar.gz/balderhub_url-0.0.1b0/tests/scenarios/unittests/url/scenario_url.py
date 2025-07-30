from .abstract_scenario_unittest import AbstractScenarioUnittestUrl
from balderhub.url.lib.utils import Url


class ScenarioUrl(AbstractScenarioUnittestUrl):

    def test_eq(self, url_without_path: Url):
        assert url_without_path == url_without_path
        assert url_without_path == Url('https://balder.dev')

    def test_str(self, url_without_path: Url, url_without_path_with_backslash, schema_url_blog):
        assert str(url_without_path) == "https://balder.dev"
        assert url_without_path.as_string() == "https://balder.dev"
        assert str(url_without_path_with_backslash) == "https://balder.dev/"
        assert url_without_path_with_backslash.as_string() == "https://balder.dev/"
        assert str(schema_url_blog) == "https://balder.dev/blog/<int:blog_id>"
        assert schema_url_blog.as_string() == "https://balder.dev/blog/<int:blog_id>"

    def test_query_params(self, url_with_query):
        query_params = url_with_query.get_query_parameters()
        assert len(query_params) == 1
        assert 'q' in query_params
        assert query_params['q'] == '1'
