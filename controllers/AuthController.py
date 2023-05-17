from database.db import pb
from models.User import User


def login(username, password):
    results = pb.collection('users').auth_with_password(username, password)
    user_dict = results.record.__dict__['collection_id']
    user = User(
        collection_id=user_dict['collectionId'],
        collection_name=user_dict['collectionName']
    ).load(data=user_dict)
    pb.auth_store.save(token=results.token, model=user)
    token = "" if pb.auth_store.token is None else pb.auth_store.token

    return token is not None


def is_valid_token() -> bool:
    token = pb.auth_store.token
    return token is not None


def logout():
    pb.auth_store.clear()


if __name__ == '__main__':
    login('james', '12345687890')
