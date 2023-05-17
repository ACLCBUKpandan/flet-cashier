migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("cwa2qqelcfsk6yr")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "r0cwz1xu",
    "name": "cash",
    "type": "number",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "k0jnxqhi",
    "name": "change",
    "type": "number",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("cwa2qqelcfsk6yr")

  // remove
  collection.schema.removeField("r0cwz1xu")

  // remove
  collection.schema.removeField("k0jnxqhi")

  return dao.saveCollection(collection)
})
