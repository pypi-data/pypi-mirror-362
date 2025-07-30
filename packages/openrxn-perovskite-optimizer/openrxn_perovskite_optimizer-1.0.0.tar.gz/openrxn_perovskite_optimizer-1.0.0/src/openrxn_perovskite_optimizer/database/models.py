from datetime import datetime
from typing import Dict, Any, Optional, List
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, JSON, DateTime, 
    Boolean, Text, ForeignKey, Table
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

Base = declarative_base()

# Association table for many-to-many relationship between experiments and materials
experiment_material_association = Table(
    'experiment_materials',
    Base.metadata,
    Column('experiment_id', Integer, ForeignKey('experiments.id')),
    Column('material_id', Integer, ForeignKey('materials.id'))
)

class Material(Base):
    __tablename__ = 'materials'
    
    id = Column(Integer, primary_key=True)
    composition = Column(String, unique=True, nullable=False)
    structure = Column(JSON)
    properties = Column(JSON)
    formation_energy = Column(Float)
    stability_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    experiments = relationship("Experiment", secondary=experiment_material_association, back_populates="materials")
    property_measurements = relationship("PropertyMeasurement", back_populates="material")
    synthesis_protocols = relationship("SynthesisProtocol", back_populates="material")

class Experiment(Base):
    __tablename__ = 'experiments'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    experiment_type = Column(String, nullable=False)  # synthesis, characterization, device_testing
    status = Column(String, default='pending')  # pending, running, completed, failed
    synthesis_protocol = Column(JSON)
    characterization_results = Column(JSON)
    conditions = Column(JSON)
    batch_id = Column(String)
    agent_id = Column(String)  # Which AI agent initiated this experiment
    priority = Column(Integer, default=5)  # 1 (highest) to 10 (lowest)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    materials = relationship("Material", secondary=experiment_material_association, back_populates="experiments")
    optimization_results = relationship("OptimizationResult", back_populates="experiment")
    property_measurements = relationship("PropertyMeasurement", back_populates="experiment")

class OptimizationResult(Base):
    __tablename__ = 'optimization_results'
    
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    optimization_type = Column(String, nullable=False)  # genetic, bayesian, grid_search
    target_properties = Column(JSON)
    optimized_parameters = Column(JSON)
    best_composition = Column(String)
    best_score = Column(Float)
    convergence_history = Column(JSON)
    iteration_count = Column(Integer)
    optimization_time = Column(Float)  # seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    experiment = relationship("Experiment", back_populates="optimization_results")

class PropertyMeasurement(Base):
    __tablename__ = 'property_measurements'
    
    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'))
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    property_type = Column(String, nullable=False)  # electronic, optical, structural, stability
    measurement_method = Column(String, nullable=False)  # xrd, uv_vis, plqy, sem, etc.
    measured_value = Column(Float)
    measurement_unit = Column(String)
    uncertainty = Column(Float)
    measurement_conditions = Column(JSON)
    raw_data = Column(JSON)
    processed_data = Column(JSON)
    quality_score = Column(Float)  # 0-1 quality assessment
    measured_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    material = relationship("Material", back_populates="property_measurements")
    experiment = relationship("Experiment", back_populates="property_measurements")

class SynthesisProtocol(Base):
    __tablename__ = 'synthesis_protocols'
    
    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'))
    protocol_name = Column(String, nullable=False)
    synthesis_method = Column(String, nullable=False)  # solution_processing, vapor_deposition, etc.
    precursors = Column(JSON)
    steps = Column(JSON)
    conditions = Column(JSON)
    estimated_duration = Column(Float)  # hours
    estimated_cost = Column(Float)  # dollars
    success_rate = Column(Float)  # 0-1
    yield_percentage = Column(Float)
    purity = Column(Float)
    safety_measures = Column(JSON)
    equipment_required = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)
    
    # Relationships
    material = relationship("Material", back_populates="synthesis_protocols")

class DigitalTwinState(Base):
    __tablename__ = 'digital_twin_states'
    
    id = Column(Integer, primary_key=True)
    composition = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    structure_data = Column(JSON)
    electronic_properties = Column(JSON)
    optical_properties = Column(JSON)
    device_properties = Column(JSON)
    stability_metrics = Column(JSON)
    experimental_conditions = Column(JSON)
    uncertainty_bounds = Column(JSON)
    validation_score = Column(Float)
    
class AgentActivity(Base):
    __tablename__ = 'agent_activities'
    
    id = Column(Integer, primary_key=True)
    agent_name = Column(String, nullable=False)
    activity_type = Column(String, nullable=False)  # discovery, synthesis, characterization, optimization
    input_data = Column(JSON)
    output_data = Column(JSON)
    execution_time = Column(Float)  # seconds
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    handoff_to = Column(String)  # Next agent in workflow
    created_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'
    
    id = Column(Integer, primary_key=True)
    topic = Column(String, nullable=False)
    content = Column(JSON)
    source = Column(String)  # literature, experiment, simulation
    confidence = Column(Float)
    relevance_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Data model classes for use in the application
class OptimizationResultData:
    """Results from optimization process"""
    def __init__(self, best_composition: str, best_score: float, 
                 optimized_parameters: Dict[str, Any], convergence_history: List[float]):
        self.best_composition = best_composition
        self.best_score = best_score
        self.optimized_parameters = optimized_parameters
        self.convergence_history = convergence_history

class PropertyMeasurementData:
    """Property measurement data"""
    def __init__(self, property_type: str, measured_value: float, 
                 measurement_unit: str, uncertainty: Optional[float] = None,
                 measurement_conditions: Optional[Dict[str, Any]] = None):
        self.property_type = property_type
        self.measured_value = measured_value
        self.measurement_unit = measurement_unit
        self.uncertainty = uncertainty
        self.measurement_conditions = measurement_conditions or {}

class SynthesisProtocolData:
    """Synthesis protocol data"""
    def __init__(self, protocol_name: str, synthesis_method: str,
                 precursors: Dict[str, float], steps: List[Dict[str, Any]],
                 conditions: Dict[str, Any]):
        self.protocol_name = protocol_name
        self.synthesis_method = synthesis_method
        self.precursors = precursors
        self.steps = steps
        self.conditions = conditions

def setup_database(db_url: str):
    """Set up database with synchronous engine"""
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

async def setup_async_database(db_url: str):
    """Set up database with asynchronous engine"""
    engine = create_async_engine(db_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_sessionmaker(engine, class_=AsyncSession)