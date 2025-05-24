from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# CPU 테이블
class CPU(db.Model):
    __tablename__ = 'cpu'
    cpu_key = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(32))
    cpu_model_name = db.Column(db.String(64))
    core_num = db.Column(db.Integer)
    single_thread_benchmark = db.Column(db.Integer)
    multi_thread_benchmark = db.Column(db.Integer)
    internal_gpu = db.Column(db.Integer, db.ForeignKey('gpu.gpu_key'), nullable=True)

# GPU 테이블
class GPU(db.Model):
    __tablename__ = 'gpu'
    gpu_key = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(32))
    internal_graphic = db.Column(db.Boolean)
    gpu_model_name = db.Column(db.String(64))
    graphics_benchmark = db.Column(db.Integer)

# Memory 테이블
class Memory(db.Model):
    __tablename__ = 'memory'
    memory_key = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(32))
    capacity = db.Column(db.Integer)  # GB
    bandwidth = db.Column(db.Integer)  # MHz 또는 GB/s

# Memory_Option (M:N 관계 - 중간 테이블)
class MemoryOption(db.Model):
    __tablename__ = 'memory_option'
    notebook_key = db.Column(db.Integer, db.ForeignKey('notebook.notebook_key'), primary_key=True)
    memory_key = db.Column(db.Integer, db.ForeignKey('memory.memory_key'), primary_key=True)
    # M:N 관계 설정

# Storage 테이블
class Storage(db.Model):
    __tablename__ = 'storage'
    storage_key = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16))  # 예: SSD, HDD
    capacity = db.Column(db.Integer)  # GB

# Storage_Option (M:N 관계 - 중간 테이블)
class StorageOption(db.Model):
    __tablename__ = 'storage_option'
    notebook_key = db.Column(db.Integer, db.ForeignKey('notebook.notebook_key'), primary_key=True)
    storage_key = db.Column(db.Integer, db.ForeignKey('storage.storage_key'), primary_key=True)

# Display 테이블
class Display(db.Model):
    __tablename__ = 'display'
    display_key = db.Column(db.Integer, primary_key=True)
    refresh_rate = db.Column(db.Integer)  # Hz
    size_inch = db.Column(db.Float)  # 인치
    resolution = db.Column(db.String(32))  # 해상도
    brightness = db.Column(db.Integer)  # 밝기

# ConvenienceFeature 테이블
class ConvenienceFeature(db.Model):
    __tablename__ = 'convenience_feature'
    convenience_key = db.Column(db.Integer, primary_key=True)
    hdmi = db.Column(db.Boolean)
    sd_port = db.Column(db.Boolean)
    lan_port = db.Column(db.Boolean)
    pd_charge = db.Column(db.Boolean)
    thunderbolt = db.Column(db.Boolean)

# Notebook 테이블
class Notebook(db.Model):
    __tablename__ = 'notebook'
    notebook_key = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(128))
    cpu = db.Column(db.Integer, db.ForeignKey('cpu.cpu_key'))
    gpu = db.Column(db.Integer, db.ForeignKey('gpu.gpu_key'))
    battery = db.Column(db.Integer)  # Wh
    display = db.Column(db.Integer, db.ForeignKey('display.display_key'))
    weight = db.Column(db.Float)  # kg
    power_consumption = db.Column(db.Integer)  # W
    convenience_key = db.Column(db.Integer, db.ForeignKey('convenience_feature.convenience_key'))

    # 관계 설정 - store_links 및 Memory, Storage Option은 중간 테이블을 통해 M:N 관계로 연결
    cpu_obj = db.relationship("CPU", backref="notebooks")
    gpu_obj = db.relationship("GPU", backref="notebooks")
    display_obj = db.relationship("Display", backref="notebooks")
    convenience_obj = db.relationship("ConvenienceFeature", backref="notebooks")

    store_links = db.relationship('StoreLink', backref='notebook', lazy='joined')
    memories = db.relationship("Memory", secondary="memory_option", backref="notebooks")
    storages = db.relationship("Storage", secondary="storage_option", backref="notebooks")

    @property
    def lowest_price(self):
        prices = [link.price for link in self.store_links if link.price is not None]
        return min(prices) if prices else None
# Store 테이블
class Store(db.Model):
    __tablename__ = 'store'
    store_key = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(64))

# Store_Link 테이블 (Notebook과 Store 간 관계)
class StoreLink(db.Model):
    __tablename__ = 'store_link'
    notebook_key = db.Column(db.Integer, db.ForeignKey('notebook.notebook_key'), primary_key=True)
    store_key = db.Column(db.Integer, db.ForeignKey('store.store_key'), primary_key=True)
    link = db.Column(db.String(256))  # Store URL
    soldout = db.Column(db.Boolean)  # True or False for soldout status
    price = db.Column(db.Integer)  # Price of the notebook
    store = db.relationship("Store", backref="store_links", foreign_keys=[store_key])


# PriceHistory 테이블 (노트북 가격 이력)
class PriceHistory(db.Model):
    __tablename__ = 'price_history'
    notebook_key = db.Column(db.Integer, db.ForeignKey('notebook.notebook_key'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)  # Date of the price
    price = db.Column(db.Integer)  # Historical price

# Consumer 테이블
class Consumer(db.Model):
    __tablename__ = 'consumer'
    consumer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

# Review 테이블
class Review(db.Model):
    __tablename__ = 'review'
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.consumer_id'), primary_key=True)
    notebook_key = db.Column(db.Integer, db.ForeignKey('notebook.notebook_key'), primary_key=True)
    comment = db.Column(db.String(512))
    rating = db.Column(db.Integer)
    consumer = db.relationship("Consumer", backref="reviews")
