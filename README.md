# Web Scraping with OpenAI Integration & Marketing Brochure Generator

This project demonstrates a robust approach to web scraping dynamic websites built with JavaScript and includes a new **Marketing Brochure Generator** for creating company brochures based on website content. Additionally, it incorporates OpenAI's **GPT-4o-mini** API for processing and analyzing scraped content, enabling enhanced functionality like summarization, sentiment analysis, insight extraction, and more.

## Problem Statement

When web scraping, static websites are straightforward to handle because their content is available in the raw HTML. However, JavaScript-driven websites dynamically render their content in the browser, making it inaccessible to traditional scraping methods. Moreover, extracting meaningful insights from scraped data often requires additional processing.

### Challenges Addressed:

- **Dynamic Content Loading**: JavaScript-rendered websites don't expose data in raw HTML.
- **Handling Browser-Specific Restrictions**: Modern browsers and OSs restrict direct access to driver binaries without appropriate security permissions.
- **Compatibility Between Browser and Driver Versions**: Mismatched versions between Chrome and ChromeDriver can result in session failures.
- **Extracting Insights from Data**: Post-scraping processing of the extracted content is essential for real-world applications.

## Solution

The project uses the following technologies to address these challenges:

### Technology Stack

- **Selenium**: A web automation framework that enables interacting with web browsers programmatically.
- **Python**: For scripting and controlling the scraping logic.
- **Selenium WebDriver**: Handles browser automation for JavaScript-heavy websites.
- **ChromeDriver**: Bridges Selenium WebDriver with the Chrome browser.
- **WebDriver Manager (Optional)**: Automatically manages ChromeDriver versions to prevent compatibility issues.
- **OpenAI API (GPT-4o-mini)**: Used for processing scraped content and generating marketing brochures. This allows for:
  - Summarizing long texts.
  - Extracting specific insights.
  - Performing sentiment analysis or categorization.
  - Creating structured outputs in JSON format.
  - Generating professional marketing brochures for prospective customers, investors, and recruits.

## Marketing Brochure Generator

The **Marketing Brochure Generator** project is designed to build a marketing brochure for a company using the content from their website. By providing a company name and their primary website, this tool will scrape relevant data from the site and create a brochure that can be shared with prospective clients, investors, and potential recruits.

### Key Features:

- **Website Scraping**: Scrapes the main landing page and relevant sections (About, Careers, Products) from the company website.
- **Relevant Link Identification**: Uses OpenAI's GPT-4o-mini to analyze the links on a webpage and determine which are most relevant for a marketing brochure.
- **Brochure Creation**: Uses the GPT-4o-mini model to analyze the scraped content and create a concise, informative brochure in Markdown format. The brochure includes details about the company's culture, customers, products, and career opportunities.

### Example Process:

1. **Scraping Website Content**: The project fetches the content from a company's website and identifies useful links for the brochure.
2. **GPT-4o-mini Integration**: The **GPT-4o-mini** model is used to analyze the content and decide which links are most relevant. It then generates a summary or brochure from the relevant pages.
3. **Marketing Brochure Generation**: The result is a professional markdown-based brochure that can be easily formatted and shared.

## Implementation Steps

1. **Launch and Control Browser**:
   - Use Selenium WebDriver to launch and control a Chrome browser session.
2. **Navigate to the Target Website**:

   - Navigate to the target website (e.g., [https://openai.com](https://openai.com)).

3. **Wait for JavaScript-Rendered Content**:

   - Use explicit waits to ensure that JavaScript-rendered content has fully loaded.

4. **Extract Relevant Data**:

   - Extract the relevant data once the content is fully loaded.

5. **Integrate OpenAI API**:
   - Use the **GPT-4o-mini** model to process the scraped content and generate the marketing brochure.

## Requirements

- Python 3.x
- Selenium
- WebDriver Manager (optional)
- OpenAI API Key (for content processing)
