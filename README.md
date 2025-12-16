## Next Steps

### Tasks

- [ ] Handle Log In to allow access to url paths that require authentication (Page Interactivity)
- [x] Label saved files using a sanitized version of the url they were scraped from
- [x] Perform [deep crawling](https://docs.crawl4ai.com/core/deep-crawling/) to scrape all internal pages

## Inference from screenshots 🔧

You can run LLM-based inference on screenshots saved in `crawl_results/screenshots` using the script:

```bash
python -m inference.screenshots_inference --pattern "www_kessbet_com"
```

The script will:
- Find screenshots whose filenames match the provided regex (default is set by `FILE_NAME_PATTERN` in `inference/screenshots_inference.py`) ⚙️
- Run OCR with `pytesseract` (if installed) 💡
- Send the extracted text to Google Gemini (`google-genai`) for analysis and save results to `crawl_results/analysis/` ✅

Make sure you set `GOOGLE_API_KEY` in your environment before running inference.
































