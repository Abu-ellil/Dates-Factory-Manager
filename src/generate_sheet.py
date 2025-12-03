import xlsxwriter
from datetime import datetime, timedelta

# File path
file_path = 'Date_Factory_Manager_v4.xlsx'

# Create a workbook and add worksheets
workbook = xlsxwriter.Workbook(file_path)
sheet_customers = workbook.add_worksheet('العملاء (Customers)')
sheet_prices = workbook.add_worksheet('أسعار اليوم (Daily Prices)')
sheet_weighbridge = workbook.add_worksheet('الميزان (Weighbridge)')
sheet_crates = workbook.add_worksheet('الصناديق (Crates)')
sheet_finance = workbook.add_worksheet('المالية (Finance)')
sheet_dashboard = workbook.add_worksheet('التقرير (Dashboard)')

# Formats
header_fmt = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'fg_color': '#2F75B5', 'font_color': 'white', 'border': 1})
cell_fmt = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
date_fmt = workbook.add_format({'num_format': 'dd/mm/yyyy', 'align': 'center', 'valign': 'vcenter', 'border': 1})
num_fmt = workbook.add_format({'num_format': '#,##0.00', 'align': 'center', 'valign': 'vcenter', 'border': 1})
title_fmt = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})

# ---------------------------------------------------------
# 1. Customers Sheet
# ---------------------------------------------------------
sheet_customers.right_to_left()
headers_cust = ['اسم العميل', 'النوع', 'رقم الهاتف']
sheet_customers.write_row('A1', headers_cust, header_fmt)
sheet_customers.set_column('A:A', 30)
sheet_customers.set_column('B:C', 15)

# Add a table for Customers (for dynamic ranges)
sheet_customers.add_table('A1:C151', {'columns': [{'header': h} for h in headers_cust], 'name': 'tbl_Customers', 'style': 'Table Style Medium 2'})

# ---------------------------------------------------------
# 2. Daily Prices Sheet
# ---------------------------------------------------------
sheet_prices.right_to_left()
# Settings for Qantar
sheet_prices.write('E1', 'وزن القنطار (كجم):', header_fmt)
sheet_prices.write('F1', 100, cell_fmt) # Default 100kg
sheet_prices.data_validation('F1', {'validate': 'decimal', 'criteria': '>', 'value': 0, 'input_title': 'وزن القنطار', 'input_message': 'أدخل وزن القنطار بالكيلو جرام'})

headers_price = ['التاريخ', 'سعر القنطار اليوم']
sheet_prices.write_row('A1', headers_price, header_fmt)
sheet_prices.set_column('A:A', 15)
sheet_prices.set_column('B:B', 20)

# Generate dates for the season (e.g., Aug 1st to Dec 31st of current year)
current_year = datetime.now().year
start_date = datetime(current_year, 8, 1)
end_date = datetime(current_year, 12, 31)
delta = end_date - start_date
date_list = []

for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    date_list.append(day)
    sheet_prices.write_datetime(i + 1, 0, day, date_fmt)

sheet_prices.add_table(f'A1:B{len(date_list)+1}', {'columns': [{'header': h} for h in headers_price], 'name': 'tbl_Prices', 'style': 'Table Style Medium 2'})

# ---------------------------------------------------------
# 3. Weighbridge Sheet
# ---------------------------------------------------------
sheet_weighbridge.right_to_left()
headers_wb = ['التاريخ', 'اسم العميل', 'الوزن الصافي (كجم)', 'سعر القنطار', 'الإجمالي']
sheet_weighbridge.write_row('A1', headers_wb, header_fmt)
sheet_weighbridge.set_column('A:A', 15)
sheet_weighbridge.set_column('B:B', 30)
sheet_weighbridge.set_column('C:E', 18)

# Data Validation for Customer Names
sheet_weighbridge.data_validation('B2:B1000', {'validate': 'list', 'source': '=INDIRECT("tbl_Customers[اسم العميل]")'})

# Data Validation for Dates (Dropdown from tbl_Prices)
sheet_weighbridge.data_validation('A2:A1000', {'validate': 'list', 'source': '=INDIRECT("tbl_Prices[التاريخ]")'})

