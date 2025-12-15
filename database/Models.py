

from sqlalchemy import (
    Column, String, Text, Numeric, Integer, ForeignKey, DateTime,
    Index, UniqueConstraint, func
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import JSONB
Base = declarative_base()


class MarinFleet(Base):
    """
    Основная сущность судна: Идентификация, Размерения, История, Жилые помещения.
    """
    __tablename__ = 'MarinFleet'

    id = Column(Integer, primary_key=True, autoincrement=True)

    # ================= Идентификация =================
    reg_number = Column(Text)
    build_number = Column(Text)
    imo_number = Column(Text)
    mmsi = Column(Text)
    vessel_name = Column(Text)
    vessel_project = Column(Text)
    vessel_purpose = Column(Text)
    class_symbol = Column(Text)
    class_formula = Column(Text)
    source = Column(Text)
    data_source = Column(Text)

    # ================= Постройка и История =================
    build_date = Column(Text)
    build_location = Column(Text)
    factory_location = Column(Text)
    build_city = Column(Text)
    build_country = Column(Text)
    refit_factory = Column(Text)
    refit_city = Column(Text)

    former_name = Column(Text)
    laid_down_date = Column(Text)
    keel_laying_date = Column(Text)
    major_part = Column(Text)
    major_part_date = Column(Text)
    launch_date = Column(Text)
    completion_date = Column(Text)
    first_inspection_date = Column(Text)

    # ================= Регистрация =================
    port_of_registry = Column(Text)
    registration = Column(Text)
    registration_authority = Column(Text)

    # ================= Размерения (Hull) =================
    max_length = Column(Text)
    calc_length = Column(Text)
    overall_length = Column(Text)
    design_length = Column(Text)
    overall_width = Column(Text)
    design_width = Column(Text)
    side_height = Column(Text)
    freeboard_height = Column(Text)

    # ================= Вместимости (Tonnage) =================
    gross_tonnage = Column(Text)
    net_tonnage = Column(Text)
    deadweight = Column(Text)
    displacement = Column(Text)
    lifting_capacity = Column(Text)

    # ================= Жилые и пассажирские (Accommodation) =================
    # Оставляем здесь, так как это касается людей, а не груза
    crew_size = Column(Text)
    special_personnel = Column(Text)
    bed_passenger_count = Column(Text)
    non_bed_passenger_count = Column(Text)
    passenger_capacity = Column(Text)

    # ================= Надстройка, корпус =================
    hull_material = Column(Text)
    superstructure_material = Column(Text)

    # Новые поля (Конструктив)
    deck_count = Column(Text)
    bulkheads_total_count = Column(Text)
    longitudinal_bulkheads_count = Column(Text)
    transverse_bulkheads_count = Column(Text)

    # ================= Прочее (Status & Owners) =================
    flag = Column(Text)
    callsign = Column(Text)
    major_conversion = Column(Text)
    main_type = Column(Text)
    current_status = Column(Text)
    owner = Column(Text)
    operator = Column(Text)
    org_group = Column(Text)
    notes = Column(Text)
    supply_characteristics = Column(Text)

    # Оборудование навигации (не двигатель и не груз)
    radio_navigation_equipment = Column(Text)
    anchor_chain_category = Column(Text)
    anchor_chain_caliber = Column(Text)

    # === СВЯЗИ ===
    # uselist=False обеспечивает связь 1-к-1
    engineering = relationship("MarinEngineering", back_populates="fleet", uselist=False, cascade="all, delete-orphan")
    cargo_spec = relationship("MarinCargoSpec", back_populates="fleet", uselist=False, cascade="all, delete-orphan")


class MarinEngineering(Base):
    """
    Техническая часть: Двигатели, Пропульсия, Энергетика, Топливо.
    """
    __tablename__ = 'MarinEngineering'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fleet_id = Column(Integer, ForeignKey('MarinFleet.id'), nullable=False, unique=True)

    # ================= Движение =================
    speed = Column(Text)
    propulsion_type = Column(Text)
    propulsion_model = Column(Text)
    propeller_count = Column(Text)
    propulsion_count = Column(Text)
    propulsor_type = Column(Text)

    # ================= Главные двигатели =================
    main_engines = Column(Text)
    main_engine_model = Column(Text)

    # ================= Электростанция (Генераторы) =================
    total_generator_power = Column(Text)
    total_electric_generators = Column(Text)

    # ================= Электродвижение (для дизель-электроходов) =================
    ged_count = Column(Text)
    total_ged_power = Column(Text)

    # ================= Котлы и системы =================
    main_boilers = Column(Text)
    heaters = Column(Text)
    refrigerants = Column(Text)  # Хладагенты систем
    working_temperature = Column(Text)

    # ================= Топливо =================
    fuel_reserves = Column(Text)
    fuel_types = Column(Text)


    fleet = relationship("MarinFleet", back_populates="engineering")


class MarinCargoSpec(Base):
    """
    Грузовая часть: Трюмы, Танки, Краны, Люки.
    """
    __tablename__ = 'MarinCargoSpec'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fleet_id = Column(Integer, ForeignKey('MarinFleet.id'), nullable=False, unique=True)

    # ================= Трюмы и Контейнеры =================
    cargo_hold_count = Column(Text)
    cargo_hold_volume = Column(Text)
    cargo_hatches = Column(Text)

    container_count = Column(Text)
    container_type = Column(Text)

    # ================= Наливные грузы (Танки) =================
    tanks = Column(Text)
    tanks_count = Column(Text)
    tank_volume = Column(Text)
    total_tank_volume = Column(Text)

    # ================= Рефрижераторы =================
    refrigerated_cargo_space = Column(Text)
    refrigerated_cargo_space_count = Column(Text)
    refrigerated_cargo_space_capacity = Column(Text)

    # ================= Грузовое устройство (Краны) =================
    booms = Column(Text)
    cranes = Column(Text)

    fleet = relationship("MarinFleet", back_populates="cargo_spec")

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)

    # Связь с ролями через UserRole
    roles = relationship("Role", secondary="UserRole", back_populates="users")


