from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from .base import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
import datetime
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict

# MySQL

class Card(Base):
  __tablename__ = 'cards'
  id = Column(String(50), primary_key=True)
  name = Column(String(255))
  supertype = Column(String(50))
  subtypes = Column(JSON)
  level = Column(Integer)
  hp = Column(Integer)
  types = Column(JSON)
  evolves_from = Column(String(255))
  evolves_to = Column(JSON)
  rules = Column(JSON)
  ancientTrait = Column(JSON)
  abilities = Column(JSON)
  attacks = Column(JSON)
  weaknesses = Column(JSON)
  resistances = Column(JSON)
  retreat_cost = Column(JSON)
  converted_retreat_cost = Column(Integer)
  set = Column(JSON)
  number = Column(String(50))
  artist = Column(String(255))
  rarity = Column(String(50))
  flavor_text = Column(Text)
  national_pokedex_numbers = Column(JSON)
  legalities = Column(JSON)
  regulationMark = Column(String(255))
  images = Column(JSON)
  tcgplayer = Column(JSON)
  cardmarket = Column(JSON)
  updated_at = Column(DateTime,
                      default=datetime.datetime.utcnow,
                      onupdate=datetime.datetime.utcnow)


# Pydantic - Data Validation

class Ability(BaseModel):
  name: str
  text: str
  type: str

class Attack(BaseModel):
  name: str
  cost: List[str]
  convertedEnergyCost: int
  damage: str
  text: str

class Weakness(BaseModel):
  type: str
  value: str

class Legality(BaseModel):
  unlimited: str
  standard: str
  expanded: str

class Image(BaseModel):
  small: HttpUrl
  large: HttpUrl

class Price(BaseModel):
  low: Optional[float]
  mid: Optional[float]
  high: Optional[float]
  market: Optional[float]
  directLow: Optional[float]

class CardMarketPrice(BaseModel):
  averageSellPrice: Optional[float]
  lowPrice: Optional[float]
  trendPrice: Optional[float]
  germanProLow: Optional[float]
  suggestedPrice: Optional[float]
  reverseHoloSell: Optional[float]
  reverseHoloLow: Optional[float]
  reverseHoloTrend: Optional[float]
  lowPriceExPlus: Optional[float]
  avg1: Optional[float]
  avg7: Optional[float]
  avg30: Optional[float]
  reverseHoloAvg1: Optional[float]
  reverseHoloAvg7: Optional[float]
  reverseHoloAvg30: Optional[float]

class Set(BaseModel):
  id: str
  name: str
  series: str
  printedTotal: int
  total: int
  legalities: Legality
  ptcgoCode: str
  releaseDate: str
  updatedAt: str
  images: Dict[str, HttpUrl]

class TCGPlayer(BaseModel):
  url: HttpUrl
  updatedAt: str
  prices: Dict[str, Price]

class CardMarket(BaseModel):
  url: HttpUrl
  updatedAt: str
  prices: CardMarketPrice

# Define the main model

class PokemonCard(BaseModel):
  id: str
  name: str
  supertype: str
  subtypes: List[str]
  hp: str
  types: List[str]
  evolvesFrom: str
  abilities: List[Ability]
  attacks: List[Attack]
  weaknesses: List[Weakness]
  retreatCost: List[str]
  convertedRetreatCost: int
  set: Set
  number: str
  artist: str
  rarity: str
  flavorText: str
  nationalPokedexNumbers: List[int]
  legalities: Legality
  images: Dict[str, HttpUrl]
  tcgplayer: TCGPlayer
  cardmarket: CardMarket
