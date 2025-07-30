import logging
from operator import itemgetter

from bson import ObjectId

import torii as Torii
from torii.dao.abstract_dao import AbstractDao


class UserManager(AbstractDao):

    COLLECTION_USERS = 'users'
    COLLECTION_SESSION = 'sessions'
    COLLECTION_TEAMS = 'teams'

    CACHED_TEAMS = []

    def __init__(self, torii):
        self.torii = torii
        self.torii_db = torii.mongo_database_torii
        self._logger = logging.getLogger('torii')
        
        self.user = None

    def check_user_permission(self, bo_class_name, read=False, write=False) -> tuple[bool, str]:
        """
        Checks User permissions for the collection in context.

        Checks if class is readable/writeable and if User is in the same team as the said class,
        from Torii.bo_classes collection.

        :param bo_class_name: the name of the BO class to check.
        :param read: Set True if User is reading any document, otherwise False.
        :param write: Set True if User is writing, updating or deleting any document, otherwise False.
        :return: A bool to identify if User has permission, and a str explaining the reason.
        """
        if not self.user:
            self.update_user()

        if self.user.admin:
            return True, 'User is admin.'

        bo_class = next((item for item in self.CACHED_BO_CLASSES if item['name'] == bo_class_name), None)
        if not bo_class:
            collection_classes = self.torii_db.get_collection(self.COLLECTION_BO_CLASSES)
            bo_class = self.find_one(collection_classes, {'name': bo_class_name})
            if bo_class is not None:
                self.CACHED_BO_CLASSES.append(bo_class)

        team = self.check_team_access(bo_class)

        if read and (team is None and not bo_class['fullReadable']):
            return False, 'Class is not readable.'

        if write and (team is None and not bo_class['fullWritable']):
            return False, 'Class is not writable.'

        return True, 'User checks out.'

    def check_team_access(self, document: dict):
        """
        Helper method.

        Check if User is in the same team as the document in question.

        :param document: JSON-like object representing the document.
        :return: The given document if teams match, otherwise None.
        """
        if not document:
            return None
        for team in self.user.teams:
            # Check if team ID match
            if team['id'] in map(itemgetter('id'), document['teams']):
                team_id = ObjectId(team['id'])
                # Check if team is enabled
                matched_team = next((item for item in self.CACHED_TEAMS if item['_id'] == team_id), None)
                if not matched_team:
                    collection = self.torii_db.get_collection(self.COLLECTION_TEAMS)
                    matched_team = self.find_one(collection, {'_id': team_id})
                    self.CACHED_TEAMS.append(matched_team)
                if matched_team['status'] == 'ENABLED':
                    return document
        return None

    def remove_no_access_documents(self, bo_class_name, documents: list) -> list:
        """
        Helper method.

        Removes all documents in the list that the User has no access to.

        :param bo_class_name: The name of the BO class to check.
        :param documents: List of JSON-like objects that represent documents.
        :return: The filtered list.
        """
        if not bo_class_name and not documents:
            return []

        bo_class = next((item for item in self.CACHED_BO_CLASSES if item['name'] == bo_class_name), None)
        if not bo_class:
            collection_classes = self.torii_db.get_collection(self.COLLECTION_BO_CLASSES)
            bo_class = self.find_one(collection_classes, {'name': bo_class_name})
            if bo_class is not None:
                self.CACHED_BO_CLASSES.append(bo_class)

        if bo_class['fullReadable']:
            return documents

        return [document for document in documents if self.check_team_access(document)]

    def update_user(self) -> None:
        """
        Private helper method.

        Get the User by ID from the current Torii session.

        :return: The User as a JSON-like object.
        """
        user_id = ObjectId(self.torii.session.user['id'])
        collection = self.torii_db.get_collection(self.COLLECTION_USERS)
        user = self.find_one(collection, {'_id': user_id})
        user['_id'] = str(user['_id'])
        self.user = Torii.ToriiObject(user)
