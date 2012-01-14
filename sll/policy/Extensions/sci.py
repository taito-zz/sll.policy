from StringIO import StringIO
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
try:
    from collective.cart.core.interfaces import IProduct, IAddableToCart#, IPotentiallyAddableToCart
    from collective.cart.core.content.product import ProductAnnotations
except ImportError:
    pass

def export_sci(self):
    catalog = getToolByName(self, 'portal_catalog')
    wftool = getToolByName(self, 'portal_workflow')
    putils = getToolByName(self, 'plone_utils')
    brains = catalog(portal_type=('SimpleCartItem'))
    data = []
    for brain in brains:
        obj = brain.getObject()
        parent = aq_parent(aq_inner(obj))
        item_id = '%s_new' % obj.getId()
        options = obj.getOptions()
        if len(options) == 0:
            parent.invokeFactory(
                'Document',
                id=item_id,
                title=obj.Title(),
                description=obj.Description(),
                text=obj.getShort_description(),
#                image=obj.getImage(),
            )
            item = parent[item_id]
            item.reindexObject()
            wftool.doActionFor(item, "publish")
            dat = dict(
                id = item_id,
                price = obj.getPrice(),
            )
            data.append(dat)
        else:
            for option in options:
                title = '%s %s' % (obj.Title(), option)
                item_id = '%s_%s' % (obj.getId(), list(options).index(option))
                parent.invokeFactory(
                    'Document',
                    id=item_id,
                    title=title,
                    description=obj.Description(),
                    text=obj.getShort_description(),
#                    image=obj.getImage(),
                )
                item = parent[item_id]
                item.reindexObject()
                wftool.doActionFor(item, "publish")
                dat = dict(
                    id = item_id,
                    price = obj.getPrice(),
                )
                data.append(dat)
        paths = [brain.getPath()]
        putils.deleteObjectsByPaths(paths=paths)
    return data

