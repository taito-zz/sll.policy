from StringIO import StringIO
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import IProduct, IAddableToCart
from collective.cart.core.content.product import ProductAnnotations
from collective.cart.core.interfaces import IPrice
from zope.component import getUtility


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


def migrate_price(self):
    catalog = getToolByName(self, 'portal_catalog')
    brains = catalog(
        object_provides=IAddableToCart.__identifier__)
    for brain in brains:
        obj = brain.getObject()
        product = IProduct(obj)
        product.price = getUtility(IPrice, name="decimal")(product.price, 2)
