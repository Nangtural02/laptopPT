import pandas as pd
from laptopDB import db, CPU, GPU, Memory, Storage, Notebook, Store, StoreLink, PriceHistory, Consumer, Review, \
    MemoryOption, StorageOption, Display, ConvenienceFeature


def initialize_db():
    db.create_all()

    # CSV 데이터 읽기 (추가로 Display, ConvenienceFeature 포함)
    cpu_df = pd.read_csv(
        'seed/cpu.csv',
        converters={
            'internal_gpu': lambda x: int(x) if str(x).strip() else None
        }
    )
    gpu_df = pd.read_csv('seed/gpu.csv')
    memory_df = pd.read_csv('seed/memory.csv')
    storage_df = pd.read_csv('seed/storage.csv')
    notebook_df = pd.read_csv('seed/notebook.csv')
    store_df = pd.read_csv('seed/store.csv')
    store_link_df = pd.read_csv('seed/store_link.csv')
    price_history_df = pd.read_csv('seed/price_history.csv')
    consumer_df = pd.read_csv('seed/consumer.csv')
    review_df = pd.read_csv('seed/review.csv')
    memory_option_df = pd.read_csv('seed/memory_option.csv')
    storage_option_df = pd.read_csv('seed/storage_option.csv')
    display_df = pd.read_csv('seed/display.csv')
    convenience_feature_df = pd.read_csv('seed/convenience_feature.csv')

    # 부모 테이블 데이터 삽입 (먼저 삽입)
    # GPU 데이터 삽입 (가장 먼저)
    for _, row in gpu_df.iterrows():
        gpu = GPU(**row)
        db.session.add(gpu)
    db.session.commit()  # GPU 데이터 삽입 후 commit 필수!

    # CPU 데이터 삽입 (GPU 이후)
    for _, row in cpu_df.iterrows():
        cpu = CPU(**row)
        db.session.add(cpu)
    db.session.commit()

    for _, row in memory_df.iterrows():
        db.session.add(Memory(**row))

    for _, row in storage_df.iterrows():
        db.session.add(Storage(**row))

    for _, row in display_df.iterrows():
        db.session.add(Display(**row))

    for _, row in convenience_feature_df.iterrows():
        db.session.add(ConvenienceFeature(**row))

    for _, row in store_df.iterrows():
        db.session.add(Store(**row))

    for _, row in consumer_df.iterrows():
        db.session.add(Consumer(**row))

    # Notebook 삽입
    db.session.commit()  # 중간 commit
    for _, row in notebook_df.iterrows():
        db.session.add(Notebook(**row))

    db.session.commit()  # 부모 데이터 최종 commit

    # 이제 자식 테이블 데이터 삽입
    for _, row in store_link_df.iterrows():
        db.session.add(StoreLink(**row))

    for _, row in review_df.iterrows():
        db.session.add(Review(**row))

    for _, row in price_history_df.iterrows():
        db.session.add(PriceHistory(**row))

    for _, row in memory_option_df.iterrows():
        db.session.add(MemoryOption(**row))

    for _, row in storage_option_df.iterrows():
        db.session.add(StorageOption(**row))

    # 최종 commit
    db.session.commit()


if __name__ == "__main__":
    initialize_db()
    print("Database initialized successfully!")
