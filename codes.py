import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
# Klasör yolunu belirtin
klasor_yolu = r'Excel Konumu'

# Türkiye illerini içeren shape dosyasını yükleyin
shape_dosyasi = r'Shape dosyasının konumu'

# Shape dosyasını yükleyin
gdf = gpd.read_file(shape_dosyasi)

# Türkçe karakterleri düzeltmek için kullanılacak haritalar
turkish_chars = {
    'İ': 'I',
    'ı': 'i',
    'Ş': 'S',
    'ş': 's',
    'Ğ': 'G',
    'ğ': 'g',
    'Ü': 'U',
    'ü': 'u',
    'Ö': 'O',
    'ö': 'o',
    'Ç': 'C',
    'ç': 'c',
}
translation_table = str.maketrans(turkish_chars)


# Şehir isimlerini düzeltmek için bir eşleştirme sözlüğü oluşturun
replace_map = {
    'K. Maras': 'Kahramanmaras',
    'Kinkkale': 'Kirikkale',
    'Zinguldak': 'Zonguldak',
    'Afyon': 'Afyonkarahisar'
}

gdf['NAME_1'] = gdf['NAME_1'].replace(replace_map)

# Excel dosyalarının bulunduğu dizindeki tüm Excel dosyalarını alın
excel_dosyalari = [dosya for dosya in os.listdir(klasor_yolu) if dosya.endswith('.xlsx')]

# Harita çizimine başlamadan önce gri bir renk paleti oluşturun
colors = ['gray' for _ in range(len(gdf))]

# Her bir Excel dosyası için işlem yapın
for excel_dosyasi in excel_dosyalari:
    # Excel dosyasını oku ve veriyi DataFrame'e yükleyin
    veri = pd.read_excel(os.path.join(klasor_yolu, excel_dosyasi))
    
    # Şehirlerin adlarını ve yerleşen sayılarını içeren bir sözlük oluşturun
    city_data = dict(zip(veri['city'], veri['Yerleşen Sayısı']))

    # Haritayı çizin
    fig, ax = plt.subplots(figsize=(20, 10))

    # Her bir şehir için döngü yapın
    for i, row in gdf.iterrows():
        city_name = row['NAME_1']
        settled_count = city_data.get(city_name, '0')  # Eğer veri yoksa "Veri Yok" yazısı kullan
        color = 'blue' if city_name in city_data else 'gray'
        gdf[gdf['NAME_1'] == city_name].plot(ax=ax, color=color, edgecolor='black', linewidth=0.5)
        
        # Şehir adını ve yerleşen sayısını ekleyin
        x, y = row['geometry'].centroid.x, row['geometry'].centroid.y
        ax.text(x, y, f"{city_name}\n({settled_count})", fontsize=8, ha='center', path_effects=[pe.withStroke(linewidth=2, foreground='white')])

    # Eksenleri kapatın
    ax.set_axis_off()

    # Başlığı ekleyin
    ax.set_title("Yerleşen Öğrencilerin Memleketi(2023)", fontsize=18, fontdict={"fontweight": 'bold'})
    dosya_adi = os.path.splitext(excel_dosyasi)[0]  # Excel dosyasının adını al
    fig.savefig(f'{dosya_adi}_haritasi.png', dpi=300, bbox_inches='tight')#dosya adına göre png olarak kaydet
    # Plot gösterin
    plt.show()
    
