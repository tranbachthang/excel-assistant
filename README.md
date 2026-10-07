# excel-assistant

Tro ly Excel nhe — doc / tao / dien form / format / toi uu file `.xlsx`.
Chi can Python + `openpyxl`, khong can cai Microsoft Excel.

Sinh ra de lam viec lap di lap: dien du lieu vao form mau, format bang hang loat,
chuyen doi CSV <-> XLSX, va giam dung luong file.

## Cai dat

```bash
pip install openpyxl
```

## Dung

```bash
python excel_assistant.py info    book.xlsx          # sheets + kich thuoc
python excel_assistant.py read    book.xlsx --head 10
python excel_assistant.py csv2xlsx data.csv out.xlsx
python excel_assistant.py xlsx2csv book.xlsx out.csv
python excel_assistant.py beautify book.xlsx         # header dam, vien, auto-width, freeze, filter
python excel_assistant.py fill    template.xlsx data.json filled.xlsx
python excel_assistant.py optimize big.xlsx small.xlsx
python excel_assistant.py demo                       # tu kiem (SELFTEST PASS)
```

### Dien form

Giu nguyen form mau (merge, mau, cong thuc, dropdown) va chi dien gia tri vao o:

```json
{
  "Sheet1": { "B2": "Tran Bach Thang", "B3": "07/10/2026", "C5": 4 }
}
```

```bash
python excel_assistant.py fill template.xlsx data.json out.xlsx
```

## Pham vi

| Lam duoc | Khong lam |
|---|---|
| Doc/ghi `.xlsx`, nhieu sheet | Tinh lai cong thuc (openpyxl khong tinh) |
| Dien gia tri theo dia chi o | Giu 100% style cua file goc khi `optimize` |
| Format bang (header, vien, width, freeze, filter) | Macro VBA |
| CSV <-> XLSX | File `.xls` cu (doi sang `.xlsx` truoc) |

## Ghi chu

- `optimize` ghi lai bang openpyxl -> bo style/part thua, giam dung luong, nhung co the mat vai dinh dang hiem.
- Khi `fill`, neu template co cong thuc trong o thi gia tri moi se **ghi de** cong thuc do.

MIT License.
