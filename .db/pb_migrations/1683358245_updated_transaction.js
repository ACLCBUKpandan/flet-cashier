migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("cwa2qqelcfsk6yr")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "klmfb08c",
    "name": "details",
    "type": "relation",
    "required": false,
    "unique": false,
    "options": {
      "collectionId": "o4mdikjauelurab",
      "cascadeDelete": false,
      "minSelect": null,
      "maxSelect": null,
      "displayFields": [
        "quantity",
        "product"
      ]
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("cwa2qqelcfsk6yr")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "klmfb08c",
    "name": "details",
    "type": "relation",
    "required": false,
    "unique": false,
    "options": {
      "collectionId": "o4mdikjauelurab",
      "cascadeDelete": false,
      "minSelect": null,
      "maxSelect": null,
      "displayFields": [
        "product",
        "quantity"
      ]
    }
  }))

  return dao.saveCollection(collection)
})
