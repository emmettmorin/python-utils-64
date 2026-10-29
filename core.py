import sys
import logging

class RobloxSessionManager:
    def __init__(self, auth_token):
        self.token = auth_token
        self.registry = {}

    def fetch_user_data(self, user_id):
        try:
            if not isinstance(user_id, int):
                raise TypeError(f'User ID must be integer, got {type(user_id).__name__}')
            
            if user_id < 0:
                raise ValueError('User ID cannot be negative')
                
            data = self.registry.get(user_id)
            if data is None:
                raise LookupError(f'User {user_id} does not exist in local context')
            
            return data
        except (TypeError, ValueError, LookupError) as e:
            logging.error(f'Edge case detected in session state: {e}')
            return {'error': str(e), 'status': 'failed'}
        except Exception as e:
            logging.critical(f'Unexpected runtime deviation: {e}')
            return {'error': 'catastrophic_failure', 'status': 'abort'}

    def register_user(self, user_id, data):
        if user_id in self.registry:
            logging.warning('Overwriting existing session mapping')
        self.registry[user_id] = data

if __name__ == '__main__':
    manager = RobloxSessionManager('secret_key_123')
    print(manager.fetch_user_data('invalid_id'))