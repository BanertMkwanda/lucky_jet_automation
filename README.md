name: Run Selenium Scraper

on:
  schedule: 
    - cron: '30 19 * * *' # Runs every day at 7:30 PM UTC
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-22.04

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install Chrome
        run: |
          wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
          sudo mkdir -p /etc/apt/sources.list.d
          sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
          sudo apt-get update
          sudo apt-get -y install google-chrome-stable

      - name: Install ChromeDriver
        run: |
          CHROMEDRIVER_VERSION="136.0.7103.94"
          echo "Installing ChromeDriver version: $CHROMEDRIVER_VERSION"
          wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip"
          unzip chromedriver-linux64.zip
          chmod +x chromedriver-linux64/chromedriver
          sudo mv chromedriver-linux64/chromedriver /usr/local/bin/

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Lucky.py script
        run: python Lucky.py