# Formulas
# Price lookup: =IFERROR(VLOOKUP([@التاريخ], tbl_Prices, 2, FALSE), 0)
# Total: =([@[الوزن الصافي (كجم)]] / 'أسعار اليوم (Daily Prices)'!$F$1) * [@[سعر القنطار]]

# We will write these as dynamic array formulas or just standard formulas in the first few rows
# Note: xlsxwriter tables handle formulas, but for simplicity in a generated sheet, we'll prep the table structure.
wb_data = []
for _ in range(100): wb_data.append([None, None, None, None, None])
sheet_weighbridge.add_table('A1:E1001', {
    'columns': [
        {'header': 'التاريخ', 'format': date_fmt},
        {'header': 'اسم العميل'},
        {'header': 'الوزن الصافي (كجم)'},
        {'header': 'سعر القنطار', 'formula': '=IFERROR(VLOOKUP([@التاريخ], tbl_Prices, 2, FALSE), 0)'},
        {'header': 'الإجمالي', 'formula': '=IFERROR(([@[الوزن الصافي (كجم)]]/\'أسعار اليوم (Daily Prices)\'!$F$1)*[@[سعر القنطار]], 0)'}
    ],
    'name': 'tbl_Weighbridge',
    'style': 'Table Style Medium 9'
})

# ---------------------------------------------------------
# 4. Crates Sheet
# ---------------------------------------------------------
sheet_crates.right_to_left()
headers_crates = ['التاريخ', 'اسم العميل', 'صناديق منصرفة (له)', 'صناديق مرتدة (عليه)', 'القائم بالتسليم', 'ملاحظات']
sheet_crates.write_row('A1', headers_crates, header_fmt)
sheet_crates.set_column('A:A', 15)
sheet_crates.set_column('B:B', 30)
sheet_crates.set_column('C:D', 18)
sheet_crates.set_column('E:F', 25)

sheet_crates.data_validation('A2:A1000', {'validate': 'list', 'source': '=INDIRECT("tbl_Prices[التاريخ]")'})
sheet_crates.data_validation('B2:B1000', {'validate': 'list', 'source': '=INDIRECT("tbl_Customers[اسم العميل]")'})

sheet_crates.add_table('A1:F1001', {'columns': [{'header': h} for h in headers_crates], 'name': 'tbl_Crates', 'style': 'Table Style Medium 10'})

# ---------------------------------------------------------
# 5. Finance Sheet
# ---------------------------------------------------------
sheet_finance.right_to_left()
headers_fin = ['التاريخ', 'اسم العميل', 'نوع المعاملة', 'مدفوع للعميل (له)', 'مقبوض من العميل (عليه)', 'ملاحظات']
sheet_finance.write_row('A1', headers_fin, header_fmt)
sheet_finance.set_column('A:A', 15)
sheet_finance.set_column('B:B', 30)
sheet_finance.set_column('C:C', 15)
sheet_finance.set_column('D:E', 20)
sheet_finance.set_column('F:F', 25)

sheet_finance.data_validation('A2:A1000', {'validate': 'list', 'source': '=INDIRECT("tbl_Prices[التاريخ]")'})
sheet_finance.data_validation('B2:B1000', {'validate': 'list', 'source': '=INDIRECT("tbl_Customers[اسم العميل]")'})
sheet_finance.data_validation('C2:C1000', {'validate': 'list', 'source': ['نقدية', 'تحويل بنكي', 'شيك']})

sheet_finance.add_table('A1:F1001', {'columns': [{'header': h} for h in headers_fin], 'name': 'tbl_Finance', 'style': 'Table Style Medium 12'})

# ---------------------------------------------------------
# 6. Dashboard Sheet
# ---------------------------------------------------------
sheet_dashboard.right_to_left()
sheet_dashboard.hide_gridlines(2)

sheet_dashboard.merge_range('B2:E2', 'لوحة تحكم العميل', title_fmt)

sheet_dashboard.write('C4', 'اختر اسم العميل:', header_fmt)
sheet_dashboard.write('D4', '', cell_fmt) # Input cell
sheet_dashboard.data_validation('D4', {'validate': 'list', 'source': '=INDIRECT("tbl_Customers[اسم العميل]")'})

