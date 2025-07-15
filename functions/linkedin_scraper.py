import time
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import warnings
warnings.filterwarnings('ignore')

class linkedin_scraper:

    def webdriver_setup():
        """
        Thiết lập Chrome driver với undetected_chromedriver
        """
        options = uc.ChromeOptions()
        options.user_data_dir = "selenium_profile"  # Lưu session để tránh phải login lại
        options.add_argument("--start-maximized")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')  # Bỏ comment nếu muốn chạy ẩn

        driver = uc.Chrome(options=options)
        return driver

    def get_userinput():
        """
        Lấy input từ người dùng
        """
        add_vertical_space(2)
        with st.form(key='linkedin_scarp'):
            
            add_vertical_space(1)
            col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
            
            with col1:
                job_title_input = st.text_input(label='Job Title')
                job_title_input = [title.strip() for title in job_title_input.split(',') if title.strip()]
            
            with col2:
                job_location = st.text_input(label='Job Location', value='Vietnam')
            
            with col3:
                job_count = st.number_input(label='Job Count', min_value=1, value=5, step=1)
            
            add_vertical_space(1)
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)
        
        return job_title_input, job_location, job_count, submit

    def build_url(job_title, job_location):
        """
        Tạo URL tìm kiếm LinkedIn
        """
        b = []
        for i in job_title:
            x = i.split()
            y = '%20'.join(x)
            b.append(y)

        job_title_encoded = '%2C%20'.join(b)
        
        # Sử dụng geoId cho Vietnam
        if job_location.lower() == 'vietnam':
            link = f"https://www.linkedin.com/jobs/search?keywords={job_title_encoded}&location=Vietnam&geoId=104195383&f_TPR=r604800&position=1&pageNum=0"
        else:
            link = f"https://www.linkedin.com/jobs/search?keywords={job_title_encoded}&location={job_location}&f_TPR=r604800&position=1&pageNum=0"
        
        return link

    def get_jobs_with_javascript(driver, base_link, max_pages=3, scroll_times=12, expected_jobs=25):
        """
        Lấy dữ liệu công việc sử dụng JavaScript
        """
        all_companies = []
        all_job_titles = []
        all_locations = []
        all_urls = []

        for page_num in range(1, max_pages + 1):
            current_link = base_link if page_num == 1 else f"{base_link}&start={25 * (page_num - 1)}"
            
            try:
                driver.get(current_link)
                time.sleep(5)

                # Cuộn danh sách để load job cards
                try:
                    scroll_container = driver.find_element(By.XPATH, "//div[contains(@class, 'jobs-search-results-list')]")
                    for _ in range(scroll_times):
                        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll_container)
                        time.sleep(1.5)
                except Exception:
                    # Nếu không tìm thấy container, cuộn trang chính
                    for _ in range(scroll_times):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1.5)

                # Đợi job cards render
                start_time = time.time()
                while time.time() - start_time < 30:
                    job_cards = driver.find_elements(By.XPATH, "//li[@data-occludable-job-id]")
                    if len(job_cards) >= expected_jobs:
                        break
                    time.sleep(2)

                # Scroll từng job để ép render
                job_cards = driver.find_elements(By.XPATH, "//li[@data-occludable-job-id]")
                for job_card in job_cards:
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", job_card)
                        time.sleep(0.5)
                    except:
                        pass

                # Lấy dữ liệu bằng JavaScript
                js_script = """
                var jobCards = document.querySelectorAll('li[data-occludable-job-id]');
                var results = [];

                jobCards.forEach(function(card) {
                    try {
                        var titleEl = card.querySelector('a.job-card-container__link span[aria-hidden="true"]') ||
                                      card.querySelector('h3') ||
                                      card.querySelector('.job-card-list__title') ||
                                      card.querySelector('.job-card-container__title');

                        var companyEl = card.querySelector('div.artdeco-entity-lockup__subtitle span') ||
                                        card.querySelector('.job-card-container__company-name') ||
                                        card.querySelector('h4');

                        var locationEl = card.querySelector('ul.job-card-container__metadata-wrapper li span[dir="ltr"]') ||
                                         card.querySelector('span.job-card-container__metadata-item') ||
                                         card.querySelector('.job-card-container__metadata-item');

                        var urlEl = card.querySelector('a.job-card-container__link') ||
                                    card.querySelector('a[href*="/jobs/view/"]');

                        var rawUrl = urlEl ? urlEl.getAttribute("href") : '';
                        var fullUrl = rawUrl.startsWith("http") ? rawUrl : "https://www.linkedin.com" + rawUrl;

                        var title = titleEl ? titleEl.textContent.trim() : '';
                        var company = companyEl ? companyEl.textContent.trim() : '';
                        var location = locationEl ? locationEl.textContent.trim() : '';

                        if (title && company && location) {
                            results.push({
                                title: title,
                                company: company,
                                location: location,
                                url: fullUrl
                            });
                        }

                    } catch (e) {
                        // Bỏ qua lỗi
                    }
                });

                return results;
                """

                job_data = driver.execute_script(js_script)
                
                for job in job_data:
                    all_job_titles.append(job['title'])
                    all_companies.append(job['company'])
                    all_locations.append(job['location'])
                    all_urls.append(job['url'])

            except Exception as e:
                st.error(f"Lỗi tại trang {page_num}: {e}")
                continue

        return all_companies, all_job_titles, all_locations, all_urls

    def job_title_filter(scrap_job_title, user_job_title_input):
        """
        Lọc tiêu đề công việc theo input của user
        """
        if pd.isna(scrap_job_title) or scrap_job_title == '':
            return np.nan
        
        # Chuyển user input thành lowercase
        user_input = [i.lower().strip() for i in user_job_title_input]
        suggestion = []
        for i in user_input:
            suggestion.extend(i.split())
        
        # Chuyển scraped title thành lowercase
        scrap_words = [i.lower().strip() for i in scrap_job_title.split()]
        
        # Tìm giao điểm
        intersection = list(set(suggestion).intersection(set(scrap_words)))
        return scrap_job_title if len(intersection) >= 1 else np.nan

    def get_job_description(driver, job_link):
        """
        Lấy mô tả công việc từ trang chi tiết
        """
        try:
            driver.get(job_link)
            
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)

            # Click "See more" nếu có
            try:
                see_more_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='see more description'], button[data-tracking-control-name*='show-more']"))
                )
                if see_more_btn.is_displayed() and see_more_btn.is_enabled():
                    driver.execute_script("arguments[0].click();", see_more_btn)
                    time.sleep(1.5)
            except TimeoutException:
                pass

            # Lấy nội dung mô tả
            desc_text = ""
            possible_selectors = [
                "div.jobs-box__html-content",
                "div.jobs-description__container",
                "div.jobs-description-content__text",
                "div.jobs-description-content",
                "div.jobs-box__body"
            ]

            for selector in possible_selectors:
                try:
                    desc_elem = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    desc_text = desc_elem.text.strip()
                    if desc_text:
                        break
                except TimeoutException:
                    continue

            return desc_text if desc_text else "Không tìm thấy mô tả công việc"

        except Exception as e:
            return f"Lỗi khi lấy mô tả: {str(e)}"

    def scrap_job_descriptions(driver, df, job_count):
        """
        Lấy mô tả công việc cho tất cả các URL
        """
        website_urls = df['Website URL'].tolist()
        job_descriptions = []
        
        # Giới hạn số lượng job descriptions theo job_count
        urls_to_process = website_urls[:job_count]
        
        for i, url in enumerate(urls_to_process):
            try:
                with st.spinner(f'Đang lấy mô tả công việc {i+1}/{len(urls_to_process)}...'):
                    desc = linkedin_scraper.get_job_description(driver, url)
                    job_descriptions.append(desc)
                    
                    # Tránh spam requests
                    time.sleep(1)
                    
            except Exception as e:
                job_descriptions.append(f"Lỗi: {str(e)}")
        
        # Cập nhật DataFrame
        df_filtered = df.iloc[:len(job_descriptions), :].copy()
        df_filtered['Job Description'] = job_descriptions
        
        # Loại bỏ các job không có mô tả hợp lệ
        df_filtered = df_filtered[
            (df_filtered['Job Description'] != 'Không tìm thấy mô tả công việc') & 
            (~df_filtered['Job Description'].str.startswith('Lỗi:'))
        ]
        
        df_filtered.reset_index(drop=True, inplace=True)
        return df_filtered

    def display_data_userinterface(df_final):
        """
        Hiển thị dữ liệu trong Streamlit
        """
        add_vertical_space(1)
        if len(df_final) > 0:
            st.success(f"Tìm thấy {len(df_final)} công việc phù hợp!")
            
            for i in range(len(df_final)):
                st.markdown(f'<h3 style="color: orange;">Công việc {i+1}</h3>', unsafe_allow_html=True)
                st.write(f"**Công ty:** {df_final.iloc[i,0]}")
                st.write(f"**Vị trí:** {df_final.iloc[i,1]}")
                st.write(f"**Địa điểm:** {df_final.iloc[i,2]}")
                st.write(f"**URL:** {df_final.iloc[i,3]}")
                
                with st.expander(label='Mô tả công việc'):
                    st.write(df_final.iloc[i, 4])
                
                add_vertical_space(2)
        else:
            st.warning("Không tìm thấy công việc phù hợp!")

    def main():
        """
        Hàm chính để chạy scraper
        """
        driver = None
        
        try:
            job_title_input, job_location, job_count, submit = linkedin_scraper.get_userinput()
            add_vertical_space(2)
            
            if submit:
                if job_title_input and job_location:
                    
                    # Hiển thị thông tin tìm kiếm
                    st.info(f"Đang tìm kiếm: {', '.join(job_title_input)} tại {job_location}")
                    
                    with st.spinner('Đang khởi tạo Chrome driver...'):
                        driver = linkedin_scraper.webdriver_setup()
                    
                    with st.spinner('Đang tải danh sách công việc...'):
                        # Tạo URL tìm kiếm
                        link = linkedin_scraper.build_url(job_title_input, job_location)
                        
                        # Lấy dữ liệu công việc
                        companies, job_titles, locations, urls = linkedin_scraper.get_jobs_with_javascript(
                            driver, link, max_pages=3
                        )
                    
                    if companies:
                        # Tạo DataFrame
                        min_length = min(len(companies), len(job_titles), len(locations), len(urls))
                        df = pd.DataFrame({
                            'Company Name': companies[:min_length],
                            'Job Title': job_titles[:min_length],
                            'Location': locations[:min_length],
                            'Website URL': urls[:min_length]
                        })
                        
                        # Lọc theo tiêu đề công việc
                        df['Job Title'] = df['Job Title'].apply(
                            lambda x: linkedin_scraper.job_title_filter(x, job_title_input)
                        )
                        df = df.dropna()
                        df.reset_index(drop=True, inplace=True)
                        
                        if len(df) > 0:
                            with st.spinner('Đang lấy mô tả công việc chi tiết...'):
                                # Lấy mô tả công việc
                                df_final = linkedin_scraper.scrap_job_descriptions(driver, df, job_count)
                            
                            # Hiển thị kết quả
                            linkedin_scraper.display_data_userinterface(df_final)
                        else:
                            st.warning("Không tìm thấy công việc phù hợp với từ khóa!")
                    else:
                        st.error("Không thể lấy dữ liệu từ LinkedIn. Vui lòng thử lại!")
                
                elif not job_title_input:
                    st.error("Vui lòng nhập tiêu đề công việc!")
                
                elif not job_location:
                    st.error("Vui lòng nhập địa điểm!")

        except Exception as e:
            st.error(f"Có lỗi xảy ra: {str(e)}")
            
        finally:
            if driver:
                driver.quit()