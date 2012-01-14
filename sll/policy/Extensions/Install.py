import transaction
from Products.CMFCore.utils import getToolByName

PRODUCT_DEPENDENCIES = (
    'PloneFormGen',
    'PFGExtendedMailAdapter',
    'PFGSelectionStringField',
    'NewSllSkin',
    'collective.folderlogo',
    'collective.pfg.payment'
    'collective.cart.core',
    'collective.cart.shipping',
    'collective.pfg.showrequest',
)
EXTENSION_PROFILES = ('sll.policy:default',)

def install(self, reinstall=False):
    installer = getToolByName(self, 'portal_quickinstaller')
    for product in PRODUCT_DEPENDENCIES:
        if reinstall and installer.isProductInstalled(product):
            installer.reinstallProducts([product])
            transaction.savepoint()
        elif not installer.isProductInstalled(product):
            installer.installProduct(product)
            transaction.savepoint()
    setup = getToolByName(self, 'portal_setup')
    for extension_id in EXTENSION_PROFILES:
        profile = 'profile-%s' % extension_id
        setup.runAllImportStepsFromProfile(
            profile,
            purge_old=False,
        )
        product_name = extension_id.split(':')[0]
        installer.notifyInstalled(product_name)
        transaction.savepoint()
