import typing as tp
import pydantic

# ID type for all identifier-like integers
Id = tp.NewType('Id', int)


class NotebookSearchIdQueryParams(pydantic.BaseModel):
    # API parameters
    exclude_refurbished: bool | None = None
    page: int | None = None
    page_size: int | None = None
    stores: list[Id] | None = None
    
    # Price range and search
    offer_price_usd_min: float | None = None
    offer_price_usd_max: float | None = None
    search: str | None = None

    # Product categories and weight
    brands: list[Id] | None = None
    lines: list[Id] | None = None
    weight_min: int | None = None
    weight_max: int | None = None
    
    # Processor specifications
    processor_brands: list[Id] | None = None
    processor_lines: list[Id] | None = None
    processor_thread_count_min: Id | None = None
    processors: list[Id] | None = None
    processor_speed_score_min: int | None = None
    processor_speed_score_max: int | None = None
    
    # RAM specifications
    ram_quantity_min: Id | None = None
    ram_types: list[Id] | None = None
    
    # Screen specifications
    screen_size_min: Id | None = None
    screen_size_max: Id | None = None
    screen_types: list[Id] | None = None
    screen_resolution_min: Id | None = None
    screen_refresh_rate_min: Id | None = None
    screen_touch: bool | None = None
    screen_is_rotating: bool | None = None
    
    # Video card specifications
    video_card_types: list[Id] | None = None
    video_card_brands: list[Id] | None = None
    video_card_lines: list[Id] | None = None
    video_cards: list[Id] | None = None
    score_games_min: int | None = None
    score_games_max: int | None = None
    
    # Storage specifications
    storage_capacity_min: Id | None = None
    storage_drive_types: list[Id] | None = None
    storage_drive_rpm: Id | None = None
    
    # Operating system specifications
    operating_systems: list[Id] | None = None
    specific_operating_systems: list[Id] | None = None
    keyboard_layouts: list[Id] | None = None
    has_fingerprint_reader: bool | None = None

# Brand literal type (alphabetically sorted)
type Brand = tp.Literal[
    "ASUS", "Acer", "Apple", "CHUWI", "Dell", "Gigabyte", 
    "HP", "Huawei", "Hyundai", "Lenovo", "MSI", "Microsoft", 
    "Samsung", "Toshiba", "Urao"
]

# Product Line literal type (alphabetically sorted)
type BrandLine = tp.Literal[
    "ASUS", "ASUS Chromebook", "ASUS ExpertBook", "ASUS ProArt", 
    "ASUS ProArt StudioBook", "ASUS ROG", "ASUS TUF", "ASUS VivoBook", 
    "ASUS Zenbook", "Acer Aspire", "Acer Nitro", "Acer Predator", 
    "Acer Swift", "Acer Travelmate", "Apple MacBook Air", "Apple MacBook Pro", 
    "CHUWI", "Dell", "Dell Alienware", "Dell Inspiron", "Dell Latitude", 
    "Dell Precision", "Dell Pro", "Dell Vostro", "Dell XPS", "Gigabyte", 
    "HP", "HP Chromebook", "HP Dragonfly", "HP Elite", "HP EliteBook", 
    "HP Envy", "HP Omen", "HP OmniBook Ultra", "HP Pavilion", "HP ProBook", 
    "HP Spectre", "HP Victus", "HP ZBook", "Huawei Matebook", "Hyundai HyBook", 
    "Lenovo", "Lenovo IdeaPad", "Lenovo IdeaPad Slim 3 14AHP10", 
    "Lenovo IdeaPad Slim 5 16IRL8", "Lenovo LOQ", "Lenovo LOQ 15ARP9", 
    "Lenovo Legion", "Lenovo ThinkBook", "Lenovo ThinkBook 14 G6 IRL", 
    "Lenovo ThinkPad", "Lenovo ThinkPad P14s Gen 4 (AMD)", 
    "Lenovo ThinkPad P15v Gen 3", "Lenovo V15 G2 ITL", "Lenovo Yoga", 
    "MSI", "MSI Bravo", "MSI Cyborg", "MSI Modern", "MSI Thin", "MSI Vector", 
    "Microsoft Surface", "Samsung", "Toshiba Dynabook", "Urao"
]

