"""Tests for relation extraction functions."""
import json

from lib.relations import (
    calculate_strong_relations,
    parse_relation_maki,
    derive_relation_spouse,
    parse_relation_haskoli,
)
from lib.mediawiki_parser import parse_mediawiki_text_and_add_to_article


def test_parse_relation_maki_single():
    """Test that a single relation is parsed correctly."""
    assert parse_relation_maki("A", "[[B]] (g. 1845)") == [
        {
            "type": "spouse",
            "source": "A",
            "target": "B",
        }
    ]


def test_parse_relation_maki_multiple():
    """Test that multiple relations are parsed correctly."""
    assert parse_relation_maki("A", "[[B]] (g. 1845), [[C]], áður [[D]]") == [
        {
            "type": "spouse",
            "source": "A",
            "target": "B",
        },
        {
            "type": "spouse",
            "source": "A",
            "target": "C",
        },
        {
            "type": "spouse",
            "source": "A",
            "target": "D",
        },
    ]


def test_parse_relation_maki_not_linked():
    """Test that relations are not parsed if they are not linked."""
    assert not parse_relation_maki("A", "B (g. 1845)")


def test_derive_relation_spouse():
    """Test that a relation is derived correctly."""
    assert derive_relation_spouse(
        {
            "type": "spouse",
            "source": "A",
            "target": "B",
        }
    ) == [
        {
            "type": "spouse",
            "source": "B",
            "target": "A",
        }
    ]


def test_parse_relation_haskoli_single():
    """Test that a single relation is parsed correctly."""
    assert parse_relation_haskoli("A", "[[B]]") == [
        {
            "type": "studied_at",
            "source": "A",
            "target": "B",
        }
    ]


