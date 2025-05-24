from flask import render_template, request
from sqlalchemy import func
from laptopDB import (Notebook, CPU, GPU, Display, ConvenienceFeature, Memory, MemoryOption,
                      Storage, StorageOption, StoreLink, db)

def render_results():
    args = request.args if request.method == "GET" else request.form
    query = Notebook.query\
        .join(CPU, Notebook.cpu == CPU.cpu_key)\
        .join(GPU, Notebook.gpu == GPU.gpu_key)\
        .join(Display, Notebook.display == Display.display_key)\
        .join(ConvenienceFeature, Notebook.convenience_key == ConvenienceFeature.convenience_key)\
        .outerjoin(StoreLink, Notebook.notebook_key == StoreLink.notebook_key)\
        .outerjoin(MemoryOption, Notebook.notebook_key == MemoryOption.notebook_key)\
        .outerjoin(Memory, MemoryOption.memory_key == Memory.memory_key)\
        .outerjoin(StorageOption, Notebook.notebook_key == StorageOption.notebook_key)\
        .outerjoin(Storage, StorageOption.storage_key == Storage.storage_key)

    # 가격 필터 (최소 가격 기준 - StoreLink 테이블에서 최저가 활용)
    budget_min = args.get("budget_min", type=int)
    budget_max = args.get("budget_max", type=int)

    # 서브쿼리: Notebook별 최저가 계산
    subquery_min_price = db.session.query(
        StoreLink.notebook_key,
        func.min(StoreLink.price).label('lowest_price')
    ).group_by(StoreLink.notebook_key).subquery()

    # 메인 쿼리에 최저가 JOIN
    query = query.join(subquery_min_price, Notebook.notebook_key == subquery_min_price.c.notebook_key)

    if budget_min:
        query = query.filter(subquery_min_price.c.lowest_price >= budget_min)
    if budget_max:
        query = query.filter(subquery_min_price.c.lowest_price <= budget_max)

    # CPU 성능 필터
    cpu_min = args.get("cpu_min", type=int)
    cpu_max = args.get("cpu_max", type=int)
    if cpu_min:
        query = query.filter(CPU.multi_thread_benchmark >= cpu_min)
    if cpu_max:
        query = query.filter(CPU.multi_thread_benchmark <= cpu_max)

    # GPU 성능 필터
    gpu_min = args.get("gpu_min", type=int)
    gpu_max = args.get("gpu_max", type=int)
    if gpu_min:
        query = query.filter(GPU.graphics_benchmark >= gpu_min)
    if gpu_max:
        query = query.filter(GPU.graphics_benchmark <= gpu_max)

    # 디스플레이 크기 필터
    display_min = args.get("display_min", type=float)
    display_max = args.get("display_max", type=float)
    if display_min:
        query = query.filter(Display.size_inch >= display_min)
    if display_max:
        query = query.filter(Display.size_inch <= display_max)

    # RAM 필터 처리 (MemoryOption, Memory JOIN 활용)
    ram_options = args.getlist("ram_options", type=int)
    if ram_options:
        query = query.filter(Memory.capacity.in_(ram_options))

    # 저장장치 필터 처리 (StorageOption, Storage JOIN 활용)
    storage_options = args.getlist("storage_options", type=int)
    if storage_options:
        query = query.filter(Storage.capacity.in_(storage_options))

    # 해상도 필터 (고급 해상도 그룹 → 실제 해상도 문자열로 확장)
    resolution_options = args.getlist("resolution_options")
    if resolution_options:
        resolution_map = {
            "FHD급": ["1920x1080", "1920x1200"],
            "QHD급": ["2560x1440", "2560x1600"],
            "UHD급": ["3840x2160"]
        }
        expanded_resolutions = []
        for grade in resolution_options:
            expanded_resolutions.extend(resolution_map.get(grade, []))

        if expanded_resolutions:
            query = query.filter(Display.resolution.in_(expanded_resolutions))
    # 편의기능 필터
    if args.get("port_hdmi"):
        query = query.filter(ConvenienceFeature.hdmi.is_(True))
    if args.get("port_sd"):
        query = query.filter(ConvenienceFeature.sd_port.is_(True))
    if args.get("port_lan"):
        query = query.filter(ConvenienceFeature.lan_port.is_(True))
    if args.get("pd_charge"):
        query = query.filter(ConvenienceFeature.pd_charge.is_(True))
    if args.get("thunderbolt"):
        query = query.filter(ConvenienceFeature.thunderbolt.is_(True))

    # 중복 Notebook 제거를 위해 distinct() 사용
    notebooks = query.distinct(Notebook.notebook_key).limit(100).all()

    return render_template("results.html", notebooks=notebooks, args=args)

