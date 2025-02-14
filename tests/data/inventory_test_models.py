from pydantic import BaseModel, Field
import datetime
from typing import Any


class Products(BaseModel):
    date: datetime.date = Field(None)
    category: str = Field(None)
    name: str = Field(None)
    manufacturer: str = Field(None)
    model_year: float = Field(None)
    part_number: str = Field(None)
    bar_code: str = Field(None)
    description: str = Field(None)
    location: str = Field(None)
    taxable: str = Field(None)
    unit_cost: float = Field(None)
    unit_price: float = Field(None)
    units_on_hand: float = Field(None)
    last_order: datetime.date = Field(None)
    stock_value: float = Field(None)
    primarykey: str = Field(None, description="Unique identifier of each record in this table")
    createdby: str = Field(None, description="Account name of the user who created each record")
    modifiedby: str = Field(None, description="Account name of the user who last modified each record")
    availability: str = Field(None)
    reorder_level: float = Field(None)
    creationtimestamp: datetime.datetime = Field(None, description="Date and time each record was created")
    modificationtimestamp: datetime.datetime = Field(None, description="Date and time each record was last modified")


class InventoryTransactions(BaseModel):
    primarykey: str = Field(None, description="Unique identifier of each record in this table")
    createdby: str = Field(None, description="Account name of the user who created each record")
    modifiedby: str = Field(None, description="Account name of the user who last modified each record")
    lot_number: str = Field(None)
    description: str = Field(None)
    type: str = Field(None)
    units: float = Field(None)
    foreignkey: str = Field(None, description="Unique identifier of each record in the related table")
    date: datetime.date = Field(None)
    units_in_|_out: float = Field(None)
    creationtimestamp: datetime.datetime = Field(None, description="Date and time each record was created")
    modificationtimestamp: datetime.datetime = Field(None, description="Date and time each record was last modified")
