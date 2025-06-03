import csv
import os
from datetime import datetime

from LabelGenerator import (
    LabelDocument,
    LabelPage,
    LabelText,
    LabelBarcode,
    LabelQRCode,
)

def template(
    qrcode_data,
    device_name_1,
    device_name_2,
    device_name_3,
    pn,
    sn,
    date,
    barcode_data,
):
        """
        Create label template
        """
        page = LabelPage()
        page.set_size(40, 30)
        page.set_background_color((255, 255, 255))  # White background

        # Add QR code
        element_qrcode = LabelQRCode()
        element_qrcode.set_location(0, 0)
        element_qrcode.set_size(40, 40)
        element_qrcode.set_data(qrcode_data)
        element_qrcode.set_color((0, 0, 0))
        element_qrcode.set_error_correction(element_qrcode.ERROR_LEVEL.LOW)
        page.add_element(element_qrcode)

        # Add device name
        element_device_name_1 = LabelText()
        element_device_name_1.set_location(45, 12)
        element_device_name_1.set_text(device_name_1)
        element_device_name_1.set_font("Microsoft YaHei", 10, "Bold")
        element_device_name_1.set_color((0, 0, 0))
        page.add_element(element_device_name_1)

        element_device_name_2 = LabelText()
        element_device_name_2.set_location(45, 24)
        element_device_name_2.set_text(device_name_2)
        element_device_name_2.set_font("Microsoft YaHei", 10, "normal")
        element_device_name_2.set_color((0, 0, 0))
        page.add_element(element_device_name_2)

        element_device_name_3 = LabelText()
        element_device_name_3.set_location(45, 36)
        element_device_name_3.set_text(device_name_3)
        element_device_name_3.set_font("Microsoft YaHei", 7, "normal")
        element_device_name_3.set_color((0, 0, 0))
        page.add_element(element_device_name_3)

        # Add device model
        element_pn_text = LabelText()
        element_pn_text.set_location(0, 50)
        element_pn_text.set_text(" P/N")
        element_pn_text.set_font("Consolas", 9, "bold")
        element_pn_text.set_color((0, 0, 0))
        page.add_element(element_pn_text)

        element_pn = LabelText()
        element_pn.set_location(22, 50)
        element_pn.set_text(pn)
        element_pn.set_font("Consolas", 8, "normal")
        element_pn.set_color((0, 0, 0))
        page.add_element(element_pn)

        # Add serial number
        element_sn_text = LabelText()
        element_sn_text.set_location(0, 60)
        element_sn_text.set_text(" S/N")
        element_sn_text.set_font("Consolas", 9, "bold")
        element_sn_text.set_color((0, 0, 0))
        page.add_element(element_sn_text)

        element_sn = LabelText()
        element_sn.set_location(22, 60)
        element_sn.set_text(sn)
        element_sn.set_font("Consolas", 8, "normal")
        element_sn.set_color((0, 0, 0))
        page.add_element(element_sn)

        # Add date
        element_date_text = LabelText()
        element_date_text.set_location(0, 70)
        element_date_text.set_text("Date")
        element_date_text.set_font("Consolas", 9, "bold")
        element_date_text.set_color((0, 0, 0))
        page.add_element(element_date_text)

        element_date = LabelText()
        element_date.set_location(22, 70)
        element_date.set_text(date)
        element_date.set_font("Consolas", 9, "normal")
        element_date.set_color((0, 0, 0))
        page.add_element(element_date)

        # Add barcode
        element_barcode = LabelBarcode()
        element_barcode.set_location(0, 85)
        element_barcode.set_size(120, 10)
        element_barcode.set_barcode_type("code128")
        element_barcode.set_data(barcode_data)
        element_barcode.set_color((0, 0, 0))
        page.add_element(element_barcode)

        return page

# ========== Batch generate labels ==========
csv_path = "label_content.csv"
output_pdf = f"device_labels_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

doc = LabelDocument()

if os.path.exists(csv_path):
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # You can adjust the field mappings below based on actual CSV field names
            qrcode_data = row.get("AssetNum", "")
            device_name_1 = row.get("Category", "")
            device_name_2 = row.get("Name", "")
            device_name_3 = row.get("Description", "")
            pn = row.get("P/N", "")
            sn = row.get("S/N", "")
            date = row.get("ImportDate", "")
            barcode_data = row.get("HASH", "")

            page = template(
                qrcode_data=qrcode_data,
                device_name_1=device_name_1,
                device_name_2=device_name_2,
                device_name_3=device_name_3,
                pn=pn,
                sn=sn,
                date=date,
                barcode_data=barcode_data,
            )
            doc.add_page(page)
    doc.export_pdf(output_pdf)

    # Export labels
    doc.export_pdf("device_label.pdf")  # Export PDF
