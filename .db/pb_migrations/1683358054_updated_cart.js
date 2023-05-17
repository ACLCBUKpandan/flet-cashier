migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("o4mdikjauelurab")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "dqjmndij",
    "name": "cart",
    "type": "relation",
    "required": false,
    "unique": false,
    "options": {
      "collectionId": "o4mdikjauelurab",
      "cascadeDelete": false,
      "minSelect": null,
      "maxSelect": 1,
      "displayFields": []
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("o4mdikjauelurab")

  // remove
  collection.schema.removeField("dqjmndij")

  return dao.saveCollection(collection)
})
