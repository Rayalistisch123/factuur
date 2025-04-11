import os
from datetime import datetime
from flask import Flask, request, jsonify
from invoice_generator import generate_invoice_pdf
from drive_uploader import upload_to_drive

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        order_data = request.get_json()
        if not order_data:
            print("❌ Geen orderdata ontvangen")
            return jsonify({"status": "error", "message": "Geen orderdata ontvangen"}), 400

        print("📦 Ontvangen orderdata:", order_data)

        # 🔍 Check of het een behang-order is
        line_items = order_data.get('line_items', [])
        bevat_behang = any("behang" in item.get('title', '').lower() for item in line_items)

        if not bevat_behang:
            print("⏭ Geen behang in order. Order wordt overgeslagen.")
            return jsonify({"status": "skipped", "message": "Geen behang-order"}), 200

        # ✅ Ga verder met factuur maken
        order_number = order_data.get('name', 'order_unknown')
        first_name = order_data.get('customer', {}).get('first_name', 'klant')
        last_name = order_data.get('customer', {}).get('last_name', '')
        datum = datetime.now().strftime('%Y-%m-%d')

        # Genereer bestandsnaam
        safe_name = f"{first_name}_{last_name}".replace(" ", "_").lower()
        drive_file_name = f"behang_factuur_{safe_name}_{order_number}.pdf"
        pdf_file = f"/tmp/{drive_file_name}"

        try:
            generate_invoice_pdf(order_data, pdf_file)
            print("✅ PDF succesvol aangemaakt:", pdf_file)
        except Exception as pdf_error:
            print("❌ Fout bij PDF-generatie:", pdf_error)
            raise pdf_error

        try:
            drive_file_id = upload_to_drive(pdf_file, drive_file_name)
            print("✅ PDF succesvol geüpload naar Drive. File ID:", drive_file_id)
        except Exception as drive_error:
            print("❌ Fout bij uploaden naar Drive:", drive_error)
            raise drive_error

        return jsonify({"status": "success", "message": "Factuur verwerkt"}), 200

    except Exception as e:
        print("❌ Algemene fout in webhook:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    return "🧾 Factuurservice draait ✅ — alleen voor behang-orders!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
