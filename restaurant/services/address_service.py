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

    @staticmethod
    def update_address(address_id, data):
        # validate requied fields for the address
        required_feilds = ['address_line_1','city','state','postal_code','country']
        for field in required_feilds:
            if not data.get(field):
                return {'error': f'{field.replace("_", " ").title()} is required'},400
        
        # Attempt to update the address in the database
        try:
            address = AddressDatabase.get_address_by_id(address_id)
            if not address:
                return {'error': "Address not found"}, 404
            
            #update address fields

            address.address_line_1 = data.get('address_line_1', address.address_line_1)
            address.address_line_2 = data.get('address_line_2', address.address_line_2)
            address.city = data.get('city', address.city)
            address.state = data.get('state', address.state)
            address.postal_code = data.get('postal_code', address.postal_code)
            address.country = data.get('country', address.country)

            #save changes to the database
            AddressDatabase.update_address(address)
            return {'message': 'Address updated successfully'},200
        
        except Exception as e:
            logger.error(f"Error update address: {e}")
            return {'error': 'Failed to update address. Please try again.'}, 500