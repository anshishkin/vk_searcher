from sqlalchemy import Column, String
import dataclasses


@dataclasses.dataclass
class BaseEvent:
    full_name: Column = Column(String, nullable=True)
    last_name: Column = Column(String, nullable=True)
    first_name: Column = Column(String, nullable=True)
    patronymic: Column = Column(String, nullable=True)
    date_of_birth: Column = Column(String, nullable=True)
    phone_number: Column = Column(String, nullable=True)
    email_address: Column = Column(String, nullable=True)
    passport_series: Column = Column(String, nullable=True)
    passport_number: Column = Column(String, nullable=True)
    foreign_passport: Column = Column(String, nullable=True)
    snils: Column = Column(String, nullable=True)
    inn: Column = Column(String, nullable=True)
    gender: Column = Column(String, nullable=True)
    month: Column = Column(String, nullable=True)
    day: Column = Column(String, nullable=True)
    year: Column = Column(String, nullable=True)
    full_address: Column = Column(String, nullable=True)
    street_address: Column = Column(String, nullable=True)
    # city: Column = Column(String, nullable=True)
    region: Column = Column(String, nullable=True)
    country: Column = Column(String, nullable=True)
    username: Column = Column(String, nullable=True)
    password_cleartext: Column = Column(String, nullable=True)
    password_hash: Column = Column(String, nullable=True)
    unknown_hash: Column = Column(String, nullable=True)
    hash_salt: Column = Column(String, nullable=True)
    ipv4_address: Column = Column(String, nullable=True)
    ipv6_address: Column = Column(String, nullable=True)
    telegram_id: Column = Column(String, nullable=True)
    instagram_name: Column = Column(String, nullable=True)
    registration_date: Column = Column(String, nullable=True)
    access_date: Column = Column(String, nullable=True)
    last_login_date: Column = Column(String, nullable=True)
    related_person: Column = Column(String, nullable=True)
    driver_license_number: Column = Column(String, nullable=True)
    oms_policy_number: Column = Column(String, nullable=True)
    military_id: Column = Column(String, nullable=True)
    pension_certificate: Column = Column(String, nullable=True)
    birth_certificate_number: Column = Column(String, nullable=True)
    residence_permit: Column = Column(String, nullable=True)
    temporary_residence_permit: Column = Column(String, nullable=True)
    migration_card: Column = Column(String, nullable=True)
    labor_book: Column = Column(String, nullable=True)
    tax_certificate: Column = Column(String, nullable=True)
    student_id: Column = Column(String, nullable=True)
    work_permit: Column = Column(String, nullable=True)
    marital_status: Column = Column(String, nullable=True)
    place_of_birth: Column = Column(String, nullable=True)
    nationality: Column = Column(String, nullable=True)
    ethnicity: Column = Column(String, nullable=True)
    social_security_number: Column = Column(String, nullable=True)
    bank_account_number: Column = Column(String, nullable=True)
    credit_card_number: Column = Column(String, nullable=True)
    credit_card_cvv: Column = Column(String, nullable=True)
    credit_card_date: Column = Column(String, nullable=True)
    passport_expiry_date: Column = Column(String, nullable=True)
    employment_status: Column = Column(String, nullable=True)
    employer: Column = Column(String, nullable=True)
    job_title: Column = Column(String, nullable=True)
    income: Column = Column(String, nullable=True)
    education_level: Column = Column(String, nullable=True)
    degree: Column = Column(String, nullable=True)
    social_media_profile: Column = Column(String, nullable=True)
    website: Column = Column(String, nullable=True)
    vkontakte_id: Column = Column(String, nullable=True)
    vkontakte_url: Column = Column(String, nullable=True)
    github_id: Column = Column(String, nullable=True)
    linkedin_id: Column = Column(String, nullable=True)
    skype_id: Column = Column(String, nullable=True)
    fax_number: Column = Column(String, nullable=True)
    emergency_contact_name: Column = Column(String, nullable=True)
    emergency_contact_phone: Column = Column(String, nullable=True)
    emergency_contact_relationship: Column = Column(String, nullable=True)
    insurance_policy_number: Column = Column(String, nullable=True)
    insurance_provider: Column = Column(String, nullable=True)
    vehicle_registration_number: Column = Column(String, nullable=True)
    license_plate_number: Column = Column(String, nullable=True)
    loyalty_card_number: Column = Column(String, nullable=True)
    blood_type: Column = Column(String, nullable=True)
    legal_cases: Column = Column(String, nullable=True)
    shopping_history: Column = Column(String, nullable=True)
    pet_name: Column = Column(String, nullable=True)
