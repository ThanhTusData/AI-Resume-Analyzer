"""
CSS Selectors for LinkedIn
Centralized selector definitions
"""


class LinkedInSelectors:
    """CSS selectors for LinkedIn elements"""
    
    # Login page
    LOGIN_EMAIL = "input#username"
    LOGIN_PASSWORD = "input#password"
    LOGIN_BUTTON = "button[type='submit']"
    LOGIN_ERROR = "div#error-for-username"
    
    # Job search
    SEARCH_INPUT = "input.jobs-search-box__text-input"
    LOCATION_INPUT = "input[aria-label*='location']"
    SEARCH_BUTTON = "button.jobs-search-box__submit-button"
    
    # Job cards
    JOB_CARD = "div.job-card-container, li.jobs-search-results__list-item"
    JOB_CARD_LINK = "a.job-card-list__title"
    JOB_TITLE = "h3.job-card-list__title, a.job-card-container__link"
    COMPANY_NAME = "h4.job-card-container__company-name, a.job-card-container__company-name"
    JOB_LOCATION = "span.job-card-container__metadata-item"
    APPLICANT_COUNT = "span.job-card-container__applicant-count"
    
    # Job details
    JOB_DETAILS = "div.jobs-search__job-details, div.job-view-layout"
    JOB_DETAILS_TITLE = "h1.job-title, h2.t-24"
    JOB_DETAILS_COMPANY = "a.job-card-container__company-name, span.jobs-unified-top-card__company-name"
    JOB_DETAILS_LOCATION = "span.jobs-unified-top-card__bullet, span.job-card-container__metadata-item"
    JOB_DESCRIPTION = "div.jobs-description__content, div.jobs-box__html-content"
    JOB_CRITERIA = "li.jobs-unified-top-card__job-insight"
    SHOW_MORE_BUTTON = "button[aria-label*='Show more'], button.jobs-description__footer-button"
    
    # Apply button
    APPLY_BUTTON = "button.jobs-apply-button"
    EASY_APPLY_BUTTON = "button.jobs-apply-button--top-card"
    
    # Search results
    SEARCH_RESULTS_LIST = "ul.jobs-search-results__list"
    JOB_CARD_LIST = "div.jobs-search-results__list-item"
    PAGINATION = "button[aria-label*='Page']"
    NEXT_PAGE = "button[aria-label='View next page']"
    
    # Filters
    DATE_POSTED_FILTER = "button[aria-label*='Date posted']"
    EXPERIENCE_LEVEL_FILTER = "button[aria-label*='Experience level']"
    JOB_TYPE_FILTER = "button[aria-label*='Job type']"
    REMOTE_FILTER = "button[aria-label*='Remote']"
    
    # Additional info
    SALARY_INFO = "span.job-card-container__salary-info"
    JOB_POSTED_DATE = "span.job-card-container__listed-time"
    PROMOTED_BADGE = "span.job-card-container__promoted-badge"