# Processor Brand literal type (alphabetically sorted)
type ProcessorBrand = tp.Literal[
    "AMD", "Apple", "Intel", "Mediatek", "Qualcomm"
]

# Processor Line literal type (alphabetically sorted)
type ProcessorLine = tp.Literal[
    "AMD A12", "AMD A6", "AMD A9", "AMD Athlon", "AMD Ryzen 3", 
    "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9", "AMD Ryzen AI 5", 
    "AMD Ryzen AI 7", "AMD Ryzen AI 9", "Apple", "Intel", "Intel Celeron", 
    "Intel Core 5", "Intel Core 7", "Intel Core Ultra 5", "Intel Core Ultra 7", 
    "Intel Core Ultra 9", "Intel Core i3", "Intel Core i5", "Intel Core i7", 
    "Intel Core i9", "Intel Pentium", "Intel Xeon", "Mediatek", 
    "Qualcomm Snapdragon X", "Qualcomm Snapdragon X Elite", 
    "Qualcomm Snapdragon X Plus"
]

# Processor Thread Count literal type (sorted numerically)
type ProcessorThreadCount = tp.Literal[
    "2", "4", "6", "8", "10", "11", "12", "14", "16", "18", 
    "20", "22", "24", "28", "32"
]

# Processor Model literal type (alphabetically sorted)
type Processor = tp.Literal[
    "AMD A12-8830B", "AMD A6-9220C", "AMD A9-9425", "AMD Athlon 3020e", 
    "AMD Ryzen 3 2200U", "AMD Ryzen 3 3250U", "AMD Ryzen 3 3300U", 
    "AMD Ryzen 3 3350U", "AMD Ryzen 3 4300U", "AMD Ryzen 3 5300U", 
    "AMD Ryzen 3 5400U", "AMD Ryzen 3 7320U", "AMD Ryzen 3 7330U", 
    "AMD Ryzen 3 7335U", "AMD Ryzen 3 PRO 4450U", "AMD Ryzen 5 2500U", 
    "AMD Ryzen 5 3450U", "AMD Ryzen 5 3500U", "AMD Ryzen 5 4500U", 
    "AMD Ryzen 5 4600H", "AMD Ryzen 5 5500U", "AMD Ryzen 5 5600H", 
    "AMD Ryzen 5 5600U", "AMD Ryzen 5 5625U", "AMD Ryzen 5 5730U", 
    "AMD Ryzen 5 7235HS", "AMD Ryzen 5 7430U", "AMD Ryzen 5 7520U", 
    "AMD Ryzen 5 7530U", "AMD Ryzen 5 7535HS", "AMD Ryzen 5 7535U", 
    "AMD Ryzen 5 7640HS", "AMD Ryzen 5 7640U", "AMD Ryzen 5 8645HS", 
    "AMD Ryzen 5 PRO 7530U", "AMD Ryzen 5 PRO 7540U", "AMD Ryzen 5 PRO 8540U", 
    "AMD Ryzen 5 PRO 8640HS", "AMD Ryzen 7 250", "AMD Ryzen 7 3700U", 
    "AMD Ryzen 7 3750H", "AMD Ryzen 7 4700U", "AMD Ryzen 7 4800H", 
    "AMD Ryzen 7 4800HS", "AMD Ryzen 7 5700U", "AMD Ryzen 7 5800H", 
    "AMD Ryzen 7 5800HS", "AMD Ryzen 7 5825U", "AMD Ryzen 7 6800H", 
    "AMD Ryzen 7 7435HS", "AMD Ryzen 7 7730U", "AMD Ryzen 7 7735HS", 
    "AMD Ryzen 7 7735U", "AMD Ryzen 7 7736U", "AMD Ryzen 7 7840HS", 
    "AMD Ryzen 7 7840U", "AMD Ryzen 7 8840HS", "AMD Ryzen 7 8845HS", 
    "AMD Ryzen 7 PRO 4750U", "AMD Ryzen 7 PRO 5850U", "AMD Ryzen 7 PRO 5875U", 
    "AMD Ryzen 7 PRO 6850H", "AMD Ryzen 7 PRO 7840U", "AMD Ryzen 7 PRO 8840HS", 
    "AMD Ryzen 7 PRO 8840U", "AMD Ryzen 7 Pro 3700U", "AMD Ryzen 7 Pro 6850U", 
    "AMD Ryzen 9 270", "AMD Ryzen 9 4900HS", "AMD Ryzen 9 5900HS", 
    "AMD Ryzen 9 5900HX", "AMD Ryzen 9 6900HS", "AMD Ryzen 9 6900HX", 
    "AMD Ryzen 9 7845HX", "AMD Ryzen 9 7940HS", "AMD Ryzen 9 7940HX", 
    "AMD Ryzen 9 8940HX", "AMD Ryzen 9 8945HS", "AMD Ryzen AI 5 340", 
    "AMD Ryzen AI 5 Pro 340", "AMD Ryzen AI 7 350", "AMD Ryzen AI 7 Pro 350", 
    "AMD Ryzen AI 7 Pro 360", "AMD Ryzen AI 9 365", "AMD Ryzen AI 9 HX 370", 
    "AMD Ryzen AI 9 HX 375", "Apple M-Series M1", "Apple M-Series M1 Pro 10 Core", 
    "Apple M-Series M1 Pro 8 Core", "Apple M-Series M2 10-Core GPU", 
    "Apple M-Series M2 8-Core GPU", "Apple M-Series M2 Pro 16-Core GPU", 
    "Apple M-Series M3 (8-Core CPU / 10-Core GPU)", 
    "Apple M-Series M3 (8-Core CPU / 8-Core GPU)", 
    "Apple M-Series M3 Max (14-Core CPU / 30-Core GPU)", 
    "Apple M-Series M3 Pro (11-Core CPU / 14-Core GPU)", 
    "Apple M-Series M3 Pro (12-Core CPU / 18-Core GPU)", 
    "Apple M-Series M4 (10-Core CPU / 10-Core GPU)", 
    "Apple M-Series M4 (10-Core CPU / 8-Core GPU)", 
    "Apple M-Series M4 Max (14-Core CPU / 32-Core GPU)", 
    "Apple M-Series M4 Pro (12-Core CPU / 16-Core GPU)", 
    "Apple M-Series M4 Pro (14-Core CPU / 20-Core GPU)", 
    "Intel Celeron N4000", "Intel Celeron N4020", "Intel Celeron N4500", 
    "Intel Celeron N5095", "Intel Core 5-120U", "Intel Core 5-210H", 
    "Intel Core 5-220U", "Intel Core 7 150U", "Intel Core 7 240H", 
    "Intel Core Ultra 5 125H", "Intel Core Ultra 5 125U", "Intel Core Ultra 5 135H", 
    "Intel Core Ultra 5 135U", "Intel Core Ultra 5 225U", "Intel Core Ultra 5 226V", 
    "Intel Core Ultra 5 228V", "Intel Core Ultra 5 235U", "Intel Core Ultra 7 155H", 
    "Intel Core Ultra 7 155U", "Intel Core Ultra 7 165H", "Intel Core Ultra 7 165U", 
    "Intel Core Ultra 7 255H", "Intel Core Ultra 7 255HX", "Intel Core Ultra 7 255U", 
    "Intel Core Ultra 7 256V", "Intel Core Ultra 7 258V", "Intel Core Ultra 7 268V", 
    "Intel Core Ultra 9 185H", "Intel Core Ultra 9 275HX", "Intel Core Ultra 9 285H", 
    "Intel Core i3-1005G1", "Intel Core i3-10110U", "Intel Core i3-1115G4", 
    "Intel Core i3-1125G4", "Intel Core i3-1215U", "Intel Core i3-1305U", 
    "Intel Core i3-1315U", "Intel Core i3-7020U", "Intel Core i3-8130U", 
    "Intel Core i3-8145U", "Intel Core i3-N300", "Intel Core i3-N305", 
    "Intel Core i5-10210U", "Intel Core i5-10300H", "Intel Core i5-1030NG7", 
    "Intel Core i5-10310U", "Intel Core i5-1035G1", "Intel Core i5-1035G4", 
    "Intel Core i5-1038NG7", "Intel Core i5-11300H", "Intel Core i5-1130G7", 
    "Intel Core i5-1135G7", "Intel Core i5-11400H", "Intel Core i5-1235U", 
    "Intel Core i5-1240P", "Intel Core i5-12450H", "Intel Core i5-12450HX", 
    "Intel Core i5-12500H", "Intel Core i5-1334U", "Intel Core i5-1335U", 
    "Intel Core i5-13420H", "Intel Core i5-13450HX", "Intel Core i5-1345U", 
    "Intel Core i5-13600HX", "Intel Core i5-5200U", "Intel Core i5-5250U", 
    "Intel Core i5-5350U", "Intel Core i5-6200U", "Intel Core i5-6260U", 
    "Intel Core i5-6300U", "Intel Core i5-7200U", "Intel Core i5-7300HQ", 
    "Intel Core i5-8210Y", "Intel Core i5-8250U", "Intel Core i5-8259U", 
    "Intel Core i5-8265U", "Intel Core i5-8279U", "Intel Core i5-8300H", 
    "Intel Core i5-8350U", "Intel Core i5-8365U", "Intel Core i5-9300H", 
    "Intel Core i7-10510U", "Intel Core i7-10610U", "Intel Core i7-1065G7", 
    "Intel Core i7-10750H", "Intel Core i7-10850H", "Intel Core i7-11370H", 
    "Intel Core i7-1165G7", "Intel Core i7-11800H", "Intel Core i7-1180G7", 
    "Intel Core i7-11850H", "Intel Core i7-1185G7", "Intel Core i7-1255U", 
    "Intel Core i7-1260P", "Intel Core i7-12650H", "Intel Core i7-1265U", 
    "Intel Core i7-12700H", "Intel Core i7-12800H", "Intel Core i7-12800HX", 
    "Intel Core i7-1355U", "Intel Core i7-1360P", "Intel Core i7-13620H", 
    "Intel Core i7-13650HX", "Intel Core i7-1365U", "Intel Core i7-13700H", 
    "Intel Core i7-13700HX", "Intel Core i7-13850HX", "Intel Core i7-14650HX", 
    "Intel Core i7-14700HX", "Intel Core i7-6600U", "Intel Core i7-6700HQ", 
    "Intel Core i7-7500U", "Intel Core i7-7600U", "Intel Core i7-8550U", 
    "Intel Core i7-8565U", "Intel Core i7-8650U", "Intel Core i7-8665U", 
    "Intel Core i7-8750H", "Intel Core i7-8850H", "Intel Core i7-9750H", 
    "Intel Core i9-11950H", "Intel Core i9-12950HX", "Intel Core i9-13900H", 
    "Intel Core i9-13900HK", "Intel Core i9-13900HX", "Intel Core i9-13950HX", 
    "Intel Core i9-13980HX", "Intel Core i9-14900HX", "Intel Core i9-9880H", 
    "Intel N150", "Intel Pentium Gold 4425Y", "Intel Pentium Gold 7505", 
    "Intel Xeon W-11955M", "Mediatek-Kompanio 520", 
    "Qualcomm Snapdragon X Elite X1E-78-100", 
    "Qualcomm Snapdragon X Plus X1P-42-100", "Qualcomm Snapdragon X X1-26-100"
]

