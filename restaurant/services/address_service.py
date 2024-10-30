from restaurant.database.address_database import AddressDatabase
import logging

logger = logging.getLogger(__name__)

class AddressService:
    @staticmethod
    def add_address(data):
        # Validate required fields for the address
        # required_fields = ['address_line_1', 'city', 'state', 'postal_code', 'country']
        # for field in required_fields:
        #     if not data.get(field):
        #         return {'error': f'{field.replace("_", " ").title()} is required'}, 400

        # Prepare the address data for insertion
        address_data = {
            'address_line_1': data.get('address_line_1'),
            'address_line_2': data.get('address_line_2'),
            'city': data.get('city'),
            'state': data.get('state'),
            'postal_code': data.get('postal_code'),
            'country': data.get('country')
        }

        # Attempt to add the address to the database
        try:
            address = AddressDatabase.add_address(address_data)
            return {'message': 'Address added successfully', 'address_id': address.id}, 201
        except Exception as e:
            logger.error(f"Error adding address: {e}")
            return {'error': 'Failed to add address. Please try again.'}, 500
