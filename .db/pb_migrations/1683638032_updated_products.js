migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("x1odqfi7tattyu4")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "6rhur66t",
    "name": "image",
    "type": "file",
    "required": false,
    "unique": false,
    "options": {
      "maxSelect": 1,
      "maxSize": 5242880,
      "mimeTypes": [
        "image/jpeg"
      ],
      "thumbs": []
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("x1odqfi7tattyu4")

  // remove
  collection.schema.removeField("6rhur66t")

  return dao.saveCollection(collection)
})
