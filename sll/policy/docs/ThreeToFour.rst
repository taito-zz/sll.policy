Plone-3::

    1. Delete Test plone instance
    2. Remove (Done for sll instance)
        /sll
            /kauppa
                ploneformmailer*
                toimitustapa
            /lomakkeet
                /liittymislomake/verkkomaksut-adapteri
                /old1
                /old2
                /liittyminen-2
                /liittyminen-3
            /ostoskori
            /product
        /sll/tuejatoimi/lahjoita/verkkomaksut-adapteri
        /sll/tuejatoimi/luonnonsuojelusenkeli/tue-vesiensuojelua/verkkomaksut-adapteri
        /sll/tuejatoimi/luonnonsuojelusenkeli/norppalahjoitus/verkkomaksut-adapteri
        /sll/tuejatoimi/luonnonsuojelusenkeli/lomaketestit
        /sll/tuejatoimi/tue-vesiensuojelua-4
        /sll/portal_skins/plone_tableless

    5. Remove (Done for sll instance)
            /portal_skins
                Deleting from Properties
                        cache_setup
                        LanguageToolFlags
                        PFGVerkkomaksut
    6. Uninstall (Done for sll instance)
        /portal_quickinstaller
            --> Uninstall
                CacheSetup
                CustomOverrides
            --> Contents
                CMFSquidTool
                CacheSetup
                CustomOverrides
                PFGVerkkomaksut
                Products.CMFSquidTool
                collective.pfg.paymentcollective.cart.core

    7. Remove
        /Control_Panel
            /Products
                CMFSquidTool
                CacheSetup
                CustomOverrides
        /Control_Panel
            /TranslationService
                *

    9. Copy and Paste::
        /banner
        /tuejatoimi/*FormFolders
        /pohjanmaa/pienvedet
        /lomakkeet



Plone-4::

    1. Add default_page to /sll Properties
    2. Migrate!
    3. Create anothre plone site and copy portal_registry to the sll site.


