migrate((db) => {
  const collection = new Collection({
    "id": "cwa2qqelcfsk6yr",
    "created": "2023-05-06 07:26:45.634Z",
    "updated": "2023-05-06 07:26:45.634Z",
    "name": "transaction",
    "type": "base",
    "system": false,
    "schema": [
      {
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
          "displayFields": []
        }
      },
      {
        "system": false,
        "id": "q2w9hzmw",
        "name": "user",
        "type": "relation",
        "required": false,
        "unique": false,
        "options": {
          "collectionId": "_pb_users_auth_",
          "cascadeDelete": false,
          "minSelect": null,
          "maxSelect": 1,
          "displayFields": []
        }
      }
    ],
    "listRule": null,
    "viewRule": null,
    "createRule": null,
    "updateRule": null,
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("cwa2qqelcfsk6yr");

  return dao.deleteCollection(collection);
})