class Role(Base):
    __tablename__ = 'Role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)

    # Связь с пользователями
    users = relationship("User", secondary="UserRole", back_populates="roles")


class UserRole(Base):
    __tablename__ = 'UserRole'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'))
    role_id = Column(Integer, ForeignKey('Role.id', ondelete='CASCADE'))


class UserLog(Base):
    __tablename__ = 'UserLog'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    login_time = Column(DateTime, nullable=False)
    logout_time = Column(DateTime, nullable=True)


##Закупки

class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id', ondelete='CASCADE'), nullable=False)

    organization = Column(Text, nullable=True)
    country = Column(Text, nullable=True)  # Исправлено: Country -> country (PEP8)
    address = Column(Text, nullable=True)  # Исправлено: adress -> address
    index_address = Column(Text, nullable=True)  # Исправлено: index_adress -> index_address
    phone = Column(Text, nullable=True)
    mail = Column(Text, nullable=True)
    status = Column(Text, nullable=True)
    inn = Column(Text, nullable=True)
    kpp = Column(Text, nullable=True)

    # Связи
    contract = relationship("Contract", back_populates="suppliers")


# ======================= PURCHASES =======================

class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reg_number = Column(String, nullable=False, unique=True)  # Добавлен unique=True из индекса

    status = Column(Text, nullable=True)
    law = Column(Text, nullable=True)
    placing_way = Column(Text, nullable=True)
    object_name = Column(Text, nullable=True)

    customer_name = Column(Text, nullable=True)
    customer_url = Column(Text, nullable=True)

    initial_price_amount = Column(Numeric(18, 2), nullable=True)
    initial_price_currency = Column(Text, nullable=True)

    published = Column(Text, nullable=True)
    updated = Column(Text, nullable=True)
    submission_end = Column(Text, nullable=True)

    url_common_info = Column(Text, nullable=True)
    contract_url = Column(Text, nullable=True)
    complaints_url = Column(Text, nullable=True)

    # JSONB Payloads
    common_info_json = Column(JSONB, nullable=True)
    documents_json = Column(JSONB, nullable=True)
    event_log_json = Column(JSONB, nullable=True)
    supplier_result_json = Column(JSONB, nullable=True)
    lots_json = Column(JSONB, nullable=True)
    protocols_json = Column(JSONB, nullable=True)
    contracts_info_json = Column(JSONB, nullable=True)
    changes_json = Column(JSONB, nullable=True)

    # Foreign Keys
    contract_id = Column(Integer, ForeignKey('contracts.id', ondelete='SET NULL'), nullable=True)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='SET NULL'), nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Связи
    ktru_positions = relationship("PurchaseKtruPosition", back_populates="purchase", cascade="all, delete-orphan")
    tabs = relationship("PurchaseTab", back_populates="purchase", cascade="all, delete-orphan")
    contract_obj = relationship("Contract",
                                foreign_keys=[contract_id])  # Имя изменено, чтобы не конфликтовать с contract_url
    customer = relationship("Customer", back_populates="purchases")

    # Индексы (объявляются внутри __table_args__)
    __table_args__ = (
        Index("ix_purchases__common_info_gin", "common_info_json", postgresql_using="gin"),
        Index("ix_purchases_documents_gin", "documents_json", postgresql_using="gin"),
        Index("ix_purchases_event_log_gin", "event_log_json", postgresql_using="gin"),
        Index("ix_purchases_supplier_result_gin", "supplier_result_json", postgresql_using="gin"),
    )


