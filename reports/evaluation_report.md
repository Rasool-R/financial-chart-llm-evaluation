# Financial Chart LLM Evaluation Report

## Dataset Summary

- Total evaluated rows: 36
- Yes/No rows: 18
- Numeric rows: 18

## Yes/No Evaluation

- Valid predictions: 18
- Accuracy: 0.6111
- F1-score (positive class: yes): 0.6957
- Incorrect predictions: 7

## Numeric Evaluation

- Valid numeric predictions: 18
- Samples used for MAPE: 18
- Zero actual values excluded from MAPE: 0
- MAPE (%): 1852.4695
- Predictions with error above 20%: 8

## Incorrect Yes/No Predictions

| image_file                      | question                                                                       | answer   | LLM_answer   |
|:--------------------------------|:-------------------------------------------------------------------------------|:---------|:-------------|
| Aram_0003.png                   | آیا این سهم در یک هفته آینده به قیمت 32000 می‌‍رسد؟                            | yes      | no           |
| Tavan_0004.png                  | قیمت 14650 برای این سهم می تواند حمایت خوبی باشد؟                              | yes      | no           |
| sa_03.png                       | آیا در دو هفته آینده، قیمت از سطح مقاومت فعلی عبور خواهد کرد؟                  | yes      | no           |
| sa_07.png                       | آیا قیمت در 2 هفته آینده به خط حمایت برخورد می‌کند؟                            | yes      | no           |
| sa_09.png                       | آیا افزایش حجم معاملات در انتهای نمودار، شکست (Breakout) روند را تایید می‌کند؟ | yes      | no           |
| khasapa_18khordad_26khordad.png | آیا نمودار در ماه آینده به سقف قیمتی ماه گذشته خواهد رسید؟                     | yes      | no           |
| vebmelat_2mehr_3Aban.png        | آیا دامنه نوسان قیمت در ماه آینده بیشتر  مساوی ۱۰ درصد خواهد بود؟              | yes      | no           |

## Numeric Predictions with High Error

| image_file                | question                                                                                                                                                       |        answer |   LLM_answer | error_pct   |
|:--------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------:|-------------:|:------------|
| chart-001.png             | قیمت این سهم تا پایان ۵ روز معاملاتی آینده در چه محدوده‌ای قرار خواهد گرفت؟                                                                                    | 463798        |         4800 | 98.97%      |
| chart-004.png             | بیشترین قیمت قابل انتظار سهم در ۱۰ روز آینده چقدر است؟                                                                                                         |  21024        |         4300 | 79.55%      |
| SekehBaharAzadi.png       | با توجه به روند صعودی پرشتاب قیمت در اواخر شهریور و عبور آن از مرز                                                                                             |      9.81e+07 |      9000000 | 90.83%      |
| SekehBaharAzadi.png       | اگر شیب رشد قیمت از اواسط مرداد تا اواخر شهریور را مبنا قرار دهیم، انتظار می‌رود قیمت در اواسط پاییز در چه محدوده‌ای تثبیت شود؟                                |      1.04e+08 |      9000000 | 91.35%      |
| SekehBaharAzadi.png       | با توجه به اعداد محور عمودی سمت راست، اختلاف قیمت بین بالاترین سقف ثبت شده در اوایل فروردین و پایین‌ترین کف ثبت شده در اواخر اردیبهشت به صورت تقریبی چقدر است؟ |      2.89e+07 |     20000000 | 30.80%      |
| sa_05.png                 | مقدار قیمت در سه ماهه بعدی را پیش‌بینی کن.                                                                                                                     |    410        |          310 | 24.39%      |
| همکاران سیستم- 6 ماهه.png | میزان سود یا زیان این سهام در یک ماه آینده چند درصد خواهد بود                                                                                                  |      0.15     |           26 | 17233.33%   |
| نمک - بازه سه ماهه.png    | میزان سود یا زیان این سهام در هفته آیند چند درصد خواهد بود                                                                                                     |     -0.09     |           14 | 15655.56%   |

## Evaluation Notes

- MAPE excludes rows where the actual value is zero.
- Numeric error examples use a 20% error threshold.
- Invalid or missing predictions are excluded from the corresponding metric calculations.
- Results reflect the available dataset and the selected model.