def test_calculate_strong_relation_for_jon_forseti():
    """Test that strong relations are calculated correctly."""
    json_str = "{\"title\":\"Jón Sigurðsson (forseti)\",\"id\":8336,\"namespace\":0,\"text\":\"{{Aðgreiningartengill|Jón Sigurðsson|Jón Sigurðsson}}\\n{{Forsætisráðherra\\n| nafn           = Jón Sigurðsson\\n| búseta         = \\n| mynd           = Sigurðsson by Þorláksson.jpg\\n| myndastærð     = 200px\\n| myndatexti1     = {{small|Málverk [[Þórarinn B. Þorláksson|Þórarins B. Þorlákssonar]] af Jóni Sigurðssyni.}}\\n| titill= [[Forseti Alþingis]]\\n| stjórnartíð_start = 2. júlí 1849\\n| stjórnartíð_end = 10. ágúst 1853\\n| stjórnartíð_start2 = 1. júlí 1857\\n| stjórnartíð_end2 = 17. ágúst 1857\\n| stjórnartíð_start3 = 1. júlí 1867\\n| stjórnartíð_end3 = 1877\\n| fæðingarnafn   = Jón Sigurðsson\\n| fæddur = 17. júní 1811\\n| fæðingarstaður = [[Hrafnseyri]] í [[Arnarfjörður|Arnarfirði]] á [[Vestfirðir|Vestfjörðum]], [[Ísland]]i\\n| dánardagur = {{dauðadagur og aldur|1879|12|7|1811|6|17}}\\n| dánarstaður    = [[Kaupmannahöfn]], [[Danmörk]]u\\n| orsök_dauða    = \\n| stjórnmálaflokkur = \\n| þekktur_fyrir  = Að vera leiðtogi íslensku sjálfstæðisbaráttunnar á 19. öld.\\n| starf          = Ritstjóri, stjórnmálamaður\\n| laun           = \\n| trú            = \\n| háskóli        = [[Kaupmannahafnarháskóli]]\\n| maki           = [[Ingibjörg Einarsdóttir]] (g. 1845)\\n| börn           = \\n| foreldrar      = Sigurður Jónsson og Þórdís Jónsdóttir\\n| heimasíða      = \\n| niðurmál       = \\n| hæð            = \\n| þyngd          = \\n|undirskrift = Jón Sigurðsson undirskrift.png\\n}}\\n'''Jón Sigurðsson''' (17. júní 1811 – 7. desember 1879), oft nefndur '''Jón forseti''', var helsti leiðtogi Íslendinga í [[Sjálfstæðisbarátta Íslendinga|sjálfstæðisbaráttunni]] á 19. öld. Til þess að minnast hans var fæðingardagur hans valinn sem sá dagur sem [[Háskóli Íslands]] var stofnaður árið 1911 og sem [[Íslenski þjóðhátíðardagurinn|þjóðhátíðardagur Íslendinga]] („17. júní“) þegar [[lýðveldið Ísland]] var stofnað þann 17. júní árið 1944.\\n\\n== Uppeldi og nám ==\\nJón Sigurðsson fæddist 17. júní árið 1811 á [[Hrafnseyri]] í [[Arnarfjörður|Arnarfirði]] á [[Vestfirðir|Vestfjörðum]]. Hann fæddist á Bótolfsvöku (á laugardegi). Hann var skírður í höfuðið á móðurafa sínum, Jóni Ásgeirssyni. Faðir hans var Sigurður Jónsson, prestur og móðir hans Þórdís Jónsdóttir, húsfreyja. Jón átti tvö systkini: Jens og Margréti. Margrét ól manninn á Vestfjörðum og gerðist bóndi á [[Steinanes]]i í Arnarfirði. Jens fluttist síðar til [[Reykjavík]]ur og gerðist kennari og rektor [[Lærði skólinn|Lærða skólans]]. Á uppvaxtarárunum stundaði Jón nám hjá föður sínum.\\n\\nJón fluttist til [[Reykjavík]]ur átján ára gamall og tók stúdentspróf árið 1829 með ágætiseinkunn. Í Reykjavík vann hann í verslun föðurbróður síns, Einars Jónssonar, og þannig kynntist hann verðandi eiginkonu sinni Ingibjörgu, sem var dóttir Einars. Vorið 1830 réðist Jón til starfa sem [[biskupsritari]] hjá [[Steingrímur Jónsson|Steingrími Jónssyni]], [[biskup Íslands|biskupi Íslands]] í [[Laugarnes]]i. Steingrímur átti stæðilegt bókasafn og fékk Jón afnot af því. Þar vaknaði áhugi hans á [[saga Íslands|sögu Íslands]] og [[íslensk menning|menningu]].\\n\\nJón hélt til [[Kaupmannahöfn|Kaupmannahafnar]] árið 1833 til náms og þar bjó hann til æviloka. Í fyrstu nam hann [[málfræði]] en þá fékk hann styrk frá gjafasjóði Árna Magnússonar og sneri sér að lestri íslenskra bókmennta og seinna sögu við [[Kaupmannahafnarháskóli|Kaupmannahafnarháskóla]]. Hann lauk þó aldrei prófi. Hann vann sem málvísindamaður hjá [[Árnasafn]]i.  Sem slíkur var hann fenginn til að aðstoða færeyska prestinn Hammershaimb við að gera færeyskt ritmál og réð því að færeysk stafsetning tekur mið af uppruna orða miklu fremur en framburði. Þá var hann aðalmaðurinn á bak við tímaritið [[Ný félagsrit]] allan tímann sem það kom út á árunum 1841-73.\\n\\nJón var kosinn þingmaður [[Ísafjarðarsýsla|Ísafjarðarsýslu]] árið 1844 og sótti hann Ísland heim á ný árið 1845 til þess að geta setið á Alþingi. Jón sat sem [[forseti Alþingis]] árin 1849-53, einn og hálfan mánuð árið 1857 og loks frá 1867–77. Viðurnefnið ''forseti'' fékk hann hins vegar vegna þess að hann var frá 1851 forseti Hafnardeildar [[Hið íslenska bókmenntafélag|Hins íslenska bókmenntafélags]]. Á tímabilinu sem Jón var þingmaður kom Alþingi saman annað hvert ár og stóð í sex vikur. Jón gat því búið í Kaupmannahöfn en komið heim og sótt þing. Einn helsti stuðningsmaður heima í héraði var varaþingmaður Jóns, [[Magnús Einarsson á Hvilft]] í [[Önundarfjörður|Önundarfirði]] og segir í skrifum [[Lúðvík Kristjánsson|Lúðvíks Kristjánssonar]], fræðimaður, að berlega sé ljóst að Magnús á Hvilft er maðurinn sem Íslendingar eiga að þakka hina traustu forystu í baklandi Jóns á Vestfjörðum og gaf honum undirstöðu til sinnar kröftugu sjálfstæðisbaráttu. \\n\\nEiginkona Jóns var [[Ingibjörg Einarsdóttir]], sem sat í festum heima á Íslandi í tólf ár frá 1833 en þau giftust loks þegar hann kom heim á þingið 1845 þann 4. september. Nokkur aldursmunur var á hjónunum, hún var sjö árum eldri. Hjónin voru bræðrabörn eignuðust engin börn. Þau ólu upp systurson Jóns, Sigurð Jónsson, frá því hann var átta ára. Þau fluttust saman til Kaupmannahafnar og bjuggu lengst á Øster Voldgade 8 (sem núna heitir Øster Voldgade 12 ([[Jónshús]])), en þar voru þau frá árinu 1852 til andláts Jóns 1879. Götuna kölluðu Íslendingar ''Austurvegg''.\\n\\n== Sjálfstæðisbaráttan ==\\nFrá Danmörku átti Jón í samskiptum við fjölda Íslendinga bréfleiðis. Varðveist hafa yfir 6.000 sendibréf til Jóns frá um 870 bréfriturum. Jón var sérlega iðjusamur og tilbúinn að gera samlöndum sínum ýmsa greiða. Hann var í ágætri stöðu til áhrifa í Kaupmannahöfn og leituðu margir til hans, meðal annars til þess að biðja um lán. Fyrir vikið varð Jón vinsæll meðal Íslendinga.\\n\\nEinn helsti samstarfsmaður Jóns var nafni hans [[Jón Guðmundsson]], ritstjóri. Hann var stundum kallaður skuggi Jóns Sigurðssonar.\\n\\n{{tilvitnun2|Alþing á að vekja og glæða þjóðlífið og þjóðarandann, skólinn á að tendra hið andliga ljós , og hið andliga afl, og veita alla þá þekkíngu sem gjöra má menn hæfiliga til framkvæmdar öllu góðu, sem auðið má verða. Verzlunin á að styrkja þjóðaraflið líkamliga, færa velmegun í landið, auka og bæta atvinnuvegi og handiðnir, og efla með því aptur hið andliga, svo það verði á ny stofn annarra enn æðri og betri framfara og blómgunar eptir því sem tímar líða fram.|[http://timarit.is/view_page_init.jsp?pageId=2015210  Ný félagsrit, Megintexti (01.01.1842), Blaðsíða 67]}}\\n\\n[[Konungur Danmerkur]] afsalaði sér [[einveldi]] árið 1848 og við það tækifæri ritaði Jón ''[[Hugvekja til Íslendinga|Hugvekju til Íslendinga]]'' þar sem hann hvatti Íslendinga til baráttu fyrir sjálfstæði. Greinin birtist í Nýjum félagsritum það ár. Rök hans voru þau að við afnám einveldisins væri Ísland orðið að sjálfstæðu landi, líkt og fyrir [[Gamli sáttmáli|Gamla sáttmála]]. Á [[þjóðfundurinn 1851|þjóðfundinum 1851]] lagði hópur Íslendinga fram mótfrumvarp við frumvarp Danakonungs um stjórnskipun Íslands. [[Jørgen Ditlev Trampe]], stiftamtmaður Danakonungs á Íslandi, neitaði frumvarpinu framgöngu og brást þá Jón við og mótmælti framgöngu Trampe. Undir tóku viðstaddir með hinum fleygu orðum „[[Vér mótmælum allir]]“. Þessi atburður er talin marka þau tímamót að þaðan af var Jón talinn óumdeildur leiðtogi sjálfstæðisbaráttunnar. Eftir þjóðfundinn ganga sögur um að dönsk yfirvöld vildu ráða Jón af dögum en seinni rannsóknir benda til þess að ekkert sé til í því.<ref>{{vefheimild|url=http://www.mbl.is/mm/frettir/innlent/frett.html?nid=1091907|titill=Ráðgerðu dönsk yfirvöld að myrða Jón Sigurðsson?|ár=2004|mánuður=4. júlí|útgefandi=Morgunblaðið}}</ref>\\n\\nJón beitti sér fyrir [[verslunarfrelsi]], m.a. með útgáfu ritgerðar um verslun á Íslandi sem kom út árið 1843 þar sem hann vísar í verk [[Adam Smith]]s. Þrátt fyrir afnám [[einokunarverslun]]ar 1787 var verslun við aðra en þegna Danakonungs áfram bönnuð. \\n\\n[[Mynd:Reykjavik-Holavallakg-Jonforseti.JPG|thumb|right|Á legsteini Jóns í Hólavallagarði stendur „''Stein þenna reistu honum landar hans 1881''“.]]\\nJón lést 7. desember 1879 eftir langvinn veikindi. Ingibjörg eiginkona hans lést níu dögum seinna og eru þau bæði grafin í [[Hólavallagarður|Hólavallagarði]].\\n\\n== Minning Jóns ==\\n[[Mynd:Iceland 10 Kronur 1928 Banknote, Obverse only.jpg|thumb|right|Jón á tíu króna seðli frá árinu 1928.]]\\nHúsið, sem Jón og Ingibjörg kona hans bjuggu í í Kaupmannahöfn, er á Øster Voldgade 12 (var áður númer 8) og heitir [[Jónshús]]. Það er í eigu íslensku ríkisstjórnarinnar og er rekið sem safn í minningu hans. Við Hrafnseyri, fæðingarstað Jóns, er einnig rekið Safn Jóns Sigurðssonar.\\n\\nStytta af Jóni, eftir [[Einar Jónsson]], stóð upphaflega fyrir framan [[Stjórnarráðshúsið]] við Lækjargötu og var afhjúpuð 10. september 1911 af [[Kristján Jónsson (dómsstjóri og ráðherra)|Kristjáni Jónssyni]] ráðherra. Styttan var flutt árið 1931 á [[Austurvöllur|Austurvöll]] fyrir framan [[Alþingishúsið]], líkt og fyrst var lagt til og hefur verið þar síðan. 17. júní er einnig haldinn hátíðlegur þar sem minningu Jóns er haldið á lofti.\\n\\nMynd af Jóni prýðir íslenska 500 króna seðilinn. Andlit hans er einnig [[vatnsmerki]]ð á öllum íslenskum peningaseðlum.\\n\\nJóns er getið í  [[söguleg skáldsaga|sögulegu skáldsögunni]] ''[[Þegar kóngur kom]]'' eftir Helga Ingólfsson.\\n\\n== Tilvitnanir ==\\n{{reflist}}\\n\\n== Heimildir ==\\n* Guðjón Friðriksson. 2002. ''Jón Sigurðsson- Ævisaga- Fyrra bindi.'' Mál og menning, Reykjavík.\\n* Guðjón Friðriksson. 2003. ''Jón Sigurðsson- Ævisaga- Seinna bindi.'' Mál og menning, Reykjavík.\\n\\n== Tenglar ==\\n{{commonscat|Jón Sigurðsson|Jóni Sigurðssyni}}\\n* [http://www.althingi.is/jon_sigurdsson/ Þingstörf Jóns Sigurðssonar á vef Alþingis] {{Webarchive|url=https://web.archive.org/web/20120412161137/http://www.althingi.is/jon_sigurdsson/ |date=2012-04-12 }}\\n* [http://www.althingi.is/cv.php4?nfaerslunr=6 Æviágrip á vef Alþingis]\\n* [http://www.hrafnseyri.is/ Vefur um Hrafnseyrar-safnið]\\n* [http://www.jonshus.is Heimasíða Jónshúss]\\n* [http://www.heimastjorn.is/leidin-til-sjalfstaedis/Jon-Sigurdsson/ Vefur um Heimastjórnina 1904 umfjöllun um Jón] {{Webarchive|url=https://web.archive.org/web/20120111202331/http://www.heimastjorn.is/leidin-til-sjalfstaedis/Jon-Sigurdsson/ |date=2012-01-11 }}\\n* [http://baekur.is/is/search/J$00f3n+Sigur$00f0sson/AUTHOR Verk eftir Jón Sigurðsson á Bækur.is] {{Webarchive|url=https://web.archive.org/web/20130523123754/http://baekur.is/is/search/J$00f3n+Sigur$00f0sson/AUTHOR |date=2013-05-23 }}\\n* [http://www.jonsigurdsson.is/ Vefur tileinkaður Jóni Sigurðssyni]\\n* [http://handrit.is/is/biography/view/JonSig004 Handrit Jóns Sigurðssonar á Handrit.is]\\n\\n=== Vísindavefurinn ===\\n* {{vísindavefurinn|3569|Hver var Jón Sigurðsson?}}\\n* {{vísindavefurinn|3573|Fyrir framan hvaða byggingu stóð minnisvarðinn um Jón Sigurðsson upphaflega?}}\\n* {{vísindavefurinn|3589|Getið þið sagt mér hvað faðir Jóns Sigurðsonar og móðir unnu við? Hvar fæddust þau?}}\\n* {{vísindavefurinn|6113|Hver var röksemdafærsla Jóns Sigurðssonar fyrir aukinni sjálfstjórn Íslendinga?}}\\n* {{vísindavefurinn|2006|Hvað voru Ný félagsrit?}}\\n* [http://islandsmyndir.is/html_skjol/vestfirdir/Hrafnseyri-2011/index.html Ljósmyndir af safnahúsinu á Hrafnseyri í borði islandsmyndir.is] {{Webarchive|url=https://web.archive.org/web/20120926112731/http://www.islandsmyndir.is/html_skjol/vestfirdir/Hrafnseyri-2011/index.html |date=2012-09-26 }}\\n\\n=== Blaða- og tímaritsgreinar ===\\n* [http://www.timarit.is/titlebrowse.jsp?t_id=300030&lang=0 Ný félagsrit]\\n* [http://www.timarit.is/?issueID=304079&pageSelected=0&lang=0 Greinin „Hugvekja til Íslendinga“ í Nýjum félagsritum]\\n* [http://www.timarit.is/?issueID=311422&pageSelected=0&lang=0 Ræða Jóns Jónssonar sagnfræðings á Alþingi þann 17. júní 1911], Þjóðviljinn 23. júní 1911\\n* [http://www.timarit.is/?issueID=312265&pageSelected=0&lang=0 ''Jón Sigurðsson''], grein í tímaritinu Reykjavík 17. júní 1911\\n* [http://www.timarit.is/?issueID=414940&pageSelected=2&lang=0 ''Nánustu ættingjar Jóns Sigurðssonar''; grein í Morgunblaðinu 17. júní 1961]\\n* [http://www.timarit.is/?issueID=414940&pageSelected=8&lang=0 ''Á Hrafnseyri 17. júní 1911''], Morgunblaðið 17. júní 1961\\n* [http://www.timarit.is/?issueID=414940&pageSelected=10&lang=0 ''Svipmyndir úr lífi Jóns forseta''; grein í Morgunblaðinu 17. júní 1961]\\n* [http://www.timarit.is/?issueID=416485&pageSelected=2&lang=0 ''Á Jólum hjá Jóni Sigurðssyni''; í Lesbók Morgunblaðsins 1933] grein eftir [[Indriði Einarsson|Indriða Einarsson]] leikskáld\\n* [http://www.timarit.is/?issueID=409714&pageSelected=0&lang=0 ''Jón Sigurðsson forseti - þjóðskörungur Íslands''; grein í Morgunblaðinu 1944]\\n* [http://timarit.is/view_page_init.jsp?pageId=3296606 ''O´Connell, hin irska fyrirmynd Jóns Sigurðssonar''; grein í Lesbók Morgunblaðsins 1974]\\n* [http://timarit.is/view_page_init.jsp?pageId=2354720 ''Jón Sigurðsson''; grein í Vísi 1961]\\n* [http://timarit.is/view_page_init.jsp?pageId=1325785 ''Í íbúð Jóns Sigurðssonar''; grein í Morgunblaðinu 1959]\\n* [http://timarit.is/view_page_init.jsp?gegnirId=000524725 ''Jón Sigurðsson, fyrsti hagfræðingurinn'' ;Vísbending 20.12.2002]\\n* [https://timarit.is/page/6531437?iabr=on#page/n65/mode/1up/search/sigurður%20s%C3%ADvertsen Hvers vegna var Jón Sigurðsson ekki á þjóðhátíðinni 1874?;] [[Lúðvík Kristjánsson]], Skírnir janúar 1979, bls. 64&ndash;99.\\n* [https://timarit.is/page/4323426?iabr=on#page/n6/mode/1up Yfirlit yfir æfi Jóns Sigurðssonar;] Eiríkur Briem, Andvari janúar 1880, bls. 1&ndash;13.\\n\\n{{Töflubyrjun}}\\n{{Erfðatafla | fyrir=[[Þórður Sveinbjörnsson]] | titill=[[Forseti Alþingis]] | frá=2. júlí 1849 | til=10. ágúst 1853 | eftir=[[Hannes Stephensen]]}}\\n{{Erfðatafla | fyrir=[[Hannes Stephensen]] | titill=[[Forseti Alþingis]] | frá=1. júlí 1857 | til=17. ágúst 1857 | eftir=[[Jón Guðmundsson]]}}\\n{{Erfðatafla | fyrir=[[Halldór Jónsson]] | titill=[[Forseti Alþingis]] | frá=1. júlí 1867 | til=1877 | eftir=[[Pétur Pétursson]]}}\\n{{Töfluendir}}\\n\\n{{fd|1811|1879}}\\n[[Flokkur:Forsetar Alþingis]]\\n[[Flokkur:Íslendingar sem gengið hafa í Kaupmannahafnarháskóla]]\\n[[Flokkur:Íslenskir sagnfræðingar]]\\n[[Flokkur:Íslenskir stjórnmálamenn]]\\n[[Flokkur:Sjálfstæðisbarátta Íslendinga]]\\n[[Flokkur:Íslenskir sjálfstæðismenn]]\",\"aliases\":[],\"wikidata_id\":\"Q321275\"}"
    article = json.loads(json_str)

    article = parse_mediawiki_text_and_add_to_article(article)

    strong_relations = calculate_strong_relations(article)

    assert strong_relations == [
        {
            "type": "studied_at",
            "source": "Jón Sigurðsson (forseti)",
            "target": "Kaupmannahafnarháskóli",
        },
        {
            "type": "had_as_student",
            "target": "Jón Sigurðsson (forseti)",
            "source": "Kaupmannahafnarháskóli",
        },
        {
            "type": "spouse",
            "source": "Jón Sigurðsson (forseti)",
            "target": "Ingibjörg Einarsdóttir",
        },
        {
            "type": "spouse",
            "target": "Jón Sigurðsson (forseti)",
            "source": "Ingibjörg Einarsdóttir",
        },
    ]