# Metrics Layout
metrics = [
    ('إجمالي الوزن الصافي (كجم)', 'E6', '=SUMIF(tbl_Weighbridge[اسم العميل], D4, tbl_Weighbridge[الوزن الصافي (كجم)])'),
    ('إجمالي قيمة التوريدات', 'E7', '=SUMIF(tbl_Weighbridge[اسم العميل], D4, tbl_Weighbridge[الإجمالي])'),
    ('إجمالي المدفوعات للعميل', 'E8', '=SUMIF(tbl_Finance[اسم العميل], D4, tbl_Finance[مدفوع للعميل (له)])'),
    ('إجمالي المقبوضات من العميل', 'E9', '=SUMIF(tbl_Finance[اسم العميل], D4, tbl_Finance[مقبوض من العميل (عليه)])'),
    ('صافي الحساب المالي', 'E11', '=E7 + E9 - E8'), # Value of dates + Received - Paid. Wait.
    # Logic:
    # Customer Credit (Loh) = Value of Dates + Cash Received from him (if he paid back?) NO.
    # Usually:
    # Factory owes Customer = (Value of Dates) - (Payments made to Customer).
    # If Customer pays money to factory (Received from Customer), it reduces what factory owes? Or adds to his credit?
    # Let's assume:
    # Balance = (Value of Dates + Received from Customer) - (Paid to Customer)
    # If positive -> Factory owes Customer.
    # If negative -> Customer owes Factory.
    # Let's stick to: Balance = (Dates Value) - (Paid to Customer) + (Received from Customer)
    
    ('صناديق منصرفة (له)', 'H6', '=SUMIF(tbl_Crates[اسم العميل], D4, tbl_Crates[صناديق منصرفة (له)])'),
    ('صناديق مرتدة (عليه)', 'H7', '=SUMIF(tbl_Crates[اسم العميل], D4, tbl_Crates[صناديق مرتدة (عليه)])'),
    ('رصيد الصناديق (باقي معه)', 'H9', '=H6 - H7'),
]

# Write Metrics
sheet_dashboard.write('D6', 'إجمالي الوزن الصافي (كجم)', header_fmt)
sheet_dashboard.write_formula('E6', metrics[0][2], num_fmt)

sheet_dashboard.write('D7', 'إجمالي قيمة التوريدات', header_fmt)
sheet_dashboard.write_formula('E7', metrics[1][2], num_fmt)

sheet_dashboard.write('D8', 'إجمالي المدفوعات للعميل', header_fmt)
sheet_dashboard.write_formula('E8', metrics[2][2], num_fmt)

sheet_dashboard.write('D9', 'إجمالي المقبوضات من العميل', header_fmt)
sheet_dashboard.write_formula('E9', metrics[3][2], num_fmt)

sheet_dashboard.write('D11', 'صافي الحساب (له/عليه)', workbook.add_format({'bold': True, 'bg_color': '#FFC000', 'align': 'center', 'border': 1}))
sheet_dashboard.write_formula('E11', '=E7+E9-E8', workbook.add_format({'bold': True, 'bg_color': '#FFC000', 'num_format': '#,##0.00', 'align': 'center', 'border': 1}))


sheet_dashboard.write('G6', 'صناديق منصرفة (له)', header_fmt)
sheet_dashboard.write_formula('H6', metrics[4][2], cell_fmt)

sheet_dashboard.write('G7', 'صناديق مرتدة (عليه)', header_fmt)
sheet_dashboard.write_formula('H7', metrics[5][2], cell_fmt)

sheet_dashboard.write('G9', 'رصيد الصناديق (باقي معه)', workbook.add_format({'bold': True, 'bg_color': '#FFC000', 'align': 'center', 'border': 1}))
sheet_dashboard.write_formula('H9', '=H6-H7', workbook.add_format({'bold': True, 'bg_color': '#FFC000', 'align': 'center', 'border': 1}))

sheet_dashboard.set_column('C:H', 20)

workbook.close()
print(f"File '{file_path}' created successfully.")
