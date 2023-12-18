import pytest
from portmap.core.models import Article

@pytest.mark.django_db
def test_get_query_structure():
    a = Article.objects.create(name='a1', datatype="DT", sources='s1,s2', destinations='d1,d2', title='foo', body='bar')
    result = Article.get_query_structure()

    assert len(result.keys()) == 1
    assert result['DT'] == {'s1':['d1','d2'],'s2':['d1','d2']}
