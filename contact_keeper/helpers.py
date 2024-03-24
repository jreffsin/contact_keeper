from contact_keeper.models import Address

# Helper functions
def get_primary_address(contact_id):
    primary_address = {}
    primary_address['record'] = Address.query.filter_by(contact_id=contact_id, is_primary=True).first()
    primary_address['exists'] = primary_address['record'] is not None
    return primary_address