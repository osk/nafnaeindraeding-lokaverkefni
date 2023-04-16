"""Test the mediawiki parser.""" ""
from lib.mediawiki_parser import parse_mediawiki_text
from lib.mediawiki_parser import parse_template_name
from lib.mediawiki_parser import parse_template_value


def test_parse_template_name():
    """Test parsing a template name."""
    assert parse_template_name("1") is None
    assert parse_template_name("Foo") == "Foo"


def test_parse_template_value():
    """Test parsing a template value."""
    assert parse_template_value("Foo") == "Foo"


def test_parse_empty():
    """Test parsing an empty string."""
    assert parse_mediawiki_text("") == {
        "templates": [],
        "all_pairs": [],
        "weak_relations": [],
        "intro_text": "",
    }


def test_parse_text():
    """Test parsing a string of MediaWiki text."""
    text = """{{Aðgreiningartengill|Jón Sigurðsson|Jón Sigurðsson}}\n{{Forsætisráðherra\n| nafn           = Jón Sigurðsson\n| búseta         = \n| mynd           = Sigurðsson by Þorláksson.jpg\n| myndastærð     = 200px\n| myndatexti1     = {{small|Málverk [[Þórarinn B. Þorláksson|Þórarins B. Þorlákssonar]] af Jóni Sigurðssyni.}}\n| titill= [[Forseti Alþingis]]\n| stjórnartíð_start = 2. júlí 1849\n| stjórnartíð_end = 10. ágúst 1853\n| stjórnartíð_start2 = 1. júlí 1857\n| stjórnartíð_end2 = 17. ágúst 1857\n| stjórnartíð_start3 = 1. júlí 1867\n| stjórnartíð_end3 = 1877\n| fæðingarnafn   = Jón Sigurðsson\n| fæddur = 17. júní 1811\n| fæðingarstaður = [[Hrafnseyri]] í [[Arnarfjörður|Arnarfirði]] á [[Vestfirðir|Vestfjörðum]], [[Ísland]]i\n| dánardagur = {{dauðadagur og aldur|1879|12|7|1811|6|17}}\n| dánarstaður    = [[Kaupmannahöfn]], [[Danmörk]]u\n| orsök_dauða    = \n| stjórnmálaflokkur = \n| þekktur_fyrir  = Að vera leiðtogi íslensku sjálfstæðisbaráttunnar á 19. öld.\n| starf          = Ritstjóri, stjórnmálamaður\n| laun           = \n| trú            = \n| háskóli        = [[Kaupmannahafnarháskóli]]\n| maki           = [[Ingibjörg Einarsdóttir]] (g. 1845)\n| börn           = \n| foreldrar      = Sigurður Jónsson og Þórdís Jónsdóttir\n| heimasíða      = \n| niðurmál       = \n| hæð            = \n| þyngd          = \n|undirskrift = Jón Sigurðsson undirskrift.png\n}}\n'''Jón Sigurðsson''' (17. júní 1811 – 7. desember 1879), oft nefndur '''Jón forseti''', var helsti leiðtogi Íslendinga í [[Sjálfstæðisbarátta Íslendinga|sjálfstæðisbaráttunni]] á 19. öld. Til þess að minnast hans var fæðingardagur hans valinn sem sá dagur sem [[Háskóli Íslands]] var stofnaður árið 1911 og sem [[Íslenski þjóðhátíðardagurinn|þjóðhátíðardagur Íslendinga]] („17. júní“) þegar [[lýðveldið Ísland]] var stofnað þann 17. júní árið 1944.\n\n== Uppeldi og nám ==\nJón Sigurðsson fæddist 17. júní árið 1811"""

    result = parse_mediawiki_text(text)

    assert len(result["templates"]) == 2
    print(result["all_pairs"])
    assert len(result["all_pairs"]) == 34
    assert result["weak_relations"] == [
        "Sjálfstæðisbarátta Íslendinga",
        "Háskóli Íslands",
        "Íslenski þjóðhátíðardagurinn",
        "lýðveldið Ísland",
    ]
    assert (
        result["intro_text"]
        == """'''Jón Sigurðsson''' (17. júní 1811 – 7. desember 1879), oft nefndur '''Jón forseti''', var helsti leiðtogi Íslendinga í [[Sjálfstæðisbarátta Íslendinga|sjálfstæðisbaráttunni]] á 19. öld. Til þess að minnast hans var fæðingardagur hans valinn sem sá dagur sem [[Háskóli Íslands]] var stofnaður árið 1911 og sem [[Íslenski þjóðhátíðardagurinn|þjóðhátíðardagur Íslendinga]] („17. júní“) þegar [[lýðveldið Ísland]] var stofnað þann 17. júní árið 1944."""
    )