# RAM Quantity literal type (sorted numerically)
type RAMQuantity = tp.Literal[
    "4 GB", "6 GB", "8 GB", "12 GB", "16 GB", "18 GB", "24 GB", 
    "32 GB", "36 GB", "40 GB", "48 GB", "64 GB"
]

# RAM Type literal type (alphabetically sorted)
type RAMType = tp.Literal[
    "DDR3", "DDR3L", "DDR4", "DDR4L", "DDR5", "LPDDR3", "LPDDR4", 
    "LPDDR4X", "LPDDR5", "LPDDR5X", "UMA"
]

# Screen Size literal type (sorted numerically)
type ScreenSize = tp.Literal[
    "7\"", "8\"", "10\"", "11\"", "12\"", "13\"", "14\"", "15\"", "16\"", "17\"", "18\"", "20\""
]

# Screen Type literal type (alphabetically sorted)
type ScreenType = tp.Literal[
    "AMOLED", "LED", "OLED"
]

# Screen Resolution literal type (sorted numerically by total pixels)
type ScreenResolution = tp.Literal[
    "1366x768", "1440x900", "1600x900", "1920x1080", "1980x1080", 
    "1920x1200", "1920x1280", "2048x1280", "2160x1440", "2240x1400", 
    "2256x1504", "2560x1440", "2560x1600", "2560x1664", "2880x1620", 
    "2880x1800", "2880x1864", "2880x1920", "2944x1840", "3000x2000", 
    "3024x1964", "3072x1920", "3200x2000", "3456x2234", "3840x2160", 
    "3840x2400"
]

