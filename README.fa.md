# ابزارهای CSV ساروی

ترجمهٔ یک ستون یا دسته‌بندی پیام‌های پشتیبانی با هوش مصنوعی؛ با کتابخانهٔ استاندارد Python، بدون نصب وابستگی. اول تعداد درخواست‌ها را ببینید، پیش‌نمایش محلی را امتحان کنید و بعد یک پردازش واقعی کوچک را شروع کنید.

[ساخت کلید API](https://api.sarovi.site/developers/start?utm_source=github&utm_medium=organic&utm_campaign=developer_tools_202610&utm_content=sarovi-batch-tools_key_fa) · [مدل‌ها و قیمت‌ها](https://api.sarovi.site/developers/pricing?utm_source=github&utm_medium=organic&utm_campaign=developer_tools_202610&utm_content=sarovi-batch-tools_pricing_fa) · [اولین درخواست](https://api.sarovi.site/developers/start?utm_source=github&utm_medium=organic&utm_campaign=developer_tools_202610&utm_content=sarovi-batch-tools_first_request_fa)

## امتحان بدون کلید و هزینه

Python نسخهٔ ۳٫۱۰ به بالا لازم است.

```sh
git clone https://github.com/sarovi-developers/sarovi-batch-tools.git
cd sarovi-batch-tools
python3 batch.py translate samples/messages.csv
python3 batch.py translate samples/messages.csv --demo --output demo.results.jsonl
python3 export_csv.py demo.results.jsonl demo.results.csv
```

دستور اول فقط تعداد درخواست‌های برنامه‌ریزی‌شده را نشان می‌دهد و هیچ داده‌ای نمی‌فرستد. حالت `--demo` خروجی ساختگی مشخص دارد و اعتبار مصرف نمی‌کند. خروجی CSV در فایل تازه ایجاد می‌شود و متن‌هایی که ممکن است در صفحه‌گسترده فرمول شمرده شوند، ایمن می‌شوند.

## ترجمهٔ واقعی

```sh
export SAROVI_API_KEY="YOUR_SAROVI_API_KEY"
python3 batch.py translate samples/messages.csv \
  --column text --target Persian --limit 5 --max-tokens 512 \
  --output translation.results.jsonl --run
```

در PowerShell از `$env:SAROVI_API_KEY="YOUR_SAROVI_API_KEY"` استفاده کنید. مدل با `SAROVI_MODEL` و دامنهٔ API با `SAROVI_BASE_URL` قابل انتخاب است. هر دو دامنهٔ ساروی کار می‌کنند.

فقط متن سلول‌های ستون انتخاب‌شده به ساروی و ارائه‌دهندهٔ مدل فرستاده می‌شود. اجرای واقعی اعتبار مصرف می‌کند. با فایل نمونه و سقف مصرف کوچک کلید یا پروژه شروع کنید؛ محدودیت توکن، سقف پولی نیست.

## دسته‌بندی پیام‌ها

```sh
python3 batch.py classify samples/messages.csv \
  --labels billing technical other --limit 5 \
  --output labels.results.jsonl --run
```

برچسب برگشتی ثبت می‌شود. اگر یکی از برچسب‌های مجاز نباشد، `valid_label: false` خواهد بود؛ برای اصلاح آن درخواست تازه‌ای مصرف نمی‌شود. پیش از استفادهٔ خودکار از برچسب‌ها، نتیجهٔ مدل را بررسی کنید.

## ادامهٔ پردازش

همان دستور را با `--resume` اجرا کنید. ردیف‌های کامل تکرار نمی‌شوند و هش ورودی و تنظیمات مانع مخلوط شدن کارهای متفاوت می‌شود. پیش‌فرض پنج ردیف غیرخالی است؛ با `--limit` می‌توانید صریحاً تا ۱۰۰ ردیف انتخاب کنید.

اگر نتیجهٔ یک درخواست نامعلوم باشد، اجرا و ادامه متوقف می‌شود. فایل پیشرفت را نگه دارید و مصرف همان درخواست را پیگیری کنید:

```sh
python3 receipt.py --idempotency-key=ORIGINAL_KEY
```

پیگیری به دسترسی `usage:read` نیاز دارد. نتیجهٔ خالی ثابت نمی‌کند درخواست قبلی رایگان بوده است. ارسال مجدد یا هزینهٔ بازیابی خودکار انجام نمی‌شود. هر بار فقط یک پردازش را روی یک فایل پیشرفت اجرا کنید.

فایل پیشرفت حاوی خروجی تولیدشده است و ممکن است خصوصی باشد. فایل نمونه ساختگی است و CSV اصلی بازنویسی نمی‌شود. [نکته‌های API](docs/API-NOTES.md) را برای جزئیات هزینه، نگهداری داده و محدودیت پیگیری ببینید.

## بررسی کد

```sh
python3 -m unittest -v test_batch.py
```

آزمون‌ها اجرای بدون شبکه، پیش‌نمایش محلی، رد تکرار ردیف کامل، تغییر ورودی، درخواست نامعلوم و محدودیت‌ها را بررسی می‌کنند؛ درخواست پولی ندارند.

[نمونه‌کدهای بیشتر](https://github.com/sarovi-developers/sarovi-api-cookbook)

کد با مجوز [MIT](LICENSE.fa.md) منتشر شده است؛ مصرف API جداگانه محاسبه می‌شود.
