from .models import Contact
from datetime import datetime

class IdentityReconciliationService:
    @staticmethod
    def identify_contact(data):
        email = data.get('email')
        phone_number = data.get('phoneNumber')
        contact_id = data.get('id')

        # Find all contacts matching the provided information
        contacts = IdentityReconciliationService.find_matching_contacts(email, phone_number, contact_id)
        
        if not contacts:
            # Create new primary contact if no matches found
            primary_contact = Contact.objects.create(
                email=email,
                phone_number=phone_number,
                link_precedence=Contact.LinkPrecedence.PRIMARY
            )
            contacts = [primary_contact]
        
        # Determine the primary contact (oldest one)
        primary_contact = IdentityReconciliationService.determine_primary_contact(contacts)
        
        # Update other contacts to be secondary to the primary
        IdentityReconciliationService.update_secondary_contacts(contacts, primary_contact)
        
        # Create new secondary contact if new information provided
        if (email and email != primary_contact.email) or (phone_number and phone_number != primary_contact.phone_number):
            Contact.objects.create(
                email=email if email != primary_contact.email else None,
                phone_number=phone_number if phone_number != primary_contact.phone_number else None,
                linked_id=primary_contact,
                link_precedence=Contact.LinkPrecedence.SECONDARY
            )
        
        # Prepare the response
        return IdentityReconciliationService.prepare_response(primary_contact)

    @staticmethod
    def find_matching_contacts(email, phone_number, contact_id):
        contacts = set()
        
        if contact_id:
            try:
                contact = Contact.objects.get(id=contact_id)
                contacts.add(contact)
                # Add all linked contacts
                contacts.update(Contact.objects.filter(linked_id=contact))
                if contact.linked_id:
                    contacts.update(Contact.objects.filter(linked_id=contact.linked_id))
                    contacts.add(contact.linked_id)
            except Contact.DoesNotExist:
                pass
        
        if email:
            contacts.update(Contact.objects.filter(email=email))
        
        if phone_number:
            contacts.update(Contact.objects.filter(phone_number=phone_number))
        
        return list(contacts)

    @staticmethod
    def determine_primary_contact(contacts):
        primary_contacts = [c for c in contacts if c.link_precedence == Contact.LinkPrecedence.PRIMARY]
        if not primary_contacts:
            # If no primary contacts, find the oldest one
            oldest_contact = min(contacts, key=lambda x: x.created_at)
            oldest_contact.link_precedence = Contact.LinkPrecedence.PRIMARY
            oldest_contact.save()
            return oldest_contact
        
        # If multiple primary contacts, set the oldest as primary and others as secondary
        if len(primary_contacts) > 1:
            primary_contacts.sort(key=lambda x: x.created_at)
            new_primary = primary_contacts[0]
            for contact in primary_contacts[1:]:
                contact.link_precedence = Contact.LinkPrecedence.SECONDARY
                contact.linked_id = new_primary
                contact.save()
            return new_primary
        
        return primary_contacts[0]

    @staticmethod
    def update_secondary_contacts(contacts, primary_contact):
        for contact in contacts:
            if contact != primary_contact and (
                contact.link_precedence != Contact.LinkPrecedence.SECONDARY or 
                contact.linked_id != primary_contact
            ):
                contact.link_precedence = Contact.LinkPrecedence.SECONDARY
                contact.linked_id = primary_contact
                contact.save()

    @staticmethod
    def prepare_response(primary_contact):
        secondary_contacts = Contact.objects.filter(linked_id=primary_contact)
        
        emails = {primary_contact.email} if primary_contact.email else set()
        phone_numbers = {primary_contact.phone_number} if primary_contact.phone_number else set()
        secondary_ids = []
        
        for contact in secondary_contacts:
            if contact.email:
                emails.add(contact.email)
            if contact.phone_number:
                phone_numbers.add(contact.phone_number)
            secondary_ids.append(contact.id)
        
        return {
            "primaryContatctId": primary_contact.id,
            "emails": list(emails),
            "phoneNumbers": list(phone_numbers),
            "secondaryContactIds": secondary_ids
        }