# Screen Refresh Rate literal type (sorted numerically)
type ScreenRefreshRate = tp.Literal[
    "60 Hz", "90 Hz", "120 Hz", "144 Hz", "165 Hz", "240 Hz", "300 Hz", "360 Hz"
]

# Video Card Type literal type (alphabetically sorted)
type VideoCardType = tp.Literal[
    "Dedicada", "Integrada"
]

# Video Card Brand literal type (alphabetically sorted)
type VideoCardBrand = tp.Literal[
    "AMD", "ARM", "Apple", "Intel", "NVIDIA", "Qualcomm"
]

# Video Card Line literal type (alphabetically sorted)
type VideoCardLine = tp.Literal[
    "AMD Radeon", "ARM Mali", "Apple M-Series", "Intel Arc", "Intel HD Graphics", 
    "Intel Iris", "Intel UHD Graphics", "NVIDIA GeForce", "NVIDIA Quadro", 
    "NVIDIA RTX", "Qualcomm Snapdragon"
]


# Video Card literal type (alphabetically sorted)
type VideoCard = tp.Literal[
    "AMD Radeon 530 (2 GB)", "AMD Radeon 610M (Integrada)", "AMD Radeon 660M (Integrada)", 
    "AMD Radeon 680M (Integrada)", "AMD Radeon 740M (Integrada)", "AMD Radeon 760M (Integrada)", 
    "AMD Radeon 780M (Integrada)", "AMD Radeon 840M (Integrada)", "AMD Radeon 860M (Integrada)", 
    "AMD Radeon 880M (Integrada)", "AMD Radeon 890M (Integrada)", "AMD Radeon Pro 450 (2 GB)", 
    "AMD Radeon Pro 5300M (4 GB)", "AMD Radeon Pro 5500M (4 GB)", "AMD Radeon Pro 555X (4 GB)", 
    "AMD Radeon R4 Graphics (Stoney Ridge) (Integrada)", "AMD Radeon R5 Graphics (Stoney Ridge) (Integrada)", 
    "AMD Radeon R7 (Carrizo) (Integrada)", "AMD Radeon RX 5500M (4 GB)", "AMD Radeon RX 560X (4 GB)", 
    "AMD Radeon RX 6500M (4 GB)", "AMD Radeon RX 6600M (8 GB)", "AMD Radeon RX 6700S (8 GB)", 
    "AMD Radeon RX Vega 10 (Integrada)", "AMD Radeon RX Vega 3 (Integrada)", "AMD Radeon RX Vega 5 (Integrada)", 
    "AMD Radeon RX Vega 6 (Integrada)", "AMD Radeon RX Vega 6 (Ryzen 2000/3000) (Integrada)", 
    "AMD Radeon RX Vega 6 (Ryzen 4000) (Integrada)", "AMD Radeon RX Vega 6 (Ryzen 4000/5000) (Integrada)", 
    "AMD Radeon RX Vega 7 (Integrada)", "AMD Radeon RX Vega 8 (Integrada)", "ARM Mali G52 MC2 2EE (Integrada)", 
    "Apple M-Series M1 (Integrada)", "Apple M-Series M1 Pro (Integrada)", "Apple M-Series M2 10-Core GPU (Integrada)", 
    "Apple M-Series M2 8-Core GPU (Integrada)", "Apple M-Series M2 Pro 16-Core GPU (Integrada)", 
    "Apple M-Series M3 10-Core GPU (Integrada)", "Apple M-Series M3 8-Core GPU (Integrada)", 
    "Apple M-Series M3 Max 30-Core GPU (Integrada)", "Apple M-Series M3 Pro 14-Core GPU (Integrada)", 
    "Apple M-Series M3 Pro 18-Core GPU (Integrada)", "Apple M-Series M4 10-Core GPU (Integrada)", 
    "Apple M-Series M4 16-Core GPU (Integrada)", "Apple M-Series M4 20-Core GPU (Integrada)", 
    "Apple M-Series M4 32-Core GPU (Integrada)", "Apple M-Series M4 8-Core GPU (Integrada)", 
    "Intel Arc 4-Cores iGPU (Integrada)", "Intel Arc 7-Cores iGPU (Integrada)", "Intel Arc 8-Core iGPU (Integrada)", 
    "Intel Arc 8-Cores iGPU (Integrada)", "Intel Arc A350M (4 GB)", "Intel Arc Graphics 130V (Integrada)", 
    "Intel Arc Graphics 140T (Integrada)", "Intel Arc Graphics 140V (Integrada)", "Intel Arc LPG 96EU (Integrada)", 
    "Intel Arc Pro A30M (4 GB)", "Intel Arc Xe-LPG Graphics 64EU (Integrada)", "Intel HD Graphics 520 (Integrada)", 
    "Intel HD Graphics 5500 (Integrada)", "Intel HD Graphics 6000 (Integrada)", "Intel HD Graphics 620 (Integrada)", 
    "Intel Iris Graphics 540 (Integrada)", "Intel Iris Plus Graphics 655 (128 MB)", "Intel Iris Plus Graphics G4 (Integrada)", 
    "Intel Iris Plus Graphics G7 (Integrada)", "Intel Iris Xe Graphics G7 80EUs (Integrada)", 
    "Intel Iris Xe Graphics G7 96EUs (Integrada)", "Intel UHD Graphics 24EUs (Alder Lake-N) (Integrada)", 
    "Intel UHD Graphics 600 (Integrada)", "Intel UHD Graphics 615 (Integrada)", "Intel UHD Graphics 617 (Integrada)", 
    "Intel UHD Graphics 620 (Integrada)", "Intel UHD Graphics 630 (Integrada)", 
    "Intel UHD Graphics 64EUs (Alder Lake 12th Gen) (Integrada)", "Intel UHD Graphics 770 (Alder Lake) (Integrada)", 
    "Intel UHD Graphics 770 (Integrada)", "Intel UHD Graphics G1 (Integrada)", "Intel UHD Graphics G4 48EUs (Integrada)", 
    "Intel UHD Graphics Jasper Lake 16 EU (Integrada)", "Intel UHD Graphics Xe 32EUs (Integrada)", 
    "Intel UHD Graphics Xe 750 32EUs (Integrada)", "Intel UHD Graphics Xe G4 48EUs (Integrada)", 
    "NVIDIA GeForce 940MX (4 GB)", "NVIDIA GeForce GTX 1050 (2 GB)", "NVIDIA GeForce GTX 1050 (3 GB)", 
    "NVIDIA GeForce GTX 1650 (4 GB)", "NVIDIA GeForce GTX 1650 Max-Q (4 GB)", "NVIDIA GeForce GTX 1650 Ti (4 GB)", 
    "NVIDIA GeForce GTX 1660 Ti (6 GB)", "NVIDIA GeForce GTX 1660 Ti Max-Q (6 GB)", "NVIDIA GeForce MX110 (2 GB)", 
    "NVIDIA GeForce MX130 (2 GB)", "NVIDIA GeForce MX250 (2 GB)", "NVIDIA GeForce MX330 (2 GB)", 
    "NVIDIA GeForce MX350 (2 GB)", "NVIDIA GeForce MX450 (2 GB)", "NVIDIA GeForce MX550 (2 GB)", 
    "NVIDIA GeForce MX570 (2 GB)", "NVIDIA GeForce RTX 2050 (4 GB)", "NVIDIA GeForce RTX 2060 (6 GB)", 
    "NVIDIA GeForce RTX 2060 Max-Q (6 GB)", "NVIDIA GeForce RTX 2070 (8 GB)", "NVIDIA GeForce RTX 2070 Super Max-Q (8 GB)", 
    "NVIDIA GeForce RTX 3050 (4 GB)", "NVIDIA GeForce RTX 3050 (6 GB)", "NVIDIA GeForce RTX 3050 Ti (4 GB)", 
    "NVIDIA GeForce RTX 3060 (6 GB)", "NVIDIA GeForce RTX 3060 Max-Q (6 GB)", "NVIDIA GeForce RTX 3070 (8 GB)", 
    "NVIDIA GeForce RTX 3070 Ti (8 GB)", "NVIDIA GeForce RTX 3080 (8 GB)", "NVIDIA GeForce RTX 3080 Ti (16 GB)", 
    "NVIDIA GeForce RTX 4050 (6 GB)", "NVIDIA GeForce RTX 4050 (8 GB)", "NVIDIA GeForce RTX 4060 (8 GB)", 
    "NVIDIA GeForce RTX 4070 (8 GB)", "NVIDIA GeForce RTX 4080 (12 GB)", "NVIDIA GeForce RTX 4090 (16 GB)", 
    "NVIDIA GeForce RTX 5060 (8 GB)", "NVIDIA GeForce RTX 5070 (8 GB)", "NVIDIA GeForce RTX 5070 Ti (12 GB)", 
    "NVIDIA GeForce RTX 5080 (16 GB)", "NVIDIA GeForce RTX 5090 (24 GB)", "NVIDIA Quadro P1000 (4 GB)", 
    "NVIDIA Quadro P520 (2 GB)", "NVIDIA Quadro P520 (4 GB)", "NVIDIA Quadro P620 (4 GB)", 
    "NVIDIA Quadro RTX 4000 (12 GB)", "NVIDIA Quadro T1000 (4 GB)", "NVIDIA Quadro T2000 (4 GB)", 
    "NVIDIA Quadro T500 (4 GB)", "NVIDIA Quadro T550 (4 GB)", "NVIDIA Quadro T600 (4 GB)", 
    "NVIDIA RTX 1000 Ada (6 GB)", "NVIDIA RTX 2000 Ada (8 GB)", "NVIDIA RTX 3000 Ada (8 GB)", 
    "NVIDIA RTX 4000 Ada (12 GB)", "NVIDIA RTX 500 Ada (4 GB)", "NVIDIA RTX 5000 Ada (16 GB)", 
    "NVIDIA RTX A1000 (4 GB)", "NVIDIA RTX A1000 (6 GB)", "NVIDIA RTX A2000 (8 GB)", "NVIDIA RTX A3000 (6 GB)", 
    "NVIDIA RTX A500 (4 GB)", "Qualcomm Snapdragon X Adreno X1-45 (Integrada)", 
    "Qualcomm Snapdragon X Adreno X1-85 (Integrada)"
]

