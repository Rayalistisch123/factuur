import os
from flask import Flask, request, jsonify
from invoice_generator import generate_invoice_pdf
from drive_uploader import upload_to_drive

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        order_data = request.get_json()
        if not order_data:
            print("Geen orderdata ontvangen")
            return jsonify({"status": "error", "message": "Geen orderdata ontvangen"}), 400
        print("Ontvangen orderdata:", order_data)
    
        order_number = order_data.get('name', 'order_unknown')
        pdf_file = f"/tmp/invoice_{order_number}.pdf"
    
        # PDF genereren
        try:
            generate_invoice_pdf(order_data, pdf_file)
            print("PDF succesvol aangemaakt:", pdf_file)
        except Exception as pdf_error:
            print("Fout bij PDF-generatie:", pdf_error)
            raise pdf_error  # of return een foutbericht
    
        # Upload naar Google Drive
        try:
            drive_file_name = f"invoice_{order_number}.pdf"
            drive_file_id = upload_to_drive(pdf_file, drive_file_name)
            print("PDF succesvol geüpload naar Drive, file ID:", drive_file_id)
        except Exception as drive_error:
            print("Fout bij uploaden naar Drive:", drive_error)
            raise drive_error  # of return een foutbericht
    
        return jsonify({"status": "success", "message": "Factuur verwerkt"}), 200
    except Exception as e:
        print("Algemene fout in webhook: ", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)

