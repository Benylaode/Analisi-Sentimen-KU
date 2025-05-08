from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv

# Konfigurasi Browser
brave_path = "/usr/bin/brave-browser" 
chromedriver_path = "/usr/local/bin/chromedriver"  

options = Options()
options.binary_location = brave_path
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

app_url = 'https://play.google.com/store/apps/details?id=app.bpjs.mobile&hl=id&pli=1'
driver.get(app_url)

def open_review_popup():
    try:
        review_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//button[.//span[contains(text(), 'Lihat semua ulasan')]]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", review_button)
        time.sleep(1)
        ActionChains(driver).move_to_element(review_button).click().perform()
        time.sleep(3)
        return True
    except Exception as e:
        print("Gagal membuka pop-up ulasan.")
        print("Error:", str(e))
        return False

if not open_review_popup():
    driver.quit()
    exit()

def scrape_reviews():
    reviews = driver.find_elements(By.CSS_SELECTOR, 'div.RHo1pe')
    new_data_count = 0
    
    for review in reviews:
        try:
            review_id = review.get_attribute('data-id') or review.id
            if review_id in processed_reviews:
                continue
                
            ulasan = review.find_element(By.CSS_SELECTOR, 'div.h3YV2d').text
            rating = "positif" if len(review.find_elements(By.CSS_SELECTOR, 'span.Z1Dz7b')) >= 3 else "negatif"
            tanggal = review.find_element(By.CSS_SELECTOR, 'span.bp9Aid').text
            nama_pengguna = review.find_element(By.CSS_SELECTOR, 'div.X5PpBb').text

            data.append({
                'rating': rating,
                'ulasan': ulasan,
                'tanggal': tanggal,
                'nama_pengguna': nama_pengguna
            })
            
            processed_reviews.add(review_id)
            new_data_count += 1
            print(f"✅ Berhasil scraping ulasan ke-{len(data)}: {nama_pengguna} | Rating: {rating} | Tanggal: {tanggal}")
            
        except Exception as e:
            print(f"❌ Gagal memproses ulasan: {str(e)}")
            continue
            
    return new_data_count

data = []
processed_reviews = set()
max_data = 5000  
max_scroll_attempts = 10
scroll_attempt = 0

try:
    review_popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.fysCi'))
    )
    print("🎯 Pop-up ulasan berhasil ditemukan!")
except Exception as e:
    print("❌ Gagal menemukan container pop-up ulasan:", str(e))
    driver.quit()
    exit()

while len(data) < max_data and scroll_attempt < max_scroll_attempts:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", review_popup)
    time.sleep(3)  

    new_reviews = scrape_reviews()
    
    if new_reviews == 0:
        scroll_attempt += 1
        print(f"🔍 Tidak ada ulasan baru (Percobaan {scroll_attempt}/{max_scroll_attempts})")
    else:
        scroll_attempt = 0 

csv_filename = 'ulasan_playstore.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['rating', 'ulasan', 'tanggal', 'nama_pengguna']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"\n💾 Data berhasil disimpan ke '{csv_filename}'")
print(f"📊 Total ulasan: {len(data)}")

driver.quit()