## Change [] to the actual products data.
DATA = [{'price': 13.0, 'id': 'index_html_0'}, {'price': 13.0, 'id': 'index_html_1'}, {'price': 13.0, 'id': 'index_html_2'}, {'price': 13.0, 'id': 'index_html_3'}, {'price': 13.0, 'id': 'index_html_4'}, {'price': 13.0, 'id': 'index_html_5'}, {'price': 1.6000000000000001, 'id': 'lahetyskuori_new'}, {'price': 1.8999999999999999, 'id': 'avolehtioA470_new'}, {'price': 0.90000000000000002, 'id': 'avolehtioa670_new'}, {'price': 0.69999999999999996, 'id': 'avolehtioa770_new'}, {'price': 2.0499999999999998, 'id': 'kierrevihkoa440_new'}, {'price': 1.55, 'id': 'kierrevihkoa540_new'}, {'price': 0.90000000000000002, 'id': 'kierrevihkoa640_new'}, {'price': 2.7000000000000002, 'id': 'kierrevihkoa480_new'}, {'price': 1.8999999999999999, 'id': 'kierrevihkoa580_new'}, {'price': 2.0499999999999998, 'id': 'nidottuvihkoa440_new'}, {'price': 1.55, 'id': 'nidottuvihkoa540_new'}, {'price': 0.90000000000000002, 'id': 'nidottuvihkoa640_new'}, {'price': 2.5499999999999998, 'id': 'teknikkolehtioa470_new'}, {'price': 2.6000000000000001, 'id': 'luentolehtioa470_new'}, {'price': 1.95, 'id': 'luentolehtioa5100_new'}, {'price': 2.6000000000000001, 'id': 'kierreluentolehtioa460_new'}, {'price': 4.7000000000000002, 'id': 'postitindexkuulakarkikyna_new'}, {'price': 3.7999999999999998, 'id': 'norppateippi_new'}, {'price': 7.2000000000000002, 'id': 'norppateippitayttopakkaus_new'}, {'price': 33.0, 'id': 'postittarralaputvalknorppa_new'}, {'price': 19.0, 'id': 'postittarralaputnorppa_new'}, {'price': 21.0, 'id': 'postittarralaputblue_new'}, {'price': 18.0, 'id': 'postittarralaputgreen_new'}, {'price': 7.5, 'id': 'postittarralaputyellow_new'}, {'price': 18.0, 'id': 'postittarralaputpink_new'}, {'price': 4.7000000000000002, 'id': 'korostuskyna-sininen_new'}, {'price': 4.7000000000000002, 'id': 'korostuskyna-keltainen_new'}, {'price': 7.5, 'id': 'ekologiset-viestilaput-38x51_new'}, {'price': 18.0, 'id': 'ekologiset-viestilaput-76x76_new'}, {'price': 21.0, 'id': 'ekologiset-viestilaput-76x127_new'}, {'price': 2.3500000000000001, 'id': 'karhulehtio-a4_new'}, {'price': 1.75, 'id': 'norppalehtio-a5_new'}, {'price': 1.3500000000000001, 'id': 'lapinpollolehtio-a6_new'}, {'price': 1.1499999999999999, 'id': 'lohilehtio-a7_new'}, {'price': 10.0, 'id': 'ekologinen-z-notes-annostelijassa_new'}, {'price': 12.0, 'id': 'ekologinen-viestilappukuutio-vihrea_new'}, {'price': 12.0, 'id': 'ekologinen-viestilappukuutio-keltainen_new'}, {'price': 14.0, 'id': 'scotch-magic-yleisteippi_new'}, {'price': 18.0, 'id': 'ekologiset-viestilaput-76x76-keltainen_new'}, {'price': 21.0, 'id': 'ekologiset-viestilaput-76x127-keltainen_new'}, {'price': 12.5, 'id': 'luonnonpoluilla_new'}, {'price': 12.5, 'id': 'sienikirja_new'}, {'price': 12.5, 'id': 'lintukirja_new'}, {'price': 12.5, 'id': 'ulos-kalaan_new'}, {'price': 9.5, 'id': 'pieni-maastokirja-otokat_new'}, {'price': 9.5, 'id': 'pieni-maastokirja-jaljet_new'}, {'price': 22.0, 'id': 'norppa_new'}, {'price': 22.0, 'id': 'merikotka_new'}, {'price': 22.899999999999999, 'id': 'norppapaitavalkoinen_0'}, {'price': 22.899999999999999, 'id': 'norppapaitavalkoinen_1'}, {'price': 22.899999999999999, 'id': 'norppapaitavalkoinen_2'}, {'price': 22.899999999999999, 'id': 'norppapaitavalkoinen_3'}, {'price': 22.899999999999999, 'id': 'norppapaitavalkoinen_4'}, {'price': 22.899999999999999, 'id': 'norppapaitamusta_0'}, {'price': 22.899999999999999, 'id': 'norppapaitamusta_1'}, {'price': 22.899999999999999, 'id': 'norppapaitamusta_2'}, {'price': 22.899999999999999, 'id': 'norppapaitamusta_3'}, {'price': 22.899999999999999, 'id': 'norppapaitamusta_4'}, {'price': 19.899999999999999, 'id': 'luonnonkukkapaita_0'}, {'price': 19.899999999999999, 'id': 'luonnonkukkapaita_1'}, {'price': 19.899999999999999, 'id': 'luonnonkukkapaita_2'}, {'price': 10.0, 'id': 'kurki_new'}, {'price': 2.5, 'id': 'talviset_new'}, {'price': 2.5, 'id': 'marjat_new'}, {'price': 2.5, 'id': 'kirjeensulkijatkukat_new'}, {'price': 2.5, 'id': 'kirjeensulkijatelainlapset_new'}, {'price': 2.5, 'id': 'kirjeensulkijatnorppa_new'}, {'price': 2.5, 'id': 'kukat_new'}, {'price': 2.5, 'id': 'simplecartitem.2008-05-06.5065155696_new'}, {'price': 2.5, 'id': 'elainlapset_new'}, {'price': 2.5, 'id': 'norppa_new'}, {'price': 2.0, 'id': 'eimainoksia_new'}, {'price': 1.2, 'id': 'harakankellot_new'}, {'price': 1.2, 'id': 'karhupaivaunilla_new'}, {'price': 1.2, 'id': 'norppalepokivella_new'}, {'price': 1.2, 'id': 'joutsenet_new'}, {'price': 1.2, 'id': 'kesainenmaisema_new'}, {'price': 7.5, 'id': 'postikorttipaketti_new'}, {'price': 22.899999999999999, 'id': 'norppapaitavalkoinen_0'}, {'price': 22.899999999999999, 'id': 'norppapaitavalkoinen_1'}, {'price': 22.899999999999999, 'id': 'norppapaitavalkoinen_2'}, {'price': 22.899999999999999, 'id': 'norppapaitavalkoinen_3'}, {'price': 22.899999999999999, 'id': 'norppapaitamusta_0'}, {'price': 22.899999999999999, 'id': 'norppapaitamusta_1'}, {'price': 22.899999999999999, 'id': 'norppapaitamusta_2'}, {'price': 19.899999999999999, 'id': 'luonnonkukkapaita_0'}, {'price': 19.899999999999999, 'id': 'luonnonkukkapaita_1'}, {'price': 19.899999999999999, 'id': 'luonnonkukkapaita_2'}, {'price': 1.2, 'id': 'lammin-henkays-talvisaassa_0'}, {'price': 1.2, 'id': 'lammin-henkays-talvisaassa_1'}, {'price': 1.2, 'id': 'lammin-henkays-talvisaassa_2'}, {'price': 1.2, 'id': 'lammin-henkays-talvisaassa_3'}, {'price': 1.2, 'id': 'lammin-henkays-talvisaassa_4'}, {'price': 1.2, 'id': 'puna-poskilla_0'}, {'price': 1.2, 'id': 'puna-poskilla_1'}, {'price': 1.2, 'id': 'puna-poskilla_2'}, {'price': 1.2, 'id': 'puna-poskilla_3'}, {'price': 1.2, 'id': 'puna-poskilla_4'}, {'price': 1.2, 'id': 'herkkuhetki-tilhellakin_0'}, {'price': 1.2, 'id': 'herkkuhetki-tilhellakin_1'}, {'price': 1.2, 'id': 'herkkuhetki-tilhellakin_2'}, {'price': 1.2, 'id': 'herkkuhetki-tilhellakin_3'}, {'price': 1.2, 'id': 'herkkuhetki-tilhellakin_4'}, {'price': 1.2, 'id': 'joulupukki-tonttuineen_0'}, {'price': 1.2, 'id': 'joulupukki-tonttuineen_1'}, {'price': 1.2, 'id': 'joulupukki-tonttuineen_2'}, {'price': 1.2, 'id': 'joulupukki-tonttuineen_3'}, {'price': 1.2, 'id': 'joulupukki-tonttuineen_4'}, {'price': 1.2, 'id': 'joulukiire-taakse-jaa_0'}, {'price': 1.2, 'id': 'joulukiire-taakse-jaa_1'}, {'price': 1.2, 'id': 'joulukiire-taakse-jaa_2'}, {'price': 1.2, 'id': 'joulukiire-taakse-jaa_3'}, {'price': 1.2, 'id': 'joulukiire-taakse-jaa_4'}, {'price': 18.5, 'id': 'joulukorttipaketti_new'}, {'price': 5.2000000000000002, 'id': 'index_html_new'}, {'price': 7.0, 'id': '2010_new'}]

def setup_products(self):
    catalog = getToolByName(self, 'portal_catalog')
    for dat in DATA:
        data_id = dat['id']
        obj = catalog(id=data_id)[0].getObject()
        alsoProvides(obj, IAddableToCart)
#        obj.restrictedTraverse('make-addable-to-cart')()
        IAnnotations(obj)['collective.cart.core'] = ProductAnnotations()
        product = IProduct(obj)
        product.price = dat['price']
        product.unlimited_stock = True
        obj.reindexObject()


def setting_up_products(self):
    out = StringIO()
    print >> out, "Start setting up products."
    setup_products(self)
    print >> out, "Setting up completed."
    return out.getvalue()