class PurchaseTab(Base):
    __tablename__ = 'purchase_tabs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reg_number = Column(String, ForeignKey('purchases.reg_number'), nullable=False)  # Сделали FK для целостности

    label = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    active = Column(Integer, nullable=False, server_default="0")

    purchase = relationship("Purchase", back_populates="tabs",
                            primaryjoin="Purchase.reg_number == PurchaseTab.reg_number")

    __table_args__ = (
        Index("ix_purchase_tabs_reg", "reg_number"),
    )


class PurchaseKtruPosition(Base):
    __tablename__ = 'purchase_ktru_positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reg_number = Column(String, ForeignKey('purchases.reg_number', ondelete='CASCADE'), nullable=False)

    code = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    unit = Column(Text, nullable=False)
    quantity = Column(Numeric(18, 3), nullable=False)

    unit_price_amount = Column(Numeric(18, 2), nullable=True)
    unit_price_currency = Column(Text, nullable=True)
    amount_amount = Column(Numeric(18, 2), nullable=True)
    amount_currency = Column(Text, nullable=True)

    purchase = relationship("Purchase", back_populates="ktru_positions",
                            primaryjoin="Purchase.reg_number == PurchaseKtruPosition.reg_number")


# ======================= CONTRACTS =======================

class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reg_number = Column(String, nullable=False, unique=True)
    contract_url = Column(Text, nullable=False)

    law = Column(Text, nullable=True)
    number = Column(Text, nullable=True)
    status = Column(Text, nullable=True)
    object_name = Column(Text, nullable=True)

    customer_name = Column(Text, nullable=True)
    customer_url = Column(Text, nullable=True)

    contract_price = Column(Text, nullable=True)
    date_contract_signed = Column(Text, nullable=True)
    date_execution_due = Column(Text, nullable=True)
    date_registered = Column(Text, nullable=True)
    date_updated_in_registry = Column(Text, nullable=True)
    version = Column(Text, nullable=True)

    # JSONB payloads
    common_info_json = Column(JSONB, nullable=True)
    payment_targets_json = Column(JSONB, nullable=True)
    process_info_json = Column(JSONB, nullable=True)
    documents_json = Column(JSONB, nullable=True)
    journal_versions_json = Column(JSONB, nullable=True)
    event_log_json = Column(JSONB, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Связи
    suppliers = relationship("Supplier", back_populates="contract", cascade="all, delete-orphan")
    tabs = relationship("ContractTab", back_populates="contract", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('reg_number', 'version', name='ux_contracts_reg_number_version'),
    )


class ContractTab(Base):
    __tablename__ = 'contract_tabs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reg_number = Column(String, ForeignKey('contracts.reg_number'), nullable=False)

    label = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    active = Column(Integer, nullable=False, server_default="0")

    contract = relationship("Contract", back_populates="tabs",
                            primaryjoin="Contract.reg_number == ContractTab.reg_number")

    __table_args__ = (
        Index("ix_contract_tabs_reg", "reg_number"),
    )


# ======================= CUSTOMERS =======================

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    law = Column(Text, nullable=True)
    ogrn = Column(String, nullable=True)
    inn = Column(String, nullable=True)
    kpp = Column(String, nullable=True)

    country = Column(Text, nullable=True)
    region = Column(Text, nullable=True)
    city = Column(Text, nullable=True)
    address_full = Column(Text, nullable=True)

    organization_url = Column(Text, nullable=True)
    organization_id = Column(Integer, nullable=True)
    customer_code = Column(String, nullable=True)

    purchases_url = Column(Text, nullable=True)
    contracts_url = Column(Text, nullable=True)
    account_card_url = Column(Text, nullable=True)
    additional_info_url = Column(Text, nullable=True)

    # JSONB payloads
    documents_card_json = Column(JSONB, nullable=True)
    additional_info_json = Column(JSONB, nullable=True)
    journal_versions_json = Column(JSONB, nullable=True)

    # Связи
    purchases = relationship("Purchase", back_populates="customer")
    tabs = relationship("CustomerTab", back_populates="customer", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('inn', name='uq_customers_inn'),
    )


class CustomerTab(Base):
    __tablename__ = 'customer_tabs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reg_number = Column(String, nullable=False)

    label = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    active = Column(Integer, nullable=False, server_default="0")


