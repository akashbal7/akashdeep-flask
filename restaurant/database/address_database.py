from restaurant.model.models import db, Address


class AddressDatabase:
    @staticmethod
    def add_address(address_data):
        new_address = Address(
            address_line_1=address_data['address_line_1'],
            address_line_2=address_data['address_line_2'],
            city=address_data['city'],
            state=address_data['state'],
            postal_code=address_data['postal_code'],
            country=address_data['country']
        )
        db.session.add(new_address)
        db.session.flush()
        return new_address.id
