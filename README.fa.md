# ابزارهای CSV ساروی

ترجمهٔ یک ستون یا دسته‌بندی پیام‌های پشتیبانی، با Python و بدون کتابخانهٔ اضافی. اول تعداد درخواست‌ها را ببینید، پیش‌نمایش محلی را امتحان کنید و بعد پردازش واقعی را شروع کنید.

[English](README.md) · [ساخت کلید API](https://api.sarovi.site/developers/start?utm_source=github&utm_medium=organic&utm_campaign=developer_tools_202610&utm_content=sarovi-batch-tools_key_fa) · [قیمت‌ها](https://api.sarovi.site/developers/pricing?utm_source=github&utm_medium=organic&utm_campaign=developer_tools_202610&utm_content=sarovi-batch-tools_pricing_fa)

Python نسخهٔ ۳٫۱۰ به بالا لازم است.

```sh
git clone https://github.com/sarovi-developers/sarovi-batch-tools.git
cd sarovi-batch-tools
python3 batch.py translate samples/messages.csv
python3 batch.py translate samples/messages.csv --demo --output demo.results.jsonl
python3 export_csv.py demo.results.jsonl demo.results.csv
```

دستور اول هیچ داده‌ای ارسال نمی‌کند؛ فقط برنامهٔ اجرا را نشان می‌دهد. demo خروجی ساختگی مشخص دارد و اعتبار مصرف نمی‌کند.

## ترجمهٔ واقعی

```sh
export SAROVI_API_KEY="YOUR_SAROVI_API_KEY"
python3 batch.py translate samples/messages.csv --target Persian --limit 5 --output translation.results.jsonl --run
```

فقط متن ستون انتخاب‌شده به ساروی و ارائه‌دهندهٔ مدل فرستاده می‌شود. برای کلید سقف مصرف کوچک بگذارید؛ محدودیت توکن، سقف پولی نیست.

برای دسته‌بندی از `classify` و `--labels billing technical other` استفاده کنید. برچسب نامعتبر مشخص می‌شود و برای اصلاح آن درخواست تازه‌ای مصرف نمی‌شود.

با `--resume`، ردیف‌های کامل تکرار نمی‌شوند. اگر پاسخ یک درخواست نامعلوم باشد، ابزار می‌ایستد؛ فایل پیشرفت را نگه دارید و با `receipt.py` مصرف همان درخواست را بررسی کنید. نتیجهٔ خالی به معنی رایگان بودن درخواست نیست. یک فایل پیشرفت را هم‌زمان با دو پردازش باز نکنید.

فایل اصلی بازنویسی نمی‌شود. خروجی می‌تواند اطلاعات خصوصی داشته باشد؛ آن را عمومی نکنید. [راهنمای کامل](README.md) · [اولین درخواست API](https://api.sarovi.site/developers/start?utm_source=github&utm_medium=organic&utm_campaign=developer_tools_202610&utm_content=sarovi-batch-tools_first_request_fa)

آزمون‌ها با `python3 -m unittest -v test_batch.py` و بدون مصرف API اجرا می‌شوند. مجوز کد MIT است؛ هزینهٔ API جداست.