# Storage Capacity literal type (sorted numerically)
type StorageCapacity = tp.Literal[
    "32 GB", "64 GB", "128 GB", "240 GB", "250 GB", "256 GB", "480 GB", 
    "500 GB", "512 GB", "960 GB", "1 TB", "2 TB", "4 TB"
]

# Storage Drive Type literal type (alphabetically sorted)
type StorageDriveType = tp.Literal[
    "HDD", "SSD", "Super RAID", "eMMC"
]


# Storage Drive RPM literal type (sorted numerically)
type StorageDriveRPM = tp.Literal[
    "0 rpm (Flash)", "5400 rpm", "7200 rpm"
]


# Operating System literal type (alphabetically sorted)
type OperatingSystem = tp.Literal[
    "Apple macOS", "FreeDOS", "Google Chrome OS", "Linux", 
    "Microsoft Windows 10", "Microsoft Windows 11", "Microsoft Windows 7"
]

# Specific Operating System literal type (alphabetically sorted)
type SpecificOperatingSystem = tp.Literal[
    "Apple macOS Big Sur", "Apple macOS Catalina", "Apple macOS High Sierra", 
    "Apple macOS Mojave", "Apple macOS Monterey", "Apple macOS Sequoia", 
    "Apple macOS Sierra", "Apple macOS Sonoma", "Apple macOS Ventura", 
    "Apple macOS Yosemite", "FreeDOS", "Google Chrome OS", "Linux Ubuntu", 
    "Microsoft Windows 10 Home", "Microsoft Windows 10 Professional", 
    "Microsoft Windows 11 Home", "Microsoft Windows 11 Pro", 
    "Microsoft Windows 7 Professional + Upgrade Windows 10 Pro", 
    "Microsoft Windows 7 Professional + Upgrade Windows 8.1 Pro"
]

