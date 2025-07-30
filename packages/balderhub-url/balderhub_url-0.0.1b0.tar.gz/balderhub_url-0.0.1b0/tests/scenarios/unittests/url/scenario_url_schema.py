from .abstract_scenario_unittest import AbstractScenarioUnittestUrl
from balderhub.url.lib.utils import Url


class ScenarioUrl(AbstractScenarioUnittestUrl):

    def test_schema_eq(self, schema_url_blog: Url, url_blog_article_1: Url):
        assert schema_url_blog.is_schema()
        assert not url_blog_article_1.is_schema()
        assert schema_url_blog != url_blog_article_1

    def test_schema_extract_parameters(self, schema_url_blog: Url, url_blog_article_1: Url):
        assert schema_url_blog.is_schema()
        assert not url_blog_article_1.is_schema()
        parameters = url_blog_article_1.extract_parameters(schema_url_blog)
        assert len(parameters) == 1
        assert 'blog_id' in parameters
        assert parameters['blog_id'] == 1

    def test_schema_wrong_type(self, schema_url_blog: Url, url_blog_article_2a: Url):
        try:
            _ = url_blog_article_2a.extract_parameters(schema_url_blog)
            assert False
        except ValueError as exc:
            assert str(exc) == "invalid literal for int() with base 10: '2a'"

    def test_fill_in_schema(self, schema_url_blog: Url, url_blog_article_1: Url):
        assert schema_url_blog.is_schema()
        assert not url_blog_article_1.is_schema()

        new_filled_url = schema_url_blog.fill_parameters(blog_id=1)
        assert new_filled_url == url_blog_article_1
        assert new_filled_url.compare(url_blog_article_1, allow_schemas=False)
        assert new_filled_url.compare(url_blog_article_1, allow_schemas=True)

    def test_query_params(self, schema_with_query):
        query_params = schema_with_query.get_query_parameters()
        assert len(query_params) == 1
        assert 'q' in query_params
        assert query_params['q'] == '<int:blog_id>'

    def test_fill_strref(self, schema_url_strref):
        new_url = schema_url_strref.fill_parameters(object_name='data')
        assert new_url == Url('https://balder.dev/data')
        new_url = schema_url_strref.fill_parameters(object_name='1')
        assert new_url == Url('https://balder.dev/1')
