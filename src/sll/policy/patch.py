from Products.ATContentTypes.content.document import ATDocumentSchema
from Products.ATContentTypes.content.event import ATEventSchema
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ATContentTypes.content.newsitem import ATNewsItemSchema
from Products.ATContentTypes.content.schemata import marshall_register
from Products.PloneFormGen.content.form import FormFolderSchema


def finalizeATCTSchema(schema, tag_default=True, related_item_default=True, exclude_from_nav_default=True):
    """Finalizes an ATCT type schema to alter some fields
    """
    field = 'subject'
    if field in schema and tag_default:
        schema.changeSchemataForField(field, 'default')

    field = 'relatedItems'
    if field in schema and related_item_default:
        schema.changeSchemataForField(field, 'default')

    field = 'excludeFromNav'
    if field in schema and exclude_from_nav_default:
        schema.changeSchemataForField(field, 'default')

    marshall_register(schema)
    return schema


DocumentSchema = ATDocumentSchema.copy()
finalizeATCTSchema(DocumentSchema, tag_default=False)
document_schema = DocumentSchema

NewsItemSchema = ATNewsItemSchema.copy()
finalizeATCTSchema(NewsItemSchema, tag_default=False)
newsitem_schema = NewsItemSchema

EventSchema = ATEventSchema.copy()
finalizeATCTSchema(EventSchema)
event_schema = EventSchema

FolderSchema = ATFolderSchema.copy()
finalizeATCTSchema(FolderSchema, tag_default=False, related_item_default=False)
folder_schema = FolderSchema

FormSchema = FormFolderSchema.copy()
finalizeATCTSchema(FormSchema, tag_default=False, related_item_default=False)
form_schema = FormSchema