# Keyboard Layout literal type (alphabetically sorted)
type KeyboardLayout = tp.Literal[
    "Desconocido", "Español", "Inglés"
]


class NotebookSearchUnicodeQueryParams(pydantic.BaseModel):
    # API parameters
    exclude_refurbished: bool = True
    page: int = 1
    page_size: int = 10
    # stores: list[Id] | None = None
    
    # Price range and search
    offer_price_usd_min: float | None = None
    offer_price_usd_max: float | None = None
    search: str | None = None

    # Product categories and weight
    brands: list[Brand] | None = None
    lines: list[BrandLine] | None = None
    weight_min: int | None = None
    weight_max: int | None = None
    
    # Processor specifications
    processor_brands: list[ProcessorBrand] | None = None
    processor_lines: list[ProcessorLine] | None = None
    processor_thread_count_min: ProcessorThreadCount | None = None
    processors: list[Processor] | None = None
    processor_speed_score_min: int | None = None
    processor_speed_score_max: int | None = None
    
    # RAM specifications
    ram_quantity_min: RAMQuantity | None = None
    ram_types: list[RAMType] | None = None
    
    # Screen specifications
    screen_size_min: ScreenSize | None = None
    screen_size_max: ScreenSize | None = None
    screen_types: list[ScreenType] | None = None
    screen_resolution_min: ScreenResolution | None = None
    screen_refresh_rate_min: ScreenRefreshRate | None = None
    screen_touch: bool | None = None
    screen_is_rotating: bool | None = None
    
    # Video card specifications
    video_card_types: list[VideoCardType] | None = None
    video_card_brands: list[VideoCardBrand] | None = None
    video_card_lines: list[VideoCardLine] | None = None
    video_cards: list[VideoCard] | None = None
    score_games_min: int | None = None
    score_games_max: int | None = None
    
    # Storage specifications
    storage_capacity_min: StorageCapacity | None = None
    storage_drive_types: list[StorageDriveType] | None = None
    storage_drive_rpm: StorageDriveRPM | None = None
    
    # Operating system specifications
    operating_systems: list[OperatingSystem] | None = None
    specific_operating_systems: list[SpecificOperatingSystem] | None = None
    keyboard_layouts: list[KeyboardLayout] | None = None
    has_fingerprint_reader: bool | None = None


class NotebookSearchResponse(pydantic.BaseModel):
    count: int
    
    class ProductBucket(pydantic.BaseModel):
        bucket: str
        
        class ProductEntry(pydantic.BaseModel):
            
            class Product(pydantic.BaseModel):
                # Required for product card
                name: str
                picture_url: str
                
                # Additional fields to keep
                id: int
                keywords: str
                url: str
                
                class ProductSpecs(pydantic.BaseModel):
                    # Processor info (for "Procesador" field)
                    processor_unicode: str
                    processor_frequency_unicode: str
                    processor_frequency_value: int
                    
                    # Cores/threads info (for "Núcleos" field)
                    processor_thread_count_name: str
                    processor_thread_count_value: int
                    
                    # RAM info (for "RAM" field)
                    ram_quantity_unicode: str
                    ram_type_unicode: str
                    ram_frequency_unicode: str
                    
                    # Screen info (for "Pantalla" field)
                    screen_size_unicode: str
                    screen_resolution_unicode: str
                    screen_refresh_rate_unicode: str
                    
                    # Graphics info (for "Tarjetas de video" field)
                    pretty_dedicated_video_card: str
                    
                    class StorageDrive(pydantic.BaseModel):
                        capacity_unicode: str
                        drive_type_unicode: str
                    
                    class GPU(pydantic.BaseModel):
                        unicode: str
                    
                    # Storage info (for "Almacenamiento" field)
                    largest_storage_drive: StorageDrive
                    
                    # Graphics info (for "Tarjetas de video" field)
                    main_gpu: GPU
                
                specs: ProductSpecs
            
            class ProductEntryMetadata(pydantic.BaseModel):
                # Required for product card
                offer_price_usd: str
            
            product: Product
            metadata: ProductEntryMetadata
        
        product_entries: list[ProductEntry]
    
    results: list[ProductBucket]